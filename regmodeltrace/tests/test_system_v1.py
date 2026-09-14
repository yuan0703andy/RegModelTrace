import json
import unittest

from regmodeltrace.contracts import ContractError, parse_model_output
from regmodeltrace.service import RegModelTrace


class FakeRetriever:
    initialization_count = 1

    def __init__(self):
        self.calls = 0

    def retrieve(self, question):
        self.calls += 1
        source = {
            "evidence_ref": "E01",
            "assertion_id": "A1",
            "text": "The Team reviewed the method.",
            "document": "Professional Team Report",
            "document_role": "PROFESSIONAL_TEAM_REPORT",
            "document_id": "team",
            "pages": [18],
            "section_path": ["document: report", "context: comments"],
            "source_spans": [{"quote": "The Team reviewed the method."}],
            "source_links": ["https://example.test/report.pdf#page=18"],
            "passage_id": "P1",
            "role_rank": 1,
        }
        return {
            "question": question,
            "sections": [{"document_role": "PROFESSIONAL_TEAM_REPORT", "passages": []}],
            "evidence_sections": [
                {
                    "document_role": "PROFESSIONAL_TEAM_REPORT",
                    "passages": [
                        {
                            "passage_ref": "PR1",
                            "assertions": [
                                {
                                    "evidence_ref": "E01",
                                    "text": source["text"],
                                    "document": source["document"],
                                    "pages": source["pages"],
                                    "section_path": source["section_path"],
                                }
                            ],
                        }
                    ],
                }
            ],
            "references": [source],
            "selected_passage_ids": ["P1"],
        }


class FakeBackend:
    initialization_count = 1

    def __init__(self, evidence_ref="E01"):
        self.calls = 0
        self.evidence_ref = evidence_ref

    def generate(self, conversations, schemas):
        self.calls += 1
        return [
            {
                "text": json.dumps(
                    {
                        "claims": [
                            {"text": "The Team reviewed the method.", "evidence_refs": [self.evidence_ref]}
                        ],
                        "evidence_status": "SUPPORTED",
                    }
                ),
                "input_tokens": 10,
                "output_tokens": 12,
            }
            for _ in conversations
        ]


class SystemContractTests(unittest.TestCase):
    def make_system(self, backend=None):
        return RegModelTrace(
            config_path="regmodeltrace/config/system_v1.json",
            retriever=FakeRetriever(),
            backend=backend or FakeBackend(),
        )

    def test_public_contract_and_host_citation(self):
        system = self.make_system()
        result = system.ask("What did the Team review?")
        self.assertEqual(set(result), {"answer", "status", "evidence"})
        self.assertEqual(result["status"], "SUPPORTED")
        self.assertEqual(result["evidence"][0]["page"], 18)
        self.assertEqual(result["evidence"][0]["quote"], "The Team reviewed the method.")
        self.assertTrue(result["answer"].endswith("[1]"))

    def test_runtime_is_reused_for_sequential_questions(self):
        system = self.make_system()
        system.ask("First question?")
        system.ask("Second question?")
        self.assertEqual(system.initialization_count, 1)
        self.assertEqual(system.retriever.initialization_count, 1)
        self.assertEqual(system.backend.initialization_count, 1)
        self.assertEqual(system.retriever.calls, 2)
        self.assertEqual(system.backend.calls, 2)

    def test_unknown_model_reference_fails_closed(self):
        system = self.make_system(FakeBackend("E99"))
        with self.assertRaises(ContractError):
            system.ask("What did the Team review?")

    def test_empty_question_is_rejected(self):
        system = self.make_system()
        with self.assertRaises(ContractError):
            system.ask("   ")

    def test_duplicate_json_key_is_rejected(self):
        bad = '{"claims": [], "claims": [], "evidence_status": "SUPPORTED"}'
        with self.assertRaises(ContractError):
            parse_model_output(bad, ["E01"])


if __name__ == "__main__":
    unittest.main()

