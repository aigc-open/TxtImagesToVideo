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
    合并多个视频（内部使用）
    
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


def merge_videos_simple(input_videos, output_video):
    """
    合并多个视频文件为一个视频（命令行使用）
    
    Args:
        input_videos: 视频文件路径，多个视频用逗号分隔（例如: a.mp4,b.mp4,c.mp4）
        output_video: 输出视频路径
    
    Returns:
        Path: 输出视频路径
    """
    # 解析视频文件列表
    video_files = [Path(v.strip()) for v in input_videos.split(',')]
    
    # 验证文件是否存在
    for video_file in video_files:
        if not video_file.exists():
            raise FileNotFoundError(f"视频文件不存在: {video_file}")
    
    output_path = Path(output_video)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("视频合并工具")
    print("=" * 60)
    print(f"\n输入视频: {len(video_files)} 个")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {video}")
    print(f"输出视频: {output_path}")
    
    print(f"\n正在合并视频...")
    result = merge_videos(video_files, output_path)
    
    print(f"\n✅ 视频合并完成: {result}")
    print("=" * 60)
    
    return result


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


def create_video(text_file, image_files, output_video, tts_service, temp_dir=None, audio_file=None, keep_audio=False):
    """
    创建视频的主函数
    
    Args:
        text_file: 旁白文本文件路径
        image_files: 图片文件路径列表
        output_video: 输出视频路径
        tts_service: TTS 服务实例
        temp_dir: 临时文件目录，默认为输出视频所在目录下的 temp 文件夹
        audio_file: 已有的语音文件路径（可选），如果提供则跳过TTS生成
        keep_audio: 是否保留生成的语音文件（默认False）
    
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
    
    # 生成或使用现有语音
    print(f"\n步骤 1/3: 处理语音文件")
    should_cleanup_audio = False  # 标记是否需要清理音频文件
    
    # 检查是否提供了语音文件路径
    if audio_file:
        audio_file = Path(audio_file)
        if audio_file.exists():
            print(f"✅ 使用已有语音文件: {audio_file}")
            audio_path = audio_file
        else:
            print(f"语音文件不存在，生成到: {audio_file}")
            # 确保目录存在
            audio_file.parent.mkdir(parents=True, exist_ok=True)
            tts_service.text_to_speech(text, audio_file)
            audio_path = audio_file
    else:
        # 没有指定 audio_file，使用默认临时路径
        audio_path = temp_dir / "audio.mp3"
        if audio_path.exists():
            print(f"✅ 发现已有语音文件，跳过生成: {audio_path}")
        else:
            print(f"生成新语音文件...")
            tts_service.text_to_speech(text, audio_path)
            should_cleanup_audio = True
    
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
    # 只清理我们生成的音频文件，保留已有的或用户要求保留的
    if should_cleanup_audio and not keep_audio and audio_path.exists():
        audio_path.unlink()
    elif keep_audio and audio_path.exists():
        print(f"✅ 语音文件已保留: {audio_path}")
    if len(video_segments) > 1 and merged_video.exists():
        merged_video.unlink()
    
    # 如果临时目录为空，删除它
    try:
        temp_dir.rmdir()
    except OSError:
        pass  # 目录不为空，不删除
    
    return output_video

