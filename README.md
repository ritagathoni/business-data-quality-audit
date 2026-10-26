# Business Data Quality Audit

**Focus:** audit-style review of synthetic invoices, anomaly detection, duplication, type/format checks, SQL reconciliation and privacy-aware exception logging.

## Business question
What could go wrong if inconsistent supplier invoice data is used for reporting or payments without a systematic QA gate?

## Synthetic dataset
Five **fabricated** invoice records intentionally include an invoice-ID duplicate, negative amount, numeric type mismatch, date-format inconsistency, non-standard currency code and example email address. No genuine vendor or financial records are used.

## Audit procedure
**Ingest → Profile → Validate → Record exceptions → Investigate → Remediate → Recheck.**

### Checks implemented
- Duplicate invoice identifiers (Python set + SQLite cross-check).
- Numeric amount type and sign.
- Currency standardization (KES/USD allowlist for this synthetic scenario).
- ISO-like `YYYY-MM-DD` date format (regex, not full calendar validity).
- Presence of an email-like string in free-text notes (potential PII flag).

## Run
```bash
python -m src.audit
python -m unittest discover -s tests -v
```

## Interpreting anomalies
A negative amount might represent a legitimate credit note. The auditor should **flag it for contextual review**, not assume fraud or delete it. Similarly, a flagged email might be allowed in one workflow but not another. This project shows *exception management*, not automatic decisions about people.

## Investigation matrix
| Finding | Risk | Suggested next step |
|---|---|---|
| Duplicate ID | Double counting/payment | Match supplier, amount, source document |
| Negative amount | Misclassified adjustment | Confirm credit memo and transaction type |
| Currency mismatch | Incorrect reporting | Validate supported code and FX assumptions |
| Text amount | Invalid aggregation | Normalize only after source verification |
| PII-like email | Privacy exposure | Apply minimization and authorized-access policy |

## Expansion roadmap
Add referential integrity, reconciliation to purchase orders, SQLite profiling reports, input-document OCR only if necessary, PII detection with false-positive analysis, a remediation log and regression test cases.

## Skills demonstrated
Python · SQL / SQLite · Data quality · Reconciliation · Document review · Audit trails · Anomaly detection · Privacy-aware QA

# Scope and evidence

This is a **synthetic, independently developed demonstration**, not a reproduction of confidential employer data. All prompts, labels, examples, names and records are fabricated for demonstration. Sample counts and test outcomes are software demonstrations, **not historical workplace impact statistics**.

The repository demonstrates evaluation methodology and runnable code; it does not certify that the author achieved a specific result at a named client.

