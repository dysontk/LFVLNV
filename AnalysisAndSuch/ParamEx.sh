#!/bin/bash
#SBATCH -N 1 -n 1 -c 8
#SBATCH --mem=8192  # Requested Memory
#SBATCH -p gpu  # Partition
#SBATCH -G 1  # Number of GPUs
#SBATCH -q long #14 day time limit
#SBATCH -t 40:00:00  # Job time limit
#SBATCH -o slurm-%j.out  # %j = job ID

export OMP_NUM_THREADS=8
python3 -u /home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/AnalysisAndSuch/Param_space_explorer.py
