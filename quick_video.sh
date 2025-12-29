#!/bin/bash

# 视频生成脚本
# 注意：需要先将 drawio 文件导出为 PNG 图片

if [ -z "$OPENAI_API_KEY" ]; then
  echo "未设置 OPENAI_API_KEY，已退出。"
  exit 1
fi

cd "$(dirname "$0")"

# 目录配置
STATIC_DIR="/workspace/code/github/TxtImagesToVideo/ph8/adv/"          # 静态资源目录（输入：图片、旁白文本）
OUTPUT_DIR="$STATIC_DIR/output"          # 输出目录（生成的视频）
VIDEO_DIR="$OUTPUT_DIR/videos"  # 章节视频目录

# 配置章节列表（格式：图片文件名:旁白文件名:视频文件名:章节标题）
# 如需添加章节，按以下格式添加一行："图片1,图片2:旁白文本文件:输出视频文件:章节标题"
CHAPTERS=(
  "01-home.png:01-home_script.txt:01-home.mp4:首页"
  "02-model.png:02-model_script.txt:02-model.mp4:模型-概述"
  "02-model-image.png:02-model-image_script.txt:02-model-image.mp4:模型-生图"
  "02-model-video.png:02-model-video_script.txt:02-model-video.mp4:模型-文/图生视频"
  "03-api.png:03-api_script.txt:03-api.mp4:API"
  "04-cases.png,04-cases-docs.png:04-cases_script.txt:04-cases.mp4:案例"
)

# 语音配置
VOICE="nova"
SPEED="1.0"

# 创建视频输出目录
mkdir -p "$VIDEO_DIR"

echo "开始生成各章节视频..."
echo "================================"

# 用于存储所有视频路径（用于合并）
VIDEO_FILES=()

# 循环生成每个章节的视频
for chapter in "${CHAPTERS[@]}"; do
  # 分割章节信息
  IFS=':' read -r image_file script_file video_file title <<< "$chapter"
  
  echo "生成章节：${title}..."
  
  # 处理多个图片的情况（逗号分隔）
  # 将相对路径转换为绝对路径
  IFS=',' read -ra IMAGE_ARRAY <<< "$image_file"
  IMAGE_PATHS=()
  for img in "${IMAGE_ARRAY[@]}"; do
    IMAGE_PATHS+=("$STATIC_DIR/${img}")
  done
  # 用逗号连接所有图片路径
  IMAGE_INPUT=$(IFS=,; echo "${IMAGE_PATHS[*]}")
  
  python -m txt_images_to_ai_video generate \
    --input_txt="$STATIC_DIR/${script_file}" \
    --input_image="$IMAGE_INPUT" \
    --output_video="$VIDEO_DIR/${video_file}" \
    --voice="$VOICE" \
    --speed="$SPEED"
  
  # 检查视频是否生成成功
  if [ $? -eq 0 ]; then
    echo "✓ ${title} 生成成功"
    VIDEO_FILES+=("$VIDEO_DIR/${video_file}")
  else
    echo "✗ ${title} 生成失败"
    exit 1
  fi
  
  echo "--------------------------------"
done

# 合并所有视频
echo "合并所有视频..."
# 将数组转换为逗号分隔的字符串
VIDEO_INPUT=$(IFS=,; echo "${VIDEO_FILES[*]}")

python -m txt_images_to_ai_video merge_video \
  --input="$VIDEO_INPUT" \
  --output_video="$OUTPUT_DIR/final_video.mp4"

if [ $? -eq 0 ]; then
  echo "================================"
  echo "✓ 完成！最终视频已生成：$OUTPUT_DIR/final_video.mp4"
else
  echo "✗ 视频合并失败"
  exit 1
fi

