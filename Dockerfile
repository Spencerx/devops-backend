FROM daocloud.io/library/nginx:1.13.0
MAINTAINER Kylin
ENV RUN_USER nginx
ENV RUN_GROUP nginx
RUN mkdir /etc/nginx/logs -p
RUN chown nginx.nginx -R /etc/nginx/
ADD nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
ENTRYPOINT nginx -g "daemon off;"
