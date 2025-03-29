import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]


# parse function acts as the brain on which the spider operates

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:

            yield{ # this just extract the name ,price and url from the first page
                'name' : book.css('h3 a::text').get() ,
                'price' : book.css('.product_price .price_color::text').get() ,
                'image_url' : book.css('h3 a').attrib['href'],
            }
        
        next_page = response.css('li.next a').attrib['href']  # next page url dinxa

        if next_page is not None:

            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page 
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page 

            yield response.follow(next_page_url, callback= self.parse) # this will call the parse function again on the next page
 