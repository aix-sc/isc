import type { Locale } from '@/i18n'

// Planned work only - no result data appears here until the corresponding
// paper is public. Specifications and deadlines are governed by a
// pre-registration committed to the experiment repository before execution.

export interface RoadmapItem { id: string; name: string; note: string }

const ROADMAP_EN: RoadmapItem[] = [
  { id: 'i5', name: 'I5 - Human calibration of the LLM judge',
    note: 'Two independent external raters double-annotate entailment and QA-fidelity judgments; chance-corrected agreement is reported before any further accuracy claims.' },
  { id: 'i6', name: 'I6 - Held-out reproduction at 500 documents',
    note: 'Re-run the full protocol on a document-disjoint held-out set to test that the measured asymmetries survive scale and fresh data.' },
  { id: 's92', name: 'Judge-model separation (pre-reg 9.2)',
    note: 'Re-judge the core held-out cells with a non-Kimi judge model chosen and recorded before the run; both judgments are reported side by side.' },
  { id: 'p1', name: 'P1 - doc2query ingest-expansion baseline',
    note: 'How does fact compilation differ from ingest-time document expansion? doc2query expands pointers while the reader still receives raw text; ISC compiles the payload itself.' },
  { id: 'g', name: 'G1-G5 - Real corpora, migration, scale, cost accounting',
    note: 'Real revision streams, embedding-model migration, corpus scaling, human validation of S2, and full-ledger cost accounting including ingest and maintenance.' },
]

const ROADMAP_JA: RoadmapItem[] = [
  { id: 'i5', name: 'I5 - LLM判定の人手較正',
    note: '独立した外部評価者2名が含意・QA忠実性の判定を二重注釈し、偶然一致補正つきの一致率を報告してから精度主張を進める。' },
  { id: 'i6', name: 'I6 - 500文書のheld-out再現',
    note: '文書を重複させないheld-outセットで全プロトコルを再実行し、実測した非対称性が規模と新データに耐えるかを検証する。' },
  { id: 's92', name: '判定モデル分離（事前登録9.2）',
    note: '中核held-outセルを、実行前に選定・記録した非Kimi判定モデルで再判定し、両判定を並記する。' },
  { id: 'p1', name: 'P1 - doc2query（取込時文書拡張）ベースライン',
    note: 'ファクトコンパイルは取込時の文書拡張と何が違うか。doc2queryはポインタを拡張し読み手は生テキストを受け取る。ISCはペイロード自体をコンパイルする。' },
  { id: 'g', name: 'G1-G5 - 実データ・移行・規模化・コスト会計',
    note: '実改訂ストリーム、埋め込みモデル移行、コーパス規模化、S2の人手検証、取込・保守を含む全台帳コスト会計。' },
]

export function getRoadmap(locale: Locale): RoadmapItem[] {
  return locale === 'ja' ? ROADMAP_JA : ROADMAP_EN
}
