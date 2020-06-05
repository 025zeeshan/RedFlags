import scrapy
from datetime import datetime, timedelta

from dateutil import parser

current_time = datetime.now()




class RedFlags(scrapy.Spider):

    name ='redflags'
    start_urls= ['https://forums.redflagdeals.com/hot-deals-f9/?sk=tt&rfd_sk=tt&sd=d']


    def parse(self, response):
        for each_item in response.xpath("//div[@class='row-item']"):
            link = each_item.xpath(".//a[@class='topic_title_link']/@href").get()
            replies_count = each_item.xpath(".//div[@class='posts']/text()").extract_first()
            upvotes_count = each_item.xpath(".//dd[contains(@class, 'total_count')]/text()").extract_first()
            post_time = each_item.xpath(".//span[@class='first-post-time']/text()").extract_first()
            retailer = each_item.xpath(".//a[@class='topictitle_retailer']/text()").extract_first()
            if replies_count and upvotes_count and post_time and retailer:
                if abs(current_time - parser.parse(post_time)) < timedelta(hours=25):
                     if int(replies_count) >= 3 or int(upvotes_count) >=7 or 'Amazon' in retailer:
                         yield response.follow(link, callback = self.nextpage)

        next_page =  response.xpath("//a[contains(@class,'pagination_next')]/@href").get()
        if next_page is not None:
              yield response.follow(next_page, callback = self.parse)



    def nextpage(self, response):

       for item in response.xpath("//dl[@class='post_offer_fields']"):
              link = item.xpath(".//a/@href").get()
              title = response.xpath(".//h1[@class='thread_title']/text()").extract()
              price  = item.xpath(".//dt[contains(text(), 'Price:')]/following-sibling::dd[1]/text()").extract()
              retailer = item.xpath(".//dt[contains(text(), 'Retailer:')]/following-sibling::dd[1]/text()").extract()
              expiry = item.xpath(".//dt[contains(text(), 'Expiry:')]/following-sibling::dd[1]/text()").extract()
              savings = item.xpath(".//dt[contains(text(), 'Savings:')]/following-sibling::dd[1]/text()").extract()

              yield {
            'title':title,
           'link': link,
           'price': price,
           'retailer':retailer,
           'expiry': expiry,
           'savings':savings,
       }


