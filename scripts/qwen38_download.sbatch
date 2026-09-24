#!/usr/bin/env bash
#SBATCH --job-name=rmt-qwen38-fetch
#SBATCH --partition=scavenger
#SBATCH --account=borsuklab
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=03:00:00

set -euo pipefail
runtime_root=/hpc/group/borsuklab/yh421/regmodeltrace-runtime
export PATH="$runtime_root/gpu-env/bin:$PATH"
export HF_HOME="$runtime_root/hf-cache"
export RMT_QWEN38_CACHE_DIR="$runtime_root/hf-cache/hub"
export HF_HUB_DOWNLOAD_TIMEOUT=120
export HF_HUB_ETAG_TIMEOUT=30
: "${RMT_QWEN38_ROOT:?Set external checkpoint workspace}"
export RMT_QWEN38_RECEIPT_DIR="$RMT_QWEN38_ROOT/download-${SLURM_JOB_ID:?}"
case "$(hostname)" in dcc-login-*) exit 91;; esac
cd "$RMT_QWEN38_ROOT"
srun "$runtime_root/gpu-env/bin/python" qwen38_download.py
