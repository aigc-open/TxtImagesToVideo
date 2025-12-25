"""
txt_images_to_ai_video - 将图片和旁白转化成视频的工具

使用 OpenAI 的 TTS 服务将旁白转化成语音，
并将生成的语音和图片组合成一个视频。
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .video import create_video

__all__ = ["create_video"]

