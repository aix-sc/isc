import type { Locale } from '@/i18n'

export interface FaqItem { q: string; a: string }

// Plain-language FAQ for the ISC (Ingest-time Semantic Compilation) work.
// Answers expanded for fuller, more careful explanations. Strings use template
// literals so quotes/apostrophes need no escaping.
const FAQ_JA: FaqItem[] = [
  {
    q: `一文でいうと、この研究は何の話？`,
    a: `多くのAIは、誰かが質問するたびに資料の意味を一から考え直し、同じ解釈コストを毎回払っています。本研究はその逆で、資料が入ってきた時に意味の作業を一度だけ行い、結果をきれいに整理した検索可能な構造として保存し、以後は引くだけにします。核心の主張は、いったん多くの読み（問い合わせ）が発生すれば、その構造を最新に保つコストは資料の『量』ではなく『変化量』に比例して増える、というもの。だから同じ資料への質問は、回数を重ねるほど安く・速く・一貫したものになります。`,
  },
  {
    q: `ChatGPT、Claude、Gemini等のLLMに関して、この研究はどの様に貢献するの？ユーザーである自分にとっては、何が良くなるの？`,
    a: `今これらのアシスタントの多くは QSR を使います：質問のたびに元資料を読み直し、意味を一から組み立て直す — つまり毎回、重いLLMの『理解』をやり直します。本研究はその理解を最初に一度だけ行い、型付きで検索可能な基層（substrate）として保存する（ISC）話です。あなたにとっての具体的な利点：(1) 速度とコスト — 同じ資料に何度も質問するほど、各回答が準備済み構造を使い回すので、速く・安くなります。(2)『それっぽいが間違い』が減る — 意味を毎回その場で当て推量せず、一度準備して確認するため、検索由来の誤りが減ります。(3) 出どころ（来歴）— 事実が出典付きで保存されるので、回答の根拠資料を示せます。(4) 脱線しにくい — ルールや事実が安定した構造に置かれるため、長い対話でもぶれにくい。(5) 保守が楽 — 事実を一度直せば直ったまま。モデルが更新されても全部をやり直す必要はありません。ChatGPT・Claude・Gemini は ISC を QSR と併用する補完モードとして採り入れ、重く反復的な資料処理を、より安く・確実に・監査可能にできます。`,
  },
  {
    q: `QSR（クエリ時意味再構成）って何？`,
    a: `今のふつうのやり方です。質問のたびに、大きな言語モデルが生の資料（または取ってきた断片）を読み直し、意味を一から組み立ててから答えます。質問のたびに関連する本を全部読み直す司書のようなもの。柔軟で常に最新の文章を使える一方、毎回フルの解釈コストを払い直し、読み違いがあれば毎回起こり得ます。`,
  },
  {
    q: `ISC（取込時意味コンパイル）って何？`,
    a: `その代わりのやり方です。意味の作業は、資料が入ってきた時に一度だけ行います：解析し、解釈し、結果を整理された型付き構造（『意味の基層』）に書き込みます。以後の質問は生の文章を解釈し直さず、その準備済み構造を引くだけ。一度だけ本を読んで丁寧な索引を作る司書のようなもので、最初に多めに払う代わり、その後の一件ごとの読みは安く一貫します。`,
  },
  {
    q: `コンパイラ vs インタプリタのたとえは？`,
    a: `インタプリタは料理のたびにレシピを一から訳し直します。コンパイラは一度訳して、その結果を毎回使い回します。QSR がインタプリタ（質問のたびに意味を導出）、ISC がコンパイラ（取込時に一度コンパイルして使い回す）。このたとえはトレードオフも表します — コンパイルは最初に多く払い、元が変わると少し古くなり得ますが、以後の実行は格段に安く予測可能になります。`,
  },
  {
    q: `「今はQSRが標準」って、ChatGPT・Claude・Geminiで本当？`,
    a: `本当です。Gemini の File Search、OpenAI の file_search、Claude のファイルアップロードとウェブ検索は、いずれも質問時に関連文章を取ってきて、モデルにそこから答えを組み立て直させます。どれもクエリ時意味再構成（QSR）の仕組みです。これらのベクトル索引は『どの断片を読むか』という検索（retrieval）は前計算で安くしますが、1問ごとのLLMによる意味の再構成は安くしません — そして、まさにその再構成こそ ISC が保存するものです。`,
  },
  {
    q: `R*（損益分岐）って何？`,
    a: `R* は、基層を一度準備する（ISC）方が、毎回意味を導出する（QSR）より総コストで安くなる『読み（質問）回数の分かれ目』です。R* より少ない（たまにしか引かない）なら QSR が安く、超えれば ISC が勝ちます。式は R* =（N·c_c + W·c_m）/（c_q − c_r）：分子は準備の総コスト（N件をコスト c_c でコンパイル＋変更 W 件をコスト c_m で保守）、分母は1問あたりの節約（QSR の問い合わせコスト c_q − ISC の安い読みコスト c_r）。要点は、保守の項が資料の『量』ではなく『変化量』W に比例して増えること。だから安定して何度も引かれる資料ほど、R* に早く到達します。`,
  },
  {
    q: `転置インデックス／マテリアライズドビューの前例とは？`,
    a: `いずれもデータベースの古典的な考え方で、ISC はそれを一般化します。転置インデックスは本の巻末索引のようなもの：一度作れば、全文を走査せずどの語も即座に見つかります。マテリアライズドビューは、繰り返し使う問い合わせの答えを前計算して保存し、最新に保ちます。どちらも『最初に一度払って、以後の読みを安くする』原理です。ISC は同じ原理を、語や表の行ではなく『意味（意味構造）』に適用します。`,
  },
  {
    q: `grep／『第三の極』とは？`,
    a: `grep は完全一致の語検索 — 多数のファイルにまたがる Ctrl+F のようなものです。クエリ時に動きますが意味の作業はゼロで、文字列を見つけるだけで意味は見ません。ここから、二つの軸（語 vs 意味、クエリ時 vs 事前準備）で三つの方式が見えます：grep（語・クエリ時）、QSR（意味・クエリ時）、ISC（意味・事前準備）。ISC は、いまの議論で抜け落ちがちな『第三の極』 — 意味を扱うが、その場で再構成せず前もってコンパイルしておく方式です。`,
  },
  {
    q: `二つの『基層形式』（幾何的 vs 記号的）とは？`,
    a: `ISC の準備済み意味は、相補的な二つの形で保存できます。幾何的形式は座標空間（ベクトル）で、近い点ほど似た意味を表し、距離で検索します — あいまいな類似検索に強い。記号的形式はラベル付きの『事実の棚』で、名前の付いた離散的な対象を正確に指させます — 厳密な参照・来歴・ルールに強い。ISC はあえて基層に依存しない設計で、類似性が要るか厳密さが要るかに応じて、どちらの形でも、あるいは両方でも動きます。`,
  },
  {
    q: `『rip-and-replace』とは？再埋め込みはなぜ高い？`,
    a: `AI は文章を、意味を幾何として符号化した長い数列『埋め込み（embedding）』に変換します。この数列は、それを生成したモデルのバージョンに固有です。モデルが更新されると古い数列は新しいものと噛み合わなくなるため、通常はコーパス全体を一から再埋め込みします — これが『rip-and-replace（総入れ替え）』です。大規模コーパスでは遅く高コストで、モデル更新をためらう大きな理由になります。本研究の主要な狙いの一つは、この総やり直しを避けることです。`,
  },
  {
    q: `増分SVD／Brand更新とは？`,
    a: `ここでの意味の基層は、語×文脈行列の打ち切り SVD（特異値分解）から作る正規直交空間です。資料の追加・退役・変更のたびに分解全体を計算し直すのではなく、Brand 流の増分 SVD が、新規・変更分のデータだけを使って既存の『意味の軸』を更新します。これで1更新あたりのコストが激減し — 合成パイロットでは約34倍安く — しかも結果は一から全再計算したものとほぼ完全に一致しました（ずれは 10⁻¹¹ 程度、検索品質も不変）。`,
  },
  {
    q: `『軸の仮想更新』／Procrustesのコツとは？`,
    a: `これは問11のモデル更新問題への対処です。モデルが変わったとき全部を再埋め込みする代わりに、旧・新モデル両方で埋め込んだ少数のサンプルから、二つの空間の系統的な『なまりの差』（Procrustes 流の整列＝最適な回転）を学び、残りは再埋め込みせず変換します。パイロットでは、約10%だけやり直すことで、全再埋め込みとの一致のおよそ95%を回復しました — 全か無かの『総入れ替え』を、ほとんど使い回せる安価な更新に変えます。`,
  },
  {
    q: `『陳腐化（staleness）』とは？なぜ許容できる？`,
    a: `基層は連続的に作り直すのではなく更新していくため、最新資料からわずかに遅れることがあります — この遅れが『陳腐化（staleness）』です。重要なのは、これが『有界で測定可能』な問題だということ：どれだけ遅れているかを定量化でき、必要に応じた頻度で更新できます。対して QSR では、読み違いや幻覚が個々の回答のどこででも、組み込みの上限なしに起こり得ます。既知で制御可能な遅れは、予測できない毎回の誤り率より扱いやすいのが普通です。`,
  },
  {
    q: `『非経済的』便益（来歴・遵守・保守性）とは？`,
    a: `コストや速度以外にも、意味を保存することで三つの質的な利点が得られます。来歴（provenance）：各事実が出典とともに保存されるので、回答の根拠を正確に示せます。遵守（compliance）：ルールや制約が安定した構造に置かれるため、非常に長い対話でも守られ、文脈から少しずつ消えていきません。保守性（maintainability）：基層の誤りを一度直せば、以後の全ての読みで直ったまま — 毎回同じ誤りを蒸し返しません。規制下や重要度の高い場面では、これらがコストと同じくらい重要になります。`,
  },
  {
    q: `『ゴールドリフト』とは？Zahnらと競合する？`,
    a: `『ゴールドリフト』とは、長いAI対話が、最初に与えられた指示や事実を少しずつ忘れたり歪めたりする傾向のことです。Zahn らはこれを測定し、対策として『Knowledge Objects』を提案しました。私たちの研究は競合ではなく相補的です：彼らの Knowledge Objects は、ISC が生み出す準備済み意味を保存する一つの具体的な形 — 記号的な基層 — にほかなりません。私たちの枠組みでは、ISC が一般原理（意味を一度コンパイルして保存する）であり、Knowledge Objects はそのコンパイル済み意味を離散的・記号的な形で保持する一つの有効な方法です。`,
  },
]

