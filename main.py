import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()
city = os.environ['CITY']

start_date = os.environ['START_DATE']
birthday = os.environ['BIRTHDAY']
# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
# 用户ID和模板ID
user_id1 = os.environ["USER_ID1"]
user_id2 = os.environ["USER_ID2"]
template_id = os.environ["TEMPLATE_ID"]

# 可通过下列代码在本地调试
# start_date = "2022-06-06"
# birthday = "05-20"
# # 微信公众测试号ID和SECRET
# app_id = ""
# app_secret = ""
# # 用户ID和模板ID
# user_id = ""
# template_id = ""


# 获取天气和温度
def get_weather():
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


# 当前城市、日期
def get_city_date():
    return city, today.date().strftime("%Y-%m-%d")


# 距离设置的日期过了多少天
def get_count():
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 距离过生日还有多少天
def get_birthday():
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

wea, temperature = get_weather()
city_q, date_q = get_city_date()

data = {
    "city": {"value": city_q, "color": get_random_color()},
    "date": {"value": date_q, "color": get_random_color()},
    "weather": {"value": wea, "color": get_random_color()},
    "temperature": {"value": temperature, "color": get_random_color()},
    "love_days": {"value": get_count(), "color": get_random_color()},
    "birthday_left": {"value": get_birthday(), "color": get_random_color()},
    "words": {"value": get_words(), "color": get_random_color()}
        }

res1 = wm.send_template(user_id1, template_id, data)
res2 = wm.send_template(user_id2, template_id, data)
print(res1, res2)
