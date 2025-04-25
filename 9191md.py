import os
import json
import requests

def scrape_videos(url, headers=None):
    """抓取视频数据并返回"""
    response = requests.get(url, headers=headers)
    data = response.json()  # 解析返回的JSON数据
    return data

def process_vod_data(data):
    """处理视频数据并生成结果"""
    videos = []

    for item in data.get('list', []):
        # 获取视频名称
        vod_name = item.get("vod_name", "").strip()
        vod_play_url = item.get("vod_play_url", "")
        
        # 处理播放地址（将“第01集”部分保留，添加播放地址）
        if "第" in vod_name and "集" in vod_name:
            video_line = f"{vod_name} {vod_play_url}"
        else:
            video_line = f"{vod_name} {vod_play_url}"
        
        videos.append(video_line)

    return videos

def save_to_file(videos, domain_name):
    """保存结果到文本文件"""
    filename = f"{domain_name}.txt"  # 使用主域名命名文件
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{domain_name}, #genre#\n")  # 写入文件头部
        for video in videos:
            f.write(f"{video}\n")  # 写入每个视频的名称和播放地址

def main():
    sources = [
        {"url": "http://www.9191md.me/api.php/provide/vod/", "domain": "www.9191md.me"}
        # 你可以在这里添加其他的源
    ]

    for source in sources:
        url = source["url"]
        domain_name = source["domain"]

        print(f"开始抓取 {domain_name} 数据...")

        # 发起请求并处理数据
        data = scrape_videos(url)
        videos = process_vod_data(data)

        # 将数据保存到文件
        save_to_file(videos, domain_name)

        print(f"{domain_name} 数据已保存到 {domain_name}.txt")

if __name__ == "__main__":
    main()
