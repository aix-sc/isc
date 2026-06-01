import type { Locale } from '@/i18n'

export interface FaqItem { q: string; a: string }

// Source: ISC strategy doc (v12) §11 “FAQ（やさしい言葉で）”. Japanese is verbatim
// from the doc; English is a faithful translation.
const FAQ_JA: FaqItem[] = [
  {
    q: '一文でいうと、この論文は何の話？',
    a: '誰かが質問するたびに資料の意味を毎回考え直すのではなく、資料が入ってきた時に一度だけその作業をして、きれいに保存しておき、あとは引くだけにしよう、という話。',
  },
  {
    q: 'QSR（クエリ時意味再構成）って何？',
    a: '今のふつうのやり方。質問のたびに大きなAIが生の資料を読み直し、意味をゼロから組み立てる。質問1つのたびに全部の本を読み直す司書のようなもの。',
  },
  {
    q: 'ISC（取込時意味コンパイル）って何？',
    a: 'その代わりのやり方。資料が来た時に意味の作業を一度だけ行い、整理した形で保存し、後の質問は準備済みの構造を見るだけにする。一度読んで良い索引を作る司書のようなもの。',
  },
  {
    q: 'コンパイラ vs インタプリタのたとえは？',
    a: 'インタプリタは料理のたびにレシピを訳し直す。コンパイラは一度訳して結果を使い回す。QSRがインタプリタ、ISCがコンパイラ。',
  },
  {
    q: '「今はQSRが標準」って、ChatGPT・Claude・Geminiで本当？',
    a: '本当。GeminiのFile Search、OpenAIのfile_search、Claudeのファイルアップロード／ウェブ検索は、いずれも質問時に文章を取ってきてモデルに答えを組み立て直させる＝QSR。',
  },
  {
    q: 'R*（損益分岐）って何？',
    a: '準備作業（ISC）の方が、毎回やり直す（QSR）より安くなる『質問回数の分かれ目』。R*より少なければQSRが安く、多ければISCが勝つ。式は『準備総コスト÷1問あたりの節約』。',
  },
  {
    q: 'なぜもう『ポジション論文』ではないの？',
    a: '本物の実験ができたから。実験A（コストモデル）とC（増分保守）は実測済みで、データ付きの公開・実行可能なサイトもある。実測結果のある論文は『着想だけ』ではなく実証論文になる。',
  },
  {
    q: 'なぜ1つでなく複数の学会に出すの？',
    a: '成果を速く出し、適した読者に届けるため。3つの別々の論文を作る：手法の論文（IES）、コスト枠組み＋ツールの論文（ICAST）、全体統合の論文（CIDR）。どれも別個に完結した貢献で、同じ論文を二度出すのではない。',
  },
  {
    q: '結果を複数論文に分けるのは『サラミ・スライス』では？',
    a: '1つの結果を薄く割れば、それに当たる。私たちはそうしない。各論文は別個の貢献と切り口を持ち、互いに引用し、重複は開示する。これは普通で許される。減点されるのは単一結果の薄切り。',
  },
  {
    q: 'IES と ICAST とは？なぜ今この2つ？',
    a: 'どちらもインドネシアの IEEE 索引の応用系会議で、Musashino University の参加が厚い。ICAST では高橋先生が基調講演者。締切が近く（IES 6/8、ICAST 7/8）、手法とツールを最速で出して人脈を作る道。',
  },
  {
    q: 'ICAST の『ダブルブラインド』は何を意味する？',
    a: '査読者が著者を分からないようにする方式。投稿PDFに著者名を書かず、サイトやコードへのリンクも匿名化するか『採択時に公開』とする。名前を戻すのは最終採択版だけ。',
  },
  {
    q: '締切とスケジュールは今どうなっている？',
    a: '近接：IES 2026 は6/8、ICAST 2026 は7/8。フラッグシップ：CIDR 2027 は8/4（採否10/6、最終12/4、会議2027年1/24〜27）。実証 preprint は今すぐ arXiv へ。',
  },
  {
    q: '転置インデックス／マテリアライズドビューの前例とは？',
    a: '転置インデックスは本の巻末索引のようなもので、一度作れば語を速く探せる。マテリアライズドビューは『質問への答え』を保存し最新に保つ仕組み。どちらも一度払って読みを安くする。ISCは同じことを意味に対して行う。',
  },
  {
    q: 'grep／『第三の極』とは？',
    a: 'grepはCtrl+Fのような完全一致の語検索。クエリ時だが意味の作業はゼロ。だから方式は三つ：grep（語・クエリ時）、QSR（意味・クエリ時）、ISC（意味・事前準備）。',
  },
  {
    q: '二つの『基層形式』（幾何的 vs 記号的）とは？',
    a: '幾何的＝座標のある地図で、近い点は似た意味。記号的＝正確に指させる『事実のラベル付き棚』。ISCはどちらでも動く。',
  },
  {
    q: '『rip-and-replace』とは？再埋め込みはなぜ高い？',
    a: 'AIは文章を数列（埋め込み）に変える。AIモデルが更新されると古い数列が新しいものと噛み合わず、通常は全資料をやり直す必要がある＝高い。この全部捨ててやり直すのが『rip-and-replace』。',
  },
  {
    q: '増分SVD／Brand更新とは？',
    a: '全部を計算し直す代わりに、新しい資料だけを使って準備済みの『意味の軸』を更新する方法。パイロットでは1更新あたり約34倍安く、しかも全再計算と完全に一致した。',
  },
  {
    q: '『軸の仮想更新』／Procrustesのコツとは？',
    a: 'AIモデルが変わったとき、少数の例から旧と新の『なまりの差』を学び、残りはやり直さず変換する。パイロットでは約10%だけやり直して95%の一致を回復した。',
  },
  {
    q: '『陳腐化（staleness）』とは？なぜ許容できる？',
    a: '準備したメモは最新資料から少し遅れることがある。だが『どれだけ遅れたか』が分かり、定期的に更新できる — 上限があり確認可能な問題。対してQSRの誤りは毎回の答えで起こりうる。',
  },
  {
    q: '『非経済的』便益（来歴・遵守・保守性）とは？',
    a: 'コスト以外の利点。来歴＝事実の出どころを正確に示せる。遵守＝長い対話でもルールを守り続ける。保守性＝誤りを一度直せば直ったまま保てる。',
  },
  {
    q: '『ゴールドリフト』とは？Zahnらと競合する？',
    a: 'ゴールドリフト＝長いAI対話が与えられたルールを少しずつ忘れること。Zahnらはこれを測定し『Knowledge Objects』を提案した。私たちは競合でなく相補的：彼らのKnowledge ObjectsはISCの準備済み意味を保存する一つの形（記号的形式）。',
  },
  {
    q: 'なぜフラッグシップは CIDR？arXiv は今使える？',
    a: 'CIDR は大胆で着想先行のデータsystems論文を歓迎しており、実データで裏打ちした統合論文の最適な場。そして実証研究になった今、preprint を arXiv（cs.DB/cs.IR）へすぐ出せる — 以前の『ポジション論文は採択が先』の制限はもう当てはまらない。',
  },
  {
    q: '最速で arXiv に載せるには？',
    a: 'もう使える：実験A・Cが実測済みなので、統合した実証レポートは研究論文として今すぐ arXiv（cs.DB/cs.IR）に出せる（採択前提なし）。先取権確保のため掲載し、IES/ICAST/CIDR 各論文がそれを引用・拡張する。',
  },
  {
    q: '実験結果ページ／プロジェクトサイトを外部資料として引用できる？',
    a: 'はい — インタラクティブなWebアプリとそのOSSリポジトリ（データ・図・コード・再現手順）は引用可能な技術資料。コツ：GitHubのReleaseを切ってZenodoのDOIを取り固定版を引用。ダブルブラインドのICASTでは匿名化版をリンクする。',
  },
  {
    q: '著者は誰で、なぜこの順番？',
    a: 'Kyle Wild と高橋雄介。取込時コンパイルの枠組みの起案者がWildなのでフラッグシップは筆頭がWild。高橋は責任著者で、モデル・コスト解析・実験・執筆を担当。応用系の IES/ICAST 論文は高橋／Musashino 主導で Wild を共著 — 投稿前に Kyle と合意する。',
  },
]

