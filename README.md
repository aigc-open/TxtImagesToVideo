# txt_images_to_ai_video

将图片和旁白转化成视频的工具，使用 OpenAI TTS 服务将旁白转化成语音，并将生成的语音和图片组合成一个视频。

## 功能特性

- 📝 使用 OpenAI TTS 服务将文本转换为高质量语音
- 🖼️ 支持多张图片按顺序组合成视频
- ⏱️ 自动根据音频时长平均分配图片展示时间
- 🎨 支持自定义语音类型和语速
- 📦 可打包成 whl 文件，方便安装和分发

## 系统要求

- Python 3.8+
- ffmpeg（用于音视频处理）

### 安装 ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
从 [ffmpeg官网](https://ffmpeg.org/download.html) 下载并添加到系统PATH。

## 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/TxtImagesToVideo.git
cd TxtImagesToVideo
pip install -r requirements.txt
pip install -e .
```

### 从 whl 文件安装

```bash
# 首先构建 whl 包
pip install build
python -m build

# 安装生成的 whl 文件
pip install dist/txt_images_to_ai_video-0.1.0-py3-none-any.whl
```

## 配置

在使用之前，需要配置 OpenAI API 密钥：

```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 可选，如果使用自定义端点
```

可以将这些配置添加到 `~/.bashrc` 或 `~/.zshrc` 中以永久保存。

## 使用方法

### 基本用法

```bash
python -m txt_images_to_ai_video \
  --input_txt script.txt \
  --input_image 1.png,2.png,3.png \
  --output_video output.mp4
```

### 查看帮助

```bash
python -m txt_images_to_ai_video --help
```

### 高级选项

```bash
python -m txt_images_to_ai_video \
  --input_txt script.txt \
  --input_image 1.png,2.png \
  --output_video output.mp4 \
  --voice nova \
  --speed 1.2 \
  --model tts-1-hd \
  --temp_dir ./temp
```

### 参数说明

- `--input_txt`: 旁白文本文件路径（必需）
- `--input_image`: 图片文件路径，多个图片用逗号分隔（必需）
- `--output_video`: 输出视频文件路径（必需）
- `--voice`: TTS 语音类型，可选值：alloy, echo, fable, onyx, nova, shimmer（默认: alloy）
- `--speed`: 语速，范围 0.25-4.0（默认: 1.0）
- `--model`: TTS 模型（默认: tts-1）
- `--temp_dir`: 临时文件目录（可选）

## 工作流程

1. 读取旁白文本文件
2. 使用 OpenAI TTS API 将文本转换为语音
3. 根据语音时长和图片数量，计算每张图片的展示时间
4. 为每张图片生成对应时长的视频片段
5. 合并所有视频片段
6. 将语音添加到合并后的视频中
7. 输出最终视频文件

## 示例

假设你有：
- 一个文本文件 `narration.txt` 包含旁白内容
- 三张图片 `slide1.png`, `slide2.png`, `slide3.png`

```bash
python -m txt_images_to_ai_video \
  --input_txt narration.txt \
  --input_image slide1.png,slide2.png,slide3.png \
  --output_video presentation.mp4 \
  --voice nova \
  --speed 1.1
```

这将生成一个名为 `presentation.mp4` 的视频，其中：
- 使用 nova 语音朗读旁白
- 语速为 1.1 倍
- 三张图片按顺序展示，每张图片的时长相同，总时长等于旁白音频的时长

## 开发

### 运行测试

```bash
python -m pytest tests/
```

### 构建 whl 包

```bash
pip install build
python -m build
```

生成的 whl 文件将位于 `dist/` 目录中。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### 0.1.0 (2024-12-25)

- 首次发布
- 支持基本的文本转语音和视频生成功能
