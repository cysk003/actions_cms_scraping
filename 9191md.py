import requests
import json

# 设置采集源 URL
url = "http://www.9191md.me/api.php/provide/vod/"

def fetch_data(page=1):
    """ 获取指定页的数据 """
    params = {
        "ac": "videolist",  # 数据请求的接口类型
        "pg": page,         # 页码
        "limit": 30          # 每页的条目数
    }

    print(f"正在请求第 {page} 页...")
    try:
        response = requests.get(url, params=params)
        data = response.json()

        # 检查响应是否成功
        if response.status_code == 200 and data.get("code") == 1:
            print(f"成功获取第 {page} 页的数据")
            return data['list'], data['pagecount']  # 返回数据和总页数
        else:
            print(f"第 {page} 页请求失败，状态码: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"请求发生异常: {e}")
        return None, None

def save_data(source_name, data):
    """ 保存抓取到的数据到文件 """
    print(f"正在保存 {source_name} 数据...")
    file_name = f"{source_name}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        for entry in data:
            vod_name = entry['vod_name']
            play_url = entry['vod_play_url']
            
            # 处理包含 "第01集" 等标识符的情况
            if '第' in vod_name:
                vod_name = f"{vod_name} {play_url.split('$')[1]}"  # 拼接标题和播放地址

            # 保存文件
            f.write(f"{vod_name}\n")
    print(f"数据已保存到 {file_name}")

def main():
    print("开始抓取 www.9191md.me 数据...")
    all_data = []
    
    # 获取第1页数据并获取总页数
    page_data, total_pages = fetch_data(1)
    if not page_data:
        print("无法获取数据，程序结束。")
        return

    print(f"总页数: {total_pages}")

    # 遍历所有页并抓取数据
    for page in range(1, total_pages + 1):
        print(f"正在抓取第 {page} 页...")
        page_data, _ = fetch_data(page)
        if page_data:
            all_data.extend(page_data)  # 将数据添加到总数据列表
        else:
            print(f"第 {page} 页没有数据，跳过。")
    
    # 保存所有抓取到的数据
    if all_data:
        save_data("www.9191md.me", all_data)
    else:
        print("没有抓取到有效数据。")

if __name__ == "__main__":
    main()
