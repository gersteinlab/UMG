import argparse
import datetime

import helper_functions as hp
import numpy as np
from scipy.stats import rankdata

parser = argparse.ArgumentParser(description="Argument Parser")
parser.add_argument("--scr", required=True, help="Score list prefix")
parser.add_argument("-o", required=True, help="Output prefix")
parser.add_argument("-T", required=True, type=int, help="Post-propagation ranking threshold")
parser.add_argument("-b", type=float, help="Mobility beta")

args = parser.parse_args()

score_list_prefix = args.scr
output_prefix = args.o
rank_threshold = args.T
    
mobility_beta = 0.1
if args.b:
    mobility_beta = args.b
    assert mobility_beta > 0 and mobility_beta < 1, "Mobility beta value must be positive and less than 1."

print('Rank threshold (T): {0}\nMobility beta (b): {1}\n'.format(rank_threshold, mobility_beta))

def calculate_mobility(score_list):
    initial_ranks = rankdata(-score_list['initial_score'], method='min')
    postprop_ranks = rankdata(-score_list['final_score'], method='min')
    
    mobility_score = initial_ranks - postprop_ranks # mobility as the difference in pre- and post-propagation ranks
    
    mobility_list = np.array(list(zip(score_list['node'], mobility_score, (initial_ranks + 1), (postprop_ranks + 1))), dtype=[('node', 'U25'), ('mobility_score', 'i4'), ('initial_rank', 'i4'), ('postprop_rank', 'i4')])
    mobility_list = np.flip(np.sort(mobility_list, order=['mobility_score']))
    
    return mobility_list

def run(mobility_list, T, b): # find UMGs
    assert T > 0 and T < mobility_list.shape[0], "Ranking threshold value must be positive and less than the total number of nodes."
    
    print('Selecting UMGs...')
    UMG_inds = np.logical_and(mobility_list['mobility_score'] >= (b * mobility_list.shape[0]), mobility_list['postprop_rank'] <= T) # select UMGs per T and b values
    UMGs = mobility_list[UMG_inds]['node']
    
    return UMGs



if __name__ == "__main__":
    score_list = hp.load_UMG_detection_data(score_list_prefix) # load data
    mobility_list = calculate_mobility(score_list)
    
    UMGs = run(mobility_list, rank_threshold, mobility_beta)
    print('Number of UMGs: {0}'.format(len(UMGs)))
    
    np.savetxt(output_prefix + '_UMGs.txt', UMGs, fmt='%s')
    print('\nUMG list saved to {0}\n{1}'.format(output_prefix + '_UMGs.txt', datetime.datetime.now()))