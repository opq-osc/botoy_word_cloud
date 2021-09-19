import base64
import time
from io import BytesIO
from pathlib import Path

from botoy import Action, jconfig, logger
from wordcloud import WordCloud

from .database import get_words, get_all_groups

curFileDir = Path(__file__).absolute().parent

# mk = imageio.imread(curFileDir / "1.png")
stopwords = [line.strip() for line in open(curFileDir / "stopwords.txt", encoding='UTF-8').readlines()]


def build_word_cloud_pic(groupid):
    word_cloud = WordCloud(
        width=550,
        height=550,
        scale=2,
        background_color='white',
        stopwords=set(stopwords),
        # mask=mk,
        # font_path=str(curFileDir / '方正黑体简体.ttf')
        # max_font_size=100,  # 设置字体最大值
        # random_state=50,  # 设置随机生成状态，即多少种配色方案
        font_path="C:\Windows\Fonts\msyh.ttc"
    )
    word_cloud.generate(' '.join(get_words(groupid)))
    img = word_cloud.to_image()
    with BytesIO() as bf:
        img.save(bf, format="PNG")
        return base64.b64encode(bf.getvalue()).decode()


def send_to_all_group():
    logger.warning('开始向有数据的群发送今日词云')
    action = Action(qq=jconfig.bot)
    groups = get_all_groups()
    for group in groups:
        logger.warning(f'开始向群{group}发送今日词云')
        action.sendGroupPic(group, picBase64Buf=build_word_cloud_pic(group))
        time.sleep(3)