const FAQ_EN: FaqItem[] = [
  {
    q: 'In one sentence, what is this paper about?',
    a: "Instead of re-deriving what documents mean every time someone asks a question, do that work once when a document arrives, store it cleanly, and afterward just look it up.",
  },
  {
    q: 'What is QSR (query-time semantic reconstruction)?',
    a: "Today's usual approach. For every question, a large AI re-reads the raw documents and rebuilds the meaning from scratch — like a librarian who re-reads every book for each question.",
  },
  {
    q: 'What is ISC (ingest-time semantic compilation)?',
    a: 'The alternative. Do the meaning-work once when a document arrives, store it in an organized form, and let later questions just consult the prepared structure — like a librarian who reads once and builds a good index.',
  },
  {
    q: 'What about the compiler vs. interpreter analogy?',
    a: 'An interpreter re-translates the recipe every time you cook. A compiler translates once and reuses the result. QSR is the interpreter; ISC is the compiler.',
  },
  {
    q: 'Is "QSR is the default today" really true for ChatGPT, Claude, and Gemini?',
    a: "Yes. Gemini's File Search, OpenAI's file_search, and Claude's file upload / web search all fetch text at question time and have the model rebuild the answer — that's QSR.",
  },
  {
    q: 'What is R* (the break-even point)?',
    a: 'The number of questions at which the preparation work (ISC) becomes cheaper than redoing it each time (QSR). Below R*, QSR is cheaper; above it, ISC wins. The formula is total preparation cost ÷ savings per question.',
  },
  {
    q: 'Why is this no longer a "position paper"?',
    a: 'Because we have real experiments. Experiment A (cost model) and C (incremental maintenance) are measured, with a public, runnable site backed by data. A paper with measured results is an empirical paper, not just an idea.',
  },
  {
    q: 'Why submit to several venues instead of one?',
    a: 'To get results out fast and reach the right readers. We write three separate papers: a method paper (IES), a cost-framework + tool paper (ICAST), and an integrated paper (CIDR). Each is a self-contained contribution, not the same paper submitted twice.',
  },
  {
    q: "Isn't splitting results across papers 'salami-slicing'?",
    a: "Slicing one result thinly would be. We don't. Each paper has a distinct contribution and angle, they cite each other, and overlap is disclosed. That is normal and allowed; what's penalized is thin-slicing a single result.",
  },
  {
    q: 'What are IES and ICAST, and why these two now?',
    a: 'Both are IEEE-indexed applied conferences in Indonesia with strong Musashino University participation; at ICAST, Prof. Takahashi is a keynote speaker. Their deadlines are near (IES 6/8, ICAST 7/8) — the fastest path to ship the method and tool and build connections.',
  },
  {
    q: "What does ICAST's 'double-blind' mean?",
    a: 'Reviewers are kept from knowing the authors. The submitted PDF carries no author names, and links to the site or code are anonymized or marked "revealed on acceptance." Names are restored only in the final accepted version.',
  },
  {
    q: 'What are the deadlines and schedule right now?',
    a: 'Near-term: IES 2026 on 6/8, ICAST 2026 on 7/8. Flagship: CIDR 2027 on 8/4 (decision 10/6, camera-ready 12/4, conference Jan 24–27, 2027). The empirical preprint goes to arXiv now.',
  },
  {
    q: 'What are the inverted-index / materialized-view precedents?',
    a: 'An inverted index is like a book\'s back-of-book index: build it once, find words fast. A materialized view stores "answers to a question" and keeps them current. Both pay once to make reads cheap. ISC does the same thing for meaning.',
  },
  {
    q: "What is grep / the 'third pole'?",
    a: 'grep is exact word search like Ctrl+F — query-time, but zero meaning-work. So there are three approaches: grep (words, query-time), QSR (meaning, query-time), and ISC (meaning, prepared in advance).',
  },
  {
    q: "What are the two 'substrate forms' (geometric vs. symbolic)?",
    a: 'Geometric = a map with coordinates, where nearby points mean similar things. Symbolic = a labeled "shelf of facts" you can point to exactly. ISC works with either.',
  },
  {
    q: "What is 'rip-and-replace'? Why is re-embedding expensive?",
    a: 'AI turns text into number sequences (embeddings). When the AI model updates, old sequences no longer match the new ones, and you normally have to redo every document — which is expensive. Throwing it all away and redoing it is "rip-and-replace."',
  },
  {
    q: 'What are incremental SVD / Brand updates?',
    a: 'Instead of recomputing everything, update the prepared "axes of meaning" using only the new documents. In the pilot this was about 34× cheaper per update — and matched the full recomputation exactly.',
  },
  {
    q: "What is the 'virtual axis update' / the Procrustes trick?",
    a: 'When the AI model changes, learn the "accent difference" between old and new from a few examples, then transform the rest instead of redoing them. In the pilot, redoing only ~10% recovered 95% of the agreement.',
  },
  {
    q: "What is 'staleness'? Why is it acceptable?",
    a: 'Prepared notes can lag slightly behind the latest documents. But you know how far behind, and can refresh periodically — a bounded, checkable problem. By contrast, QSR errors can happen on every single answer.',
  },
  {
    q: "What are the 'non-economic' benefits (provenance, compliance, maintainability)?",
    a: 'Benefits beyond cost. Provenance = you can show exactly where a fact came from. Compliance = rules are kept even across long conversations. Maintainability = fix an error once and it stays fixed.',
  },
  {
    q: "What is 'gold drift'? Does it compete with Zahn et al.?",
    a: 'Gold drift = a long AI conversation gradually forgetting the rules it was given. Zahn et al. measured this and proposed "Knowledge Objects." We are complementary, not competing: their Knowledge Objects are one way (a symbolic form) to store ISC\'s prepared meaning.',
  },
  {
    q: 'Why is CIDR the flagship? Can we use arXiv now?',
    a: 'CIDR welcomes bold, idea-first data-systems papers — the ideal home for an integrated paper backed by real data. And now that this is empirical research, we can post a preprint to arXiv (cs.DB/cs.IR) immediately — the old "position papers need acceptance first" limit no longer applies.',
  },
  {
    q: 'How do we get onto arXiv fastest?',
    a: "It's ready: with Experiments A and C measured, the integrated empirical report can go to arXiv (cs.DB/cs.IR) as a research paper right now (no acceptance required). Post it to secure priority; the IES/ICAST/CIDR papers then cite and extend it.",
  },
  {
    q: 'Can the results page / project site be cited as an external resource?',
    a: 'Yes — the interactive web app and its OSS repository (data, figures, code, reproduction steps) are a citable technical resource. Tip: cut a GitHub Release and mint a Zenodo DOI to cite a fixed version. For the double-blind ICAST, link an anonymized version.',
  },
  {
    q: 'Who are the authors, and why this order?',
    a: 'Kyle Wild and Yusuke Takahashi. Wild originated the ingest-time compilation framing, so he is first author on the flagship. Takahashi is the corresponding author, handling the model, cost analysis, experiments, and writing. The applied IES/ICAST papers are Takahashi/Musashino-led with Wild as co-author — agreed with Kyle before submission.',
  },
]

const FAQ_BY_LOCALE: Record<Locale, FaqItem[]> = { en: FAQ_EN, ja: FAQ_JA }

export function getFaq(locale: Locale): FaqItem[] {
  return FAQ_BY_LOCALE[locale] ?? FAQ_EN
}
