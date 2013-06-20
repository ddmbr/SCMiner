import cPickle

data = []
rid = 0

def logmdl(record):
    global data, rid

    data += [[rid]+record]
    rid += 1

def savemdl():
    global data

    cPickle.dump(data, open("mdllog", "w"))
