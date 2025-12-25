"""
命令行接口模块
"""

import sys
import fire
from pathlib import Path
from .tts import TTSService
from .video import create_video, merge_videos_simple


class CLI:
    """txt_images_to_ai_video 命令行工具"""
    
    def generate(
        self,
        input_txt,
        input_image,
        output_video,
        voice="alloy",
        speed=1.0,
        model="tts-1",
        temp_dir=None,
        audio_file=None,
        keep_audio=False
    ):
        """
        将图片和旁白转化成视频
        
        Args:
            input_txt: 旁白文本文件路径
            input_image: 图片文件路径，多个图片用逗号分隔（例如: 1.png,2.png,3.png）
            output_video: 输出视频文件路径
            voice: TTS 语音类型（alloy/echo/fable/onyx/nova/shimmer，默认: alloy）
            speed: TTS 语速，范围 0.25-4.0（默认: 1.0）
            model: TTS 模型（默认: tts-1）
            temp_dir: 临时文件目录（默认: 输出视频所在目录下的 temp 文件夹）
            audio_file: 语音文件路径（可选）：如果文件存在则使用，不存在则生成到该路径
            keep_audio: 保留生成的语音文件（默认: False）
        
        示例:
            python -m txt_images_to_ai_video generate --input_txt=script.txt --input_image=1.png,2.png --output_video=output.mp4
            python -m txt_images_to_ai_video generate --input_txt=script.txt --input_image=1.png,2.png --output_video=output.mp4 --voice=nova --speed=1.2
        
        环境变量:
            OPENAI_API_KEY     OpenAI API密钥（必需）
            OPENAI_BASE_URL    OpenAI API基础URL（可选）
        """
        try:
            # 验证输入文件
            text_file = Path(input_txt)
            if not text_file.exists():
                print(f"❌ 错误: 文本文件不存在: {text_file}", file=sys.stderr)
                return False
            
            # 解析图片文件列表
            image_files = [Path(img.strip()) for img in input_image.split(',')]
            for img_file in image_files:
                if not img_file.exists():
                    print(f"❌ 错误: 图片文件不存在: {img_file}", file=sys.stderr)
                    return False
            
            # 创建输出目录
            output_video_path = Path(output_video)
            output_video_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 初始化 TTS 服务
            print("=" * 60)
            print("txt_images_to_ai_video - 图片旁白转视频")
            print("=" * 60)
            print(f"\n配置:")
            print(f"  文本文件: {text_file}")
            print(f"  图片文件: {len(image_files)} 个")
            for i, img in enumerate(image_files, 1):
                print(f"    {i}. {img}")
            print(f"  输出视频: {output_video_path}")
            print(f"  语音类型: {voice}")
            print(f"  语速: {speed}")
            print(f"  模型: {model}")
            if audio_file:
                audio_path = Path(audio_file)
                if audio_path.exists():
                    print(f"  语音文件: {audio_file} (使用已有)")
                else:
                    print(f"  语音文件: {audio_file} (将生成到此)")
            
            tts_service = TTSService(
                voice=voice,
                speed=speed,
                model=model
            )
            
            # 生成视频
            create_video(
                text_file=text_file,
                image_files=image_files,
                output_video=output_video_path,
                tts_service=tts_service,
                temp_dir=temp_dir,
                audio_file=audio_file,
                keep_audio=keep_audio
            )
            
            print("\n" + "=" * 60)
            print("✅ 处理完成！")
            print("=" * 60)
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断操作", file=sys.stderr)
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return False
    
    def merge_video(self, input, output_video):
        """
        合并多个视频文件为一个视频
        
        Args:
            input: 视频文件路径，多个视频用逗号分隔（例如: a.mp4,b.mp4,c.mp4）
            output_video: 输出视频路径
        
        示例:
            python -m txt_images_to_ai_video merge_video --input=a.mp4,b.mp4 --output_video=output.mp4
            python -m txt_images_to_ai_video merge_video --input=video1.mp4,video2.mp4,video3.mp4 --output_video=final.mp4
        """
        try:
            merge_videos_simple(input, output_video)
            return True
        except KeyboardInterrupt:
            print("\n\n⚠️  用户中断操作", file=sys.stderr)
            return False
        except Exception as e:
            print(f"\n❌ 错误: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数入口"""
    fire.Fire(CLI)

