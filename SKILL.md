---
name: wecom-voice
description: 向支持语音消息的即时通讯平台发送语音消息（企业微信已验证）。使用 edge-tts 生成语音 + ffmpeg 转 AMR 格式 + MEDIA 指令发送。当用户要求"发语音""语音说 xxx""念给我听"时使用此技能。支持 8 种中文音色（默认小艺），完全免费，无需 API Key，适用于所有 OpenClaw + 企微通道及其他支持语音的平台。
---

# WeCom Voice — 语音消息 Skill

**一句话**：让 AI Agent 能向用户发送真实语音消息，完全免费。

**工作流**：
```
文字 → edge-tts 生成语音 → ffmpeg 转目标格式 → MEDIA 指令发送
```

**各平台语音格式要求**：

| 平台 | 格式 | 命令 |
|------|------|------|
| 企业微信 | AMR | `ffmpeg -i in.mp3 -ar 8000 -ac 1 -c:a amr_nb out.amr` |
| 飞书 | opus/ogg | `ffmpeg -i in.mp3 -c:a libopus -b:a 16k out.ogg` |
| Telegram | opus/ogg | `ffmpeg -i in.mp3 -c:a libopus -b:a 16k out.ogg` |
| WhatsApp | opus | `ffmpeg -i in.mp3 -c:a libopus -b:a 16k out.opus` |

> 不确定平台时，默认用 AMR 格式（企微要求）。

## 零、效果验证

安装后，运行以下命令验证环境是否就绪：

```bash
python scripts/generate_voice.py "你好，这是一条测试语音" --output /tmp/test_voice.amr
```

如果输出 `[OK] 完成！AMR 文件: ...` 且文件存在，说明环境配置正确。在 OpenClaw 中配合 MEDIA 指令即可发送语音。

## 一、安装

### 1. 安装依赖（2 个，均免费）

```bash
# edge-tts - 微软免费语音合成，无需 API Key
pip install edge-tts

# ffmpeg - 音频格式转换
# Windows:
winget install ffmpeg
# macOS:
brew install ffmpeg
# Ubuntu/Debian:
sudo apt install ffmpeg
```

### 2. 验证安装

```bash
python -m edge_tts --version   # 应输出版本号
ffmpeg -version                 # 应输出版本号
```

### 3. 安装 Skill

将 `wecom-voice` 目录放入 OpenClaw 的 skills 目录即可。

## 二、触发命令

当用户使用以下表达时，自动触发此 Skill：

| 用户说 | 含义 |
|--------|------|
| "发语音" | 用默认音色朗读回复内容 |
| "语音说 xxx" | 用默认音色说指定文字 |
| "语音告诉我 xxx" | 同上 |
| "念给我听" | 同上 |
| "用 [音色] 说 xxx" | 用指定音色说指定文字 |

**指定音色的说法**：
- "用小艺说 xxx" → zh-CN-XiaoyiNeural
- "用晓晓说 xxx" → zh-CN-XiaoxiaoNeural
- "用云希说 xxx" → zh-CN-YunxiNeural
- "用云扬说 xxx" → zh-CN-YunyangNeural

## 三、使用方法

### 方法 A：使用脚本（推荐）

```bash
python scripts/generate_voice.py "文字内容"
```

默认音色：zh-CN-XiaoyiNeural（小艺，活泼女声）
默认平台：wecom（企业微信，AMR 格式）

指定音色：
```bash
python scripts/generate_voice.py "文字内容" --voice zh-CN-XiaoxiaoNeural
```

指定平台（自动转对应格式）：
```bash
python scripts/generate_voice.py "文字内容" --platform feishu
```

指定输出路径：
```bash
python scripts/generate_voice.py "文字内容" --platform wecom --output /tmp/voice.amr
```

脚本会自动完成：edge-tts 生成 → ffmpeg 转目标格式 → 输出 MEDIA 指令。

**完整命令**：
```bash
python scripts/generate_voice.py "文字内容" \
  --voice zh-CN-XiaoyiNeural \
  --platform wecom \
  --output /tmp/voice.amr
```

### 方法 B：手动执行

```bash
# Step 1: 生成语音
python -m edge_tts --voice zh-CN-XiaoyiNeural \
  --text "陈丰哥哥你好，我是阿淘" \
  --write-media /tmp/voice.mp3

# Step 2: 转 AMR 格式（企微强制要求）
ffmpeg -y -i /tmp/voice.mp3 -ar 8000 -ac 1 -c:a amr_nb /tmp/voice.amr

# Step 3: 发送给用户
MEDIA: /tmp/voice.amr
```

## 四、可用音色（8 种，全部免费）

| 音色 ID | 名称 | 性别 | 风格 |
|---------|------|------|------|
| zh-CN-XiaoyiNeural | **小艺** | 女 | 活泼可爱（默认） |
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 温暖亲切 |
| zh-CN-YunxiNeural | 云希 | 男 | 阳光开朗 |
| zh-CN-YunjianNeural | 云健 | 男 | 激情有力 |
| zh-CN-YunyangNeural | 云扬 | 男 | 专业稳重 |
| zh-CN-YunxiaNeural | 云霞 | 男 | 可爱童趣 |
| zh-CN-liaoning-XiaobeiNeural | 晓北 | 女 | 辽宁方言 |
| zh-CN-shaanxi-XiaoniNeural | 晓妮 | 女 | 陕西方言 |

## 五、免费优势

| 项目 | 说明 |
|------|------|
| **费用** | $0，完全免费 |
| **API Key** | 不需要 |
| **注册账号** | 不需要 |
| **额度限制** | 无官方限制 |
| **商业使用** | 允许 |
| **离线依赖** | 仅生成时需要联网（调用 Edge API） |
| **本地工具** | ffmpeg 完全离线 |

## 六、适用平台

任何同时满足以下条件的平台均可使用：
- 支持 MEDIA 指令（OpenClaw 通道）
- 支持 AMR 格式语音消息（或可适配其他格式）
- 有 Python + edge-tts + ffmpeg 环境

**已验证**：
- ✅ 企业微信（AMR 格式）
- ✅ 飞书（opus/ogg 格式，格式转换已验证通过）

**理论支持**（格式已就绪，需对应通道验证）：
- ⏳ Telegram（opus/ogg）
- ⏳ WhatsApp（opus）
- ⏳ Signal（opus）

## 七、注意事项

1. **语音只发一次**，不重复发送同一条
2. 企微语音**必须 AMR 格式**，wav/mp3 不可直接发送
3. 内容控制在 **30 秒以内**（最佳体验）
4. 企微语音消息大小上限 **2MB**，15 秒 AMR 约 10-25KB，远低于限制
5. edge-tts 生成语音时需要联网（调用微软 Edge API），ffmpeg 转换完全离线

## 八、常见问题

**Q: 为什么一定要转 AMR？**
A: 企业微信语音消息强制要求 AMR 格式，这是企微的技术限制。其他平台可能支持 mp3/wav，需根据平台要求调整。

**Q: 可以调节语速吗？**
A: 可以。edge-tts 支持 `--rate` 参数，如 `--rate "+10%"` 加快，`--rate "-10%"` 减慢。

**Q: 支持英文语音吗？**
A: 支持。使用英文音色（如 en-US-JennyNeural）即可生成英文语音。
