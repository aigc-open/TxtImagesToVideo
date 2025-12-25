# 图片旁白转视频

- 将图片和对应的旁白转化成视频
- 使用 OpenAI 的 TTS 服务将旁白转化成语音
- 将生成的 语音和图片组合成一个视频
- 一个旁白可能对应多个图片，最终一个视频，多个图片之间按顺序平均分配时间

# 要求
- 使用命令行工具运行
- 将项目发表成whl包
- 使用如下
```bash
python -m txt_images_to_video --help
```
- 使用如下命令运行
```bash
python -m txt_images_to_ai_video --input_txt xxx.txt --input_image 1.png,2.png --output_video xxx.mp4
```
- 请你项目结构清晰，放进一个 txt_images_to_ai_video 目录中
- openai的大模型配置通过环境变量 OPENAI_API_KEY 和 OPENAI_BASE_URL 配置
