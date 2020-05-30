# Description

Discord上で、
予め登録したメンバーを元にパーティを作ってくれる簡易ツールです。
特に、以下のような使い方を想定しています。

* たとえば守備・攻撃・支援・戦力外といった、役割を表すグループを定義する
* グループに属する形でメンバーを定義する
* BOTに、できるだけ多くのグループからメンバーを集めたパーティを編成させる

# Commands

[ ]は任意入力, <>は必須入力パラメータです。

---- 
`/show`

* 現在のグループとメンバーの定義状態を見る

出力例:

    /show
    現在の登録メンバーは次の通りです。
    defense= a, b, c
    attack= d, e
    support= f, g, h, i
    bench= j


---- 
`/regroup <Group-1> [Group-n]`

* グループを再定義する。
  * `Group-x`: グループ名。スペースで区切って複数のグループを指定可能。
  全てのグループとメンバーが消去され、指定したグループが作られます。


出力例:

    /regroup 壁 火力 支援 お座り
    グループを再作成しました。
    壁= 
    火力= 
    支援= 
    お座り=

---- 
`/clear [Group]`

* すべてまたは指定のグループから、全メンバーを消去する
  * `Group`: 対象とするグループ名。省略時は全グループが対象となる。

出力例:

    /clear defense
    defense グループのメンバーリストを空にしました。
    defense=
    attack= d, e
    support= f, g, h, i
    bench= j

---- 
`/remove <Group> <Member-1> [Member-n]`

* 指定したグループから、指定したメンバーを消去する
  * Group: 対象とするグループ名。
  * Member-x: 消去したいメンバー名。スペースで区切って複数のメンバー名を指定可能。

出力例:

    /remove defense c
    c を defense グループから除去しました。
    defense= a, b
    attack= d, e
    support= f, g, h, i
    bench= j

---- 
`/add <Group> <Member-1> [Member-n]`

* 指定したグループにメンバーを追加する
  * Group: 対象とするグループ名。
  * Member-x: 追加したいメンバー名。スペースで区切って複数のメンバー名を指定可能。

出力例:

    /add defense Z
    メンバー Z を defense に追加しました。
    defense= a, b, c, Z
    attack= d, e
    support= f, g, h, i
    bench= j


---- 
`/count`

* 現在のメンバーの定義数を見る

出力例:

    /count
    現在 10 メンバーをストックしています。

---- 
`/party [<Party Number> [Allocation Number]]`

* パーティ編成例を出力する。予め、グループとメンバーが定義されている必要がある。
  * Party Number: 編成するパーティの数。1~`/count`で得られるメンバー数まで。省略すると2。
  * Allocation Number for each Party: パーティに参加させるメンバーの数。1~`/count`で得られるメンバー数まで。省略すると5。

出力例:

      /party
      次のようなパーティ編成はいかがでしょう。
      Party-1= a, d, f, j, b
      Party-2= e, g, c, h, i
      /party 2 5
      次のようなパーティ編成はいかがでしょう。
      Party-1= a, d, f, j, b
      Party-2= e, g, c, h, i

---- 
`/save`

* 現在のグループとメンバーの登録状態をセーブする



# Requirement

* Python 3.7 >=
* discord.py 1.3.3

# Installation for heroku

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


# Installation for docker

1. docker サーバを立てる
1. docker サーバ上にこのリポジトリを clone する
1. `docker-compose up -d` する

# Reference

[こちら](https://github.com/Rabbit-from-hat/make-team) のフォークを参考にさせていただきました。

