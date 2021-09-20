import asyncio
import base64
import re
import time
from io import BytesIO
from pathlib import Path

import ujson as json
from botoy import Action, jconfig, logger
from botoy import GroupMsg
from botoy.contrib import to_async
from botoy.parser import group as gp
from wordcloud import WordCloud

from .database import get_words, get_all_groups

curFileDir = Path(__file__).absolute().parent


# mk = imageio.imread(curFileDir / "1.png")


def parser_msg(ctx: GroupMsg):
    if msg_data := gp.reply(ctx) or gp.pic(ctx):
        return re.sub("@.* ", "", msg_data.Content)
    elif ctx.MsgType == "ReplayMsg":
        msg = json.loads(ctx.Content)
        return re.sub(f"@{msg['UserExt'][0]['QQNick']}\\s+", "", msg["Content"])
    elif msg_data := gp.at(ctx) or ctx:
        return msg_data.Content
    # if data := gp.pic(ctx):
    #     print('pic')
    # elif data := gp.at(ctx):
    #     print('at')
    #     msg = re.sub(data.UserExt["QQNick"], '', data.Content)
    # elif data := gp.reply(ctx):
    #     print('rep')
    #     msg = re.sub(data.UserExt["QQNick"], '', data.Content)
    # else:
    #     print('?')
    #     msg = ctx.Content
    # print(msg)
    # return msg


@to_async
def build_word_cloud_pic(groupid):
    word_cloud = WordCloud(
        width=500,
        height=500,
        scale=2,
        max_words=700,
        max_font_size=270,
        background_color="white",
        # stopwords=set(stopwords),
        # mask=mk,
        # font_path=str(curFileDir / '方正黑体简体.ttf')
        # max_font_size=100,  # 设置字体最大值
        # random_state=50,  # 设置随机生成状态，即多少种配色方案
        font_path=str(curFileDir / "msyh.ttc"),
    )
    word_cloud.generate(" ".join(get_words(groupid)))
    img = word_cloud.to_image()
    with BytesIO() as bf:
        img.save(bf, format="PNG")
        return base64.b64encode(bf.getvalue()).decode()


def send_to_all_group():
    logger.warning("开始向有数据的群发送今日词云")
    action = Action(qq=jconfig.bot)
    groups = get_all_groups()
    for group in groups:
        logger.warning(f"开始向群{group}发送今日词云")
        action.sendGroupPic(
            group, picBase64Buf=asyncio.run(build_word_cloud_pic(group))
        )
        time.sleep(3)
