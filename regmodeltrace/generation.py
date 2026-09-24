"""Persistent local Qwen/vLLM answer-generation backend."""

import os
import hashlib
from pathlib import Path

os.environ.setdefault("VLLM_ENABLE_V1_MULTIPROCESSING", "0")


class VLLMGenerationBackend:
    """Load one vLLM engine and reuse it for every request."""

    def __init__(self, config):
        from vllm import LLM

        self.config = config
        model_path = os.environ.get("REGMODELTRACE_MODEL_PATH") or config.get("model_path")
        if not model_path:
            raise ValueError(
                "Set REGMODELTRACE_MODEL_PATH to the pinned Qwen snapshot before starting inference"
            )
        expected_revision = config.get("model_revision")
        if expected_revision and Path(model_path).resolve().name != expected_revision:
            raise ValueError("Model path does not resolve to the configured revision")
        expected_config_hash = config.get("model_config_sha256")
        if expected_config_hash:
            config_path = Path(model_path) / "config.json"
            if not config_path.is_file():
                raise ValueError("Model checkpoint has no config.json")
            actual_hash = hashlib.sha256(config_path.read_bytes()).hexdigest()
            if actual_hash != expected_config_hash:
                raise ValueError("Model checkpoint config hash does not match")
        self.chat_template_kwargs = {
            "enable_thinking": bool(config.get("enable_thinking", False))
        }
        self.llm = LLM(
            model=model_path,
            tokenizer=model_path,
            dtype=config["dtype"],
            max_model_len=config["max_model_len"],
            gpu_memory_utilization=config["gpu_memory_utilization"],
            tensor_parallel_size=config.get("tensor_parallel_size", 1),
            seed=config["seed"],
            enforce_eager=True,
            max_num_seqs=config["max_num_seqs"],
            enable_prefix_caching=False,
            disable_log_stats=True,
        )
        self.tokenizer = self.llm.get_tokenizer()
        self.initialization_count = 1

    def generate(self, conversations, schemas):
        from vllm import SamplingParams
        from vllm.sampling_params import StructuredOutputsParams

        sampling = []
        prompt_token_counts = []
        for conversation, schema in zip(conversations, schemas):
            rendered = self.tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True,
                **self.chat_template_kwargs,
            )
            token_ids = self.tokenizer.encode(rendered, add_special_tokens=False)
            if len(token_ids) + self.config["max_output_tokens"] > self.config["max_model_len"]:
                raise ValueError("Context truncation is forbidden")
            prompt_token_counts.append(len(token_ids))
            sampling.append(
                SamplingParams(
                    temperature=self.config["temperature"],
                    seed=self.config["seed"],
                    max_tokens=self.config["max_output_tokens"],
                    structured_outputs=StructuredOutputsParams(json=schema),
                )
            )
        generated = self.llm.chat(
            conversations,
            sampling,
            chat_template_kwargs=self.chat_template_kwargs,
            use_tqdm=False,
        )
        results = []
        for index, output in enumerate(generated):
            response = output.outputs[0]
            results.append(
                {
                    "text": response.text,
                    "finish_reason": response.finish_reason,
                    "input_tokens": prompt_token_counts[index],
                    "output_tokens": len(response.token_ids),
                }
            )
        return results
