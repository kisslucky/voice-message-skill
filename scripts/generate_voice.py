#!/usr/bin/env python3
"""
wecom-voice: 生成语音 + 转目标平台格式
用法: python generate_voice.py "文字内容" [--voice 音色ID] [--platform 平台] [--output 输出路径]
默认音色: zh-CN-XiaoyiNeural（小艺）
默认平台: wecom（企业微信）

支持平台:
  wecom     - 企业微信 (AMR)
  feishu    - 飞书 (opus/ogg)
  telegram  - Telegram (opus/ogg)
  whatsapp  - WhatsApp (opus)
  generic   - 通用 (mp3，不转换)
"""

import argparse
import subprocess
import sys
import os
import tempfile

# Fix encoding for Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


# 平台格式配置
PLATFORM_FORMATS = {
    "wecom": {
        "ext": "amr",
        "cmd": ["ffmpeg", "-y", "-i", "{input}", "-ar", "8000", "-ac", "1", "-c:a", "amr_nb", "{output}"],
        "desc": "AMR（企业微信）"
    },
    "feishu": {
        "ext": "ogg",
        "cmd": ["ffmpeg", "-y", "-i", "{input}", "-c:a", "libopus", "-b:a", "16k", "{output}"],
        "desc": "Opus/OGG（飞书）"
    },
    "telegram": {
        "ext": "ogg",
        "cmd": ["ffmpeg", "-y", "-i", "{input}", "-c:a", "libopus", "-b:a", "16k", "{output}"],
        "desc": "Opus/OGG（Telegram）"
    },
    "whatsapp": {
        "ext": "opus",
        "cmd": ["ffmpeg", "-y", "-i", "{input}", "-c:a", "libopus", "-b:a", "16k", "{output}"],
        "desc": "Opus（WhatsApp）"
    },
    "generic": {
        "ext": "mp3",
        "cmd": None,  # 不需要转换
        "desc": "MP3（通用）"
    }
}


def generate_tts(text, voice, output_mp3):
    """使用 edge-tts 生成语音"""
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", voice,
        "--text", text,
        "--write-media", output_mp3
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] edge-tts 失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(output_mp3):
        print(f"[ERROR] 未生成音频文件: {output_mp3}", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(output_mp3)
    print(f"[OK] MP3 生成成功 ({size} bytes)")
    return output_mp3


def convert_format(mp3_path, platform, output_path):
    """根据平台转换格式"""
    fmt = PLATFORM_FORMATS.get(platform)
    if not fmt:
        print(f"[ERROR] 不支持的平台: {platform}", file=sys.stderr)
        print(f"支持的平台: {', '.join(PLATFORM_FORMATS.keys())}", file=sys.stderr)
        sys.exit(1)

    if fmt["cmd"] is None:
        print(f"[OK] 使用 MP3 格式（通用）")
        return mp3_path

    cmd = [arg.replace("{input}", mp3_path).replace("{output}", output_path) for arg in fmt["cmd"]]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] ffmpeg 转换失败: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    size = os.path.getsize(output_path)
    print(f"[OK] {fmt['desc']} 转换成功 ({size} bytes)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="生成语音并转目标平台格式")
    parser.add_argument("text", help="要转换为语音的文字内容")
    parser.add_argument("--voice", default="zh-CN-XiaoyiNeural", help="音色 ID（默认: zh-CN-XiaoyiNeural 小艺）")
    parser.add_argument("--platform", default="wecom", choices=list(PLATFORM_FORMATS.keys()),
                        help="目标平台（默认: wecom）")
    parser.add_argument("--output", default=None, help="输出文件路径（默认自动生成）")
    args = parser.parse_args()

    fmt = PLATFORM_FORMATS[args.platform]

    # 输出路径
    if args.output:
        base = args.output
        if base.endswith(".mp3"):
            mp3_path = base
            output_path = base.replace(".mp3", f".{fmt['ext']}") if fmt["cmd"] else base
        elif base.endswith(f".{fmt['ext']}"):
            mp3_path = base.replace(f".{fmt['ext']}", ".mp3")
            output_path = base
        else:
            mp3_path = base + ".mp3"
            output_path = base + f".{fmt['ext']}" if fmt["cmd"] else base
    else:
        mp3_path = os.path.join(tempfile.gettempdir(), "wecom_voice.mp3")
        output_path = os.path.join(tempfile.gettempdir(), f"wecom_voice.{fmt['ext']}")

    print(f"Voice: {args.voice}")
    print(f"Platform: {args.platform} ({fmt['desc']})")
    print(f"Text: {args.text[:50]}{'...' if len(args.text) > 50 else ''}")

    # 生成语音
    generate_tts(args.text, args.voice, mp3_path)

    # 转目标格式
    final_path = convert_format(mp3_path, args.platform, output_path)

    print(f"\n[DONE] 发送指令:")
    print(f"MEDIA: {final_path}")
    print(f"\n[OK] 完成！文件: {final_path}")


if __name__ == "__main__":
    main()
