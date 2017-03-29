import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
from scrapy.utils.project import get_project_settings


class ImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['image_urls']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        os.rename((self.IMAGES_STORE+"/" + image_paths[0]), self.IMAGES_STORE+"/" + item['name']+".jpg")

        item['image_paths'] = self.IMAGES_STORE+"/" + item['name']+".jpg"
        return item