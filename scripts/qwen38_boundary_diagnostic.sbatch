#!/usr/bin/env bash
#SBATCH --job-name=rmt-qwen38-boundary
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --partition=gpu-common
#SBATCH --account=borsuklab
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:5000_ada:2

set -euo pipefail
runtime_root=/hpc/group/borsuklab/yh421/regmodeltrace-runtime
export PATH="$runtime_root/gpu-env/bin:$PATH"
export HF_HOME="$runtime_root/hf-cache"
export VLLM_CACHE_ROOT="$runtime_root/vllm-cache"
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export HF_HUB_OFFLINE=1

: "${RMT_QWEN38_BOUNDARY_ROOT:?Set the diagnostic workspace before submission}"
checkpoint="$runtime_root/hf-cache/hub/models--Qwen--Qwen3.8-27B-FP8/snapshots/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a"
case "$(hostname)" in dcc-login-*) exit 91;; esac
cd "$RMT_QWEN38_BOUNDARY_ROOT"
srun --ntasks=1 --cpus-per-task="${SLURM_CPUS_PER_TASK:-8}" \
  "$runtime_root/gpu-env/bin/python" qwen38_boundary_diagnostic.py \
  --cases "$RMT_QWEN38_BOUNDARY_ROOT/cases.json" \
  --model-path "$checkpoint" \
  --output "$RMT_QWEN38_BOUNDARY_ROOT/run-${SLURM_JOB_ID:?}"
