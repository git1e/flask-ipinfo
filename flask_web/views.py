import os

from flask_web import app, logger

import re

from flask import Flask, request, jsonify, render_template
from .ip2region.xdbSearcher import XdbSearcher

# 加载 ip 数据库
DATABASE_PATH = 'ip2region.xdb'

def get_ip_address_info(ip_address):
    try:
        # 获取当前文件路径
        dbPath = os.path.join(os.path.dirname(__file__), "ip2region.xdb")
        print(dbPath)

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

        result_dict["IP"] = ip_address

        # 默认的 region 信息都固定了格式：国家|区域|省份|城市|ISP，缺省的地域信息默认是0
        keys = ["国家", "区域", "省份", "城市", "ISP"]
        # 将分割后的数据填充到字典中
        for i, key in enumerate(keys):
            result_dict[key] = split_data[i]
        logger.info(f"Success Ip2region: {result_dict}")
        return result_dict
    except Exception as e:
        logger.error(f"Error Ip2region: {ip_address}")

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
        data = {"error": "Invalid IP address %s" % ip_address}
        logger.error(data)
        return jsonify(data)

    # 获取IP地址信息并返回
    data = get_ip_address_info(ip_address)
    # return jsonify(data)
    return render_template('ip.html', result=data)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip', methods=['GET', 'POST'])
def ip_lookup():
    if request.method == 'POST':
        ip_address = request.form.get('ip')
        if not validate_ip_address(ip_address):
            data = {"error": "Invalid IP address %s" % ip_address}
            logger.error(data)
            return jsonify(data)  # 修改为返回 JSON 格式的错误信息

        # 获取IP地址信息并返回
        data = get_ip_address_info(ip_address)
        return render_template('ip.html', result=data)

    return render_template('ip.html')

# 主入口
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
