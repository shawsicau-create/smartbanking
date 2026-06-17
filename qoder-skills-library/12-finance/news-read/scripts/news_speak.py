#!/usr/bin/env python3
"""
news_speak.py — 新闻语音播报辅助脚本（v2.0 edge-tts 版）

用法:
    # 中文播报（默认晓晓女声）
    python news_speak.py "今日新闻摘要内容..."

    # 指定音色
    python news_speak.py --voice zh-CN-YunyangNeural "新闻内容..."

    # 英文播报
    python news_speak.py --voice en-US-JennyNeural "Today's news summary..."

    # 保存为音频文件（不播放）
    python news_speak.py --save ~/Desktop/news.mp3 "新闻内容..."

    # 保存并播放
    python news_speak.py --save ~/Desktop/news.mp3 --play "新闻内容..."

    # 降级到 macOS say（离线模式）
    python news_speak.py --fallback "新闻内容..."
"""

import asyncio
import subprocess
import argparse
import sys
import platform
from datetime import datetime
from pathlib import Path


# ========== 语音配置 ==========

VOICES = {
    # 中文
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",    # 女，温暖专业（默认）
    "yunyang":  "zh-CN-YunyangNeural",      # 男，新闻播音
    "yunjian":  "zh-CN-YunjianNeural",      # 男，激情体育
    "yunxi":    "zh-CN-YunxiNeural",        # 男，阳光活泼
    "xiaoyi":   "zh-CN-XiaoyiNeural",       # 女，活泼可爱
    # 英文
    "jenny":    "en-US-JennyNeural",        # 女，自然亲切
    "guy":      "en-US-GuyNeural",          # 男，成熟专业
    "aria":     "en-US-AriaNeural",         # 女，温柔
    "davis":    "en-US-DavisNeural",        # 男，沉稳
}

# 简写 → 完整 voice ID 的映射
SHORT_NAMES = {v.split("-")[-1].replace("Neural", "").lower(): v for v in VOICES.values()}


def resolve_voice(name: str) -> str:
    """解析用户输入的 voice 名称为 edge-tts voice ID。"""
    if name in VOICES:
        return VOICES[name]
    if name in SHORT_NAMES:
        return SHORT_NAMES[name]
    # 直接传入了完整 ID
    if "Neural" in name:
        return name
    # 默认
    return "zh-CN-XiaoxiaoNeural"


# ========== edge-tts 引擎 ==========

async def _edge_tts_generate(text: str, voice: str, output: str) -> None:
    """使用 edge-tts 生成语音文件。"""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)


def speak_edge_tts(text: str, voice: str, save_path: str = None, play: bool = True) -> str:
    """生成并播放 edge-tts 语音。返回生成的文件路径。"""
    output = save_path or "/tmp/news_speak_edge.mp3"
    print(f"  🔊 生成语音中... (voice: {voice})")

    asyncio.run(_edge_tts_generate(text, voice, output))

    file_size = Path(output).stat().st_size / 1024
    print(f"  💾 音频已生成: {output} ({file_size:.0f} KB)")

    if play:
        print("  🎙️ 开始播放...")
        _play_audio(output)

    return output


# ========== macOS say 引擎（降级方案）==========

def speak_say(text: str, voice: str = "Tingting") -> None:
    """使用 macOS say 命令播报（离线降级方案）。"""
    system = platform.system()
    if system != "Darwin":
        print("❌ say 命令仅适用于 macOS", file=sys.stderr)
        sys.exit(1)

    # 分段避免过长
    chunks = _chunk_text(text)
    for i, chunk in enumerate(chunks):
        print(f"  🎙️ 播报片段 {i+1}/{len(chunks)}...")
        subprocess.run(["say", "-v", voice, chunk], check=True)


# ========== 播放器 ==========

def _play_audio(path: str) -> None:
    """跨平台音频播放。"""
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["afplay", path], check=True)
    elif system == "Windows":
        subprocess.run(["start", path], shell=True)
    else:
        # Linux: 尝试 mpv → vlc → ffplay
        for player in ["mpv", "vlc", "ffplay"]:
            try:
                subprocess.run([player, path], check=True)
                return
            except FileNotFoundError:
                continue
        print("⚠️ 未找到音频播放器，请手动播放:", path)


# ========== 工具函数 ==========

def _chunk_text(text: str, max_chars: int = 800) -> list[str]:
    """将长文本按句子拆分为片段。"""
    for sep in ["。", "！", "？", ".", "!", "?"]:
        text = text.replace(sep, sep + "\n")
    sentences = [s.strip() for s in text.split("\n") if s.strip()]

    chunks, current = [], ""
    for s in sentences:
        if len(current) + len(s) > max_chars:
            if current:
                chunks.append(current.strip())
            current = s
        else:
            current += s
    if current.strip():
        chunks.append(current.strip())
    return chunks or [text]


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(
        description="📻 新闻语音播报（edge-tts 自然语音）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
可用音色:
  中文: xiaoxiao(默认), yunyang, yunjian, yunxi, xiaoyi
  英文: jenny, guy, aria, davis
  或直接传入完整 voice ID (如 zh-CN-XiaoxiaoNeural)
        """,
    )
    parser.add_argument("text", help="要播报的文本内容")
    parser.add_argument("--voice", "-v", default="xiaoxiao",
                        help="音色名称或 voice ID (默认: xiaoxiao)")
    parser.add_argument("--save", "-s", metavar="FILE",
                        help="保存为音频文件（默认不保存）")
    parser.add_argument("--play", "-p", action="store_true", default=True,
                        help="生成后播放 (默认开启)")
    parser.add_argument("--no-play", action="store_true",
                        help="只保存不播放")
    parser.add_argument("--fallback", "-f", action="store_true",
                        help="降级到 macOS say（离线模式）")
    args = parser.parse_args()

    if args.no_play:
        args.play = False

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"\n📻 新闻语音播报 — {date_str}")
    print(f"   文本长度: {len(args.text)} 字\n")

    if args.fallback:
        voice_map = {"xiaoxiao": "Tingting", "jenny": "Samantha", "guy": "Daniel"}
        say_voice = voice_map.get(args.voice, "Tingting")
        print(f"   引擎: macOS say (降级模式)")
        print(f"   音色: {say_voice}\n")
        speak_say(args.text, say_voice)
    else:
        voice_id = resolve_voice(args.voice)
        print(f"   引擎: edge-tts (自然语音)")
        print(f"   音色: {voice_id}\n")
        speak_edge_tts(args.text, voice_id, save_path=args.save, play=args.play)

    print("\n✅ 完成")


if __name__ == "__main__":
    main()
