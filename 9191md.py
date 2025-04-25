import requests
from urllib.parse import urlparse
import os

def get_domain(url):
    """提取主域名作为文件名"""
    return urlparse(url).netloc

def fetch_all_pages(base_url, base_params):
    """分页抓取所有视频并按类型分类"""
    page = 1
    result = {}
    total_pages = None

    while True:
        params = base_params.copy()
        params["pg"] = page

        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"[错误] 第 {page} 页请求失败：{e}")
            break

        if data.get("code") != 1 or "list" not in data:
            print(f"[警告] 第 {page} 页返回无效数据，停止采集")
            break

        if total_pages is None:
            total_pages = data.get("pagecount", 1)
            print(f"总页数：{total_pages}")

        print(f"→ 正在采集第 {page}/{total_pages} 页，共 {len(data['list'])} 项")

        for item in data["list"]:
            type_name = item.get("type_name", "未知分类")
            vod_name = item.get("vod_name", "未命名")
            vod_play_url = item.get("vod_play_url", "")

            entries = []
            for part in vod_play_url.split("#"):
                if "$" in part:
                    name, url = part.split("$", 1)
                else:
                    name, url = vod_name, part
                entries.append(f"{name}, {url}")

            result.setdefault(type_name, []).extend(entries)

        if page >= total_pages:
            break
        page += 1

    print("分类汇总：")
    for cat, items in result.items():
        print(f"  • {cat}: {len(items)} 条")

    return result

def save_grouped_to_file(grouped_data, filename):
    """保存为文本文件，分类整理"""
    with open(filename, "w", encoding="utf-8") as f:
        for type_name, items in grouped_data.items():
            f.write(f"{type_name}, #genre#\n")
            for line in items:
                f.write(f"{line}\n")
            f.write("\n")
    print(f"已保存到文件：{filename}")

def main():
    # 🔧 你的源地址和参数配置在这里
    base_url = "http://www.9191md.me/api.php/provide/vod/"
    base_params = {
        "ac": "list",
        "type": "",  # 可指定类型 ID，不填为全部
        "pg": 1
    }

    print(f"开始采集：{base_url}")
    grouped_data = fetch_all_pages(base_url, base_params)
    domain = get_domain(base_url)
    filename = f"{domain}.txt"
    save_grouped_to_file(grouped_data, filename)

if __name__ == "__main__":
    main()
