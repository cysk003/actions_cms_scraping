import requests
import json

# 获取视频数据
def fetch_video_data(api_url, page):
    params = {
        'ac': 'videolist',
        'pg': page,
        'limit': 30  # 每页数据
    }
    response = requests.get(api_url, params=params)
    data = response.json()
    return data

# 保存数据到文件
def save_data(file_name, all_data):
    with open(file_name, "w", encoding="utf-8") as f:
        for type_name, videos in all_data.items():
            f.write(f"{type_name}, #genre#\n")  # 写入分类
            for vod_name, play_url in videos:
                f.write(f"{vod_name} {play_url}\n")  # 写入视频名称和播放地址

# 主函数
def main():
    api_url = 'http://www.9191md.me/api.php/provide/vod/'
    all_data = {}
    
    # 假设每个源最多有 670 页
    total_pages = 670
    print(f"开始抓取 {api_url} 数据...")
    
    for page in range(1, total_pages + 1):
        print(f"正在抓取第 {page} 页...")
        data = fetch_video_data(api_url, page)
        
        if data['code'] == 1:
            for item in data['list']:
                type_name = item['type_name']  # 获取分类
                vod_name = item['vod_name']  # 获取视频名称
                play_url = item['vod_play_url'].split('$')[1]  # 获取播放地址

                # 将数据按分类整理
                if type_name not in all_data:
                    all_data[type_name] = []
                all_data[type_name].append((vod_name, play_url))
        
    # 保存数据到文件
    save_data("www.9191md.me.txt", all_data)
    print(f"{api_url} 数据已保存到 www.9191md.me.txt")

if __name__ == "__main__":
    main()