const FAQ_EN: FaqItem[] = [
  {
    q: `In one sentence, what is this paper about?`,
    a: `Most AI systems re-derive what your documents mean every single time someone asks a question, paying the same interpretation cost over and over. This research proposes the opposite: do that meaning-work once, at the moment a document is ingested, store the result in a clean, queryable structure, and from then on simply look it up. The core claim is that once you have many reads, the cost of keeping that prepared structure up to date scales with how much the data changes, not with how large the corpus is — so repeated questions get steadily cheaper, faster, and more consistent.`,
  },
  {
    q: `How does this research contribute to LLMs like ChatGPT, Claude, and Gemini? As a user, what gets better for me?`,
    a: `Today these assistants mostly use QSR: each time you ask, they re-read the source documents and reconstruct their meaning from scratch — including a fresh, expensive pass of LLM understanding on every query. This research is about doing that understanding once, up front, and persisting it as a typed, queryable substrate (ISC). Concretely, for you that can mean: (1) Speed and cost — when you ask many questions about the same material, each answer reuses the prepared structure instead of re-paying the interpretation cost, so answers get faster and cheaper the more you ask. (2) Fewer confident-but-wrong answers — meaning is prepared and checked once rather than re-guessed under time pressure on every query, removing one common source of retrieval-borne mistakes. (3) Provenance — because facts are stored with where they came from, the system can show you the exact source behind an answer. (4) Staying on task — long conversations drift less, because rules and facts live in a stable structure rather than only in the model's short-term context. (5) Easier maintenance — correct a fact once and it stays fixed, and when the underlying model is upgraded you don't necessarily have to reprocess everything. ChatGPT, Claude, and Gemini could adopt ISC as a complementary mode alongside QSR, making heavy, repeated document work cheaper, more reliable, and more auditable.`,
  },
  {
    q: `What is QSR (query-time semantic reconstruction)?`,
    a: `It is today's usual approach. For every question, a large language model re-reads the raw documents (or retrieved chunks of them) and rebuilds their meaning from scratch before answering — like a librarian who re-reads every relevant book for each new question. It is flexible and always uses the latest text, but you pay the full interpretation cost again on every single query, and any misreading can recur each time.`,
  },
  {
    q: `What is ISC (ingest-time semantic compilation)?`,
    a: `It is the alternative. The meaning-work happens once, when a document is ingested: the system parses it, interprets it, and writes the result into an organized, typed structure (the semantic substrate). Later questions just consult that prepared structure instead of re-interpreting the raw text — like a librarian who reads each book once and builds a careful index. You pay more up front, but every subsequent read is cheap and consistent.`,
  },
  {
    q: `What about the compiler vs. interpreter analogy?`,
    a: `An interpreter re-translates the recipe from scratch every time you cook; a compiler translates it once and reuses the compiled result on every run. QSR is the interpreter — it re-derives meaning per query. ISC is the compiler — it compiles meaning once at ingest and reuses it. The analogy also captures the trade-off: compilation costs more up front and can go slightly stale if the source changes, but it makes every later execution far cheaper and more predictable.`,
  },
  {
    q: `Is "QSR is the default today" really true for ChatGPT, Claude, and Gemini?`,
    a: `Yes. Gemini's File Search, OpenAI's file_search, and Claude's file upload and web search all work the same way: at question time they fetch the relevant text and have the model reconstruct the answer from it. Each is a query-time semantic reconstruction (QSR) pipeline. A vector index in these systems amortizes the retrieval step — finding which chunks to read — but it does not amortize the per-query LLM reconstruction of meaning, and that reconstruction is exactly what ISC persists.`,
  },
  {
    q: `What is R* (the break-even point)?`,
    a: `R* is the number of reads (questions) at which preparing the substrate once (ISC) becomes cheaper in total than re-deriving meaning every time (QSR). Below R*, when material is queried only rarely, QSR is cheaper; above R*, ISC wins. The formula is R* = (N·c_c + W·c_m) / (c_q − c_r): the numerator is the total preparation cost (compiling N items at cost c_c, plus maintaining W changes at cost c_m), and the denominator is how much you save per query (the QSR query cost c_q minus the cheaper ISC read cost c_r). The key point is that the maintenance term grows with the amount of change (W), not with corpus size — so stable, heavily-read corpora reach R* quickly.`,
  },
  {
    q: `What are the inverted-index / materialized-view precedents?`,
    a: `These are long-established database ideas that ISC generalizes. An inverted index is like a book's back-of-book index: pay once to build it, and afterward find any word instantly instead of scanning the whole text. A materialized view pre-computes and stores the answer to a recurring query and keeps it refreshed, so reads stay cheap. Both follow the same principle — pay once up front to make many later reads fast. ISC applies exactly this principle, but to meaning (semantic structure) rather than to words or table rows.`,
  },
  {
    q: `What is grep / the 'third pole'?`,
    a: `grep is exact, literal word matching — like Ctrl+F across many files. It runs at query time but does zero semantic work: it finds the string, not the meaning. That gives three distinct approaches, along two axes (words vs. meaning, and query-time vs. prepared-in-advance): grep (words, query-time), QSR (meaning, query-time), and ISC (meaning, prepared in advance). ISC is the third pole that has been largely missing from the current conversation — semantic, but compiled ahead of time rather than reconstructed on demand.`,
  },
  {
    q: `What are the two 'substrate forms' (geometric vs. symbolic)?`,
    a: `ISC's prepared meaning can be stored in two complementary forms. The geometric form is a coordinate space (vectors): nearby points mean similar things, and you search by distance — good for fuzzy, similarity-based recall. The symbolic form is a labeled shelf of facts — discrete, named objects you can point to exactly — good for precise reference, provenance, and rules. ISC is deliberately substrate-agnostic: it works with either form, or both together, depending on whether you need similarity or exactness.`,
  },
  {
    q: `What is 'rip-and-replace'? Why is re-embedding expensive?`,
    a: `AI systems turn text into long sequences of numbers called embeddings, which encode meaning as geometry. Those numbers are specific to the model version that produced them. When the model is upgraded, the old embeddings no longer line up with the new ones, so the usual fix is to re-embed every document in the entire corpus from scratch — rip-and-replace. For a large corpus that is slow and costly, and it is a big reason teams hesitate to upgrade models. A major aim of this work is to avoid that full redo.`,
  },
  {
    q: `What are incremental SVD / Brand updates?`,
    a: `The semantic substrate here is an orthonormal space built from a truncated SVD (singular value decomposition) of a term–context matrix. Instead of recomputing that whole decomposition whenever documents are added, retired, or changed, Brand-style incremental SVD updates the existing axes of meaning using only the new or changed data. This drops the per-update cost dramatically — about 34× cheaper per update in the synthetic pilot — while producing a result that matched the full from-scratch recomputation essentially exactly (drift on the order of 10⁻¹¹, with retrieval quality unchanged).`,
  },
  {
    q: `What is the 'virtual axis update' / the Procrustes trick?`,
    a: `This addresses the model-upgrade problem from the rip-and-replace question. Instead of re-embedding everything when the model changes, you take a small sample of items embedded by both the old and new models, learn the systematic accent difference between the two spaces (a Procrustes-style alignment — an optimal rotation), and then transform the remaining items rather than re-embedding them. In the pilot, redoing only about 10% of the work recovered roughly 95% of the agreement with a full re-embedding — turning an all-or-nothing rip-and-replace into a cheap, mostly-reused update.`,
  },
  {
    q: `What is 'staleness'? Why is it acceptable?`,
    a: `Because the prepared substrate is updated rather than rebuilt continuously, it can lag slightly behind the very latest documents — that lag is staleness. The important point is that it is a bounded and measurable problem: you can quantify exactly how far behind you are and refresh on a schedule that fits your needs. By contrast, QSR errors — a misreading or hallucination — can occur on any individual answer with no built-in bound. A known, controllable lag is usually easier to manage than an unpredictable per-answer error rate.`,
  },
  {
    q: `What are the 'non-economic' benefits (provenance, compliance, maintainability)?`,
    a: `Beyond raw cost and speed, persisting meaning brings three qualitative benefits. Provenance: because each fact is stored together with its source, the system can show exactly where an answer came from. Compliance: rules and constraints live in a stable structure, so they are respected even across very long conversations rather than slowly fading from the model's context. Maintainability: fix an error once in the substrate and it stays fixed for every future read — you don't re-introduce the same mistake on each query. In regulated or high-stakes settings, these often matter as much as cost.`,
  },
  {
    q: `What is 'gold drift'? Does it compete with Zahn et al.?`,
    a: `Gold drift is the tendency of a long AI conversation to gradually forget or distort the instructions and facts it was originally given. Zahn et al. measured this effect and proposed Knowledge Objects as a remedy. Our work is complementary rather than competing: their Knowledge Objects are essentially one concrete form — a symbolic substrate — for storing the kind of prepared meaning that ISC produces. In our framing, ISC is the general principle (compile and persist meaning once), and Knowledge Objects are one valid way to hold that compiled meaning in discrete, symbolic form.`,
  },
]

const FAQ_BY_LOCALE: Record<Locale, FaqItem[]> = { en: FAQ_EN, ja: FAQ_JA }

export function getFaq(locale: Locale): FaqItem[] {
  return FAQ_BY_LOCALE[locale] ?? FAQ_EN
}
