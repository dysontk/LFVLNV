#!/bin/bash
#SBATCH -c 4  # Number of Cores per Task
#SBATCH --mem=8192  # Requested Memory
#SBATCH -p gpu  # Partition
#SBATCH -G 1  # Number of GPUs
#SBATCH -t 20:00:00  # Job time limit
#SBATCH -o slurm-%j.out  # %j = job ID

python3 /work/pi_mjrm_umass_edu/LNV_collider/Generated/LNVF/bin/madevent /home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/GenerationFiles/LNVF_run.dat 2>&1 | tee /home/dkennedy_umass_edu/LNV/MG5_aMC_v3_5_4/MyFiles/LFVLNV/GenerationFiles/logs/LNVF/outputLNVF.txt