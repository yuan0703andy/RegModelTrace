"""The host must use one model identity and chat template for token accounting."""

import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from regmodeltrace.generation import VLLMGenerationBackend


class FakeTokenizer:
    def __init__(self):
        self.template_options = None

    def apply_chat_template(self, messages, **options):
        self.template_options = options
        return "rendered"

    def encode(self, rendered, **options):
        return [1, 2]


class FakeLLM:
    instance = None

    def __init__(self, **options):
        self.tokenizer = FakeTokenizer()
        self.chat_options = None
        self.load_options = options
        FakeLLM.instance = self

    def get_tokenizer(self):
        return self.tokenizer

    def chat(self, conversations, sampling, **options):
        self.chat_options = options
        return [types.SimpleNamespace(outputs=[types.SimpleNamespace(
            text='{"claims": [], "evidence_status": "SUPPORTED"}',
            finish_reason="stop", token_ids=[3],
        )])]


class GenerationRuntimeContractTests(unittest.TestCase):
    def config(self, path):
        return {
            "model_path": str(path), "model_revision": "pinned-revision",
            "enable_thinking": False, "dtype": "auto", "max_model_len": 100,
            "gpu_memory_utilization": 0.85, "seed": 0,
            "max_num_seqs": 1, "tensor_parallel_size": 2,
            "temperature": 0, "max_output_tokens": 10,
        }

    def fake_vllm(self):
        module = types.ModuleType("vllm")
        module.LLM = FakeLLM
        module.SamplingParams = lambda **kwargs: kwargs
        params = types.ModuleType("vllm.sampling_params")
        params.StructuredOutputsParams = lambda **kwargs: kwargs
        return {"vllm": module, "vllm.sampling_params": params}

    def test_wrong_revision_fails_before_model_load(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "other-revision"
            path.mkdir()
            with patch.dict(sys.modules, self.fake_vllm()), patch.dict(
                "os.environ", {"REGMODELTRACE_MODEL_PATH": str(path)}
            ):
                FakeLLM.instance = None
                with self.assertRaisesRegex(ValueError, "configured revision"):
                    VLLMGenerationBackend(self.config(path))
                self.assertIsNone(FakeLLM.instance)

    def test_token_count_and_generation_share_thinking_mode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pinned-revision"
            path.mkdir()
            with patch.dict(sys.modules, self.fake_vllm()), patch.dict(
                "os.environ", {"REGMODELTRACE_MODEL_PATH": str(path)}
            ):
                backend = VLLMGenerationBackend(self.config(path))
                self.assertEqual(FakeLLM.instance.load_options["tensor_parallel_size"], 2)
                result = backend.generate([[{"role": "user", "content": "test"}]], [{}])
                self.assertEqual(result[0]["input_tokens"], 2)
                self.assertIs(
                    FakeLLM.instance.tokenizer.template_options["enable_thinking"], False
                )
                self.assertEqual(
                    FakeLLM.instance.chat_options["chat_template_kwargs"],
                    {"enable_thinking": False},
                )


if __name__ == "__main__":
    unittest.main()
