#version設定
FROM python:3.10-alpine3.19

#インストール
RUN apk update && apk add git bash make

#/appディレクトリ配下で作業
WORKDIR /app

#ライブラリインストール
COPY ./python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt