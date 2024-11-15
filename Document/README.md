# 使い方

## 1. 下準備

### 1.1. チャンネルに Bot アプリを登録する。

<img src="src\image1.svg">

1. チャンネルを開いて、上部の「チャンネルの詳細を取得する」から設定画面を開く
1. 「インテグレーション」からアプリを追加するで「Ned Ludd」を選択
1. 以下のようになれば OK
   <img src="src\image2.svg">

1. ついでにチャンネル ID をコピペしておく。
   <img src="src\image3.svg">

## 2. 操作

### 2.1. アプリを起動する。

1. 適当なフォルダを作って exe ファイルを移動する。
1. 起動する。
1. パスワードを入力
   <img src="src\image4.svg" width=60%>
1. exe ファイルに同階層に db ファイルが生成される。

※db ファイルをいじるとバグるので注意。中身のテーブルを書き換えないように。

### 2.2. チャンネル登録

1. 「SET CHANNEL」をクリック
   <img src="src\image5.svg" width=60%>
1. 「Channel 名」に適当な文字列を入力（ラベルなのでなんでもいい）
1. 「ChannelID」にコピペしたチャンネル ID を貼り付け
1. 「OK」ボタンを押す。
   <img src="src\image6.svg" width=60%>
1. チャンネルは何個でも登録できる。複数登録したときは「SET CHANNEL」左隣のコンボボックスから操作したいチャンネルを選択する。

### 2.3. メッセージログを取得

1. 「FETCH」ボタンを押す。
1. ウィンドウが開いたら「OK」ボタンを押す。

### 2.4. csv 出力

1. 「OUTPUT」ボタンを押す。
1. 必要に応じて時点を指定する。TIMESTAMP に変換できない文字列なら無視される。
1. ウィンドウが開いたら「OK」ボタンを押す。
1. exe ファイルと同階層に出力される。ファイルの上書きはされない。
   <img src="src\image7.svg" >

## 3. 注意点

Bot アプリを忍ばせないとメッセージの取得はできません。
Bot のトークンが変わると使えなくなります。（書き換えることは可能です）

## 4. 問題点

1. スレッドの取得ができない。
1. ファイル出力場所を選べない。
1. ChannelID が数値から始まると登録できない。
