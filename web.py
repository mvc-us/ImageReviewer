#!/usr/bin/python
#for reviewing images only
import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import random

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField

import pickle

cwd = os.getcwd()
cwd = '/'.join(cwd.split('/')[:-1])
UPLOAD_FOLDER = cwd + '/upload'
SWT_FOLDER = cwd + '/swt'
SWT_INTERP_FOLDER = cwd + '/swt_interp'
TESSERACT_FOLDER = cwd + '/tesseract'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SWT_FOLDER'] = SWT_FOLDER
app.config['TESSERACT_FOLDER'] = TESSERACT_FOLDER
app.config['SWT_INTERP_FOLDER'] = SWT_INTERP_FOLDER
app.config['PRECOMPUTED_FOLDER'] = cwd + '/text_img'
app.config['WTF_CSRF_ENABLED'] = False
app.config['PICKLE_FILE_NAME'] = 'img_errors.pickle'

class ImgForm(Form):
    tess_fp_architectural = BooleanField('architectural patterns')
    swt_fp_architectural = BooleanField('architectural patterns')
    tess_fp_natural = BooleanField('natural patterns')
    swt_fp_natural = BooleanField('natural patterns')
    tess_fp_reflection = BooleanField('reflection glass')
    swt_fp_reflection = BooleanField('reflection glass')
    tess_fp_nature = BooleanField('nature patterns')
    swt_fp_nature = BooleanField('nature patterns')
    tess_fp_blur = BooleanField('blur')
    swt_fp_blur = BooleanField('blur')
    tess_fn_shadows = BooleanField('shadows')
    swt_fn_shadows = BooleanField('shadows')
    tess_fn_logos = BooleanField('logos')
    swt_fn_logos = BooleanField('logos')
    tess_fn_cut = BooleanField('cut off')
    swt_fn_cut = BooleanField('cut off')
    tess_fn_angle = BooleanField('angle')
    swt_fn_angle = BooleanField('angle')
    tess_fn_curved = BooleanField('curved')
    swt_fn_curved = BooleanField('curved')
    tess_fn_blur = BooleanField('blur')
    swt_fn_blur = BooleanField('blur')
    tess_fn_spaced_out_text = BooleanField('spaced_out_text')
    swt_fn_spaced_out_text = BooleanField('spaced_out_text')

def configure_pre_images():
    images = []
    for f in os.listdir("../tesseract"):
        if f.endswith(".jpg"):
            img = {}
            img['url'] = "/pre/result/" + f
            img['name'] = f
            images.append(img)
    app.config['IMAGE_LIST'] = images

@app.route('/pre/result/list')
def pre_result_list():
    configure_pre_images()
    images = app.config['IMAGE_LIST']
    random_image_url = images[random.randrange(len(images))]['url']
    return render_template("img_list.html", images=images, random_img_url=random_image_url)


@app.route('/pre/result/<img_name>')
def pre_result(img_name):
    image_list = app.config['IMAGE_LIST']
    img = {'url': "/pre/result/" + img_name, 'name': img_name}
    if img not in image_list:
        return "No image found"    
    idx = image_list.index(img)
    prev_image_url = image_list[(idx-1)%len(image_list)]['url']
    next_image_url = image_list[(idx+1)%len(image_list)]['url']
    random_image_url = image_list[random.randrange(len(image_list))]['url']
    # import pdb; pdb.set_trace()
    return render_template('pre_result.html', img_name=img_name, prev_img_url=prev_image_url, next_img_url=next_image_url, random_img_url=random_image_url)

@app.route('/precomp_upload/<img_name>')
def precomp_upload(img_name):
    return send_from_directory(app.config['PRECOMPUTED_FOLDER'], img_name)

@app.route('/result/<img_name>')
def result(img_name):
    return render_template('result.html', img_name=img_name)

@app.route('/swt/<img_name>')
def swt_output(img_name):
    return send_from_directory(app.config['SWT_FOLDER'], img_name)

@app.route('/tesseract/<img_name>')
def tesseract_output(img_name):
    return send_from_directory(app.config['TESSERACT_FOLDER'], img_name)

