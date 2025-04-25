import json
import requests
from urllib.parse import urlparse

def get_domain(url):
    return urlparse(url).netloc

def fetch_all_pages(source_url, base_params):
    """抓取所有分页数据并记录日志"""
    page = 1
    result = {}
    total_pages = None

    while True:
        params = base_params.copy()
        params["pg"] = page
        try:
            response = requests.get(source_url, params=params, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"[错误] 第 {page} 页请求失败：{e}")
            break

        if data.get("code") != 1 or "list" not in data:
            print(f"[警告] 第 {page} 页数据无效，停止采集")
            break

        if total_pages is None:
            total_pages = data.get("pagecount", 1)
            print(f"  ↳ 总页数：{total_pages}")

        print(f"    → 正在采集第 {page}/{total_pages} 页，共 {len(data['list'])} 项")

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

        if page >= total_pages:
            break
        page += 1

    # 日志输出每个分类多少条数据
    print("  ↳ 分类统计：")
    for type_name, items in result.items():
        print(f"    • {type_name}: {len(items)} 条")

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
        print(f"\n开始采集源：{url}")
        grouped_data = fetch_all_pages(url, base_params)
        domain = get_domain(url)
        filename = f"{domain}.txt"
        save_to_file(grouped_data, filename)
        print(f"完成保存文件：{filename}")

if __name__ == "__main__":
    main()
