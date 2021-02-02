import argparse
import datetime

import helper_functions as hp
import numpy as np

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument("-n", required=True, help="Network adjacency matrix prefix")
parser.add_argument("-m", required=True, help="Gene-sample matrix prefix")
parser.add_argument("-o", required=True, help="Output prefix")
parser.add_argument("-a", type=float, help="Propagation alpha value")

args = parser.parse_args()

network_prefix = args.n
matrix_prefix = args.m
output_prefix = args.o

alpha = 0.8 # propagation alpha
if args.a:
    alpha = args.a
    assert alpha > 0 and alpha < 1, "Propagation alpha value must be positive and less than 1."
    print("Propagation alpha set to {}".format(alpha))


def get_scores(M, M_postprop, common_index): # writes initial and postprop score of each node
    initial_scores = np.mean(M, axis=1)
    postprop_scores = np.mean(M_postprop, axis=1)
    
    score_list = np.array(list(zip(common_index, initial_scores, postprop_scores)), 
                          dtype=[('node', 'U25'), ('initial_score', 'f'), ('postprop_score', 'f')])
    
    return score_list
    
def run(M, W, alpha): # propagates scores over the network
    i = 0; epsilon = 1 / np.power(10, 6); max_iterations = 350
    M0 = M; M_delta = epsilon

    print('{0}\nPropagation in progress...'.format(datetime.datetime.now()))
    while M_delta >= epsilon and i < max_iterations:
        previous = M

        M = (alpha * np.dot(W, M)) + ((1 - alpha) * M0) # propagation step      
        M_delta = np.linalg.norm(M - previous)
        
        i += 1

    print('Propagation done: {0} iterations.'.format(i))
    print(datetime.datetime.now())

    return M

if __name__ == "__main__":
    M, W, common_index = hp.load_propagation_data(network_prefix, matrix_prefix) # load network (W) and gene-sample (M) matrices
    M_postprop = run(M, W, alpha)
    
    np.savetxt(output_prefix + '_matrix_postprop.txt', M_postprop, fmt='%f', delimiter='\t')
    np.savetxt(output_prefix + '_matrix_postprop_index.txt', common_index, fmt='%s')
    print('\nPostpropagation matrix saved to {0}'.format(output_prefix + '_postprop.txt'))

    score_list = get_scores(M, M_postprop, common_index)
    np.savetxt(output_prefix + '_scores.txt', score_list, header="node\tinitial_score\tpostprop_score", fmt=['%s', '%f', '%f'], delimiter='\t', comments='')
    print('Score list saved to {0}'.format(output_prefix + '_scores.txt'))