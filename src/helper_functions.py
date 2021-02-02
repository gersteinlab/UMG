import datetime
import numpy as np

def load_matrix(matrix_prefix): # loads a matrix and index
    print('{0}\nLoading matrix with prefix {1} ...'.format(datetime.datetime.now(), matrix_prefix))
    matrix = np.loadtxt(matrix_prefix + '.txt', dtype='f', delimiter='\t')
    matrix_index = np.loadtxt(matrix_prefix + '_index.txt', dtype='U25', delimiter='\t')
    
    print('Loading done. Matrix size: {0}.\n'.format(matrix.shape))
    
    return matrix, matrix_index

def load_propagation_data(network_prefix, matrix_prefix, normalize_network=True):
    W, W_index = load_matrix(network_prefix) # load network
    M, M_index = load_matrix(matrix_prefix) # load gene-sample matrix

    common_index, M_inds, W_inds = np.intersect1d(M_index, W_index, return_indices=True) # keep common nodes
    M = M[M_inds, :]; W = W[W_inds, :]; W = W[:, W_inds]

    if normalize_network:
        print('{0}\nNormalizing network adjacency matrix...'.format(datetime.datetime.now()))
        D = np.diag(np.sum(W, axis=0))
        W = np.matmul(W, np.linalg.inv(D))
        
        print('Normalization done.\n')

    return M, W, common_index

def load_UMG_detection_data(score_list_prefix):
    score_list = np.genfromtxt(score_list_prefix + '_scores.txt', delimiter='\t', skip_header=1,
                               dtype=[('node', 'U25'), ('initial_score', 'f'), ('final_score', 'f')])
    return score_list