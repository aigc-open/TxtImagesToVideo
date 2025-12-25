"""
TTS (Text-to-Speech) 模块
使用 OpenAI TTS API 将文本转换为语音
"""

import os
from pathlib import Path
from openai import OpenAI


class TTSService:
    """OpenAI TTS 服务封装"""
    
    def __init__(self, api_key=None, base_url=None, voice="alloy", speed=1.0, model="tts-1"):
        """
        初始化 TTS 服务
        
        Args:
            api_key: OpenAI API Key，默认从环境变量 OPENAI_API_KEY 读取
            base_url: OpenAI API Base URL，默认从环境变量 OPENAI_BASE_URL 读取
            voice: 语音类型，可选: alloy, echo, fable, onyx, nova, shimmer
            speed: 语速 (0.25 - 4.0)
            model: TTS 模型，默认 tts-1
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.voice = voice
        self.speed = speed
        self.model = model
        
        if not self.api_key:
            raise ValueError("未设置 OPENAI_API_KEY 环境变量")
        
        # 初始化 OpenAI 客户端
        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        
        self.client = OpenAI(**client_kwargs)
    
    def text_to_speech(self, text, output_path):
        """
        将文本转换为语音文件
        
        Args:
            text: 输入文本
            output_path: 输出音频文件路径
        
        Returns:
            Path: 输出文件路径
        """
        output_path = Path(output_path)
        
        print(f"正在生成语音: {output_path.name}")
        
        with self.client.audio.speech.with_streaming_response.create(
            model=self.model,
            voice=self.voice,
            input=text,
            speed=self.speed
        ) as response:
            response.stream_to_file(output_path)
        
        print(f"语音生成完成: {output_path}")
        return output_path

