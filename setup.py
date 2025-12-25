"""
setup.py - 打包配置文件
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
this_directory = Path(__file__).parent
long_description = ""
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

setup(
    name="txt_images_to_ai_video",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="将图片和旁白转化成视频的工具，使用 OpenAI TTS 服务",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TxtImagesToVideo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "txt_images_to_ai_video=txt_images_to_ai_video.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/TxtImagesToVideo/issues",
        "Source": "https://github.com/yourusername/TxtImagesToVideo",
    },
)

