import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
# # 用户ID和模板ID
# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]

# 可把os.environ结果替换成字符串在本地调试
user1 = {
    'city': '北京',
    'start_date': "2022-02-15",
    'birthday': "02-15",
    'user_id': os.environ["USER_ID1"],
    'template_id': os.environ["TEMPLATE_ID"]
}
user2 = {
    'city': '秦皇岛',
    'start_date': "2022-10-24",
    'birthday': "11-08",
    'user_id': os.environ["USER_ID2"],
    'template_id': os.environ["TEMPLATE_ID"]
}
user3 = {
    'city': '秦皇岛',
    'start_date': "2004-11-11",
    'birthday': "11-11",
    'user_id': os.environ["USER_ID3"],
    'template_id': os.environ["TEMPLATE_ID"]
}


# 获取天气和温度
def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])


# 当前城市、日期
def get_city_date(city):
    return city, today.date().strftime("%Y-%m-%d")


# 距离设置的日期过了多少天
def get_count(start_date):
    delta = today - datetime.strptime(start_date, "%Y-%m-%d")
    return delta.days


# 距离过生日还有多少天
def get_birthday(birthday):
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


for user in [user1, user2, user3]:
    wea, temperature = get_weather(user['city'])
    city_q, date_q = get_city_date(user['city'])
    data = {
        "city": {"value": city_q, "color": get_random_color()},
        "date": {"value": date_q, "color": get_random_color()},
        "weather": {"value": wea, "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "love_days": {"value": get_count(user['start_date']), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(user['birthday']), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
            }
    
    res = wm.send_template(user['user_id'], user['template_id'], data)
    print(res)
