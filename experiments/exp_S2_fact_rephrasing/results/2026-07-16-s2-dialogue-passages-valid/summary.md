# S2 Fact Rephrasing Measurement: Dialogue Subset

Passage set: 25 Federal Reserve press-conference dialogue excerpts snapshotted in `passages.jsonl`.

Attempted passages: 30; excluded malformed model completions: 5.

Token counter: `tiktoken:cl100k_base`.

| Metric | Value |
| :-- | --: |
| Original tokens | 6,789 |
| S2 fact tokens | 3,310 |
| Overall compression ratio | 0.4876 |
| Median passage compression ratio | 0.4734 |
| Compression ratio range | 0.2575-0.8143 |
| Generated facts | 165 |
| Entailed fact rate | 0.9758 |
| QA fidelity rate | 0.9200 |
| Passages with missing major claims | 1 |

Suggested manuscript sentence:

> On 25 Federal Reserve press-conference dialogue excerpts, S2 reduced token count to 0.49x of the original passage text using `tiktoken:cl100k_base`, with 97.6% of generated facts judged source-entailed and 92.0% passage-level QA-fidelity pass rate.
