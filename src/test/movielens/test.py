import csv

def gen_data(G):
    reader = csv.reader(open('test/movielens/ml-100k/u.data'), dialect='excel-tab')
    reader = list(reader)

    edges = [{}, {}]
    for row in reader:
        if int(row[2]) >= 3:
            rate = 1
        else: rate = 0

        user = 'u'+row[0]
        movie = 'm'+row[1]

        if user not in edges[0]:
            edges[0][user] = {}
        edges[0][user][movie] = rate

        if movie not in edges[1]:
            edges[1][movie] = {}
        edges[1][movie][user] = rate

    max_u_rate = 0
    min_u_rate = 100

    # Trim
    while True:
        print 'users:', len(edges[0]), 'movies:', len(edges[1])
        toDel = [[], []]
        for user in edges[0]:
            if len(edges[0][user]) < 30:
                toDel[0].append(user)
        for movie in edges[1]:
            if len(edges[1][movie]) < 30:
                toDel[1].append(movie)
        if toDel == [[], []]: break

        for user in toDel[0]:
            for movie in edges[0][user]:
                try:del edges[1][movie][user]
                except:pass
            del edges[0][user]
        for movie in toDel[1]:
            for user in edges[1][movie]:
                try:del edges[0][user][movie]
                except:pass
            del edges[1][movie]

    for user in edges[0]:
        max_u_rate = max(len(edges[0][user]), max_u_rate)
        min_u_rate = min(len(edges[0][user]), min_u_rate)

    for user in edges[0]:
        for movie in edges[0][user]:
            if edges[0][user][movie] == 1:
                G.add_edge_by_name(user, movie)

    print max_u_rate, min_u_rate

    return G
