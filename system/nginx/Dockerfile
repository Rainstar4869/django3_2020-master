FROM nginx:1.19.0-alpine

# 設定ファイル
ADD ./config/nginx.conf /etc/nginx/nginx.conf
ADD ./config/uwsgi_params /etc/nginx/uwsgi_params
ADD ./config/conf.d/default.conf /etc/nginx/sites-available/default
ADD ./config/conf.d/default.conf /etc/nginx/sites-enabled/default

RUN mkdir /var/www
RUN mkdir /var/www/front
RUN mkdir /var/www/staticfiles
RUN mkdir /var/www/mediafiles