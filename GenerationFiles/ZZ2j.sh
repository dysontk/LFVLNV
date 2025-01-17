#!/bin/bash
#SBATCH -c 4  # Number of Cores per Task
#SBATCH --mem=8192  # Requested Memory
#SBATCH -p gpu  # Partition
#SBATCH -G 1  # Number of GPUs
#SBATCH -t 01:00:00  # Job time limit
#SBATCH -o slurm-%j.out  # %j = job ID

/work/pi_mjrm_umass_edu/LNV_collider/Generated/ZZ2j/bin/madevent /home/dkennedy_umass_edu/LNV/MyFiles/LFVLNV/GenerationFiles/ZZ2j_run.dat
