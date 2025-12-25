"""
视频生成模块
将图片和音频合成视频
"""

import subprocess
from pathlib import Path
from typing import List


def get_audio_duration(audio_path):
    """
    获取音频时长
    
    Args:
        audio_path: 音频文件路径
    
    Returns:
        float: 音频时长（秒）
    """
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', str(audio_path)],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def create_image_video(image_path, duration, output_path):
    """
    将单张图片转换为指定时长的视频
    
    Args:
        image_path: 图片路径
        duration: 视频时长（秒）
        output_path: 输出视频路径
    
    Returns:
        Path: 输出视频路径
    """
    output_path = Path(output_path)
    
    cmd = [
        'ffmpeg',
        '-loop', '1',
        '-i', str(image_path),
        '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',  # 确保宽高是偶数
        '-c:v', 'libx264',
        '-tune', 'stillimage',
        '-pix_fmt', 'yuv420p',
        '-t', str(duration),
        '-y',  # 覆盖输出文件
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_path


def merge_videos(video_list, output_path):
    """
    合并多个视频
    
    Args:
        video_list: 视频文件路径列表
        output_path: 输出视频路径
    
    Returns:
        Path: 输出视频路径
    """
    output_path = Path(output_path)
    temp_dir = output_path.parent
    list_file = temp_dir / "concat_list.txt"
    
    # 创建文件列表
    with open(list_file, 'w') as f:
        for video in video_list:
            f.write(f"file '{Path(video).absolute()}'\n")
    
    # 使用 ffmpeg concat
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        '-y',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    
    # 清理临时文件
    list_file.unlink()
    
    return output_path


def add_audio_to_video(video_path, audio_path, output_path):
    """
    将音频添加到视频
    
    Args:
        video_path: 视频文件路径
        audio_path: 音频文件路径
        output_path: 输出视频路径
    
    Returns:
        Path: 输出视频路径
    """
    output_path = Path(output_path)
    
    cmd = [
        'ffmpeg',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-shortest',
        '-y',
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_path


def create_video(text_file, image_files, output_video, tts_service, temp_dir=None):
    """
    创建视频的主函数
    
    Args:
        text_file: 旁白文本文件路径
        image_files: 图片文件路径列表
        output_video: 输出视频路径
        tts_service: TTS 服务实例
        temp_dir: 临时文件目录，默认为输出视频所在目录下的 temp 文件夹
    
    Returns:
        Path: 输出视频路径
    """
    text_file = Path(text_file)
    image_files = [Path(img) for img in image_files]
    output_video = Path(output_video)
    
    # 创建临时目录
    if temp_dir is None:
        temp_dir = output_video.parent / "temp"
    else:
        temp_dir = Path(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取旁白文本
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    if not text:
        raise ValueError(f"文本文件为空: {text_file}")
    
    # 生成语音
    print(f"\n步骤 1/3: 生成语音")
    audio_path = temp_dir / "audio.mp3"
    tts_service.text_to_speech(text, audio_path)
    
    # 获取音频时长
    audio_duration = get_audio_duration(audio_path)
    print(f"音频时长: {audio_duration:.2f} 秒")
    
    # 计算每张图片的时长
    num_images = len(image_files)
    duration_per_image = audio_duration / num_images
    print(f"\n步骤 2/3: 生成 {num_images} 个图片视频片段（每个 {duration_per_image:.2f} 秒）")
    
    # 为每张图片生成视频片段
    video_segments = []
    for i, image_file in enumerate(image_files, 1):
        print(f"  处理图片 {i}/{num_images}: {image_file.name}")
        segment_path = temp_dir / f"segment_{i:03d}.mp4"
        create_image_video(image_file, duration_per_image, segment_path)
        video_segments.append(segment_path)
    
    # 合并所有视频片段
    print(f"\n步骤 3/3: 合并视频片段")
    if len(video_segments) > 1:
        merged_video = temp_dir / "merged_video.mp4"
        merge_videos(video_segments, merged_video)
    else:
        merged_video = video_segments[0]
    
    # 添加音频
    print(f"添加音频到视频")
    add_audio_to_video(merged_video, audio_path, output_video)
    
    print(f"\n✅ 视频生成完成: {output_video}")
    
    # 清理临时文件
    print(f"清理临时文件...")
    for segment in video_segments:
        if segment.exists():
            segment.unlink()
    if audio_path.exists():
        audio_path.unlink()
    if len(video_segments) > 1 and merged_video.exists():
        merged_video.unlink()
    
    # 如果临时目录为空，删除它
    try:
        temp_dir.rmdir()
    except OSError:
        pass  # 目录不为空，不删除
    
    return output_video

