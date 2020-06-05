# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class SQLlitePipeline(object):
    def open_spider(self, spider):
        self.connection =  sqlite3.connect('Red Flags')
        self.c = self.connection.cursor()
        self.c.execute('''
                    CREATE TABLE Red_Flags(
                    title TEXT,
                    link TEXT,
                    price TEXT,
                    retailer TEXT,
                    expiry TEXT,
                    savings TEXT,
                    )
                    ''')
        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO Red_Flags (title, link, price, retailer, expiry, savings) VALUES(?,?,?,?,?,?)
            ''', (
                   item.get('title'),
                   item.get('link'),
                   item.get('price'),
                   item.get('retailer'),
                   item.get('expiry'),
                   item.get('savings'),

        )

        )
        return item
