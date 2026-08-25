// Measured results shown on the site. Source of truth: the accepted ICAST-ES 2026
// camera-ready and the public frozen artifacts (tag data-freeze-2026-07-16).
// Policy: only published / accepted numbers appear here. Planned experiments
// publish no numbers until the corresponding paper is public.

export interface BarDatum { label: string; value: number; accent?: boolean }
export interface MeasuredView {
  id: 'exact' | 'cost' | 'tokens' | 's2'
  log?: boolean
  unit: string
  bars: BarDatum[]
}

export const MEASURED_VIEWS: MeasuredView[] = [
  {
    id: 'exact',
    unit: '%',
    bars: [
      { label: 'ISC / DeepSeek V4 Flash', value: 100, accent: true },
      { label: 'QSR / DeepSeek V4 Flash', value: 3.3 },
      { label: 'QSR / GLM 5.2 (spot)', value: 73.3 },
      { label: 'QSR / Kimi K2.7 Code (spot)', value: 6.7 },
    ],
  },
  {
    id: 'cost',
    log: true,
    unit: 'USD / question',
    bars: [
      { label: 'ISC / Flash', value: 0.0001, accent: true },
      { label: 'QSR / Flash (adversarial)', value: 0.00131 },
      { label: 'QSR / Flash (128 rows)', value: 0.00142 },
      { label: 'QSR / Kimi K2.7 Code', value: 0.01086 },
      { label: 'QSR / GLM 5.2', value: 0.01389 },
      { label: 'QSR / DeepSeek V4 Pro', value: 0.01851 },
    ],
  },
  {
    id: 'tokens',
    unit: 'tokens / question',
    bars: [
      { label: 'ISC / Flash', value: 453, accent: true },
      { label: 'QSR / Flash (128 rows)', value: 9777 },
      { label: 'QSR / DeepSeek V4 Pro', value: 10018 },
    ],
  },
  {
    id: 's2',
    unit: '%',
    bars: [
      { label: 'Dialogue: entailed', value: 97.6, accent: true },
      { label: 'Dialogue: QA fidelity', value: 92.0, accent: true },
      { label: 'Prose: entailed', value: 100.0 },
      { label: 'Prose: QA fidelity', value: 96.7 },
    ],
  },
]

export const HEADLINE = [
  { value: '30/30 vs 1/30', key: 'exact' },
  { value: '12.89x', key: 'readCost' },
  { value: '21.6x', key: 'tokens' },
  { value: '2.9x', key: 'latency' },
] as const
