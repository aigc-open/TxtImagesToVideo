#!/bin/bash

# 视频生成脚本
# 注意：需要先将 drawio 文件导出为 PNG 图片

cd "$(dirname "$0")"

# 目录配置
STATIC_DIR="output"          # 静态资源目录（输入：图片、旁白文本）
OUTPUT_DIR="output"          # 输出目录（生成的视频）
VIDEO_DIR="$OUTPUT_DIR/videos"  # 章节视频目录

# 配置章节列表（格式：图片文件名:旁白文件名:视频文件名:章节标题）
CHAPTERS=(
  "01_cover.png:01_cover_script.txt:01_cover.mp4:封面"
  "02_features.png:02_features_script.txt:02_features.mp4:核心功能"
  "03_installation.png:03_installation_script.txt:03_installation.mp4:快速开始"
  "04_usage.png:04_usage_script.txt:04_usage.mp4:使用示例"
  "05_summary.png:05_summary_script.txt:05_summary.mp4:总结"
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
  
  python -m txt_images_to_ai_video generate \
    --input_txt="$STATIC_DIR/${script_file}" \
    --input_image="$STATIC_DIR/${image_file}" \
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

