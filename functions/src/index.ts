import { onCall, HttpsError } from 'firebase-functions/v2/https'
import { defineSecret, defineString } from 'firebase-functions/params'
import { logger } from 'firebase-functions/v2'
import { initializeApp } from 'firebase-admin/app'
import { getFirestore, FieldValue } from 'firebase-admin/firestore'
import { google } from 'googleapis'

initializeApp()

const GEMINI_KEY = defineSecret('GEMINI_KEY')
const MODEL = 'gemini-2.5-flash'

// Spreadsheet that mirrors newsletter sign-ups. Share this sheet (Editor) with the
// function's runtime service account, then set SUBSCRIBERS_SHEET_ID in functions/.env.
const SUBSCRIBERS_SHEET_ID = defineString('SUBSCRIBERS_SHEET_ID', { default: '' })
const SUBSCRIBERS_SHEET_TAB = defineString('SUBSCRIBERS_SHEET_TAB', { default: 'Subscribers' })

interface ChatTurn { role: 'user' | 'model'; text: string }
interface ChatRequest { context?: string; history?: ChatTurn[]; question?: string }

interface GeminiPart { text?: string }
interface GeminiResponse {
  error?: { message?: string }
  candidates?: { content?: { parts?: GeminiPart[] }; finishReason?: string }[]
}

// Server-side Gemini proxy: keeps the API key in a Secret, never on the client.
// Grounds answers in the experiment context, and logs the question to Firestore.
export const geminiChat = onCall(
  { secrets: [GEMINI_KEY], cors: true, region: 'us-central1' },
  async (req): Promise<{ text: string }> => {
    const { context, history, question } = (req.data ?? {}) as ChatRequest
    if (!question || typeof question !== 'string')
      throw new HttpsError('invalid-argument', 'A "question" string is required.')

    const turns = Array.isArray(history) ? history : []
    const contents = [
      ...turns.map((h) => ({ role: h.role, parts: [{ text: h.text }] })),
      { role: 'user', parts: [{ text: question }] },
    ]
    const body = {
      systemInstruction: { parts: [{ text: String(context ?? '') }] },
      contents,
      generationConfig: {
        temperature: 0.4,
        maxOutputTokens: 1024,
        thinkingConfig: { thinkingBudget: 0 },
      },
    }

    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GEMINI_KEY.value()}`,
      { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) },
    )
    const data = (await res.json()) as GeminiResponse
    if (data.error) throw new HttpsError('internal', data.error.message ?? 'Gemini API error')

    const candidate = data.candidates?.[0]
    let text =
      candidate?.content?.parts?.map((p) => p.text ?? '').join('') || '(no response)'
    if (candidate?.finishReason === 'MAX_TOKENS') text += ' […]'

    await getFirestore()
      .collection('questions')
      .add({ question, answerChars: text.length, at: FieldValue.serverTimestamp() })

    return { text }
  },
)

// ---------------------------------------------------------------------------
// Newsletter subscription: validate → store in Firestore → mirror to a Google
// Sheet (best-effort). Firestore is the source of truth; a Sheet failure never
// fails the subscription. Client analytics (generate_lead) is fired separately.
// ---------------------------------------------------------------------------
interface SubscribeRequest { email?: string; locale?: string }
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export const subscribeNewsletter = onCall(
  { cors: true, region: 'us-central1' },
  async (req): Promise<{ ok: true }> => {
    const { email: rawEmail, locale: rawLocale } = (req.data ?? {}) as SubscribeRequest
    const email = String(rawEmail ?? '').trim().toLowerCase()
    const locale = rawLocale === 'ja' ? 'ja' : 'en'
    if (!EMAIL_RE.test(email) || email.length > 254)
      throw new HttpsError('invalid-argument', 'A valid email address is required.')

    const now = FieldValue.serverTimestamp()
    // doc id = email → idempotent (re-subscribing updates the record, no duplicates).
    const ref = getFirestore().collection('subscribers').doc(email)
    const existed = (await ref.get()).exists
    await ref.set(
      {
        email,
        locale,
        source: 'isc-site',
        userAgent: String(req.rawRequest?.headers['user-agent'] ?? '').slice(0, 300),
        updatedAt: now,
        ...(existed ? {} : { subscribedAt: now }),
      },
      { merge: true },
    )

    // Mirror to Google Sheet (best-effort).
    const sheetId = SUBSCRIBERS_SHEET_ID.value()
    if (sheetId && !existed) {
      try {
        const auth = new google.auth.GoogleAuth({
          scopes: ['https://www.googleapis.com/auth/spreadsheets'],
        })
        const sheets = google.sheets({ version: 'v4', auth })
        await sheets.spreadsheets.values.append({
          spreadsheetId: sheetId,
          range: `${SUBSCRIBERS_SHEET_TAB.value()}!A:D`,
          valueInputOption: 'RAW',
          insertDataOption: 'INSERT_ROWS',
          requestBody: { values: [[new Date().toISOString(), email, locale, 'isc-site']] },
        })
      } catch (e) {
        logger.warn('Newsletter Sheet append failed (saved to Firestore regardless).', e)
      }
    }

    return { ok: true }
  },
)
