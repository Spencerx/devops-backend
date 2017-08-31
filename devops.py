#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, abort
from app import create_app
app = create_app()


# 全局访问日志
# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(levelname)s %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='{0}/production.log'.format(Config.LOG_DIR),
#                 filemode='a+')


@app.before_request
def before_request():
    if request.method != 'OPTIONS':
        current_uri = request.path
        if current_uri.startswith("/api/v1/common") or current_uri.startswith("/api/v1/auth/login") \
                or current_uri.startswith("/api/v1/auth/logout"):
            print 'pass'
        else:
            authorization = request.headers.get('Authorization', None)
            if authorization:
                print authorization
            else:
                abort(401)

    else:
        pass
    # if 'auth/login' in current_uri or 'auth/register' in current_uri:
    #     pass
    # else:
    #     authentication = request.headers.get('Token',None)
    #     if authentication:
    #         token_status = check_token_status(authentication)
    #         if token_status:
    #             print 'validate token'
    #         else:
    #             print 'invalidate token'
    #     else:
    #         pass
    #         print 'deny!'


# @app.after_request
# def after_request(response):
#     print 'end request!'
#     return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)
