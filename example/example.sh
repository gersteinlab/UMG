#!/usr/bin/env bash

data_dir=example/data
results_dir=example/results

if [ ! -d $results_dir ] 
then 
	mkdir $results_dir 
fi

### Run Propagation ###

python src/propagate.py \
	-n $data_dir/network \
	-m $data_dir/matrix \
	-o $results_dir/example
	
### Find UMGs ###

# we use a small T for the toy example
python src/find_UMGs.py \
	--scr $results_dir/example \
	-o $results_dir/example \
	-T 15 \
	-b 0.25 

echo "Execution has completed."
