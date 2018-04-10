# -*- coding:utf-8 -*-
from scrapy import cmdline

name = 'xiaorui'
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())