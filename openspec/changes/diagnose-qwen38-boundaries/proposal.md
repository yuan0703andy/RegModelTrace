# Diagnose Qwen3.8 synthetic evidence boundaries

The pinned Qwen3.8 checkpoint loaded and produced valid JSON, but one synthetic
reviewer-scrutiny sentence was labeled as a reviewer challenge. One response
does not establish a systematic model weakness. The existing product default
remains Qwen2.5 while a small, frozen diagnostic distinguishes a repeatable
review/challenge error from a single result and checks the adjacent causal-link
boundary.

This is a synthetic diagnostic, not natural-document validation or a release
gate. It does not modify prompts, gold, historical FG-2 scores, model weights,
retrieval, or the active service default. Its strongest limitation is that
short constructed sentences omit the complexity of real regulatory documents.
