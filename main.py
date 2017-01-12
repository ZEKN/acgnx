import requests
import gevent
from gevent import monkey;monkey.patch_socket()
from get_category import category
from redis_and_file import write_to_file,rds
from crawl_info import Crawl_info
from random_user_agents import random_user_agent


def start_crawl(cate):
    s = requests.Session()
    while True:
        url = rds.rpop('list_'+cate)
        if url:
            Crawl_info(s,cate,url.decode('utf-8'))
        else:
            break

g_jobs = []
def mult_gevent(cate,page_nums,wtf=False):
    cate_list = category()
    if cate in cate_list:
        url_split = cate_list[cate].split('-')
        with rds.pipeline() as pipe:
            for p in range(1,page_nums+1):
                url_split[-1]=str(p)+".html"
                url = '-'.join(url_split)
                pipe.lpush('list_'+cate,url)
            pipe.execute()
        for i in range(5):
            g_jobs.append(gevent.spawn(start_crawl,cate=cate))
        gevent.joinall(g_jobs)
    if wtf == True:
        write_to_file(cate)

if __name__ == '__main__':
    # 100 页，4000条数据，花费 109 s
    mult_gevent('music',100,wtf=True)
