import sys
from rediscluster import StrictRedisCluster


def redis_cluster():
    redis_nodes =  [{'host':'192.168.222.66','port':6378},
                    {'host':'192.168.222.66','port':6380},
                    {'host':'192.168.222.66','port':6381},
                    {'host':'192.168.222.66','port':6382},
                    {'host':'192.168.222.66','port':6383},
                    {'host':'192.168.222.66','port':6384},
                    {'host':'192.168.222.66','port':6385}
                   ]
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception,e:
        print "Connect Error!"
        sys.exit(1)

    redisconn.set('name','admin')
    redisconn.set('age',18)
    print "name is: ", redisconn.get('name')
    print "age  is: ", redisconn.get('age')

redis_cluster()