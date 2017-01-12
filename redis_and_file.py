import redis
import os
pool=redis.ConnectionPool(host='localhost',port=6379,db=0)
rds=redis.StrictRedis(connection_pool=pool)


def write_to_file(name):
    with open(os.path.split(os.path.realpath(__file__))[0]+'/'+name,'a') as f:
        while True:
            info_line = rds.spop(name)
            if info_line:
                f.write(info_line.decode('utf-8')+"\n")
            else:
                break
