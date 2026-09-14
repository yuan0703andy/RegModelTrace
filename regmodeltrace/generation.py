"""Persistent local Qwen/vLLM answer-generation backend."""

import os

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
        self.llm = LLM(
            model=model_path,
            tokenizer=model_path,
            dtype=config["dtype"],
            max_model_len=config["max_model_len"],
            gpu_memory_utilization=config["gpu_memory_utilization"],
            tensor_parallel_size=1,
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
                conversation, tokenize=False, add_generation_prompt=True
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
        generated = self.llm.chat(conversations, sampling, use_tqdm=False)
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
