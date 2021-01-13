import re
class PropertiesPipeline(object):
    def process_item(self, item, spider):
        #item["category"] = item["category"][-1].strip().title()
        #item["title"] = item["title"][-1].strip().title()
        #item["article"] = re.sub(r"[A-Za-z0-9]{12}", "",item["article"])
        #item["price_current"] = re.sub(r'[\s,.0-9]+', "", item["price"]).strip().replace(' ', '')
    	#item["first_price"] = re.sub(r'[\s,.0-9]+', "", item["price"]).strip().replace(' ', '')
        #item["image_url"] = item["image_url"][-1].urljoin(i)
        return item