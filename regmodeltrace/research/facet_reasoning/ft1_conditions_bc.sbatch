#!/usr/bin/env bash
#SBATCH --job-name=rmt-ft1-bc
#SBATCH --time=00:45:00
#SBATCH --nodes=1
#SBATCH --partition=gpu-common,scavenger-gpu
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --gres=gpu:5000_ada:1
#SBATCH --output=artifacts/ft-1/run-%j.log

set -euo pipefail
cd /hpc/home/yh421/CIRCAD-LLM
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-4}"
case "$(hostname)" in dcc-login-*) exit 91;; esac
nvidia-smi --query-gpu=index,name,uuid,memory.total --format=csv,noheader

: "${FT1_FROZEN:?Export FT1_FROZEN only after independent human truth is frozen}"
srun --ntasks=1 --cpus-per-task="${SLURM_CPUS_PER_TASK:-4}" \
  bash scripts/run_ft1_conditions_bc_local.sh
