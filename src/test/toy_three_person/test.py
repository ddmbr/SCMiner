def gen_data(G):
    G.add_edge_by_name('ddmbr', 'Programming')  # owned by everybody
    G.add_edge_by_name('ddmbr', 'Debian')
    G.add_edge_by_name('ddmbr', 'Linux')

    G.add_edge_by_name('ray', 'Programming')    # owned by everybody
    G.add_edge_by_name('ray', 'Arch')
    G.add_edge_by_name('ray', 'Linux')

    G.add_edge_by_name('kaze', 'Programming')   # not owned by everybody
    G.add_edge_by_name('kaze', 'Windows')

    return G
