#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-26 22:52:07
# Project: reeoo_detail

from pyspider.libs.base_handler import *
from pyspider.database.mysql.mysqldb import SQL
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.reeoo.com', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div[class="thumb"]').items():
            detail_url = each('a').attr.href
            self.crawl(detail_url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        header = response.doc('body > article > section > header')
        title = header('h1').text()
        tags = []
        for each in header.items('a'):
            tags.append(each.text())
        tags = ','.join(tags)
        content = response.doc('div[id="post_content"]')
        description = content('blockquote > p').text()
        website_url = content('a').attr.href

        image_url_list = []
        for each in content.items('img[data-src]'):
            image_url_list.append(each.attr('data-src'))
        image_url_list = ','.join(image_url_list)
        return {
            "title": title,
            "tags": tags,
            "description": description,
            "image_url_list": image_url_list,
            "website_url": website_url,
        }

    def on_result(self, result):
        if not result:
            return
        db=SQL()
        result['insert_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        db.insert('reeoo_detail',**result)


