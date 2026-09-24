# Upgrade the active local model to Qwen3.8-27B-FP8

The owner requested a direct upgrade to the newer local Qwen model. The active
RegModelTrace service still names Qwen2.5-32B-Instruct-AWQ, while the completed
FG-2 experiment used a pinned Qwen3.5-27B-FP8 checkpoint. This change upgrades
only the active product runtime and future requests. It does not rewrite frozen
experiments or claim improved documentary judgment from a runtime smoke test.

The strongest operational objection is that a newer checkpoint may not load in
the installed vLLM environment, and its default thinking mode may break the
existing bounded JSON interface. The exact public revision and checksum-verified
weights are selected now, with fail-closed model-path validation. A bounded GPU
smoke remains the separate readiness gate; queue delay must not be reported as
runtime success or improved semantic quality.
