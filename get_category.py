import requests
from lxml import html


def category():
    main_url = "https://share.acgnx.se/"
    try:
        r = requests.get(main_url)
    except Exception as e:
        print(e)
    if r.status_code == 200:
        tree = html.fromstring(r.text)
        cate_ip = tree.xpath('//div[@class="nav mos"]/ul/li/a/@href')[1:-1]
        # 为了方便存入redis
        cate_id = ['new','anime','manga','music','teleplay','raw','game','tokusatsu','other']
        cate_list = dict(zip(cate_id,cate_ip))
        return cate_list
