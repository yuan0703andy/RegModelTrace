#!/usr/bin/env bash
set -euo pipefail

cd /hpc/home/yh421/CIRCAD-LLM
runtime_root=/hpc/group/borsuklab/yh421/regmodeltrace-runtime
python_bin="$runtime_root/gpu-env/bin/python"
export PATH="$runtime_root/gpu-env/bin:$PATH"
export HF_HOME="$runtime_root/hf-cache"
export VLLM_CACHE_ROOT="$runtime_root/vllm-cache"
export TOKENIZERS_PARALLELISM=false

frozen=${FT1_FROZEN:?Set FT1_FROZEN to the prospectively frozen Phase 1 directory}
run_root=${FT1_RUN_ROOT:-artifacts/ft-1/runs}
run_dir="$run_root/run-${SLURM_JOB_ID:?}"

if [[ ! -f "$frozen/freeze.json" ]]; then
  echo "FT-1 human/facet freeze is absent; B/C inference blocked" >&2
  exit 93
fi
if find "$run_root" -mindepth 1 -maxdepth 1 -type d -name 'run-*' -print -quit 2>/dev/null | grep -q .; then
  echo "An FT-1 B/C run already exists; implicit rerun prohibited" >&2
  exit 94
fi

PYTHONPATH=. "$python_bin" -m regmodeltrace.research.facet_reasoning.run_conditions_bc \
  --frozen "$frozen" \
  --output "$run_dir"

echo "Raw B/C results persisted at $run_dir"
echo "Scoring requires frozen truth and an independently audited safety-violation count."