@app.route('/')
def index():
    if 'IMAGE_LIST' not in app.config: configure_pre_images()
    image_list = app.config['IMAGE_LIST']
    return redirect('/review/' + image_list[0]['name'] + '/0')

@app.route('/last_review/<int:rand>')
def last_review(rand):
    if 'IMAGE_LIST' not in app.config: configure_pre_images()
    image_list = app.config['IMAGE_LIST']

    try:
        f = open(app.config['PICKLE_FILE_NAME'])
        d = pickle.load(f)
        f.close()
        if rand:
            while True:
                img = random.choice(image_list)
                if img['name'] not in d:
                    return redirect('/review/' + img['name'] + '/1')
        else:
            for img in image_list:
                if img['name'] not in d:
                    return redirect('/review/' + img['name'] + '/0')
    except EOFError:
        pass

    return redirect('/')


@app.route('/review/<img_name>/<int:rand>', methods=['GET', 'POST'])
def review(img_name, rand):  
    if 'IMAGE_LIST' not in app.config: configure_pre_images()
    image_list = app.config['IMAGE_LIST']
    img = {'url': "/pre/result/" + img_name, 'name': img_name}
    if img not in image_list:
        return "No image found"    
    
    form = ImgForm()
    tess_fp = {'tess_fp_blur': form.tess_fp_blur,'tess_fp_natural': form.tess_fp_natural,'tess_fp_reflection': form.tess_fp_reflection,'tess_fp_architectural': form.tess_fp_architectural,'tess_fp_nature': form.tess_fp_nature}
    swt_fp = {'swt_fp_reflection': form.swt_fp_reflection,'swt_fp_architectural': form.swt_fp_architectural,'swt_fp_nature': form.swt_fp_nature,'swt_fp_natural': form.swt_fp_natural,'swt_fp_blur': form.swt_fp_blur}
    tess_fn = {'tess_fn_cut': form.tess_fn_cut,'tess_fn_curved': form.tess_fn_curved,'tess_fn_spaced_out_text': form.tess_fn_spaced_out_text,'tess_fn_blur': form.tess_fn_blur,'tess_fn_logos': form.tess_fn_logos,'tess_fn_angle': form.tess_fn_angle,'tess_fn_shadows': form.tess_fn_shadows}
    swt_fn = {'swt_fn_spaced_out_text': form.swt_fn_spaced_out_text,'swt_fn_logos': form.swt_fn_logos,'swt_fn_shadows': form.swt_fn_shadows,'swt_fn_cut': form.swt_fn_cut,'swt_fn_angle': form.swt_fn_angle,'swt_fn_curved': form.swt_fn_curved,'swt_fn_blur': form.swt_fn_blur}
    complete = tess_fp.copy()
    complete.update(swt_fp)
    complete.update(tess_fn)
    complete.update(swt_fn)

    if form.validate_on_submit():
        idx = image_list.index(img)
        next_image_url = '/review/' + image_list[(idx+1)%len(image_list)]['name']
        img_d = {}
        for field in complete:
            img_d[field] = complete[field].data

        try:
            f = open(app.config['PICKLE_FILE_NAME'])
            d = pickle.load(f)
            f.close()
        except EOFError:
            d = {}

        d[img_name] = img_d
        with open(app.config['PICKLE_FILE_NAME'], 'wb') as handle:
            pickle.dump(d, handle)

        print(len(d))
        if rand: return redirect('/last_review/' + str(rand))
        return redirect(next_image_url)

    '''
    pickle stores a dictionary
    pickle[img_name][field] = True/False
    '''
    try:
        f = open(app.config['PICKLE_FILE_NAME'])
        d = pickle.load(f)
        f.close()
        if img_name in d:
            for field in d[img_name]:
                complete[field].data = d[img_name][field]
    except EOFError:
        pass

    return render_template('review.html', img_name=img_name, form=form,
        tess_fp=tess_fp, tess_fn=tess_fn, swt_fp=swt_fp, swt_fn=swt_fn, rand=rand)

if __name__ == '__main__':
    app.run(debug=True)