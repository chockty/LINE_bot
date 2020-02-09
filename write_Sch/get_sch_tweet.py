#Twitterのつぶやきから特定のツイートをAPIを叩いて検索する。
import tweepy
import datetime
import os

CONSUMERKEY = os.environ["C_SKEY"]
SECRETKEY = os.environ["S_RKEY"]
ACCESSTOKEN = os.environ["A_CTOKEN"]
SECRETTOKEN = os.environ["S_RTOKEN"]
    
#tweepyの認証,ツイート取得
def get_API_tweet():
    auth = tweepy.OAuthHandler(CONSUMERKEY, SECRETKEY)
    auth.set_access_token(ACCESSTOKEN,SECRETTOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    q="2月前半"
    Sch_list = ()
    get_tweets = api.user_timeline(screen_name = "toricago_O",tweet_mode = "extended",count = 100)
    for tweet in get_tweets:
        if q in tweet.full_text:
            if not "RT @" in tweet.full_text:
                Sch_list = tweet.full_text
            else:
                Sch_list = tweet.retweeted_status.full_text
    return Sch_list

#取得ツイートをカレンダーへ入力可能な形へ変形
def edit_sch(Sch_list):
    Sch_list = Sch_list.split("\n")
    edited_Sch_list = []
    now = datetime.datetime.now()
    now = str(now.year)
    Remove_list = ["(月)","(火)","(水)","(木)","(金)","(土)","(日)","（月）","（火）","（水）","（木）","（金）","（土）","（日）",
               "(月/祝)","(火/祝)","(水/祝)","(木/祝)","(金/祝)","（月/祝）","（火/祝）","（水/祝）","（木/祝）","（金/祝）"]

    for num in range(0, len(Sch_list)):
        if not "" == Sch_list[num] and not "#鶯籠" in Sch_list[num]:
            Sch_list[num] = Sch_list[num].replace(" ","")
            Sch_list[num] = now + "/" + Sch_list[num]
    
    for num in range(0, len(Sch_list)):
        for Removal in Remove_list:
            if not Removal in Sch_list[num]:
                continue
            else:
                Sch_list[num] = Sch_list[num].split(Removal)
                Sch_list[num][0] = Sch_list[num][0].replace("/", "-")
                Sch_list[num][0] = str(datetime.datetime.strptime(Sch_list[num][0], '%Y-%m-%d'))
                Sch_list[num][0] = Sch_list[num][0].replace(" 00:00:00", "")
                edited_Sch_list.append(Sch_list[num])
    edited_Sch_list = dict(edited_Sch_list)
    return edited_Sch_list

