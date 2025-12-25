"""
命令行接口模块
"""

import sys
import argparse
from pathlib import Path
from .tts import TTSService
from .video import create_video


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="txt_images_to_ai_video",
        description="将图片和旁白转化成视频的工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python -m txt_images_to_ai_video --input_txt script.txt --input_image 1.png,2.png --output_video output.mp4
  
环境变量:
  OPENAI_API_KEY     OpenAI API密钥（必需）
  OPENAI_BASE_URL    OpenAI API基础URL（可选）
        """
    )
    
    parser.add_argument(
        "--input_txt",
        required=True,
        help="旁白文本文件路径"
    )
    
    parser.add_argument(
        "--input_image",
        required=True,
        help="图片文件路径，多个图片用逗号分隔（例如: 1.png,2.png,3.png）"
    )
    
    parser.add_argument(
        "--output_video",
        required=True,
        help="输出视频文件路径"
    )
    
    parser.add_argument(
        "--voice",
        default="alloy",
        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        help="TTS 语音类型（默认: alloy）"
    )
    
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="TTS 语速，范围 0.25-4.0（默认: 1.0）"
    )
    
    parser.add_argument(
        "--model",
        default="tts-1",
        help="TTS 模型（默认: tts-1）"
    )
    
    parser.add_argument(
        "--temp_dir",
        help="临时文件目录（默认: 输出视频所在目录下的 temp 文件夹）"
    )
    
    parser.add_argument(
        "--audio_file",
        help="语音文件路径（可选）：如果文件存在则使用，不存在则生成到该路径"
    )
    
    parser.add_argument(
        "--keep_audio",
        action="store_true",
        help="保留生成的语音文件（默认会清理）"
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    try:
        # 验证输入文件
        text_file = Path(args.input_txt)
        if not text_file.exists():
            print(f"❌ 错误: 文本文件不存在: {text_file}", file=sys.stderr)
            sys.exit(1)
        
        # 解析图片文件列表
        image_files = [Path(img.strip()) for img in args.input_image.split(',')]
        for img_file in image_files:
            if not img_file.exists():
                print(f"❌ 错误: 图片文件不存在: {img_file}", file=sys.stderr)
                sys.exit(1)
        
        # 创建输出目录
        output_video = Path(args.output_video)
        output_video.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化 TTS 服务
        print("=" * 60)
        print("txt_images_to_ai_video - 图片旁白转视频")
        print("=" * 60)
        print(f"\n配置:")
        print(f"  文本文件: {text_file}")
        print(f"  图片文件: {len(image_files)} 个")
        for i, img in enumerate(image_files, 1):
            print(f"    {i}. {img}")
        print(f"  输出视频: {output_video}")
        print(f"  语音类型: {args.voice}")
        print(f"  语速: {args.speed}")
        print(f"  模型: {args.model}")
        if args.audio_file:
            audio_path = Path(args.audio_file)
            if audio_path.exists():
                print(f"  语音文件: {args.audio_file} (使用已有)")
            else:
                print(f"  语音文件: {args.audio_file} (将生成到此)")
        
        tts_service = TTSService(
            voice=args.voice,
            speed=args.speed,
            model=args.model
        )
        
        # 生成视频
        create_video(
            text_file=text_file,
            image_files=image_files,
            output_video=output_video,
            tts_service=tts_service,
            temp_dir=args.temp_dir,
            audio_file=args.audio_file,
            keep_audio=args.keep_audio
        )
        
        print("\n" + "=" * 60)
        print("✅ 处理完成！")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

