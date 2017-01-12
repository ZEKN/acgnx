# acgnx
### 反爬
+ acgnx除了首页，访问其他页面时，会先得到一段Js代码，里面有 cookies 里的 SafeTechSYS_sign_javascript 字段值，这个字段有一定的失效时间，而且和其他两个 cookies 字段匹配，然后Js会重定向到原url并验证 cookies。
+ 无法执行Js代码的爬虫，用 re 模块取出Js字段中 SafeTechSYS_sign_javascript 的值并写入 cookies，就能正常访问其他页面，当 cookies 失效时（判断方法是响应内容的长度），便再构造一次cookies

### 并发，写入文件
+ 因为涉及到 url 队列，所以使用多线程或多进程或携程时，读同一个 url 队列，可以使用 Queue 模块，也可以用 redis，同一个redis节点对并发的请求是序列化的，而且因为不会涉及到 read&write 操作，所以不需要加锁。
+ 先将爬下来的字段写入redis set, 然后再写入文件。否则原因同上，多线程或多进程对同一文件进行操作需要用到文件锁

### 文件说明
+ crawl_info.py 爬取某页的类，写入redis，以 category 命名的 set
+ main.py 实现并发，mult_gevent('目录'，页码数，‘是否写入文件’)
+ get_category.py 返回 目录：url 的一个字典

### 测试
+ 指定爬取 音乐 类，指定爬取 1000 页，耗时 1271s，应该得到数据 40000 条，实际得到 39800
