import re
from pathlib import Path

import jieba
from botoy import GroupMsg, logger, S
from botoy import async_decorators as deco
from botoy.collection import MsgTypes
from botoy.contrib import async_run
from botoy.schedule import scheduler

from .database import log_words, reset_database
from .word_cloud import build_word_cloud_pic, send_to_all_group, parser_msg

__doc__ = "词云"
curFileDir = Path(__file__).parent

# jieba.initialize()
stopwords = [
    line.strip()
    for line in open(curFileDir / "stopwords.txt", encoding="UTF-8").readlines()
]
jieba.load_userdict(str(curFileDir / "dict.txt"))

scheduler.add_job(
    send_to_all_group,
    "cron",
    hour=21,
    minute=00,
    misfire_grace_time=30,
)  # 每天21点把词云发送到所有群

scheduler.add_job(
    reset_database,
    "cron",
    hour=4,
    minute=00,
    misfire_grace_time=30,
)  # 每天4点重置数据库


@deco.ignore_botself
@deco.these_msgtypes(
    MsgTypes.TextMsg,
    MsgTypes.AtMsg,
    MsgTypes.PicMsg,
    MsgTypes.ReplyMsgA,
    MsgTypes.ReplyMsg,
)
async def receive_group_msg(ctx: GroupMsg):
    if ctx.Content == "词云":
        await S.atext("正在合成词云...")
        word_cloud_pic_b64 = await build_word_cloud_pic(ctx.FromGroupId)
        await S.aimage(word_cloud_pic_b64)
        logger.success("词云")
    else:
        if msg := parser_msg(ctx):
            words = await async_run(
                jieba.lcut, re.sub(r"\[表情\d+]", "", msg)
            )  # 过滤表情,并分词
            words_finish = [
                word for word in words if word not in stopwords and not word.isspace() and word.isprintable()
            ]  # 去除stopwords
            logger.success(
                f"[{ctx.FromGroupName}:{ctx.FromGroupId}] ; [{ctx.FromNickName}:{ctx.FromUserId}] 分词-->{words_finish}"
            )
            await log_words(ctx.FromGroupId, words_finish)
