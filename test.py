


import consul
ret = {}
try:
    c = consul.Consul(host='192.168.15.255', port=8500, scheme='http')
    res = c.kv.delete(key='upstreams/haixue_test/192.168.16.16:9090')
    print res
except Exception, e:
    print e