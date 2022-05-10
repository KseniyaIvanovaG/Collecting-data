import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    base_url = 'https://www.labirint.ru'
    start_urls = ['https://www.labirint.ru/search/%D0%B4%D0%B5%D1%82%D1%81%D0%BA%D0%B8%D0%B5/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        name = response.css('h1::text').get()
        authors = response.xpath('//div[@class="authors"]/a/text()').getall()
        price = response.xpath('//span[@class="buying-priceold-val-number"]//text()').getall()
        discount_price = response.xpath('//span[@class="buying-pricenew-val-number"]//text()').getall()
        rate = response.xpath('//div[@id="rate"]//text()').getall()
        yield BookparserItem(url=url, name=name, authors=authors, price=price, discount_price=discount_price, rate=rate  )
