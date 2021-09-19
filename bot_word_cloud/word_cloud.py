import base64

from io import BytesIO
from pathlib import Path
import imageio

from wordcloud import WordCloud

from .database import get_words

curFileDir = Path(__file__).absolute().parent

# mk = imageio.imread(curFileDir / "1.png")


def build_word_cloud_pic(groupid):
    word_cloud = WordCloud(
        width=550,
        height=550,
        scale=2,
        background_color='white',
        stopwords={'的', '我'},
        # mask=mk,
        # font_path=str(curFileDir / '方正黑体简体.ttf')
        # max_font_size=100,  # 设置字体最大值
        # random_state=50,  # 设置随机生成状态，即多少种配色方案
        font_path=str(curFileDir / 'msyh.ttc')
    )
    word_cloud.generate(' '.join(get_words(groupid)))
    img = word_cloud.to_image()
    with BytesIO() as bf:
        img.save(bf, format="PNG")
        return base64.b64encode(bf.getvalue()).decode()
