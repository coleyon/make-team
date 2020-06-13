# Description

Googleスプレッドシート上に記入したメンバーから、バランスの良いパーティ編成案を作って発言してくれます。

# Requirement

* Python 3.7 >=
* discord.py 1.3.3

# How to Setup

1. https://gspread.readthedocs.io/en/latest/oauth2.html
  * GCP上でサービスアカウントを作成する
  * スプレッドシートを用意し、サービスアカウントに対して共有する
1. サービスアカウントのJSON形式のキーを、環境変数 `WORKSHEET_NAME` のパスに配置する
1. `docker-compose.yml` の `DISCORD_BOT_TOKEN` 環境変数 にBotのトークンを指定する
1. `docker-copose up -d` する
1. [Discord のサーバーを作る](https://support.discord.com/hc/ja/articles/204849977-%E3%82%B5%E3%83%BC%E3%83%90%E3%83%BC%E3%81%AE%E4%BD%9C%E6%88%90%E3%81%AE%E4%BB%95%E6%96%B9)
1. このリポジトリをフォークして、ローカルまたは[Herokuなどにデプロイする](https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8)
1. [Discord Developer Portal](https://discord.com/developers/applications) 上で、[Botを作ってOAUTH2 URLを得る](https://qiita.com/PinappleHunter/items/af4ccdbb04727437477f)
1. OAUTH2 URL へアクセスして、Botが作ったサーバーに参加することを許可（認証）する
   * https://discord.com/oauth2/authorize?client_id=${CLIENT_ID}&permissions=0&scope=bot

      URLにアクセスすると、次のようにサーバへBOTを参加させて良いかを問われるので、よければ認証する。

      <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/157638/2b006f68-d8b2-8eb5-81c6-aaa4c6af59cd.jpeg" width=50%>

      ロボットではないこと確認をする。

      <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/157638/a5e18cbc-14d4-12d5-fdd5-830635c385e1.jpeg" width=50%>

      認証完了。これでサーバにBOTが参加してくる。

      <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/157638/75b28f89-6090-eca4-0d03-7499aed19590.jpeg" width=50%>

      サーバにBOTが入った事確認をする。

      <img src="https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/157638/7bafcd0c-9d00-2b49-2122-583afe83542d.jpeg">

# Reference

[こちら](https://github.com/Rabbit-from-hat/make-team) のフォークを参考にさせていただきました。

