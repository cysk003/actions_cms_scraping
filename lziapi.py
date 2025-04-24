import requests
import time
import os
from urllib.parse import urlparse

TYPE_ID = ""  # 可选类型ID

BASE_URL = "http://cj.lziapi.com/api.php/provide/vod/"
PAGE = 1
MAX_PAGE = 1000

# 提取主域名（去掉协议部分，提取主机名）
parsed_url = urlparse(BASE_URL)
domain_name = parsed_url.netloc  
print(f"抓取的主域名是：{domain_name}")

print("开始抓取播放数据...")

# 打开文件用于写入
while PAGE <= MAX_PAGE:
    url = f"{BASE_URL}?ac=videolist&pg={PAGE}"
    if TYPE_ID:
        url += f"&t={TYPE_ID}"

    print(f"正在抓取第 {PAGE} 页: {url}")

    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        vod_list = data.get('list', [])

        if not vod_list:
            print("✅ 没有更多数据了，抓取结束。")
            break

        # 用字典来分类不同类型
        site_vod_map = {}

        # 遍历每个视频
        for vod in vod_list:
            type_name = vod.get('type_name', '未知类型')
            vod_name = vod.get('vod_name', '未知片名')
            play_data = vod.get('vod_play_url', '')
            play_items = play_data.split('#')
            site_name = vod.get('vod_play_from', '未知网站')  # 使用网站名称作为文件名

            # 将视频数据按类型分组
            if site_name not in site_vod_map:
                site_vod_map[site_name] = {}

            if type_name not in site_vod_map[site_name]:
                site_vod_map[site_name][type_name] = []

            for item in play_items:
                parts = item.split('$')
                if len(parts) == 2:
                    title, url = parts
                else:
                    title = "播放"
                    url = parts[0]
                site_vod_map[site_name][type_name].append(f"{vod_name}, {url.strip()}")

        # 为每个网站创建一个文件，并按类别保存数据
        for site_name, type_map in site_vod_map.items():
            file_name = f"{domain_name}.txt"  # 文件名使用主域名
            with open(file_name, "w", encoding="utf-8") as f:
                for type_name, vods in type_map.items():
                    f.write(f"{type_name}, #genre#\n")
                    for vod in vods:
                        f.write(f"{vod}\n")
                    f.write("\n")  # 每个类别后加一个空行
            print(f"数据已保存到 {file_name}")

        PAGE += 1
        time.sleep(1)  # 延迟1秒，防止请求过快

    except Exception as e:
        print(f"❌ 第 {PAGE} 页抓取失败: {e}")
        break

print("✅ 数据抓取并保存完毕！每个网站的数据已保存到对应的文件中。")
