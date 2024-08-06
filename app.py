import os
import logging
import re

from dotenv import load_dotenv
from flask import Flask,request,jsonify
from xdbSearcher import XdbSearcher

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
logger = logging.getLogger('werkzeug')
logger.addHandler(console_handler)  # 添加控制台处理器
logger.setLevel(logging.DEBUG)     # 设置日志级别



# 加载环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# 创建 Flask 应用实例
app = Flask(__name__)

# 加载 ip 数据库
DATABASE_PATH = 'ip2region.xdb'

def get_ip_address_info(ip_address):
    try:
        dbPath = "ip2region.xdb"

        cb = XdbSearcher.loadContentFromFile(dbfile=dbPath)

        # 2. 仅需要使用上面的全文件缓存创建查询对象, 不需要传源 xdb 文件
        searcher = XdbSearcher(contentBuff=cb)


        region_str = searcher.search(ip_address)
        print(region_str)

        # 4. 关闭searcher
        searcher.close()

        # 按 "|" 分割字符串
        split_data = region_str.split("|")

        # 创建一个空字典
        result_dict = {}

        result_dict["IP"]=ip_address

        # 默认的 region 信息都固定了格式：国家|区域|省份|城市|ISP，缺省的地域信息默认是0
        keys = ["国家", "区域", "省份", "城市", "ISP"]
        # 将分割后的数据填充到字典中
        for i, key in enumerate(keys):
            result_dict[key] = split_data[i]
        logger.info(f"Success Ip2region: {result_dict}")
        return result_dict
    except Exception as e:
        logger.error(f"Error Ip2region: {ip_address}")

# 路由定义
@app.route('/')
def ip_info():
    logger.info('Received request at /')
    # 获取客户端 IP 地址,如果经过了代理服务器,client_ip则从x-forwarded-for头中获取
    X_Forwarded_For=request.headers.get("X-Forwarded-For")
    if X_Forwarded_For:
        client_ip = X_Forwarded_For[0]
        logger.info(f"get client ip:{client_ip} from X-Forwarded-For:{X_Forwarded_For}")
    else:
        client_ip = request.remote_addr
        logger.info(f"get client ip:{client_ip} from remote_addr:{client_ip}")

    data=get_ip_address_info(client_ip)
    # 使用 jsonify 将字典转换为 JSON 响应
    return jsonify(data)


def validate_ip_address(ip_address):
    """
    验证IP地址的合法性。
    """
    # 简化并清晰化的正则表达式
    ip_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip_address) is not None


@app.route('/<string:ip_address>/json')
def single_ip_info(ip_address):
    """
    处理IP地址：先验证，后获取信息。
    """
    if not validate_ip_address(ip_address):
        data={"error": "Invalid IP address %s"%ip_address}
        logger.error(data)
        return jsonify(data)

    # 获取IP地址信息并返回
    data = get_ip_address_info(ip_address)
    return jsonify(data)


#


# 主入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
