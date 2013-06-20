import csv
import cPickle

def gen_data(G=None, fn="test/delicious/user_taggedbookmarks-timestamps.dat"):
    reader = csv.reader(open(fn), dialect='excel-tab')

    print '... Data loading: Delicious bookmarks stats.'

    # Skip header
    reader.next()

    try:
        L = cPickle.load(open("/home/ddmbr/play/DM/scminer/src/test/delicious/pkl"))
    except:
        L = []
        i = 0
        for row in reader:
            i += 1
            L.append(('u'+row[0], 't'+row[1]))
            print '... %.2f%% loaded' % ((i/437593.)*100)

        cPickle.dump(L, open("/home/ddmbr/play/DM/scminer/src/test/delicious/pkl", "w"))

    i = 0
    for p in L:
        if G != None:
            print i
            i += 1
            G.add_edge_by_name(p[0], p[1])  # user id, item id
    print '... Data loaded: Delicious bookmarks stats.'
    return G

if __name__ == '__main__':
    gen_data(G=None, fn="user_taggedbookmarks-timestamps.dat")
