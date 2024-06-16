import asyncio
import base64
from io import BytesIO
from pathlib import Path

from botoy import Action, logger
from botoy import contrib
from wordcloud import WordCloud

from .database import get_words, get_all_groups

curFileDir = Path(__file__).parent


# mk = imageio.imread(curFileDir / "1.png")


@contrib.to_async
def build_word_cloud_pic(groupid) -> str:
    word_cloud = WordCloud(
        width=420,
        height=420,
        scale=2,
        # max_words=200,
        max_font_size=110,
        background_color="white",
        # stopwords=set(stopwords),
        # mask=mk,
        # font_path=str(curFileDir / '方正黑体简体.ttf')
        # max_font_size=100,  # 设置字体最大值
        # random_state=50,  # 设置随机生成状态，即多少种配色方案
        font_path=str(curFileDir / "LXGWWenKai-Regular.ttf"),
    )
    # word_cloud.generate(" ".join(get_words(groupid)))
    word_cloud.generate_from_frequencies(get_words(groupid))
    img = word_cloud.to_image()
    with BytesIO() as bf:
        img.save(bf, format="PNG")
        return base64.b64encode(bf.getvalue()).decode()


async def send_to_all_group():
    logger.warning("开始向有数据的群发送今日词云")
    groups_info = get_all_groups()
    for group, botqq in groups_info.items():
        logger.warning(f"bot:[{botqq}] 开始向群->{group}<-发送今日词云")
        try:
            image_base64 = await build_word_cloud_pic(group)
            await Action(qq=botqq).sendGroupPic(
                group, base64=image_base64, 
            )
            await asyncio.sleep(2)
        except Exception as e:
            logger.error(f"Failed to send word cloud to group {group}: {e}")
