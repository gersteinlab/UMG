# UMG #

A network propagation method to detect 'upward mobility' nodes, i.e. ones whose rank improves significantly, during propagation. The method is developed to prioritize long tail genes in cancer and can be used for other applications with a similar goal.


### Requirements ###

Python 3.6
Numpy 1.16

### Code ###

Code is available through this GitHub repository.

To clone the code, please run: git clone https://github.com/gersteinlab/UMG

### Example ###

To run a toy example , please run: sh example/example.sh.

### Input ###

To run UMG on a single network and gene-sample matrix, two matrix files and their indices are required (i.e. 4 files in total).

Each index includes node names in the order that matches the corresponding matrix's rows. For sample files, see example/data/.

### Output ###

The first step in UMG, i.e. network propagation using propagate.py, outputs the post-propagation matrix and its index, and the score file with 3 columns: node name, intial score across samples, and final score.

The second step, i.e. UMG detection using find_UMGs.py, outputs the list of detected upward mobility genes (UMGs).

### Notes ###

All files are tab-delimited and end with /txt.

A matrix index file must have the same matrix filename appended with 'index' (e.g. matrix.txt and matrix_index.txt).

### License ###

UMG is under the MIT License, copyrighted by the Gerstein Lab. Please see License.md for more details.