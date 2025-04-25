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

    print(f"开始采集：{base_url}")
    
    while True:
        params = base_params.copy()
        params["pg"] = page

        try:
            print(f"→ 正在请求第 {page} 页...")
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()  # 如果请求失败，会引发异常
            data = response.json()

        except requests.exceptions.RequestException as e:
            print(f"[错误] 第 {page} 页请求失败：{e}")
            break
        except ValueError:
            print(f"[错误] 第 {page} 页返回的不是有效的 JSON 数据")
            break

        if data.get("code") != 1 or "list" not in data:
            print(f"[警告] 第 {page} 页返回无效数据，停止采集")
            break

        if total_pages is None:
            total_pages = data.get("pagecount", 1)
            print(f"总页数：{total_pages}")

        page_items = data["list"]
        print(f"→ 正在采集第 {page}/{total_pages} 页，共 {len(page_items)} 项数据")

        for item in page_items:
            type_name = item.get("type_name", "未知分类")
            vod_name = item.get("vod_name", "未命名")
            vod_play_url = item.get("vod_play_url", "")

            if vod_play_url.strip():  # 如果有播放地址
                # 分割多个播放地址
                entries = []
                for part in vod_play_url.split("$"):
                    if part.strip():
                        # 处理播放地址和"第01集"等标识符
                        if "," in part:
                            name, url = part.split(",", 1)
                            entries.append(f"{vod_name} {name.strip()}, {url.strip()}")
                        else:
                            entries.append(f"{vod_name} {part.strip()}")

                if entries:
                    result.setdefault(type_name, []).extend(entries)

        if page >= total_pages:
            break
        page += 1

    return result

def save_grouped_to_file(grouped_data, filename):
    """保存为文本文件，分类整理"""
    with open(filename, "w", encoding="utf-8") as f:
        for type_name, items in grouped_data.items():
            f.write(f"{type_name}, #genre#\n")
            for line in items:
                f.write(f"{line}\n")  # 确保引号闭合
            f.write("\n")
    print(f"✅ 已保存到文件：{filename}")

def main():
    # 修改这里为你的 CMS 播放源地址
    base_url = "http://www.9191md.me/api.php/provide/vod/"
    base_params = {
        "ac": "videolist",  # 修改为 'videolist' 以匹配你的接口
        "type": "",  # 可指定分类 ID，不填为全部
        "pg": 1
    }

    grouped_data = fetch_all_pages(base_url, base_params)
    domain = get_domain(base_url)
    filename = f"{domain}.txt"
    save_grouped_to_file(grouped_data, filename)

if __name__ == "__main__":
    main()
