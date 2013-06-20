def gen_data(G):
    G.add_edge_by_name('ddmbr', 'Python')
    G.add_edge_by_name('ddmbr', 'Debian')

    G.add_edge_by_name('ray', 'Python')
    G.add_edge_by_name('ray', 'Arch')

    return G
