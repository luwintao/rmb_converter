#!/bin/bash
echo "正在安装依赖..."
pip install -r requirements.txt

echo "正在打包程序..."
pyinstaller --onefile --windowed --name "RMBConverter" --icon=NONE rmb_converter.py

echo "打包完成！可执行文件在 dist 文件夹中"