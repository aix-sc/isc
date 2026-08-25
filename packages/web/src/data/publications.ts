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
  aixHref: string
  links: PubLink[]
}

const PUBS_EN: Publication[] = [
  {
    id: 'icast2026',
    badge: 'IEEE ICAST-ES 2026 - accepted; Oct 9-10, Surabaya',
    title: 'Ingest-Time Fact Compilation for Cost-Efficient and Reliable Question Answering over Revised Corpora',
    authors: 'K. Wild, Y. Takahashi and A. Uraki',
    venueLine: 'Proc. 2026 Int. Conf. on Applied Science and Technology (ICAST 2026), Surabaya, Indonesia',
    summary:
      'The measured architecture study: failure asymmetry (1/30 vs 30/30 across five seeds), the 12.89x read-cost gap, the 21.6x token gap, and the S2 rephrasing measurements on Federal Reserve dialogue and Wikipedia prose.',
    aixHref: 'https://aix.sc/publications/icast2026-ingest-time-fact-compilation',
    links: [
      { label: 'Harness & frozen data', href: 'https://github.com/aix-sc/isc' },
    ],
  },
  {
    id: 'position2026',
    badge: 'Position paper - arXiv, Aug 21, 2026',
    title: 'RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation',
    authors: 'K. Wild, Y. Takahashi and A. Uraki',
    venueLine: 'arXiv preprint arXiv:2608.20845 [cs.AI], 2026',
    summary:
      'The argument in one place: query-time semantic reconstruction re-pays the same interpretive labor on every read; compiling meaning once at ingest into a typed, provenance-carrying substrate changes the cost law of retrieval systems.',
    aixHref: 'https://aix.sc/publications/arxiv2608-rag-deserves-an-index',
    links: [
      { label: 'arXiv:2608.20845', href: 'https://arxiv.org/abs/2608.20845' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.20845' },
    ],
  },
  {
    id: 'substrate-arxiv',
    badge: 'arXiv - Aug 18, 2026',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Y. Takahashi, K. Wild and A. Uraki',
    venueLine: 'arXiv preprint arXiv:2608.16621 [cs.AI], 2026',
    summary:
      'The maintenance study, open-access version: an incrementally maintained substrate is 33.7x cheaper to update than rebuilding, with cost governed by the amount of change rather than corpus size; derives the break-even read frequency R*.',
    aixHref: 'https://aix.sc/publications/arxiv2608-semantic-substrate',
    links: [
      { label: 'arXiv:2608.16621', href: 'https://arxiv.org/abs/2608.16621' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
    ],
  },
  {
    id: 'ies2026',
    badge: 'IEEE IES 2026 - presented Aug 2, Yogyakarta',
    award: 'Best Paper Award',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Y. Takahashi, K. Wild and A. Uraki',
    venueLine: 'Proc. Int. Electronics Symposium 2026 (IES 2026), Yogyakarta, Indonesia',
    summary:
      'The peer-reviewed conference version of the maintenance study, presented at IES 2026 and awarded Best Paper.',
    aixHref: 'https://aix.sc/publications/ies2026-semantic-substrate',
    links: [
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
    ],
  },
]

const PUBS_JA: Publication[] = [
  {
    id: 'icast2026',
    badge: 'IEEE ICAST-ES 2026 - 採択；10/9-10 スラバヤ発表',
    title: 'Ingest-Time Fact Compilation for Cost-Efficient and Reliable Question Answering over Revised Corpora',
    authors: 'K. Wild, Y. Takahashi and A. Uraki',
    venueLine: 'Proc. 2026 Int. Conf. on Applied Science and Technology (ICAST 2026), Surabaya, Indonesia',
    summary:
      '実測アーキテクチャ実証：失敗の非対称性（5シードで1/30対30/30）、読み取りコスト12.89倍差、トークン21.6倍差、連邦準備制度対話とWikipedia散文でのS2言い換え実測。',
    aixHref: 'https://aix.sc/publications/icast2026-ingest-time-fact-compilation',
    links: [
      { label: 'ハーネスと凍結データ', href: 'https://github.com/aix-sc/isc' },
    ],
  },
  {
    id: 'position2026',
    badge: 'ポジション論文 - arXiv 2026/8/21公開',
    title: 'RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation',
    authors: 'K. Wild, Y. Takahashi and A. Uraki',
    venueLine: 'arXiv preprint arXiv:2608.20845 [cs.AI], 2026',
    summary:
      '主張を一枚に：クエリ時の意味再構成は同じ解釈労働を読みのたびに払い直す。取込時に一度だけ意味をコンパイルし、型付き・来歴付きの基層に保存すれば、検索システムのコスト法則そのものが変わる。',
    aixHref: 'https://aix.sc/publications/arxiv2608-rag-deserves-an-index',
    links: [
      { label: 'arXiv:2608.20845', href: 'https://arxiv.org/abs/2608.20845' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.20845' },
    ],
  },
  {
    id: 'substrate-arxiv',
    badge: 'arXiv - 2026/8/18公開',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Y. Takahashi, K. Wild and A. Uraki',
    venueLine: 'arXiv preprint arXiv:2608.16621 [cs.AI], 2026',
    summary:
      '保守研究のオープンアクセス版：増分保守される基層は再構築より33.7倍安価に更新でき、コストはコーパス規模ではなく変化量に比例。損益分岐の読み取り頻度 R* を導出。',
    aixHref: 'https://aix.sc/publications/arxiv2608-semantic-substrate',
    links: [
      { label: 'arXiv:2608.16621', href: 'https://arxiv.org/abs/2608.16621' },
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
    ],
  },
  {
    id: 'ies2026',
    badge: 'IEEE IES 2026 - 8/2 発表（ジョグジャカルタ）',
    award: 'Best Paper Award',
    title: 'Cost Scales with Change, Not Corpus Size: Incrementally Maintaining an Evolving Semantic Substrate',
    authors: 'Y. Takahashi, K. Wild and A. Uraki',
    venueLine: 'Proc. Int. Electronics Symposium 2026 (IES 2026), Yogyakarta, Indonesia',
    summary:
      '保守研究の査読付き会議版。IES 2026で発表し、Best Paper Awardを受賞。',
    aixHref: 'https://aix.sc/publications/ies2026-semantic-substrate',
    links: [
      { label: 'DOI', href: 'https://doi.org/10.48550/arXiv.2608.16621' },
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
