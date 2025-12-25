#!/bin/bash

# 生成视频示例
export OPENAI_API_KEY="sk-xxx" 
export OPENAI_BASE_URL="https://xxxx/v1"

# 使用新的 generate 命令
python -m txt_images_to_ai_video generate \
  --input_txt=test/page01-cover-script.txt \
  --input_image=test/page01-cover.png,test/page02-introduction.png \
  --output_video=test/demo.mp4 \
  --audio_file=test/page01-cover-audio.mp3 \
  --keep_audio=True

# 合并视频示例（如果有多个视频需要合并）
# python -m txt_images_to_ai_video merge_video \
#   --input=test/video1.mp4,test/video2.mp4 \
#   --output_video=test/final.mp4