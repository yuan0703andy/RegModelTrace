# Gold Case 001 — Frozen Gold Core

版本：`gold-case-001-v0.3.0`。目前 substantive conclusion：**CAUSAL ATTRIBUTION = UNRESOLVED**。

**Gold Core：12 個 records、17 個完整 source spans。Audit Context：57 個 records。** 後者保留在完整 audit trail，對 primary recall 分母的貢獻為零。

這是本案採用的操作性最小集合；不宣稱它是唯一或數學上最小的集合。使用者提出的替代項中，選用 `S_M3_CONTEXT` 與 `T_HISTORY`。

## 五項 substantive statements

1. M-3.B 要求 coastal-segment historical consistency。
2. Professional Team 確實檢查 gate/category landfall methodology 與 historical-frequency smoothing。
3. RMS 描述自己的 methodology；固定三份 PDF 未找到明確的 post-review M-3.B response。
4. Model updates 確實存在；固定三份 PDF 未建立它們由 April review 造成的因果連結。
5. 因此結論為 UNRESOLVED；不能據此斷言 regulation caused modification，也不能斷言 regulation caused no modification。

## Gold Core 與來源

Document codes：S = 2019 FCHLPM Standards；V = RMS 21.0 revised submission；T = April 19–22, 2021 Professional Team Report。頁碼為實體 PDF 頁碼。

| Core record | Document / page / exact span | 納入理由 |
|---|---|---|
| S_M3B | [S p.120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) `[191,463)` | Regulatory coastal-segment historical-consistency requirement. |
| S_M3_CONTEXT | [S p.120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) `[0,190)`; [S p.120](https://fchlpm.sbafla.com/media/o10dfucl/2019_hurricaneroa.pdf#page=120) `[464,1714)` | Same-standard purpose and intensity context qualify consistency; selected instead of adding S_S1_DIFFERENCES to the denominator. |
| V_M3B | [V p.67](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=67) `[250,856)` | Vendor compliance assertion, distinct from a dated review response. |
| V_SMOOTHING | [V p.16](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=16) `[259,841)` | Coastal-frequency smoothing and calibration methodology. |
| V_POISSON | [V p.88](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=88) `[3550,3753)`; [V p.89](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=89) `[62,446)` | Poisson means calibrated toward smoothed coastal counts; continuation must survive parsing. |
| T_LANDFALL_REVIEW | [T p.17](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=17) `[1921,2024)`; [T p.18](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=18) `[47,162)` | Completed scrutiny of gate/category updates and historical-frequency smoothing. |
| T_M3_REVIEW | [T p.20](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=20) `[128,313)` | Actual M-3 comments and verification; no explicit modification instruction in these comments. |
| V_PRIOR_UPDATE | [V p.35](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=35) `[651,1180)`; [V p.35](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=35) `[1639,1918)` | Update description explicitly uses the prior-accepted to initial-submission baseline. |
| V_BASELINE_VERSION | [V p.36](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=36) `[1690,2237)` | Identifies the versions being compared and prevents a within-review baseline substitution. |
| T_OPENING_UPDATES | [T p.3](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=3) `[393,1390)` | The event-set update was already presented at the opening briefing. |
| T_HISTORY | [T p.62](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=62) `[675,930)`; [T p.62](https://fchlpm.sbafla.com/media/uzkplkto/20210422_rms_2019stds_ptrpt.pdf#page=62) `[1625,1970)` | Actual change-history reference remains unmatched; selected instead of S_REVISION_PROCESS for this minimum. |
| V_M1_TABLE | [V p.178](https://fchlpm.sbafla.com/media/c5apncqi/rms19standardsdisclosures_04222021.pdf#page=178) `[0,1468)` | Observed and modeled values differ; table row/column associations matter. |

Exact spans 是 whitespace-normalized `pdftotext -layout -enc UTF-8` page text 的零起算 Unicode `[start,end)` 位置；每段完整文字、頁面與 PDF 均有 checksum。

## Evaluation contract

**Primary denominator = 12 個唯一 core records。** 同一 record 出現在多個問題時只計一次；一個 record 有多段 source spans，也只算一個 record，但所有 spans 都必須可恢復。未找到的 response/modification slots 不存在可供 positive recall 的 passage，因此另行評估狀態與因果判斷。

內容完整性、coherent unit、page provenance、headers/footers 分離、Table M-1 欄列正確性分開驗收。保存所有文字不代表上述結構都正確，更不等同 retrieval 或 semantic conclusion accuracy。尚未執行 parser，因此沒有 recovery 分數。

`T_FORM_M3`、`T_INDEPENDENCE`、`V_TRACK_SMOOTHING`、`V_WIND_NO_CHANGE` 留在 audit context / rejected candidates；不列入 core 分母。

## 狀態與 freeze 範圍

`specific_m3b_challenge`、`explicit_post_review_vendor_response`、`review_induced_model_modification` 均使用 `SEARCHED_AND_NOT_FOUND_IN_FIXED_CORPUS`。`causal_attribution` 保持 `UNRESOLVED`。

使用者於 2026-09-10 回報 critical-page spot-check，並明確接受 UNRESOLVED 結論。本 freeze 記錄這個審查範圍；不把它擴寫為 69 個 records 全數獲得 independent human sign-off。這不阻止以固定版本進行 parser 設計與測試。

## 檢視與後續設計

[完整 audit trail](m3b_rms_review.md) · [Core JSON](m3b_rms_gold_core.json) · [全部 annotations](m3b_rms_chain.json)

[Milestone 2 parser design](</Users/andyhou/Documents/ChatGPT/CIRCAD-LLM/openspec/changes/design-parser/design.md>)

僅列印這十二個 records 的完整原文：

```sh
.venv/bin/python regmodeltrace/scripts/inspect_gold_passage.py --core
```
