from os                     import listdir
from os.path                import join
from nltk.corpus            import stopwords
# from nltk.stem.lancaster    import LancasterStemmer
from nltk.stem.wordnet      import WordNetLemmatizer
import nltk
import re

def get_body(f):
    body = ''
    text = f.readlines()

    mode = 'head'
    for line in text:
        line = line.strip()
        # Skip headers
        if mode == 'head' and line == '':
            mode = 'tail'

        # Looking for the tail
        if mode == 'tail' and line != '':
            # if len(line) > 3 and line[:3] == '---': break
            body += line

    return body

def gen_data(G=None, g1='rec.sport.baseball', g2='comp.graphics', n_msg=100):
    data = []

    fileList1 = listdir(join('test', 'newsgroups', '20_newsgroups', g1))[:n_msg]
    fileList2 = listdir(join('test', 'newsgroups', '20_newsgroups', g2))[:n_msg]
    assert set(fileList1).intersection(set(fileList2)) == set()

    for fn in fileList1:
        f = open(join('test', 'newsgroups', '20_newsgroups', g1, fn))
        data += [{'orig_msg':get_body(f), 'name':fn, 'tag':g1}]
        
    for fn in fileList2:
        f = open(join('test', 'newsgroups', '20_newsgroups', g2, fn))
        data += [{'orig_msg':get_body(f), 'name':fn, 'tag':g2}]

    # stemmer = LancasterStemmer()
    lmtzr = WordNetLemmatizer()

    occur = {}
    for case in data:
        msg = case['orig_msg']
        msg = re.findall(r'\w+', msg)
        new_msg = []
        for word in msg:
            if word not in stopwords.words('english'):
                word = lmtzr.lemmatize(word)
                if not word.islower(): continue
                if len(word) <= 2: continue
                if word not in occur: occur[word] = 1
                else: occur[word] += 1
                new_msg += [word]
        case['msg'] = new_msg

    occurTh = 3
    for case in data:
        msg = case['msg']
        for word in msg:
            if occur[word] < occurTh: continue
            G.add_edge_by_name(case['name'], word)
            G.set_attrs(case['name'], 0, 'cls', case['tag'])
            G.set_attrs(case['name'], 0, 'name', case['name'])
            G.set_attrs(case['name'], 0, 'orig_msg', case['orig_msg'])
            G.set_attrs(case['name'], 0, 'msg', case['msg'])
            G.set_attrs(word, 1, 'word', word)

    return G
