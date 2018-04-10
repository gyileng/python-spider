# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class XiaoruiPipeline(object):
    def process_item(self, item, spider):
        # 文件名为子链接url中间部分，并将 / 替换为 _，保存为 .txt格式
        filename = item['head']
        filename += ".html"

        fp = open('Data/' + item['parentTitle'] + '/' + filename, 'w')
        fp.write(item['content'])
        fp.close()
        return item
