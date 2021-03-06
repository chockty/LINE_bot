from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
import os
import random
import collections
import get_keyword_photo as gkp
import get_web_schedules as gws
from write_Sch import get_sch_tweet as gst
from write_Sch import write_calendar as wcr
from write_Sch import get_websch_forcalendar as gwc
from write_Sch import write_calendar_detail as wcd
 
app = Flask(__name__)
 
#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
 
## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    #  署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'
 
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。


KeyErrorlist = ["いいからカメコになれ","いいからライブ行け"]
#Success
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    key_word = event.message.text
    if key_word == "スケジュール" or key_word == "いつ？":
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="ちょい待ち"))
        event_info = gws.get_schedules()
        line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=event_info))

    elif "カレンダー" in key_word or "入れておいて" in key_word:
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="しばし待ちを"))
        try:
            auth_caledar = wcr.calendar_user_auth()
            get_calendar = wcr.get_calendar_events(auth_caledar)
            event_info = gwc.get_edit_sch_info()
            wcd.write_calendar_details(get_calendar,event_info,auth_caledar)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="入力したで。"))
        except KeyError as key:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="なんか無理やったわ"))
            
    elif "月" in key_word and "日" in key_word:
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="まぁ待てって"))
        event_info = gws.get_a_schedule()
        try:
            choice_day = gws.choice_a_day(key_word,event_info)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=choice_day))
        except KeyError as key:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="その日にはないよ"))

    elif "/" in key_word:
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="まぁ待チー二"))
        event_info = gws.get_a_schedule()
        try:
            choice_day = gws.choice_a_day(key_word,event_info)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=choice_day))
        except KeyError as key:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="その日にはないよ"))

    elif "次" in key_word:
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="焦んなって"))
        event_info = gws.get_a_schedule()
        try:
            earlist_one = gws.get_a_earlist_schedule(event_info)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=earlist_one))
        except Exception as ex:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="すまん。エラー。"))
        
    elif key_word == "今日":
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="今日はな"))
        event_info = gws.get_a_schedule()
        try:
            today_one = gws.get_today_event(event_info)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=today_one))
        except Exception as ex:
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text="ないんだよ。。。"))

    elif "月" in key_word and "半" in key_word:
        profile = event.source.user_id
        line_bot_api.push_message(
                profile,TextSendMessage(text="まぁ待てや"))
        try:    
            get_tweet = gst.get_API_tweet(key_word)
            get_sch = gst.edit_sch(get_tweet)
            auth_caledar = wcr.calendar_user_auth()
            get_calendar = wcr.get_calendar_events(auth_caledar)
            write = wcr.hantei_wtite(get_calendar,get_sch.edited_Sch_list,auth_caledar)
            line_bot_api.push_message(
                profile,TextSendMessage(text=get_tweet))
            if len(get_sch.except_list) == 0:
                line_bot_api.reply_message(
                    event.reply_token,TextSendMessage(text="カレンダーにも入れておいたよ"))
            else:
                line_bot_api.reply_message(
                    event.reply_token,TextSendMessage(text="これは自己管理な。\n{}".format(get_sch.except_list)))
        except Exception as EX:
            line_bot_api.push_message(
                profile,TextSendMessage(text="ツイートなかったわ"))
    else:
        auth = gkp.photo_user_auth()
        image_info = gkp.get_photo_url(key_word)
        if not image_info:
            error_object = random.choice(KeyErrorlist)
            line_bot_api.reply_message(
                event.reply_token,TextSendMessage(text=error_object))
        else:
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(original_content_url=image_info[0],preview_image_url=image_info[1]))
         
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)