# iCAST-ES 2026 presentation

**Kyle Wild, Yusuke Takahashi, and Asako Uraki**  
*Ingest-Time Fact Compilation for Cost-Efficient and Reliable Question Answering over Revised Corpora* — paper #1571327482.

Review draft, September 13, 2026:

- [Editable PowerPoint with speaker notes](icast-2026-kyle-wild.pptx)
- [PDF slides](icast-2026-kyle-wild.pdf)
- [Slide titles, notes, and timing](slide-manifest.json)
- [Example inputs, saved outputs, and source hashes](examples.json)
- [Camera-ready paper](../icast2026-camera-ready/main.pdf)

Artifact review and publication tracking: [issue #4](https://github.com/aix-sc/isc/issues/4).

The deck contains 12 main slides and 4 appendices in the supplied iCAST template.
It starts with an exact source-to-fact example, explains the revision rules
through three competing versions of one decision, and presents results as
visual comparisons with their interpretations.

Slide 10, “Not every corpus is equal,” compares **Human Dialogue** (25 Federal
Reserve Q&A passages) with **Wikipedia content** (30 passages): generated facts
use 49% and 103% of the original tokens, respectively. Wikipedia’s prior human
editing is presented as an explanatory analogy—already “compiled” prose—not a
measured causal effect of editing.

The synthetic comparison supplies the resolved input from expected-answer
fields; it evaluates reading from that input, not end-to-end compiler accuracy.
All 29 QSR failures lacked a parseable final answer at the completion cap.
The separate real-passage S2 study uses automatic fidelity judgments. Detailed
measurements, limitations, and saved response excerpts remain in the appendices.
No experimental results were changed and no new inference runs were performed.

The PDF was rendered through LibreOffice and checked against all slide text.
The example bundle preserves the source records and saved outputs; `source_files`
paths are relative to the repository root and include SHA-256 hashes.
