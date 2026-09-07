# Contract Playbook Comparison System
 
**A Retrieval-Augmented System for Automated Contract Clause Review**
 
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://upasnawadhwa.github.io/UCS503P-202627-Contract-Playbook-Comparison/)
[![Status](https://img.shields.io/badge/status-proposal-yellow)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
 
> Course project for **UCS503 — Software Engineering**, UCS503P (2026–27 ODD)
> Thapar Institute of Engineering and Technology
 
---
 
## Course & Instructor Details
 
| | |
|---|---|
| **Course** | UCS503 — Software Engineering (UCS503P, 2026–27 ODD) |
| **Institute** | Thapar Institute of Engineering and Technology |
| **Instructor** | Dr. Jeelani Asif |
| **Repository** | [UCS503P-202627-Contract-Playbook-Comparison](https://github.com/UpasnaWadhwa/UCS503P-202627-Contract-Playbook-Comparison) |
 
---
 
## Team
 
| Name | Branch | Roll No. | Email |
|---|---|---|---|
| Mannat | DSAI | 1024240023 | mmannat_be24@thapar.edu |
| Upasna Wadhwa | DSAI | 1024240022 | uwadhwa_be24@thapar.edu |
| Yuvicka | DSAI | 1024240016 | yyuvicka_be24@thapar.edu |
 
---
 
## Overview
 
Legal and procurement teams review the vendor, SaaS, and service contracts against an internal **playbook** that is a set of pre-approved clause positions (e.g., liability caps, termination notice periods, auto-renewal opt-outs etc). This manual review is slow, inconsistent across reviewers, and hard to audit, and naively feeding whole contracts to an LLM risks hallucinated, unverifiable decisions.
 
The **Contract Playbook Comparison System** is a retrieval-augmented generation (RAG) pipeline that grounds every verdict in an exact, cited span of the source contract. Rather than asking an LLM "does this contract comply with our policy?", the system:
 
1. Retrieves the specific contract chunk(s) relevant to each playbook clause type.
2. Asks the LLM to compare *only* that retrieved text against the playbook position.
3. Classifies the clause as **Match**, **Deviation**, or **Missing**, with a citation back to the source text.
This keeps every output traceable and auditable which is required when a missed clause carries real financial or legal consequences.
 
---
 
## Problem Statement
 
- **Slow, non-scaling review** : manual review takes significant time per contract and doesn't scale with volume.
- **Inconsistent outcomes** : different reviewers catch different variations.
- **No audit trail** : verdicts aren't linked back to the exact source text.
- **Hallucination risk** : naive "read the whole contract and answer" LLM use produces unverifiable, sometimes fabricated answers.
Contract Lifecycle Management (CLM) is an established, funded software category (Ironclad, LinkSquares, Lawgeex, Evisort), confirming this is a genuine workflow gap rather than a contrived exercise.
 
---
 
## Proposed Solution
 
### Pipeline Stages
 
| Stage | Description |
|---|---|
| **Ingestion** | Parse contracts (PDF/text) and chunk into ~300–500 token segments with ~15% overlap, tuned for long legal clauses. |
| **Indexing** | Sentence-transformer embeddings (FAISS/ChromaDB) + a BM25 keyword index for hybrid retrieval because exact legal terms like "indemnify" or "force majeure" often matter as much as semantic similarity. |
| **Retrieval** | For each playbook clause type, return top-*k* candidate chunks. If nothing passes a similarity threshold, classify the clause as **Missing** directly and hence the LLM is never asked to guess from nothing. |
| **Comparison** | An LLM receives only the playbook position and the retrieved chunk(s), and classifies the clause as **Match**, **Deviation**, or **Missing** with a one-sentence, text-grounded explanation. |
| **Reporting** | A structured, reviewer-facing report: one row per playbook clause, with status, explanation, and an exact citation into the source contract. |
 
### Core Workflow
 
1. Contract is parsed and chunked.
2. Retrieval returns top-*k* candidates per playbook clause type.
3. Below-threshold clauses are marked **Missing** without LLM involvement.
4. Otherwise, the LLM compares retrieved text to the playbook position.
5. Results are compiled into a structured, citation-backed report.
### Operational Constraints
 
- Uses the public **CUAD** dataset rather than sourcing/labelling proprietary contracts.
- Favours standard, well-documented retrieval and evaluation techniques over unproven algorithms.
- Targets a reproducible local/demo deployment (Streamlit or Gradio) rather than production infrastructure.
---
 
## Dataset
 
**CUAD (Contract Understanding Atticus Dataset)** — 510 real commercial contracts with 13,000+ expert-annotated clause spans across 41 categories.
 
- 5–8 clause categories are selected based on sufficient positive-example counts, each with a documented standard playbook position.
- Held-out CUAD contracts provide automatic ground truth for retrieval evaluation.
- A small hand-labelled set (~50–100 pairs) supports Match/Deviation/Missing classification evaluation.
---
 
## Tech Stack
 
- **Embeddings:** `sentence-transformers` (e.g., `all-mpnet-base-v2`, or a legal-domain model like Legal-BERT)
- **Vector store:** FAISS or ChromaDB
- **Keyword index:** `rank_bm25`
- **LLM:** any accessible LLM API (comparison/classification step)
- **Evaluation:** RAGAS (RAG-specific evaluation framework)
- **Demo UI:** Streamlit or Gradio
- **Parsing:** pdfplumber / PyMuPDF
---
 
## Evaluation Criteria
 
| Metric | What it measures | Ground truth |
|---|---|---|
| **Retrieval accuracy** (primary) | Recall@k (k=3–5), MRR per clause category | CUAD labelled spans |
| **Classification accuracy** | Agreement between pipeline verdicts and hand-labelled test set | Manually labelled Match/Deviation/Missing pairs |
| **Faithfulness** | Whether the LLM's explanation is grounded in retrieved text | Manual check + optional RAGAS NLI-based check |
| **Coverage** | % of clause types returning confident retrieval vs. falling back to Missing | Threshold-based, computed automatically |
 
**Validation plan:** evaluate on a held-out CUAD split not used to design playbook positions; compare hybrid (semantic + BM25) retrieval against semantic-only retrieval as an ablation.
 
---
 
## Project Structure
 
```
.
├── proposal/                  # Project Proposal (LaTeX)
├── prototype-report/          # Project Report, Prototype Stage (LaTeX)
├── final-report/              # Project Report Final (LaTeX)
├── journals/                  # One folder per team member, weekly journal entries
│   ├── Mannat/
│   ├── Upasna-Wadhwa/
│   └── Yuvicka/
├── code/                      # Source code for the pipeline
├── docs/                      # Markdown docs, built via mkdocs
└── README.md
```
 
---
 
## Documentation
 
Docs are written in Markdown under `docs/` and built with [MkDocs](https://www.mkdocs.org/). Any commit to `master` triggers CI/CD to build and deploy the docs (including journals) to GitHub Pages.
 
To view a local dev build of the docs:
 
```shell
make docs
```
 
---
 
## Project Roadmap
 
### Initial Deliverable
- [ ] Playbook definition for 5–8 clause categories with documented positions
- [ ] Ingestion and chunking pipeline for CUAD contract text
- [ ] Embedding index (FAISS/ChromaDB) with basic semantic retrieval
- [ ] Retrieval evaluation against CUAD ground-truth spans (Recall@k, MRR)
- [ ] CI: automated evaluation run + linting on every change
### Subsequent Deliverables
- [ ] Hybrid retrieval (BM25 + semantic) with ablation comparison
- [ ] LLM-based clause comparison with structured Match/Deviation/Missing output
- [ ] Hand-labelled classification test set + accuracy/faithfulness evaluation
- [ ] Streamlit/Gradio demo: contract selection → playbook comparison → cited report
---
 
## Risks & Mitigations
 
| Risk | Mitigation |
|---|---|
| LLM hallucination even with retrieved context | Strict prompting ("only use provided text; say 'cannot determine' if unclear"); always surface retrieved source text alongside the verdict |
| Class imbalance in CUAD categories | Check per-category label counts early; choose clause types with enough representation |
| Fuzzy clause boundaries | Allow retrieval to return multiple adjacent chunks rather than a single best match |
| Domain-specific phrasing confusing embeddings | Hybrid semantic + keyword retrieval |
 
---
 
## CI/CD
 
- Automated retrieval and classification validation scripts run on every pipeline change.
- Repeatable demo builds (Streamlit/Gradio) generated for weekly review.
- Enables safe, frequent iteration on individual pipeline stages without manual full-system re-evaluation.
---
 
## License
 
This project is licensed under the [MIT License](LICENSE), a permissive, widely-used open-source license that lets others use, modify, and share the code as long as they include the original copyright notice.
 
---
 
## Contact
 
For questions about this project, reach out to any team member listed above, or open an issue on the [repository](https://github.com/UpasnaWadhwa/UCS503P-202627-Contract-Playbook-Comparison).
 
