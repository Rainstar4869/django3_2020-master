FROM redis:latest

#COPY ./conf/6379.conf /usr/local/etc/redis/redis.conf

RUN set -x && \
    touch /var/log/redis.log && \
    chown redis:root /var/log/redis.log && \
    chmod 664 /var/log/redis.log

RUN apt-get update && \
    apt-get install vim -y

#CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
