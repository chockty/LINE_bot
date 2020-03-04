#Twitterのつぶやきから特定のツイートをAPIを叩いて検索する。
import tweepy
import datetime
import os
import collections

CONSUMERKEY = os.environ["C_SKEY"]
SECRETKEY = os.environ["S_RKEY"]
ACCESSTOKEN = os.environ["A_CTOKEN"]
SECRETTOKEN = os.environ["S_RTOKEN"]

#全角→半角のテーブル
henkan_table = str.maketrans({"１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9","０":"0"})

#tweepyの認証,ツイート取得
def get_API_tweet(keyword):
    auth = tweepy.OAuthHandler(CONSUMERKEY, SECRETKEY)
    auth.set_access_token(ACCESSTOKEN,SECRETTOKEN)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    q=keyword.translate(henkan_table)
    Sch_list = ()
    get_tweets = api.user_timeline(screen_name = "toricago_O",tweet_mode = "extended",count = 100)
    for tweet in get_tweets:
        if q in get_tweets:
            if not "RT @" in tweet.full_text:
                Sch_list = tweet.full_text
                break
            else:
                Sch_list = tweet.retweeted_status.full_text
                break
    if not Sch_list:
        for num in range(50,200,50):
            get_tweets = api.user_timeline(screen_name = "toricago_O",tweet_mode = "extended",count = 100+int(num))
            for tweet in get_tweets:
                if q in tweet.full_text:
                    if not "RT @" in tweet.full_text:
                        Sch_list = tweet.full_text
                        break
                    else:
                        Sch_list = tweet.retweeted_status.full_text
                        break
                else:
                    continue
    return Sch_list
    
#取得ツイートをカレンダーへ入力可能な形へ変形
def edit_sch(Sch_list):
    Sch_list = Sch_list.split("\n")
    edited_Sch_list = []
    except_list = []
    now = datetime.datetime.now()
    now = str(now.year)
    Remove_list = ["(月)","(火)","(水)","(木)","(金)","(土)","(日)","（月）","（火）","（水）","（木）","（金）","（土）","（日）",
               "(月/祝)","(火/祝)","(水/祝)","(木/祝)","(金/祝)","（月/祝）","（火/祝）","（水/祝）","（木/祝）","（金/祝）"]

    for num in range(0, len(Sch_list)):
        if not "" == Sch_list[num] and not "#鶯籠" in Sch_list[num] and not "半" in Sch_list[num]:
            Sch_list[num] = Sch_list[num].replace(" ","")
            Sch_list[num] = now + "/" + Sch_list[num]

    for num in range(0, len(Sch_list)):
        for Removal in Remove_list:
            if not Removal in Sch_list[num]:
                continue
            else:
                Sch_list[num] = Sch_list[num].split(Removal)

    for num in range(0, len(Sch_list)):
        if "" == Sch_list[num]:
            continue
        elif "月" in Sch_list[num] or "半" in Sch_list[num]:
            continue
        elif "#鶯籠" in Sch_list[num]:
            continue
        else:
            try:
                Sch_list[num][0] = Sch_list[num][0].replace("/", "-")
                Sch_list[num][0] = str(datetime.datetime.strptime(Sch_list[num][0], '%Y-%m-%d'))
                Sch_list[num][0] = Sch_list[num][0].replace(" 00:00:00", "")
                edited_Sch_list.append(Sch_list[num])
            except:
                except_list.append(Sch_list[num])
    edited_Sch_list = dict(edited_Sch_list)
    result = collections.namedtuple("result", ["edited_Sch_list","except_list"])
    return result(edited_Sch_list=edited_Sch_list,except_list=except_list)


