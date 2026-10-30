# Week_08 — Design Documentation: Sequence Diagram & Chunking/Evaluation Work

**Project:** Contract Playbook Comparison System  
**Team Member:** Yuvicka  
**Week:** 26-Oct-2026 to 01-Nov-2026

## Work Completed

- Prepared the Sequence Diagram showing the flow of a contract review: contract upload, parsing and chunking, indexing, retrieval for each playbook clause, LLM comparison and report generation.
- Included the Missing-clause path in the diagram, where no chunk passes the similarity threshold and the LLM is not called.
- Reviewed the Class Diagram and updated Gantt chart prepared by teammates and checked that the flow and components matched across all three.
- Updated the project documentation to include the Sequence Diagram.
- Continued the chunking experiments locally and started drafting a small script to compute Recall@k and MRR against CUAD labelled spans.

## Team Collaboration

The team divided the design work equally: one member prepared the Sequence Diagram, one prepared the Class Diagram, and one prepared the updated Gantt chart. Each member then reviewed the others' work so that the diagrams stayed consistent with the system workflow and the implementation. Implementation experiments continued in parallel and were discussed in the team meetings.

## Deliverables Completed

- Sequence Diagram
- Reviewed Class Diagram and updated Gantt chart

## Outcome

The Sequence Diagram was completed and the other design artifacts were reviewed for consistency. The team is better prepared to continue the final-product implementation.
