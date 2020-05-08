# Description

Discord上で、
予め登録したメンバーを元にパーティを作ってくれる簡易ツールです。
特に、以下のような概念を全面に押し出しています。

* 守備・攻撃・支援・戦力外といった役割を表すグループを定義する
* グループに属するメンバーを定義する
* できるだけ多くのグループからメンバーを拾う形で、パーティを編成する

# Commands

[ ]は任意入力, <>は必須入力パラメータです。

---- 
`/group <Group-1> [Group-n]`

* グループを再定義する。
  * `Group-x`: グループ名。スペースで区切って複数のグループを指定可能。
  全てのグループとメンバーが消去され、指定したグループが作られます。

---- 
`/clear [Group]`

* すべてまたは指定のグループから、全てのメンバーを消去する
  * `Group`: 対象とするグループ名。省略時は全グループが対象となる。

---- 
`/remove <Group> <Member-1> [Member-n]`

* 指定したグループから、指定したメンバーを消去する
  * Group: 対象とするグループ名。
  * Member-x: 消去したいメンバー名。スペースで区切って複数のメンバー名を指定可能。

---- 
`/show`

* 現在のグループとメンバーの定義状態を見る

出力例:

    現在の登録メンバーは次の通りです。
    defense= a, b, c
    attack= d, e
    support= f, g, h, i
    bench= j

---- 
`/add <Group> <Member-1> [Member-n]`

* 指定したグループにメンバーを追加する
  * Group: 対象とするグループ名。
  * Member-x: 追加したいメンバー名。スペースで区切って複数のメンバー名を指定可能。


---- 
`/count`
* 現在のメンバーの定義数を見る

出力例:

    現在 10 メンバーをストックしています。

---- 
`/party [Party Number] [Allocation Number]`

* パーティ編成例を出力する
  * Party Number: 編成するパーティの数
  * Allocation Number for each Party: パーティに参加させるメンバーの数


# Requirement

* Python 3.7.x
* discord.py 1.3.3

# Installation
このmake-teamをForkして、Heroku上にデプロイしてください。  
やり方は、以下の記事を参考にしてください。  
なお、Herokuではなくとも、ローカルでも実行可能です。  
[Discord Bot 最速チュートリアル【Python&Heroku&GitHub】](https://qiita.com/1ntegrale9/items/aa4b373e8895273875a8)
