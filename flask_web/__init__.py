#包构造文件，创建程序实例
import os
import sys

from flask import Flask

import os
import logging
import re

from dotenv import load_dotenv
from flask import Flask,request,jsonify

# 配置日志
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='app.log',  # 日志文件名
                    filemode='a')       # 文件打开模式，'a' 表示追加模式

# 创建一个处理器，用于控制台输出
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
console_handler.setFormatter(formatter)

# 获取 Flask 的根日志记录器
logger = logging.getLogger(__name__)
logger.addHandler(console_handler)  # 添加控制台处理器
logger.setLevel(logging.DEBUG)     # 设置日志级别



# 加载环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
from flask_web import views, errors, commands