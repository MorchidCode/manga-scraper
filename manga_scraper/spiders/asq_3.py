import scrapy
from scrapy.crawler import CrawlerProcess
import os
import requests

class Asq3Spider(scrapy.Spider):
    name = "asq_3"
    allowed_domains = ["3asq.org"]
    start_urls = ["https://3asq.org/manga/one-piece/319/"]

    def parse(self, response):
        directory_name = "one-piece-manga"
        if not os.path.isdir(directory_name):
            os.mkdir(directory_name)

        chapter_title = response.css("h1#chapter-heading::text").get().replace(" - ", "-").replace(" ", "-")
        image_urls = { image.css('::attr(id)').get() + ".png": image.css('::attr(src)').get().strip() for image in response.css("img.wp-manga-chapter-img")}

        chapter_folder = os.path.join(directory_name, chapter_title)
        os.makedirs(chapter_folder)

        for filename, url in image_urls.items():
            re_response = requests.get(url)
            if re_response.status_code == 200:
                with open(os.path.join(chapter_folder, filename), 'wb') as f:
                    f.write(re_response.content)
    
        next_page = response.css("a.next_page::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

process = CrawlerProcess()
process.crawl(Asq3Spider)
process.start()