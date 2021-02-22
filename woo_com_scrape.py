import scrapy
import scraper_helper as sh


class WoocommerceSpider(scrapy.Spider):
    name = 'woocommerce'
    start_urls = ['https://themes.woocommerce.com/storefront/shop/']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': sh.headers()
    }

    product_selector = '.woocommerce-loop-product__link::attr(href)'

    def parse(self, response):
        for product in response.css(self.product_selector).getall():
            yield scrapy.Request(response.urljoin(product), callback=self.product_details)

        next_page = response.css('.next::attr(href)').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))

    def product_details(self, response):
        yield {
            'Title': response.css('.product_title::text').get(),
            'Amount': response.css('.entry-summary .amount::text').get(),
            'SKU': response.css('.sku::text').get(),
            'PostedIn': response.css('.posted_in::text').get(),
            'Tags': ', '.join(response.css('.tagged_as::text').getall()),
            'Weight': response.css('.product_weight::text').get(),
            'Dimensions': response.css('.product_dimensions::text').get(),
        }
