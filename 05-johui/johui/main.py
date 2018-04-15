# -*- coding:utf-8 -*-
from scrapy import cmdline

name = 'zhiyouwang'
cmd = 'scrapy crawl {}'.format(name)
cmdline.execute(cmd.split())