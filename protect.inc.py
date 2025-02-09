"""
参见https://blog.arisa.moe/blog/2023/230114-matrix-qq-wechat-bridge/#_5
用于给homeserver设置定期删除媒体后，保护贴纸不被删除
此文件不应被公共仓库的GIT提交和追踪
请注意修改其中的 Bearer token 和 matrix.moeworld.top 以及 os.walk() 的路径

Admin API文档 https://element-hq.github.io/synapse/latest/admin_api/media_admin_api.html
返回{}代表执行成功

晓空 2025.2.9
"""

# Run （在开始之前，请重命名回到 protect.py）
"""
source venv/bin/activate
python protect.py
"""

import os
import json
from aiohttp import ClientSession

# 定义一个函数，用于获取所有贴纸的 media_id 列表
def get_media_id_list() -> list:
    result = []
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(r'/root/stickerpicker/web/packs'):
        for file in files:
            # 跳过名为 'index.json' 的文件
            if file == 'index.json':
                continue
            # 处理以 '.json' 结尾的文件
            if file.endswith('.json'):
                print("加载："+file)
                # 加载 JSON 文件
                with open(os.path.join(root, file), 'r') as f:
                    j = json.load(f)
                # 提取每个贴纸的 media_id
                for sticker in j['stickers']:
                    media_id = sticker['url'].split('/')[-1]
                    result.append(media_id)
    return result

# 定义一个异步函数，用于保护媒体文件不被删除
async def protect():
    # 设置请求头，包含授权令牌
    headers = {"Authorization": "Bearer 11111111111111111111111111"}
    # 创建一个异步 HTTP 会话
    async with ClientSession() as session:
        # 遍历所有获取到的 media_id
        for media_id in get_media_id_list():
            # 构建保护媒体文件的 API URL
            url = f'https://matrix.moeworld.top/_synapse/admin/v1/media/protect/{media_id}'
            # 发送 POST 请求以保护媒体文件
            async with session.post(url, headers=headers) as resp:
                # 输出请求的 URL 和响应结果
                print(url)
                print(await resp.json())

# 主程序入口
if __name__ == '__main__':
    import asyncio
    # 运行异步 protect 函数
    asyncio.run(protect())
