FROM node:12.12.0-alpine

WORKDIR /usr/src/app

RUN apk update && \
    npm install -g npm @vue/cli

RUN npm install
#COPY ./vue_django /use/src/app
#COPY ./entrypoint.sh .
#COPY . .
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
#CMD ["npm", "run", "serve"]