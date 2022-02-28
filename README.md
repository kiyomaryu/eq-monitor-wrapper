# eq-monitor-wrapper

## Motivation

VR中に地震があった時にすぐ気が付きたいよねー、というお話が発端です。  
調べたところGoogleChromeの拡張機能の「強振モニタ」というものがありました。  
NeosVRでは外部通信としてWebsocketが利用することができます。  
上記を中継するサーバがあれば実現できるということがわかり作ることにしました。

## Overview

緊急地震速報をWebsocketにて接続しているクライアントに通知するためのWrapperになります。
このWebアプリでは下記の機能を提供しています。

- 強振モニタからのPOSTリクエストを受け取るWebAPIのエンドポイント
- 緊急地震速報をNeosVR内から受け取るためのWebsocketのエンドポイント

強振モニタには外部WebAPIのエンドポイントに対して地震情報をJson形式でPOSTする機能があります。  
この機能のエンドポイントとして実装を行いました。

## Infrastructure

### 論理構成図
![論理構成図](https://user-images.githubusercontent.com/24783202/155921480-b5e5f48b-fd2e-4107-b398-1fbd916dde79.png)

### WebAPIエンドポイント
// TODO

### サーバ情報

- ConoHaVPS (vCPU:1,Mem:512MB)

#### webサーバ

- nginx
  - 443にてListen
  - 証明書はLet's Encrypt

#### ASGIサーバ

- gunicorn
- uvicorn

##### プロセス管理

- systemdにてgunicornをデーモン化
- gunicornではuvicornをマルチプロセス化して起動

### Pythonのバージョン管理

- pyenvを利用
- systemdにて起動

#### ファイアウォール

- ufwにて制御

## Application

### 技術仕様

- 言語：Pytnon3系
- フレームワーク：FastAPI

### 緊急地震速報通知フロー

- 1.緊急地震速報クライアントからWebsocketのエンドポイントに接続
- 2.緊急地震速報が発報され強振モニタプラグインからWebAPIのエンドポイントにPOSTされる
- 3.1でコネクションを張っている緊急地震速報クライアントに対してPOSTのタイミングでWebsocketのSendで送信(複数コネクションがあれば全てに対してSend)
- 4.緊急地震速報クライアントで通知されたJsonを解析し該当の音声データにてワールド内にいるユーザに対して通知

### コネクション数制限
// TODO 調整中

## About
// TODO
