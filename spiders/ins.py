# -*- coding: utf-8 -*-

# define the InstagramSpider in details

import scrapy
import json
import sys
sys.path.append("../../")
from Instagram.items import InstagramItem
from scrapy.spiders import CrawlSpider,Rule
import re
import time

class InstagramSpider(CrawlSpider):
    #define the name of spider
    #define the domain of spider
    #define the urls
    name = "Instagram"
    allowed_domains = ["instagram.com"]
    start_urls = [
        "https://www.instagram.com/hxmfamily/",
        "https://www.instagram.com/caitylotz/"
                    #"https://www.instagram.com/nike",
                  #"https://www.instagram.com/adidas",
                  #"https://www.instagram.com/olympics/",
                  #"https://www.instagram.com/teamcanada/",
                  #"https://www.instagram.com/google",
                  #"https://www.instagram.com/animal.co",
                  #"https://www.instagram.com/car",
                  #"https://www.instagram.com/flowerschannel",
                  #"https://www.instagram.com/flowerschannel_",
                  #"https://www.instagram.com/flower.channel/",
                  #"https://www.instagram.com/theflowerchannel/",
                  #"https://www.instagram.com/the_loft_flowers/",
                  #"https://www.instagram.com/amaryllis_flowers/",
                  #"https://www.instagram.com/sneakernews",
                  #"https://www.instagram.com/boeing_747_pics/",
                  #"https://www.instagram.com/boeing/",
                  #"https://www.instagram.com/insta_dog/",
                  #"https://www.instagram.com/dogs/",
                  #"https://www.instagram.com/dogs_of_world_/",
                  #"https://www.instagram.com/dogs.lovers/",
                  #"https://www.instagram.com/lions/",
                  #"https://www.instagram.com/bh_phones7/",
                  #"https://www.instagram.com/windows/",
                  #"https://www.instagram.com/gaming_laptop/",
                  #"https://www.instagram.com/alienware/",
                  #"https://www.instagram.com/airbus/",
                  #"https://www.instagram.com/airbus_a380_lovers/",
                  #"https://www.instagram.com/airbus_a380_800/",
                  #"https://www.instagram.com/airbusa350xwb/",
                  #"https://www.instagram.com/airbuslovers/",
                  #"https://www.instagram.com/airbus_fanclub/",
                  #"https://www.instagram.com/a350_production/",
                  #"https://www.instagram.com/747.boeing/",
                  #"https://www.instagram.com/boeinglovers/",
                  #"https://www.instagram.com/airplaneslovers/",
                  #"https://www.instagram.com/airplane2017/",
                  #"https://www.instagram.com/airplanes.us/",
                  #"https://www.instagram.com/deskspaces/",
                  #"https://www.instagram.com/laptop.desktop.gadjet.murah/",
                  #"https://www.instagram.com/isetups/",
                  #"https://www.instagram.com/gaminglaptop/",
                  #"https://www.instagram.com/laptop_second_murah/",
                  #"https://www.instagram.com/ultrawidedesksetups/",
                  #"https://www.instagram.com/desksetuptour/",
                  #"https://www.instagram.com/desksetups_2016/",
                  #"https://www.instagram.com/aestheticsetups/",
                  #"https://www.instagram.com/minimalsetups/",
                  #"https://www.instagram.com/samsung_id/",
                  #"https://www.instagram.com/samsungmobile/",
                  #"https://www.instagram.com/dailywatch/",
                  #"https://www.instagram.com/watch/",
                  #"https://www.instagram.com/rolex.watches/",
                  #"https://www.instagram.com/mercedesbenz/",
                  #"https://www.instagram.com/africa.lions/",
                  #"https://www.instagram.com/africa_lions/",
                  #"https://www.instagram.com/lions.africa/",
                  #"https://www.instagram.com/wild_lions_/",
                  #"https://www.instagram.com/lionswildusa/",
                  #"https://www.instagram.com/statebicycleco/",
                  #"https://www.instagram.com/thrill_bicycle/",
                  #"https://www.instagram.com/trekbikes/",
                  #"https://www.instagram.com/discoverlions/",
                  #"https://www.instagram.com/lobbyforlions/",
                  #"https://www.instagram.com/thelionworld/",
                  #"https://www.instagram.com/savingthelion/",
                  #"https://www.instagram.com/thelionstation/",
                  #"https://www.instagram.com/sick_camera/",
                  #"https://www.instagram.com/shahalamcamera/",
                  #"https://www.instagram.com/dslr.shop/",
                  #"https://www.instagram.com/store.camera/",
                  #"https://www.instagram.com/camera_store_/",
                  #"https://www.instagram.com/camerashop_th/",
                  #"https://www.instagram.com/camera_shop78/",
                  #"https://www.instagram.com/camera_shop/",
                  #"https://www.instagram.com/camera_shop4you/",
                       ]

    #rules = [
    #    Rule(sle(allow=('?max_id\.php')), callback='parse'),
    #]
    def parse(self, response):
        # We get the json containing the photos's path
        items = []
        item = InstagramItem()
        js = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()
        js = js[0].replace("window._sharedData = ", "")
        jscleaned = js[:-1]
        ts = str(int(time.time()))
        data = json.loads(jscleaned)
        open(ts + ".json", "w").write(json.dumps(data))
        user = data['entry_data']['ProfilePage'][0]['graphql']['user']
        user_name = user['username']
        for edge in user['edge_owner_to_timeline_media']['edges']:
            # print(edge.keys())
            node = edge['node']
            display_url = node['display_url']
            is_video = node['is_video']
            taken_at = node['taken_at_timestamp']
            dim = node['dimensions']
            ch = dim['height']
            cw = dim['width']
            id = node['id']
            item = {
                'username': user_name,
                'image_url': display_url,
                'is_video': is_video,
                'taken_at': taken_at,
                'ch': ch,
                'cw': cw,
                'id': id
            }
            yield item
        has_next_page = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
        #
        if has_next_page:
            last_id = user['edge_owner_to_timeline_media']['edges'][-1]['node']['id']
            url = "https://www.instagram.com/"+ user_name + "?max_id=" + last_id
            yield scrapy.Request(url, callback=self.parse)
