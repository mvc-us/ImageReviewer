#!/usr/bin/python
import pickle
ERROR_FILE = 'img_errors.pickle'

def tally():
    f = open(ERROR_FILE)
    d = pickle.load(f)
    f.close()

    num_img = 0
    totals = {} #[field] = count
    for img_name in d:
        num_img += 1
        for field in d[img_name]:
            if d[img_name][field]:
                if field not in totals:
                    totals[field] = 1
                else:
                    totals[field] += 1

    return num_img, totals

if __name__ == '__main__':
    print(tally())