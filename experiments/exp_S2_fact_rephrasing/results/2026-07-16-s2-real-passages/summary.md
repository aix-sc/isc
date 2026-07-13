# S2 Fact Rephrasing Measurement

Passage set: 30 public Wikipedia passages snapshotted in `passages.jsonl`.

Token counter: `tiktoken:cl100k_base`.

| Metric | Value |
| :-- | --: |
| Original tokens | 3,748 |
| S2 fact tokens | 3,854 |
| Overall compression ratio | 1.0283 |
| Median passage compression ratio | 1.0227 |
| Compression ratio range | 0.8571-1.4561 |
| Generated facts | 223 |
| Entailed fact rate | 1.0000 |
| QA fidelity rate | 0.9667 |
| Passages with missing major claims | 0 |

Suggested manuscript sentence:

> On 30 public Wikipedia passages, S2 fact rephrasing produced 1.03x as many tokens as the original passage text using `tiktoken:cl100k_base`, with 100.0% of generated facts judged source-entailed and 96.7% passage-level QA-fidelity pass rate.
