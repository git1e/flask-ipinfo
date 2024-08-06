#!/bin/bash
set -e

# 定义路径变量，提高可维护性
SOURCE_FILE="../ip2region/binding/python/xdbSearcher.py"
PYTHON_SCRIPT_PATH="../ip2region/maker/python"
DATA_FILE_PATH="../../data/ip.merge.txt"
TARGET_FILE="ip2region.xdb"
FINAL_DESTINATION="../../../"

# 检查源文件是否存在
if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: Source file $SOURCE_FILE does not exist."
    exit 1
fi

# 复制源文件，注意安全性，使用-v选项
cp -av "$SOURCE_FILE" ../

# 进入Python脚本路径并执行脚本
echo "Generating database..."
cd "$PYTHON_SCRIPT_PATH" || { echo "Error: Directory $PYTHON_SCRIPT_PATH does not exist."; exit 1; }
python main.py gen --src="$DATA_FILE_PATH" --dst="$TARGET_FILE" || { echo "Error: Failed to generate the database using the Python script."; exit 1; }

# 检查目标文件是否存在
if [ ! -f "$TARGET_FILE" ]; then
    echo "Error: Target file $TARGET_FILE does not exist."
    exit 1
fi

# 复制生成的数据库文件到最终目的地
cp -av "$TARGET_FILE" "$FINAL_DESTINATION"

echo "Process completed successfully."