export OPENAI_API_KEY="sk-xxx" 
export OPENAI_BASE_URL="https://xxxx/v1"
python -m txt_images_to_ai_video \
  --input_txt test/page01-cover-script.txt \
  --input_image test/page01-cover.png,test/page02-introduction.png \
  --output_video test/demo.mp4