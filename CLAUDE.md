# still.hooping.sean

Sean 的 Instagram 帳號內容產線。用 `instagram-agent` 和 `marketing-skills` 兩組 plugin 產內容，發布前一律走 `speak-human-tw`。

## 規則 0：所有可發布內容，輸出前必走 `speak-human-tw`

這兩組 plugin 都是英文的，產出的東西會有英文思路和 AI 味。所以：

- 任何「可以直接貼去發布」的文字（Reel 腳本、口白、字幕、caption、hashtag、Story 文案、留言、回覆、DM、輪播文字），在給 Sean 看之前，都要先用 `speak-human-tw`（在本 repo `.claude/skills/speak-human-tw/`）過一遍。
- 順序固定：先跑 `/ig-*` 或 `/marketing-skills:*` 產草稿 → 跑 `speak-human-tw` 去 AI 味、校正台灣用語與全形標點 → 再給 Sean。
- `instagram-agent` 自己的 `/ig-human` 是英文的 humanizer，對中文沒用。中文內容一律用 `speak-human-tw` 取代，不要跑 `/ig-human`。
- 最終輸出語言是繁體中文、台灣用語。除非 Sean 明確說要英文。

不受此規則影響：分析報告、數據解讀、skill 內部的評分表（例如 hook 分數、profile 分數），這些是給 Sean 看的過程資料，不是發布內容。

## 口吻檔

`instagram-agent` 的每個 skill 都會讀 `~/.claude/instagram/voice.md`。Sean 正在另一個對話轉錄自己發過的影片，voice.md 會從那些逐字稿生出來。voice.md 還沒出現之前，寫出來的稿子只能算半成品，要跟 Sean 說。

## Skill 安裝原則

skill 和 plugin 一律裝在這個 repo（project scope），不要裝到 user level。plugin 啟用清單在 `.claude/settings.json`，自帶的 skill 放 `.claude/skills/`。
