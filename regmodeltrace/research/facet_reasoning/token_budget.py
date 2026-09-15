"""Count token IDs, not mapping fields, across tokenizer API return shapes."""
from collections.abc import Mapping


def count_chat_tokens(tokenizer, conversation) -> int:
    encoded = tokenizer.apply_chat_template(
        conversation, tokenize=True, add_generation_prompt=True, return_dict=False
    )
    if isinstance(encoded, Mapping):
        encoded = encoded['input_ids']
    if len(encoded) and isinstance(encoded[0], (list, tuple)):
        if len(encoded) != 1:
            raise ValueError('Expected a single conversation for token budget validation')
        encoded = encoded[0]
    return len(encoded)
