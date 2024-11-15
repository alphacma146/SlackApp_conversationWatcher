# Slack Bot 作成手順

---

- [Slack Bot 作成手順](#slack-bot-作成手順)
  - [1. 公式サイトから「Create an app」](#1-公式サイトからcreate-an-app)
  - [2. 最初から](#2-最初から)
  - [3. アプリ名とワークスペースを選択](#3-アプリ名とワークスペースを選択)
  - [4. Bots を選択](#4-bots-を選択)
  - [5. 権限の設定](#5-権限の設定)
  - [6. bot の設定](#6-bot-の設定)
  - [7. アプリのインストール](#7-アプリのインストール)
  - [8. トークン発行](#8-トークン発行)
  - [9. bot ユーザーの見た目の変更](#9-bot-ユーザーの見た目の変更)
  - [10. 参考](#10-参考)

---

<div style="page-break-before:always"></div>

## 1. 公式サイトから「Create an app」

[Slack](https://api.slack.com/)

## 2. 最初から

From scratch を選択
@import "src\slack_1.svg"{width=80%}

## 3. アプリ名とワークスペースを選択

App Name に適当な名前を入力し、その下のプルダウンからワークスペースを選択する。
@import "src\slack_2.svg"{width=80%}

## 4. Bots を選択

開いた画面の下部にある「Bots」を押下する。
次に「Review Scopes to Add」を押下し、スコープを設定する。
@import "src\slack_3.svg"

## 5. 権限の設定

-   Bot Token Scopes:`Scopes that govern what your app can access.`
    投稿する bot の権限
-   User Token Scopes:`Scopes that access user data and act on behalf of users that authorize them.`
    メンバー情報を取得する権限

@import "src\slack_4.svg"

メッセージの取得に必要そうなのは以下

-   `channel:read`
-   `groups:read`
-   `im:read`
-   `mpim:read`

-   `channels:history`
-   `groups:history`
-   `im:history`
-   `mpim:history`

-   `files:read`
-   `emoji:read`

添付ファイル、リアクションが読み取れるか不明
Bot token と user tokens の違いが不明

## 6. bot の設定

「App Home」メニューから Bot の設定
勤怠をお知らせしてくれる bot の名前と、メンバー名を入力
@import "src\slack_5.svg"{width=80%}

## 7. アプリのインストール

「install to Workspace」押下後、リクエストが飛んでくるので許可するを押す。
@import "src\slack_6.svg"

## 8. トークン発行

コピーしておく。
@import "src\slack_7.svg"

## 9. bot ユーザーの見た目の変更

「Basic Information」メニューの「Display Information」からアプリの名前やアイコン画像などを変更できる。

## 10. 参考

[Scope について](https://api.slack.com/legacy/oauth-scopes)
[無料版 Slack メッセージ保存・退避ツール！フリープランの 1 万 →90 日の変更への対策法](https://auto-worker.com/blog/?p=6184)
[30 人以上いるグループの勤怠連絡チェックを自動化した話](https://qiita.com/tmryr/items/45dafc71d951553523fb#:~:text=%E2%91%A0)
[Python を使った、Slack からのメッセージ取得 2/3](https://www.estie.jp/blog/entry/2022/11/04/110000)
[【Slack】Bot User OAuth Token の取得方法](https://qiita.com/80syokumotsu/items/041e99e99d8ecaa3c42b)
[Slack で Private channel や DM を含む発言とファイルをエクスポートしてみる](https://qiita.com/SorAmber/items/4703e293d0b21fea5ee5)
[【Python】Slack API を使用してチャンネルの全メッセージとファイルをダウンロードするコード](https://qiita.com/Masahiro_T/items/d17e3193ad535c119978)
