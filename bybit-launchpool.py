import requests
from bs4 import BeautifulSoup
import time


def bybit_launchpool():
    # 基礎URL
    base_url = 'https://announcements.bybit.com/zh-TW/?category=latest_activities&page='

    # 設置請求頭信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
    }

    page = 1
    max_pages = 5
    launchpool_articles = {}

    while page <= max_pages:
        # 構造完整的URL
        url = base_url + str(page)

        # 發送GET請求
        response = requests.get(url, headers=headers, timeout=30)

        # 檢查響應狀態碼
        if response.status_code != 200:
            print(f"請求失敗，狀態碼: {response.status_code}")
            break

        # 解析HTML內容，使用html.parser
        soup = BeautifulSoup(response.content, 'html.parser')

        # 查找所有class為no-style的a標籤
        a_tags = soup.find_all('a', class_='no-style')

        # 如果沒有找到a標籤，說明到達最後一頁，退出循環
        if not a_tags:
            print("沒有更多內容")
            break

        # 過濾並存儲包含"Launchpool"的標題和鏈接
        for a_tag in a_tags:
            # 獲取a標籤的href屬性
            href = a_tag.get('href', '無鏈接')
            full_url = f"https://announcements.bybit.com{href}"

            # 查找a標籤中的span標籤
            span = a_tag.find('span')
            if span:
                title_text = span.get_text(strip=True)
                if "Launchpool" in title_text:
                    launchpool_articles[title_text] = full_url
                #launchpool_articles[title_text] = full_url

        # 下一頁
        page += 1

    return launchpool_articles


def send_to_discord(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("消息已成功發送到Discord")
    else:
        print(f"發送到Discord失敗，狀態碼: {response.status_code}")


if __name__ == "__main__":
    # Discord Webhook URL
    webhook_url = "Discord Webhook URL"
    last_launchpool_articles = bybit_launchpool()

    while True:
        time.sleep(1200)  # 每隔60秒抓取一次
        now_launchpool_articles = bybit_launchpool()

        # 比較兩個字典，找出新增的文章
        new_articles = {k: v for k, v in now_launchpool_articles.items() if k not in last_launchpool_articles}

        # 如果有新的文章，發送到Discord
        for title, url in new_articles.items():
            #message = f"新的Launchpool文章:\n標題: {title}\n鏈接: {url}"
            message = f"[📢]({url})  {title}\n[⛓️點擊查看]{url}"
            send_to_discord(webhook_url, message)

        # 更新last_launchpool_articles
        last_launchpool_articles = now_launchpool_articles
