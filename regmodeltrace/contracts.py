"""Strict model-output and public-response contracts for RegModelTrace v1."""

import json


STATUSES = (
    "SUPPORTED",
    "PARTIALLY_SUPPORTED",
    "UNRESOLVED_FROM_RETRIEVED_EVIDENCE",
)


class ContractError(ValueError):
    """Raised when an answer cannot be safely materialized."""


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError("DUPLICATE_JSON_KEY")
        value[key] = item
    return value


def model_output_schema(valid_refs):
    refs = list(valid_refs)
    return {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "minItems": 1,
                "maxItems": 10,
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "minLength": 1},
                        "evidence_refs": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 12,
                            "items": {"type": "string", "enum": refs},
                        },
                    },
                    "required": ["text", "evidence_refs"],
                    "additionalProperties": False,
                },
            },
            "evidence_status": {"type": "string", "enum": list(STATUSES)},
        },
        "required": ["claims", "evidence_status"],
        "additionalProperties": False,
    }


def parse_model_output(text, valid_refs):
    """Validate model JSON without repairing or borrowing context."""
    try:
        value = json.loads(text, object_pairs_hook=_unique_object)
    except ContractError:
        raise
    except (TypeError, ValueError) as exc:
        raise ContractError("INVALID_JSON") from exc

    if not isinstance(value, dict) or set(value) != {"claims", "evidence_status"}:
        raise ContractError("INVALID_TOP_LEVEL")
    if value["evidence_status"] not in STATUSES:
        raise ContractError("INVALID_STATUS")
    if not isinstance(value["claims"], list) or not 1 <= len(value["claims"]) <= 10:
        raise ContractError("INVALID_CLAIMS")

    allowed = set(valid_refs)
    for claim in value["claims"]:
        if (
            not isinstance(claim, dict)
            or set(claim) != {"text", "evidence_refs"}
            or not isinstance(claim["text"], str)
            or not claim["text"].strip()
        ):
            raise ContractError("INVALID_CLAIM")
        refs = claim["evidence_refs"]
        if not isinstance(refs, list) or not refs or any(ref not in allowed for ref in refs):
            raise ContractError("INVALID_EVIDENCE_REFS")
        claim["text"] = claim["text"].strip()
        claim["evidence_refs"] = list(dict.fromkeys(refs))
    return value


def validate_question(question):
    if not isinstance(question, str) or not question.strip():
        raise ContractError("QUESTION_REQUIRED")
    question = question.strip()
    if len(question) > 2000:
        raise ContractError("QUESTION_TOO_LONG")
    return question

