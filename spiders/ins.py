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
from urllib import parse
import traceback

sleep_secs = 2

class InstagramSpider(CrawlSpider):
    name = "Instagram"
    allowed_domains = ["instagram.com"]
    start_urls = [
        "https://www.instagram.com/hxmfamily/",
        "https://www.instagram.com/caitylotz/"
    ]

    def parse(self, response):
        """
        解析用户主页内容
        :param response:
        :return:
        """
        json_body = response.selector.xpath('//script[contains(., "window._sharedData")]/text()').extract()[0].replace("window._sharedData = ", "")[:-1]
        root = json.loads(json_body)
        user = root['entry_data']['ProfilePage'][0]['graphql']['user']
        username = user['username']
        user_id = user['id']
        for edge in user['edge_owner_to_timeline_media']['edges']:
            node = edge['node']

            display_url = node['display_url']
            is_video = node['is_video']
            taken_at = node['taken_at_timestamp']
            dim = node['dimensions']
            ch = dim['height']
            cw = dim['width']
            id = node['id']
            text = ""
            try:
                texts = [edge['node']['text'] for edge in node["edge_media_to_caption"]["edges"]]
                text = "\n".join(texts)
            except:
                pass
            item = {
                'user_name': username,
                'user_id': user_id,
                'media_id': id,
                'media_url': display_url,
                'is_video': is_video,
                'taken_at': taken_at,
                'ch': ch,
                'cw': cw,
                'text': text
            }
            yield item

            if is_video:
                url = "https://www.instagram.com/p/%s/?__a=1" % node['shortcode']
                yield scrapy.Request(url, callback=self.parse_video, meta = {
                    "user_name": username,
                    "user_id": user_id
                })
        #
        if user['edge_owner_to_timeline_media']['page_info']['has_next_page']:
            #query_hash = "472f257a40c653c64c666ce877d59d2b"
            end_cursor = user['edge_owner_to_timeline_media']['page_info']['end_cursor']
            # params = {
            #     'query_hash': query_hash,
            #     'variables': '{"id":"%s","first":12,"after":"%s"}' % (user_id, end_cursor)
            # }
            # url = "https://www.instagram.com/graphql/query/?" + parse.urlencode(params)
            # yield scrapy.Request(url, callback=self.parse_next, meta = {'id': user_id, 'username': username})
            time.sleep(sleep_secs)
            yield self.start_next_page(user_id, end_cursor, meta = {'id': user_id, 'username': username})

    def start_next_page(self, user_id, end_cursor, meta):
        query_hash = "472f257a40c653c64c666ce877d59d2b"
        params = {
            'query_hash': query_hash,
            'variables': '{"id":"%s","first":12,"after":"%s"}' % (user_id, end_cursor)
        }
        url = "https://www.instagram.com/graphql/query/?" + parse.urlencode(params)
        return scrapy.Request(url, callback=self.parse_next, meta = meta)

    def parse_next(self, response):
        data = json.loads(response.text)
        user_id = response.meta['id']
        username = response.meta['username']
        timeline_media = data['data']['user']['edge_owner_to_timeline_media']
        for edge in timeline_media['edges']:
            node = edge['node']
            display_url = node['display_url']
            is_video = node['is_video']
            taken_at = node['taken_at_timestamp']
            dim = node['dimensions']
            ch = dim['height']
            cw = dim['width']
            id = node['id']
            try:
                texts = [edge['node']['text'] for edge in node["edge_media_to_caption"]["edges"]]
                text = "\n".join(texts)
            except:
                pass
            item = {
                'user_name': username,
                'user_id': user_id,
                'media_id': id,
                'media_url': display_url,
                'is_video': is_video,
                'taken_at': taken_at,
                'ch': ch,
                'cw': cw,
                'text': text
            }
            yield item
            if is_video:
                url = "https://www.instagram.com/p/%s/?__a=1" % node['shortcode']
                yield scrapy.Request(url, callback=self.parse_video, meta = {
                    "user_name": username,
                    "user_id": user_id
                })


        has_next_page = timeline_media['page_info']['has_next_page']
        if has_next_page:
            end_cursor = timeline_media['page_info']['end_cursor']
            time.sleep(sleep_secs)
            yield self.start_next_page(user_id, end_cursor, response.meta)

    def parse_video(self, response):
        """
        解析视频信息
        :param response:
        :return:
        """
        try:
            data = json.loads(response.text)
            media = data['graphql']['shortcode_media']
            yield {
                "user_name": response.meta["user_name"],
                "user_id": response.meta["user_id"],
                'media_id': media['id'],
                'shortcode': media['shortcode'],
                'media_url': media['video_url'],
                "is_video": True
            }
        except:
            traceback.print_exc()
