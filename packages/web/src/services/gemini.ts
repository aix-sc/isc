import { httpsCallable } from 'firebase/functions'
import { functions, firebaseEnabled } from './firebase'
import type { ExperimentMeta, ExpCSummary } from '@/types/experiment'
import type { Locale } from '@/i18n'

export interface ChatTurn { role: 'user' | 'model'; text: string }

const LANGUAGE_INSTRUCTION: Record<Locale, string> = {
  en: 'Answer in English, in 2–5 sentences, plainly.',
  ja: 'Answer in Japanese (日本語), in 2–5 sentences, plainly. 専門用語は適切な日本語で。',
}

export function buildContext(
  experiments: ExperimentMeta[],
  summary: ExpCSummary | null,
  locale: Locale = 'en',
): string {
  let s =
    'You are a concise research assistant for the ISC (Ingest-time Semantic Compilation) experiments. ' +
    'ISC = compile semantic labour once at ingest into a persistent typed substrate; QSR = query-time ' +
    'semantic reconstruction (re-derive meaning every query, e.g. RAG). ' +
    'Break-even reads R* = (N·c_c + W·c_m)/(c_q − c_r). ' +
    LANGUAGE_INSTRUCTION[locale] + '\n\n'
  for (const e of experiments)
    s += `## ${e.name}\nPurpose: ${e.purpose}\nData: ${e.data}\nEvaluation: ${e.evaluation}\nStatus: ${e.status}\n\n`
  if (summary) s += '## Experiment C measured results (synthetic pilot)\n' + JSON.stringify(summary) + '\n'
  return s
}

// Calls the `geminiChat` Cloud Function, which holds the API key server-side and logs the
// question to Firestore. Never ships an API key to the client.
export async function askGemini(
  context: string,
  history: ChatTurn[],
  question: string,
): Promise<string> {
  if (!firebaseEnabled || !functions)
    throw new Error('Chat needs Firebase configured (set .env and deploy the geminiChat function, or run emulators).')
  const callable = httpsCallable<
    { context: string; history: ChatTurn[]; question: string },
    { text: string }
  >(functions, 'geminiChat')
  const res = await callable({ context, history, question })
  return res.data.text
}

// --- Dynamic follow-up suggestions ----------------------------------------
// Reuses the deployed `geminiChat` function (frontend-only; no Functions change).
// Asks the model, given the conversation so far, for ~6 short follow-up questions.
const SUGGEST_INSTRUCTION: Record<Locale, string> = {
  en: 'Based on the conversation so far, propose 6 short follow-up questions the user is likely to ask next about these ISC experiments. Each under ~12 words, specific and varied. Output ONLY a JSON array of exactly 6 strings — no preamble, numbering, or markdown.',
  ja: 'これまでの会話を踏まえ、ユーザーが次に尋ねそうな短い質問を6個、日本語で提案してください。各質問は約12語以内で、具体的かつ多様に。出力は6要素のJSON配列の文字列のみ（前置き・番号・記号・マークダウンは不要）。',
}

function parseSuggestions(raw: string): string[] {
  const cleaned = raw.replace(/```json/gi, '').replace(/```/g, '').trim()
  let arr: string[] = []
  try {
    const j = JSON.parse(cleaned)
    if (Array.isArray(j)) arr = j.map((x) => String(x))
  } catch {
    arr = cleaned
      .split('\n')
      .map((l) => l.replace(/^[\s\-*•\d.,、・)）]+/, '').trim())
      .filter(Boolean)
  }
  return arr.map((s) => s.trim()).filter(Boolean).slice(0, 6)
}

export async function suggestQuestions(
  context: string,
  history: ChatTurn[],
  locale: Locale = 'en',
): Promise<string[]> {
  if (!firebaseEnabled || !functions) return []
  const raw = await askGemini(context, history, SUGGEST_INSTRUCTION[locale])
  return parseSuggestions(raw)
}
