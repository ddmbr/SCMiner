def gen_data(G):
    G.add_edge_by_name('Alice', 'Mammals')
    G.add_edge_by_name('Alice', 'Biology')
    G.add_edge_by_name('Alice', 'Ecology')
    G.add_edge_by_name('Alice', 'Science')

    G.add_edge_by_name('Bob', 'Insects Anatomy')
    G.add_edge_by_name('Bob', 'Insects')
    G.add_edge_by_name('Bob', 'Biology')
    G.add_edge_by_name('Bob', 'Ecology')
    G.add_edge_by_name('Bob', 'Science')

    G.add_edge_by_name('Catherine', 'Vertibrate')
    G.add_edge_by_name('Catherine', 'Biology')
    G.add_edge_by_name('Catherine', 'Ecology')
    G.add_edge_by_name('Catherine', 'Science')

    G.add_edge_by_name('Dick', 'Programming')
    G.add_edge_by_name('Dick', 'Insects Anatomy')
    G.add_edge_by_name('Dick', 'Data Mining')
    G.add_edge_by_name('Dick', 'SVM')
    G.add_edge_by_name('Dick', 'Science')

    G.add_edge_by_name('Erik', 'Programming')
    G.add_edge_by_name('Erik', 'Insects Anatomy')
    G.add_edge_by_name('Erik', 'Machine Learning')
    G.add_edge_by_name('Erik', 'Random Forest')
    G.add_edge_by_name('Erik', 'Science')

    G.add_edge_by_name('Fiona', 'Programming')
    G.add_edge_by_name('Fiona', 'Neural Network')
    G.add_edge_by_name('Fiona', 'SVM')
    G.add_edge_by_name('Fiona', 'Science')

    return G
