#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import request, abort
from app import create_app
from app.tools.tokenUtils import decrypt_token, check_token_status
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
            pass
        else:
            authorization = request.headers.get('Authorization', None)
            if authorization:
                username = decrypt_token(authorization)
                if username:
                    if check_token_status(username, authorization):
                        pass
                    else:
                        abort(401, 'token is expired')
                else:
                    abort(401, 'token is invalidate')
            else:
                abort(401, 'no token in header')

    else:
        pass


@app.after_request
def after_request(response):
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
