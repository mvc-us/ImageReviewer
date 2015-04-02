#!/usr/bin/python
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guessiwy3p98rywfhabsjk'

fp_reasons = ['architectural patterns', 'natural patterns', 'reflection glass', 'nature patterns', 'blur']
fn_reasons = ['shadows', 'logos', 'cut off', 'angle', 'curved', 'blur', 'spaced_out_text']

if __name__ == '__main__':
	tess_fp = set()
	swt_fp = set()
	for fp in fp_reasons:
	    tess_name = 'tess_fp_' + fp.split()[0]
	    swt_name = 'swt_fp_' + fp.split()[0]
	    print(tess_name + " = BooleanField('" + fp + "')")
	    print(swt_name + " = BooleanField('" + fp + "')")
	    tess_fp.add(tess_name)
	    swt_fp.add(swt_name)

	tess_fn = set()
	swt_fn = set()
	for fn in fn_reasons:
	    tess_name = 'tess_fn_' + fn.split()[0]
	    swt_name = 'swt_fn_' + fn.split()[0]
	    print(tess_name + " = BooleanField('" + fn + "')")
	    print(swt_name + " = BooleanField('" + fn + "')")
	    tess_fn.add(tess_name)
	    swt_fn.add(swt_name)

	strings = ["tess_fp", "swt_fp", "tess_fn", "swt_fn"]
	for st in strings:
	    s = st + " = {"
	    for name in eval(st):
	        s += "'" + name + "': form." + name + ','

	    s = s[:-1]
	    s += '}'
	    print(s)

