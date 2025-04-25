import json
import requests
import os
from urllib.parse import urlparse

def get_domain(url):
    """提取主域名用于文件名"""
    return urlparse(url).netloc

def fetch_all_pages(source_url, base_params):
    """抓取所有分页数据"""
    page = 1
    result = {}
    while True:
        params = base_params.copy()
        params["pg"] = page
        response = requests.get(source_url, params=params, timeout=10)
        data = response.json()

        if data["code"] != 1 or "list" not in data:
            break

        for item in data["list"]:
            type_name = item.get("type_name", "未知分类")
            vod_name = item.get("vod_name", "无名")
            play_urls = item.get("vod_play_url", "").split("#")
            for play in play_urls:
                if "$" in play:
                    name, url = play.split("$", 1)
                else:
                    name, url = vod_name, play
                result.setdefault(type_name, []).append(f"{name}, {url}")

        if page >= data.get("pagecount", 1):
            break
        page += 1

    return result

def save_to_file(data_by_type, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for type_name, items in data_by_type.items():
            f.write(f"{type_name}, #genre#\n")
            for line in items:
                f.write(f"{line}\n")
            f.write("\n")

def main():
    with open("sources_config.json", "r", encoding="utf-8") as f:
        sources = json.load(f)["sources"]

    for source in sources:
        url = source["url"]
        base_params = source.get("params", {})
        print(f"开始采集：{url}")

        grouped_data = fetch_all_pages(url, base_params)

        domain = get_domain(url)
        filename = f"{domain}.txt"
        save_to_file(grouped_data, filename)
        print(f"保存完成：{filename}")

if __name__ == "__main__":
    main()
