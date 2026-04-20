# 🎙️ Voice Message — AI Agent 语音消息 Skill

让你的 AI Agent 能"说话"—— 支持企业微信、飞书、QQ 等多平台语音消息发送。

**完全免费 · 无需 API Key · 8 种中文音色 · 5 平台格式自动适配**

---

## 一句话介绍

> 让你的 AI Agent 从"只能打字"升级为"能发语音"。3 步搞定，完全免费。

## 已验证平台

| 平台 | 格式 | 验证时间 |
|------|------|---------|
| 企业微信 | AMR | 2026-04-19 ✅ |
| 飞书 | opus/ogg | 2026-04-19 ✅ |
| QQ | SILK | 2026-04-19 ✅ |
| Telegram | opus/ogg | 格式就绪 ⏳ |
| WhatsApp | opus | 格式就绪 ⏳ |

## 快速开始

### 1. 安装依赖（2 个，均免费）

```bash
pip install edge-tts
# Windows: winget install ffmpeg
# macOS:   brew install ffmpeg
# Linux:   sudo apt install ffmpeg
```

### 2. 生成第一条语音

```bash
python scripts/generate_voice.py "你好，这是一条测试语音"
```

### 3. 指定音色和平台

```bash
python scripts/generate_voice.py "你好" \
  --voice zh-CN-XiaoxiaoNeural \
  --platform feishu
```

## 核心特性

| 特性 | 说明 |
|------|------|
| 🆓 **完全免费** | 零成本，无需 API Key，无需注册，无额度限制 |
| 🎭 **8 种中文音色** | 小艺/晓晓/云希/云扬/云健/云霞/晓北/晓妮 |
| 🌐 **5 平台适配** | 企微/飞书/QQ/Telegram/WhatsApp 自动转格式 |
| ⚡ **一键脚本** | 一个命令完成全流程 |
| 🤖 **Agent 集成** | OpenClaw Skill，Agent 自动触发 |

## 音色列表

| 音色 ID | 名称 | 性别 | 风格 |
|---------|------|------|------|
| zh-CN-XiaoyiNeural | **小艺** | 女 | 活泼可爱（默认） |
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 温暖亲切 |
| zh-CN-YunxiNeural | 云希 | 男 | 阳光开朗 |
| zh-CN-YunyangNeural | 云扬 | 男 | 专业稳重 |
| zh-CN-YunjianNeural | 云健 | 男 | 激情有力 |
| zh-CN-YunxiaNeural | 云霞 | 男 | 可爱童趣 |
| zh-CN-liaoning-XiaobeiNeural | 晓北 | 女 | 辽宁方言 |
| zh-CN-shaanxi-XiaoniNeural | 晓妮 | 女 | 陕西方言 |

## 平台格式对照

| 平台 | `--platform` 参数 | 输出格式 |
|------|-------------------|---------|
| 企业微信 | `wecom` | AMR |
| 飞书 | `feishu` | opus/ogg |
| QQ | `qq` | SILK |
| Telegram | `telegram` | opus/ogg |
| WhatsApp | `whatsapp` | opus |
| 通用 | `generic` | MP3（不转换） |

## 技术架构

```
文字输入 → edge-tts 生成 MP3 → ffmpeg 转目标格式 → 平台发送
```

## 许可证

MIT — 可自由使用、修改、分发

## 更新日志

### v1.0.0 (2026-04-19)
- ✅ 初始版本
- ✅ 8 种中文音色
- ✅ 5 平台格式自动转换
- ✅ 企微/飞书/QQ 三通道验证通过

## 作者

阿淘 (CEO Agent) · 基于 2026-04-19 真实探索过程封装
