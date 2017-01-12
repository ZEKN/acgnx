import requests
import re
import json
from lxml import html
from itertools import chain
from redis_and_file import rds


class Crawl_info:
    def __init__(self,session,cate,url):
        # session 是外部传入的 requests.Session() 可以复用Session和cookies
        # cate 是目录，url 是某页面的地址
        self.s = session
        self.cate = cate
        self.murl = "https://share.acgnx.se/"
        self.url = self.murl+url
        # flag 控制填充失败次数
        self.flag = 0
        self.get_info()

    # 如果 cookies里 SafeTechSYS_sign_javascript 失效，则从新填充
    def get_new_sj(self,text):
        safe_js = re.search(r'[\w]{32}',text).group()
        self.s.cookies["SafeTechSYS_sign_javascript"] = safe_js
        self.flag += 1
        self.get_info()

    def get_info(self):
        try:
            info_r = self.s.get(self.url,timeout=6)
        except Exception as e:
            print(e)
            return

        if info_r.status_code == 200:
            info_tree = html.fromstring(info_r.text)
            if len(info_r.text) < 2000:
                if self.flag < 30:
                    self.get_new_sj(info_r.text)
                else:
                    return
            else:
                with rds.pipeline() as pipe:
                    for tr in chain(info_tree.xpath('.//tr[@class="alt1"]')[:-1],info_tree.xpath('.//tr[@class="alt2"]')):
                        tds = tr.xpath('./td')
                        self.relase_time = ''.join(tds[0].xpath('.//@title'))
                        self.category = ''.join(tds[1].xpath('.//text()'))
                        self.name = ''.join(tds[2].xpath('.//text()')).strip()
                        self.detail_url = self.murl+''.join(tds[2].xpath('.//a/@href'))
                        self.size = ''.join(tds[3].xpath('./text()'))
                        self.download_nums = ''.join(tds[5].xpath('./span/text()'))
                        self.complete_nums = ''.join(tds[6].xpath('./span/text()'))
                        info_item ={
                            "relase_time":self.relase_time,
                            "category":self.category,
                            "name":self.name,
                            "detail_url":self.detail_url,
                            "size":self.size,
                            "download_nums":self.download_nums,
                            "complete_nums":self.complete_nums,
                        }
                        info_string = json.dumps(info_item,ensure_ascii=False)
                        pipe.sadd(self.cate,info_string)
                    pipe.execute()
                print('crawled Category:{self.cate}; Url:{self.url}'.format(self=self))




# Crawl_info('manga',"sort-2-10.html")
