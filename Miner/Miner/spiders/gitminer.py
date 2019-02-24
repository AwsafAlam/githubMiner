import scrapy

class GitMiner(scrapy.Spider):
    name = 'gitminer'
    # start_urls = ['https://github.com/iluwatar/java-design-patterns']

    # def parse(self, response):
    #     for title in response.css('.post-header>h2'):
    #         yield {'title': title.css('a ::text').get()}

    #     for next_page in response.css('div.prev-post > a'):
    #         yield response.follow(next_page, self.parse)

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }

    def start_requests(self):
        # urls = ['https://github.com/iluwatar/java-design-patterns']
        urls = [
            'https://github.com/iluwatar/java-design-patterns/blob/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/AbstractDocument.java',
            'https://raw.githubusercontent.com/iluwatar/java-design-patterns/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/AbstractDocument.java',
            'https://raw.githubusercontent.com/iluwatar/java-design-patterns/master/abstract-document/src/main/java/com/iluwatar/abstractdocument/App.java',
        ]
        ## Need to extract raw contant and fix referencing
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = '%s' % page
        # filename = 'gitfile.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)