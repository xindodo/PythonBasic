import scrapy
from ftx_spider.items import FtxSpiderItem

class roompriceSpider(scrapy.Spider):
    name = 'roomprice'

    start_urls = ['http://wuhan.esf.fang.com/house-a013126/i3']

    def parse(self, response):
        room_domain = FtxSpiderItem()
        rooms = response.xpath('//dl[@class="clearfix"]')
        for room in rooms:
            title_list = room.xpath('./dd//span[@class="tit_shop"]/text()')
            if len(title_list):
                title = title_list.extract_first().replace(' ', '').replace('\r\n', '')
                room_domain['title'] = title

            info_list = room.xpath('./dd//p[@class="tel_shop"]/text()').extract()
            if len(info_list) > 4:
                huxing = info_list[0].replace(' ', '').replace('\r\n', '')  # 户型
                size = info_list[1].replace(' ', '').replace('\r\n', '').replace('�O', '')  # 面积
                floor = info_list[2].replace(' ', '').replace('\r\n', '')  # 楼层
                fangxiang = info_list[3].replace(' ', '').replace('\r\n', '')  # 方向
                year = info_list[4].replace(' ', '').replace('\r\n', '')  # 年代

                room_domain['huxing'] = huxing
                room_domain['size'] = size
                room_domain['floor'] = floor
                room_domain['fangxiang'] = fangxiang
                room_domain['year'] = year

            shop_community_list = room.xpath('./dd//p[@class="add_shop"]/a/@title').extract()
            if shop_community_list:
                shop_community = shop_community_list[0]
                room_domain['shop_community'] = shop_community

            address_list = room.xpath('./dd//p[@class="add_shop"]/span/text()').extract()
            if address_list:
                address = address_list[0]
                room_domain['address'] = address

            total_price_list = room.xpath('./dd[@class="price_right"]/span/b/text()').extract()
            if total_price_list:
                total_price = total_price_list[0]
                room_domain['total_price'] = total_price

            price_list = room.xpath('./dd[@class="price_right"]/span/text()').extract()
            if price_list:
                price = price_list[1].replace('�O', 'm2')
                room_domain['price'] = price

            yield room_domain
        total_pages = response.xpath('//div[@class="page_al"]//p/text()').extract()[-1].replace('共', '').replace('页', '')
        print('总页数', total_pages)
        current_page = response.xpath('//div[@class="page_al"]//span[@class="on"]/text()').extract_first().replace('\r\n', '').replace(' ', '')
        print('当前页:', current_page)

        if int(current_page) < int(total_pages):
            next_url = 'http://wuhan.esf.fang.com/house-a013126/i3' + str(int(current_page)+1)
            print('下一页:', next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

