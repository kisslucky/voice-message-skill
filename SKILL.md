---
name: voice-message
description: Send text-to-speech voice messages to chat channels that accept audio attachments or MEDIA uploads. Use when the user asks to send a voice message, speak text aloud, read a reply as audio, or generate platform-specific audio files for WeCom, Feishu, Telegram, WhatsApp, or generic MP3 delivery.
license: MIT
metadata:
  openclaw:
    emoji: "🎙️"
    category: "communication"
    tags: ["voice", "tts", "audio-message", "wecom", "feishu"]
  hermes:
    tags: ["communication", "voice", "tts", "audio", "wecom", "feishu"]
    related_skills: ["wecom-install"]
    requires_toolsets: [terminal]
---

# Voice Message

Turn text into a platform-ready voice file, then hand the file back to the caller for delivery.

## Runtime Notes

- OpenClaw can use this skill directly as written.
- Hermes can also use this skill because the package follows the `SKILL.md` convention. If Hermes is not already running inside the skill directory, call the helper script via `${HERMES_SKILL_DIR}/scripts/generate_voice.py`.

## Core Rules

1. Prefer `voice-message` as the canonical skill name for new workflows. Treat WeCom as one target platform, not the only one.
2. Keep the spoken message concise. Default to under 30 seconds unless the user asks for a longer clip.
3. Match the output format to the destination platform before sending.
4. If the caller only needs a file, stop after generation. Do not assume a delivery channel.
5. If generation fails, report which dependency is missing or which conversion step failed.

## Preflight Check

Confirm these dependencies before generating audio:

- `python` is available.
- `edge-tts` is installed: `python -m edge_tts --version`
- `ffmpeg` is installed: `ffmpeg -version`

If a dependency is missing, install it first or tell the caller exactly what is missing.

## Platform Mapping

| Platform | Output format | Notes |
| --- | --- | --- |
| WeCom | `amr` | Use 8kHz mono AMR-NB. |
| Feishu | `ogg` | Use Opus in OGG. |
| Telegram | `ogg` | Use Opus in OGG. |
| WhatsApp | `opus` | Use Opus. |
| Generic | `mp3` | Use when the caller only needs a voice file. |

When the target platform is unclear, default to `generic` and return an MP3.

## Workflow

1. Confirm the text to speak and the destination platform.
2. Pick a voice. Default to `zh-CN-XiaoyiNeural`.
3. Run the script:

```bash
python scripts/generate_voice.py "文字内容" --platform wecom
```

4. Return the generated file path.
5. If the caller supports `MEDIA:` style sending, pass the final path through unchanged.

## Common Commands

Basic generation:

```bash
python scripts/generate_voice.py "陈丰哥哥你好，我是阿淘"
```

Specify a platform:

```bash
python scripts/generate_voice.py "这是一条企微语音" --platform wecom
python scripts/generate_voice.py "这是一条飞书语音" --platform feishu
```

Specify a voice:

```bash
python scripts/generate_voice.py "用晓晓说这句话" --voice zh-CN-XiaoxiaoNeural
```

Write to a known location:

```bash
python scripts/generate_voice.py "发给用户的语音" --platform wecom --output D:/openclaw-workspace/outputs/test_voice.amr
```

## Voice Selection

Use these voices unless the caller requests a different one:

| Voice ID | Name | Style |
| --- | --- | --- |
| `zh-CN-XiaoyiNeural` | 小艺 | lively default |
| `zh-CN-XiaoxiaoNeural` | 晓晓 | warm |
| `zh-CN-YunxiNeural` | 云希 | upbeat male |
| `zh-CN-YunjianNeural` | 云健 | energetic male |
| `zh-CN-YunyangNeural` | 云扬 | steady male |
| `zh-CN-YunxiaNeural` | 云霞 | playful |
| `zh-CN-liaoning-XiaobeiNeural` | 晓北 | Liaoning dialect |
| `zh-CN-shaanxi-XiaoniNeural` | 晓妮 | Shaanxi dialect |

## Failure Handling

- `edge-tts` fails: check Python, network access, and whether `edge-tts` is installed.
- `ffmpeg` fails: check `ffmpeg -version`, then retry conversion.
- Wrong file type for the channel: regenerate with the correct `--platform`.
- File too long: shorten the text and regenerate.

## Validation

Use a representative command after changes:

```bash
python scripts/generate_voice.py "你好，这是一条测试语音" --platform generic
```

The command is valid if it produces an output file path and exits cleanly.
