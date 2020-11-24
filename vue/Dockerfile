FROM node:lts
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
WORKDIR /src

RUN apt-get update && \
    apt-get install -y vim less git

RUN npm install -g npm && \
    npm install -g @vue/cli @vue/cli-init && \
    npm install -D webpack webpack-cli babel-loader @babel/core @babel/preset-env


EXPOSE 8080