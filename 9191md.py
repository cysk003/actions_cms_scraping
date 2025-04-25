import requests
import json
import os

# 配置源，包含多个网站的API地址
sources = [
    {"name": "www.9191md.me", "url": "http://www.9191md.me/api.php/provide/vod/"},
    {"name": "cj.lziapi.com", "url": "http://cj.lziapi.com/api.php/provide/vod/"},
    # 添加更多源
]

def save_data(source_name, all_data):
    """保存数据到文件"""
    file_name = f"{source_name}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for category, data in all_data.items():
            # 类别名称
            f.write(f"{category}, #genre#\n")
            for line in data:
                vod_name, play_url = line
                # 确保名称与播放地址之间有一个逗号和空格
                f.write(f"{vod_name}, {play_url}\n")

def fetch_data_from_source(source_name, api_url):
    """从指定的API源抓取数据"""
    all_data = {}
    page = 1

    while True:
        # 请求参数
        params = {
            "ac": "videolist",  # 请求的视频列表
            "pg": page,         # 当前页数
            "limit": "30",      # 每页数量
        }

        print(f"正在抓取 {source_name} 第 {page} 页...")
        response = requests.get(api_url, params=params)

        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            break

        data = response.json()

        if data["code"] != 1:
            print(f"数据获取失败，错误信息：{data['msg']}")
            break

        total_pages = data["pagecount"]
        print(f"总页数：{total_pages}")

        for item in data["list"]:
            # 获取分类名称
            category = item['type_name']
            vod_name = item['vod_name']
            play_url = item['vod_play_url']

            # 处理播放地址，确保提取正确
            if '$' in play_url:
                play_url = play_url.split('$')[1]
            # 如果有标识符（如"第01集"），则拼接名称和播放地址
            if '第' in vod_name:
                vod_name = f"{vod_name} {play_url}"

            if category not in all_data:
                all_data[category] = []

            all_data[category].append((vod_name, play_url))

        page += 1

        if page > total_pages:  # 如果抓取完所有页
            break

    return all_data

def main():
    """主程序，抓取所有源的数据并保存"""
    for source in sources:
        source_name = source["name"]
        api_url = source["url"]
        print(f"开始抓取 {source_name} 数据...")
        all_data = fetch_data_from_source(source_name, api_url)
        print(f"{source_name} 数据抓取完毕，正在保存...")
        save_data(source_name, all_data)
        print(f"{source_name} 数据已保存到 {source_name}.txt\n")

if __name__ == "__main__":
    main()
