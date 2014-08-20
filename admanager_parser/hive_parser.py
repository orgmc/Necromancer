import json
import sys
import time
from functools import wraps
import cProfile
import pstats

reload(sys)
sys.setdefaultencoding('utf-8')

def timediff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print '>> Spend {1} seconds'.format(func.__name__, end - start)
        return result
    return wrapper

@timediff
def parser():
    dataset = []
    with open(r'admanager.log') as f:
        for line in f:
            tmp = []
            start = line.find('{')
            data = json.loads(line[start:])
            tmp.append(data['tags'].get('model',' '))
            tmp.append(data['tags'].get('publisherId', ' '))
            tmp.append(data['tags'].get('channelId', ' '))
            tmp.append(data['tags'].get('adtype', ' '))
            tmp.append(data['tags'].get('osver', ' '))
            tmp.append(data['tags'].get('country', ' '))
            tmp.append(data['tags'].get('ip', ' '))
            tmp.append(data['tags'].get('android_id', ' '))
            tmp.append(data['tags'].get('category', ' '))
            tmp.append(data['tags'].get('brand', ' '))
            tmp.append(data['tags'].get('ua', ' '))
            tmp.append(data.get('reqnum', ' '))
            tmp.append(data.get('resnum', ' '))
            tmp.append(data.get('reqTime', ' '))
            dataset.append(tmp)

    with open(r'output.log', 'w') as f:
        for datas in dataset:
            for data in datas:
                f.write('{0}\001'.format(data))
            f.write('\n')


if __name__ == '__main__':
    cProfile.run("parser()","tmp")
    p = pstats.Stats("tmp")
    p.strip_dirs().sort_stats(-1).print_stats()