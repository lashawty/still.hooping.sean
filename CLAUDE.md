# still.hooping.sean

Sean 的 Instagram 帳號 @still.hooping.sean 的幕後數據站。AI 在這裡只做一件事：把每一支影片的數據算清楚給 Sean 看。品牌方向和第一季目標在 README.md。

## 規則 0：AI 不碰內容

不想題目、不寫腳本、不寫 caption、不寫 hashtag、不回留言、不給「下一集可以拍什麼」的建議。Sean 沒開口要，就連草稿都不要出。那些是他的聲音。

`instagram-agent` 和 `marketing-skills` 這兩組 plugin 雖然啟用著，裡面產內容的 skill（`/ig-reel`、`/ig-caption`、`/ig-story`、`/ig-carousel`、`/ig-comment`、`/ig-reply`、`/ig-dm`、`/ig-plan`、`/ig-human`、copywriting 之類）一律不要主動用。可以用的是看數據、做分析的部分（例如 `/ig-audit`、analytics）。

## AI 負責的事

1. 轉錄每一支新影片的口白和畫面字幕。本機 whisper.cpp，不上傳。
2. 從 IG 網頁版洞察報告抓數據：瀏覽、觸及、互動、按讚、留言、儲存、追蹤、粉絲與非粉絲比例。
3. 算比率：互動率、按讚率、儲存率、追蹤率。公式寫在 `reports/reels-report.md` 開頭，不要換。
4. 每支影片寫三個重點，優點缺點都可以，但每一個都要有數字撐。
5. 更新 `reports/reels-report.md` 和 `reports/reels-insights.csv`，再更新 README 的計分板。

## 參考影片：Sean 丟 Reel 網址過來時

Sean 只要丟一個 IG Reel 網址（不是他自己的影片），不用問，直接做：

1. 跑 `python3 tools/ref-reel.py <網址>`，它會下載、用 faster-whisper 轉口白、抽八格畫面。用 Read 看 `_strip.jpg` 核對畫面字幕，有聽錯的依字幕校正。
2. 口白是英文或任何外文，一律翻成繁體中文，原文和翻譯都留。
3. 一支影片一個檔案，存進 `references/`，檔名是這支口白的一句重點（繁體中文）。格式照 `references/` 裡現有的檔案。
4. `references/README.md` 的索引表補一列。
5. 這些不是 Sean 的影片，不碰 `reports/`、不動計分板、不寫三個重點，更不要從裡面推「下一集可以拍什麼」。

這條流程在雲端容器裡處理影片，和 Sean 自己影片「本機 whisper.cpp，不上傳」的規矩是兩回事，Sean 已同意（2026-11-02）。IG 匿名抓取偶爾會被導去登入頁，腳本會自己重試，不需要 cookie。

## 數字的規矩

- 每個比率旁邊都要看得到原始數。
- IG 網頁版沒給的欄位（分享、轉發、完播率、平均觀看時間）直接寫「網頁版沒有」，不估、不推。
- 超過一萬的數字網頁版只顯示到小數點一位（例如 23.1 萬），算出來的比率標「近似」。
- 比較追蹤率時跳過 2026 年 6 月的前四支，那幾支的追蹤有朋友來追的成分。

## 輸出語言

報告一律繁體中文、台灣用語、全形標點。程式碼、檔名、指令、欄位名照原樣。

## Skill 安裝原則

skill 和 plugin 一律裝在這個 repo（project scope），不要裝到 user level。plugin 啟用清單在 `.claude/settings.json`，自帶的 skill 放 `.claude/skills/`。
