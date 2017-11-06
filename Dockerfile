FROM daocloud.io/library/nginx:1.13.0
MAINTAINER Kylin
ENV env dev
RUN mkdir /var/www -p
ADD ./ /var/www
EXPOSE 8888
RUN pip install -r dependance

