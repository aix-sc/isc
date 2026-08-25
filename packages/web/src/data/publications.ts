import type { Locale } from '@/i18n'

export interface PubLink { label: string; href: string }
export interface Publication {
  id: string
  badge: string
  award?: string
  title: string
  authors: string
  venueLine: string
  summary: string
  links: PubLink[]
}

const PUBS_EN: Publication[] = [
  {
    id: 'ies2026',
    badge: 'IEEE IES 2026 - presented Aug 2, Yogyakarta',
    award: 'Best Paper Award',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Yusuke Takahashi, Kyle Wild, Asako Uraki',
    venueLine: 'Int. Electronics Symposium (IES-KCIC 2026), IEEE',
    summary:
      'The maintenance study: a compiled semantic substrate can be kept current under corpus change at a cost that scales with the amount of change - measured at 33.7x cheaper than rebuilding - and derives the break-even read frequency R*.',
    links: [
      { label: 'arXiv:2608.16621', href: 'https://arxiv.org/abs/2608.16621' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
    ],
  },
  {
    id: 'position2026',
    badge: 'Position paper - arXiv, Aug 21',
    title: 'RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation',
    authors: 'Kyle Wild, Yusuke Takahashi, Asako Uraki',
    venueLine: 'arXiv preprint (cs.AI, cs.DB, cs.IR), 6 pages',
    summary:
      'The argument in one place: query-time semantic reconstruction re-pays the same interpretive labor on every read; compiling meaning once at ingest into a typed, provenance-carrying substrate changes the cost law of retrieval systems.',
    links: [
      { label: 'arXiv:2608.20845', href: 'https://arxiv.org/abs/2608.20845' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.20845' },
    ],
  },
  {
    id: 'icast2026',
    badge: 'IEEE ICAST-ES 2026 - accepted; Oct 9-10, Surabaya',
    title: 'Ingest-Time Fact Compilation for Cost-Efficient and Reliable Question Answering over Revised Corpora',
    authors: 'Kyle Wild, Yusuke Takahashi, Asako Uraki',
    venueLine: 'Int. Conf. on Applied Science and Technology - Engineering Science, IEEE',
    summary:
      'The measured architecture study behind the results above: failure asymmetry (1/30 vs 30/30), the 12.89x read-cost gap, the 21.6x token gap, and the S2 rephrasing measurements. Camera-ready submitted; the arXiv version follows shortly.',
    links: [
      { label: 'Harness & frozen data', href: 'https://github.com/aix-sc/isc' },
    ],
  },
]

const PUBS_JA: Publication[] = [
  {
    id: 'ies2026',
    badge: 'IEEE IES 2026 - 8/2 発表（ジョグジャカルタ）',
    award: 'Best Paper Award',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Yusuke Takahashi, Kyle Wild, Asako Uraki',
    venueLine: 'Int. Electronics Symposium (IES-KCIC 2026), IEEE',
    summary:
      '保守の研究：コンパイル済み意味基層は、コーパスの変化のもとで「変化量」に比例するコストで最新に保てる（再構築比33.7倍安価を実測）。損益分岐の読み取り頻度 R* を導出。',
    links: [
      { label: 'arXiv:2608.16621', href: 'https://arxiv.org/abs/2608.16621' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
    ],
  },
  {
    id: 'position2026',
    badge: 'ポジション論文 - arXiv 8/21公開',
    title: 'RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation',
    authors: 'Kyle Wild, Yusuke Takahashi, Asako Uraki',
    venueLine: 'arXiv preprint（cs.AI, cs.DB, cs.IR）・6頁',
    summary:
      '主張を一枚に：クエリ時の意味再構成は同じ解釈労働を読みのたびに払い直す。取込時に一度だけ意味をコンパイルし、型付き・来歴付きの基層に保存すれば、検索システムのコスト法則そのものが変わる。',
    links: [
      { label: 'arXiv:2608.20845', href: 'https://arxiv.org/abs/2608.20845' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.20845' },
    ],
  },
  {
    id: 'icast2026',
    badge: 'IEEE ICAST-ES 2026 - 採択；10/9-10 スラバヤ発表',
    title: 'Ingest-Time Fact Compilation for Cost-Efficient and Reliable Question Answering over Revised Corpora',
    authors: 'Kyle Wild, Yusuke Takahashi, Asako Uraki',
    venueLine: 'Int. Conf. on Applied Science and Technology - Engineering Science, IEEE',
    summary:
      '上の実測値の出どころとなるアーキテクチャ実証：失敗の非対称性（1/30対30/30）、読み取りコスト12.89倍差、トークン21.6倍差、S2言い換え実測。カメラレディ提出済み・arXiv版は近日公開。',
    links: [
      { label: 'ハーネスと凍結データ', href: 'https://github.com/aix-sc/isc' },
    ],
  },
]

export function getPublications(locale: Locale): Publication[] {
  return locale === 'ja' ? PUBS_JA : PUBS_EN
}

export const DATA_LINKS = [
  { id: 'repo', href: 'https://github.com/aix-sc/isc' },
  { id: 'freeze', href: 'https://github.com/aix-sc/isc/tree/data-freeze-2026-07-16' },
  { id: 'evidence', href: 'https://github.com/aix-sc/isc/blob/main/experiments/CAMERA_READY_EVIDENCE_2026-08-20.md' },
] as const
