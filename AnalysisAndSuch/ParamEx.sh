#!/bin/bash
#SBATCH -N 1 -n 1 -c 8
#SBATCH --mem=10000  # Requested Memory
#SBATCH -p cpu  # Partition
#SBATCH -q long #14 day time limit
#SBATCH --time=14-0 # Job time limit
#SBATCH -o slurm-%j.out  # %j = job ID

export OMP_NUM_THREADS=8
python3 -u /home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/Param_space_explorer.py
