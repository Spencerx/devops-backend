#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import request, abort
from app import create_app
from config import Dev
from app.tools.tokenUtils import decrypt_token, check_token_status
app = create_app()


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
                        app.logger.error('token is expired')
                        abort(401, 'token is expired')
                else:
                    app.logger.error('token is invalidate')
                    abort(401, 'token is invalidate')
            else:
                abort(401, 'no token in header')

    else:
        pass


@app.after_request
def after_request(response):
    return response


if __name__ == '__main__':
    app.run(host=Dev.DEVOPS['IP'], port=Dev.DEVOPS['PORT'], threaded=True)
