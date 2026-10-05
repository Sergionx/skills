---
name: venezuelan-prescription-pdf-validator
description: "Trigger: validate Venezuelan prescription PDF, revisar récipe médico venezolano. Screen prescription completeness with page-cited evidence."
license: Apache-2.0
metadata:
  author: "sergionx"
  version: "1.0"
---

# Venezuelan Prescription PDF Validator

## Activation Contract

Load when asked to screen a Venezuelan medical prescription supplied as a PDF path or attachment against the completeness checklist.

## Hard Rules

- Inspect every relevant page with available PDF extraction, vision, and OCR; reconcile conflicting outputs. Never infer absent, obscured, cropped, or unreadable content.
- Minimize sensitive-data reproduction: redact identifiers and avoid retaining or sharing full names, dates of birth, addresses, telephone numbers, or prescription details unless essential and authorized.
- Distinguish visible presence and legibility from authenticity. Never claim a signature, stamp, identity, professional status, medicine class, or legal validity was authenticated without explicit authoritative external verification.
- Treat this as document-completeness screening, not medical or legal advice. Do not alter treatment instructions or assess clinical appropriateness.
- Cite page and concise, redacted evidence for every verdict. Record inspection limitations and tools used.

## Decision Gates

| Condition | Verdict |
|---|---|
| Required item clearly present and legible | `PASS` |
| Required item clearly absent | `FAIL` |
| Presence, meaning, class, or date cannot be established | `UNVERIFIABLE` |
| Conditional item clearly does not apply | `NOT_APPLICABLE` |

Overall: `NON_COMPLIANT` if any applicable item is `FAIL`; otherwise `MANUAL_REVIEW_REQUIRED` if any applicable item is `UNVERIFIABLE`; otherwise `COMPLIANT`.

## Execution Steps

1. Resolve report language from the user; otherwise use neutral Spanish. Obtain PDF and optional reference/current date. Do not silently substitute a date.
2. Count pages. Extract text and visually inspect every relevant page, including handwriting, stamps, signatures, headers, footers, and annexes. OCR unclear regions when available.
3. Evaluate every checklist item exactly as defined in `references/checklist.md`; preserve its IDs and conditional/date logic.
4. For unreadable or conflicting evidence, return `UNVERIFIABLE` and explain what manual verification is needed.
5. Compute overall result from applicable item verdicts only. Render the compact structure in `assets/report-schema.json`; keep evidence redacted.
6. After presenting the report, ask the user ONE question and STOP: whether to extract the data below. Do not extract before an explicit yes. If the invoice is not in the supplied PDF, ask for it in the same question.
7. On yes, locate each field below and verify it is legible (same `PASS`/`FAIL`/`UNVERIFIABLE` gates, with page and redacted evidence) BEFORE transcribing it. Transcribe only fields judged legible; for the rest return `null` with the reason and a manual action. Never guess or complete a partly legible value.

## Extraction Fields

| Group | Field | Key |
|---|---|---|
| Prescription | Beneficiary | `beneficiary` |
| Prescription | Treatment type | `treatment_type` |
| Prescription | Prescription date | `prescription_date` |
| Invoice | State where the purchase was made | `purchase_state` |
| Invoice | Invoice number | `invoice_number` |
| Invoice | Invoice date | `invoice_date` |
| Invoice | Invoice amount (with currency) | `invoice_amount` |

Dates use ISO `YYYY-MM-DD`; flag ambiguous day/month order as `UNVERIFIABLE`. Extracted values are shown only to the requesting user, never persisted or shared.

## Output Contract

Return one structured report containing `overall_result`, per-item `checks`, `document_scope`, `limitations`, `manual_actions`, and `disclaimer`. Each check includes ID, verdict, page/evidence, and reason; include calculation inputs for the seven-day rule. When extraction was accepted, also include `extraction` with one entry per field: `legibility` verdict, `page`, `value` (or `null`), and `reason`.

## References

- `references/checklist.md` — authoritative item definitions and conditional logic.
- `assets/report-schema.json` — compact machine-readable report shape.
