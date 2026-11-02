#!/usr/bin/env python3
"""抓一支公開 IG Reel、轉錄口白、抽畫面格。給 AI 做參考影片逐字稿用。

用法：python3 tools/ref-reel.py <reel 網址或 shortcode> [輸出目錄]

輸出（預設 /tmp/ref-reel/<shortcode>/）：
  <id>.mp4          影片
  <id>.info.json    yt-dlp 中繼資料（帳號、日期、按讚、留言、文案）
  <id>.meta.txt     上面的摘要
  <id>.srt.txt      口白逐句轉錄（faster-whisper medium，關閉語音偵測，低音量旁白才不會漏）
  <id>_strip.jpg    八格畫面拼圖，給 AI 看畫面字幕用

需要：yt-dlp、ffmpeg、faster-whisper（pip install yt-dlp faster-whisper）。
翻譯不在這支腳本裡，由 AI 讀完逐字稿後做。
"""
import json, re, subprocess, sys, time
from pathlib import Path

def sh(*cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    m = re.search(r"(?:reel|p|reels)/([A-Za-z0-9_-]+)", sys.argv[1])
    sid = m.group(1) if m else sys.argv[1]
    url = f"https://www.instagram.com/reel/{sid}/"
    out = Path(sys.argv[2] if len(sys.argv) > 2 else f"/tmp/ref-reel/{sid}")
    out.mkdir(parents=True, exist_ok=True)
    mp4 = out / f"{sid}.mp4"

    # 下載。IG 匿名流量有上限，被導去登入頁就等一下重試。
    for attempt in range(1, 6):
        if mp4.exists():
            break
        r = subprocess.run(["yt-dlp", "-q", "--no-warnings", "--write-info-json",
                            "-o", str(out / f"{sid}.%(ext)s"), url], capture_output=True, text=True)
        if mp4.exists():
            break
        print(f"下載第 {attempt} 次失敗：{r.stderr.strip()[:120]}", file=sys.stderr)
        time.sleep(attempt * 5)
    else:
        sys.exit("下載失敗，稍後再試。")

    info = json.load(open(out / f"{sid}.info.json"))
    dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)))
    meta = "\n".join([
        f"url: {url}",
        f"account: @{info.get('channel') or info.get('uploader_id')}",
        f"name: {info.get('uploader')}",
        f"date: {info.get('upload_date')}",
        f"duration_s: {dur:.1f}",
        f"likes: {info.get('like_count')}",
        f"comments: {info.get('comment_count')}",
        "caption:", (info.get("description") or "").strip(),
    ])
    (out / f"{sid}.meta.txt").write_text(meta + "\n")
    print(meta)

    # 轉錄。音訊走 ffmpeg 解成 16k 單聲道，避開 faster-whisper 與新版 av 的相容問題。
    import numpy as np
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.float32)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    segs, lang = model.transcribe(audio, beam_size=5, vad_filter=False)
    lines = [f"lang: {lang.language} ({lang.language_probability:.2f})"]
    for s in segs:
        lines.append(f"[{s.start:6.1f}-{s.end:6.1f}] {s.text.strip()}")
    (out / f"{sid}.srt.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    # 畫面抽格，八格拼成一條。
    step = max(1.0, round(dur / 8, 2))
    for f in out.glob(f"{sid}_frame_*.jpg"):
        f.unlink()
    sh("ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"fps=1/{step},scale=320:-1", str(out / f"{sid}_frame_%02d.jpg"))
    frames = sorted(out.glob(f"{sid}_frame_*.jpg"))[:8]
    cmd = ["ffmpeg", "-v", "error", "-y"]
    for f in frames:
        cmd += ["-i", str(f)]
    cmd += ["-filter_complex", "".join(f"[{i}]" for i in range(len(frames))) + f"hstack={len(frames)}", str(out / f"{sid}_strip.jpg")]
    sh(*cmd)
    print(f"strip: {out / f'{sid}_strip.jpg'}")

if __name__ == "__main__":
    main()
