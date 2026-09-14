# RegModelTrace REVIEW-1 — 專案負責人摘要

## 最需要先看到的限制

這份報告不能證明 RegModelTrace 已經能可靠判斷所有 vendor–regulator alignment。現有五個 v2.2 fixtures 只有 30 個 primary comparisons，而且共享監管要求、文件與 organization lineage；它們不是 30 個獨立樣本。更直接的限制是：5 個 human-truth `PARTIALLY_ALIGNED` cases 全部被模型判成 `ALIGNED`，而 `CONFLICT` 完全沒有 truth support。因此目前最能支持的結論是「系統可以穩定保存 provenance 並執行 frozen interface」，不是「alignment classifier 已充分泛化或 calibrated」。

## 這次完成了什麼

REVIEW-1 只讀取並重算既有結果，沒有執行新的 Qwen inference、parser、retrieval 或 training。它把五個 v2.2 corpora 的 52 筆 cases 統一成可稽核報告：30 筆 primary comparisons、22 筆 adverse controls。Primary cases 的 evidence-sufficiency 判斷為 23/30 correct；conditional relation 在 29 筆 truth-sufficient cases 中為 21/29 correct；兩階段 joint correctness 為 18/30。

`ALIGNED` 的 precision/recall/F1 是 80.77% / 87.50% / 84.00%。`PARTIALLY_ALIGNED` 是 0% / 0% / 0%。`CONFLICT` 沒有 truth cases 也沒有 predictions，因此 precision、recall、F1 是未測且未定義，不是 100%。Proper scores 只沿用 frozen formulas 與 denominators；它們不能被解讀成全域 probability calibration。

RAG 結果另行報告，沒有混入 alignment classification。RAG v0.2 的 16/16 表示 substantive claims 都能以 ID/span 回到 source assertion；它不等於 16/16 semantic entailment。Same-corpus unseen audit 有 20/20 valid bindings、14 pass/5 partial/1 fail usefulness，以及 3 題共 6 個 unsupported claims。因為 total substantive-claim denominator 沒有 freeze，claim precision 不能計算。

## 我們到底有沒有用 SQL

有，但目前 SQL 只是 original RMS 三份文件的歷史 retrieval layer。三個 SQLite/FTS5 stores 合計 106.56 MiB：一個有 9,946 searchable records 的 foundation store、一個有 9,750 narrative candidates 的 M4A store，以及一個有 6,009 passages 的 M4C store。它們不是 unified cross-vendor production database。

多數後期資料仍在 Parquet、JSON、JSONL、NumPy arrays 與 immutable PDFs。排除 REVIEW-1 自己的輸出後，`regmodeltrace/data` 約 1.63 GiB；45 份 physical PDFs 對應 33 個 unique content hashes。SCALE-1 有 47,458 eligible source assertions，但只有 30 筆 primary alignment comparisons 經 owner adjudication。這兩個數字不能混用。

KCC 的 pages 184–185 仍保留 `FAIL_TABLE_IDENTITY`：4 個 panels 有 140 個 duplicate row/column identities。受影響的 numeric evidence 已排除，沒有在這次報告中修復。

## LoRA 決定

```text
RELEASE_TRAINING_DECISION = NO_TRAINING_THIS_RELEASE
NEXT_RELEASE_RESEARCH_OPTION = ADAPTER_COMPARISON_PROPOSED
TRAINING_AUTHORIZATION = NONE
```

LoRA 仍可能是下一個 release 的研究選項，但現在不授權訓練。Impact G-4、CoreLogic M-2/CI-5 與 KCC V-2/CI-6 都呈現 partial-to-aligned error；然而 KCC 是 final test 結果揭露後才可見，不能回頭改寫原本的 training-trigger decision，也不能再當 untouched test。現有資料缺少 `CONFLICT`，partial examples 太少，且「明確缺少 required facet」與「文件沒有證明 facet」的 label convention 仍需 prospective clarification。

若未來另行批准，正確實驗是比較 unchanged base model、facet-explicit non-training baseline、以及 LoRA model，並用 vendor lineage、related version、shared passages、requirement family 做 leakage-aware split。現在 served 的 AWQ model 也不能直接假設是 QLoRA training base。

## 下一階段應該是什麼

設計上最合理的下一步是 sequential alignment audit：把 requirement 拆成保留 `AND`/`OR`、applicability、exceptions 與 version scope 的 facets，對每個 unresolved facet 選擇 inspect source、request clarification、request validation artifact 或 approved conformance test。Reviewer evidence、vendor evidence 與 independently observed behavior 必須分開。

這份設計不授權 vendor contact 或 test execution。未來若要使用 value of information，也必須先定義 observation model、decision loss 與 acquisition cost；v2.2 token probabilities 不能直接當 Bayesian posterior。沒有 accessible action 或 budget 用完時，正確結果可以是 unresolved。

## Closure

```text
REVIEW_1 = COMPLETE_WITH_LIMITATIONS
REPORTING_ONLY = TRUE
NEW_INFERENCE_RUNS = 0
TRAINING_AUTHORIZATION = NONE
ANONYMITY_WORK = OUT_OF_SCOPE
NEXT_RELEASE_IMPLEMENTATION = NOT_AUTHORIZED
```

完整技術結果、資料庫盤點、LoRA memo 與 sequential audit design 均保留在同一 REVIEW-1 output roots。Closed release 的既有 truth、scores、runtime 與 final decisions 沒有被修改。
