from lxml import html
import requests
from pprint import pprint

# сбор новостей с сайта Lenta.ru

url = 'https://www.lenta.ru'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
top_news = dom.xpath("//div[@class='topnews__first-topic']")
news = []
for item in top_news:
    news_info = {}
    name = item.xpath(".//h3/text()")[0]
    link = item.xpath(".//a/@href")
    time = item.xpath(".//time/text()")

    news_info['name'] = name
    news_info['link'] = link
    news_info['time'] = time
    news_info['source'] = 'Lenta.ru'

    news.append(news_info)

mini_news = dom.xpath("//a[contains(@class, 'card-mini _topnews')]")

for item in mini_news:
    news_info = {}
    name = item.xpath(".//span/text()")[0]
    link = item.xpath(".//a[@class='card-mini _topnews']/@href")
    time = item.xpath(".//time/text()")

    news_info['name'] = name
    news_info['link'] = link
    news_info['time'] = time
    news_info['source'] = 'Lenta.ru'

    news.append(news_info)

pprint(news)