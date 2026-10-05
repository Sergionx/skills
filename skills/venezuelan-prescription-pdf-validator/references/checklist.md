# Prescription Completeness Checklist

Use only evidence visible in the supplied PDF or explicitly verified through an authoritative source. Evidence snippets must be concise and redact sensitive values (for example, `V-12***89`). A page citation may be `p. 2`; use `page: null` when no page supports an absent item.

| ID | Required check | Evaluation |
|---|---|---|
| `issuer_identity` | Doctor, clinic, or institute name plus cédula or RIF | `PASS` only when both a qualifying name and corresponding cédula/RIF are legible. |
| `issue_date` | Issue date | `PASS` only when a complete, legible issue date is present. |
| `patient_identity` | Patient first name, surname, and C.I. or cédula number | `PASS` only when all three components are legible. |
| `pediatric_birth_date` | Patient birth date only for pediatric treatments | If treatment is clearly pediatric, birth date is required. If clearly not pediatric, use `NOT_APPLICABLE`. If pediatric applicability cannot be established, use `UNVERIFIABLE`; do not infer age from medicine, dose, appearance, or partial identifiers. |
| `medication_directions` | Medication directions or indications | `PASS` only when directions/indications are present and legible enough to identify their existence and content. Do not assess clinical adequacy. |
| `doctor_stamp` | Original stamp or legible image of doctor's stamp | `PASS` when a legible image of the doctor's stamp is visibly present. A PDF cannot establish that a stamp is physically original; use `UNVERIFIABLE` if originality, rather than visible presence, must be established. Never claim authenticity. |
| `specialist_signature` | Specialist doctor's signature | `PASS` when a signature attributed by the document to the specialist doctor is visibly present and legible as a signature mark. Do not authenticate it or independently assert specialist status. |
| `provider_contact` | Physical address and telephone numbers for office, clinic, institute, or medical service provider | `PASS` only when both a physical address and at least one legible telephone number are present. |
| `seven_day_validity` | Psychotropic or antibiotic prescriptions are valid for seven consecutive calendar days from issue | Apply the calculation below. |

## Seven-day rule

1. Classify the prescribed medicine only from clear document text or an explicitly supplied authoritative classification. If any relevant medicine cannot be classified confidently as psychotropic, antibiotic, or neither, use `UNVERIFIABLE` and identify the classification needed. Never classify by guesswork.
2. If every medicine is confidently neither psychotropic nor antibiotic, use `NOT_APPLICABLE`.
3. If any medicine is psychotropic or antibiotic, require a legible issue date and an explicit reference/current date. If either is unavailable or invalid, use `UNVERIFIABLE`.
4. Count the issue date as calendar day 1. The valid window is issue date through issue date + 6 calendar days, independent of hours. Report dates, elapsed calendar days, and inclusive window.
5. Use `PASS` when the reference date is within that window and `FAIL` when it is later. If the reference date precedes the issue date or date interpretation conflicts, use `UNVERIFIABLE` and request manual review.

This verdict addresses only the stated seven-day document rule. It does not establish dispensing eligibility or broader legal validity.
