# LINE_bot
個人用LINE Chat botです。  
試作なのでこれから改良予定です。  
（※特定の情報を扱うように作っているため汎用性は現在ほぼ皆無です）

## 機能
### LINE Chat botから特定のキーワードを入力する事によって、応じた内容を返す。  
＜バックエンド機能＞
- webサイトから情報を取得する（webスクレイピング使用）
- twitterから特定のキーワードに沿った情報を取得（現在はイベントの日付のみを想定）  
（twitterからの情報取得に関しては、特定のフォーマットを想定しているため修正する必要があります。）
- Google Calendarにイベントと日付を自動登録
- Google photoに保存してある写真の呼び出し

## 環境など
- python 3.7
- Messasing API
- Twitter API
- Google Calendar API
- Google Photo API
- heroku
