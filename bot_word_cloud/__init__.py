import asyncio
import re

import jieba
from botoy import GroupMsg, logger, S
from botoy import async_decorators as deco
from botoy.collection import MsgTypes
from botoy.schedule import scheduler

from .database import log_words, reset_database
from .word_cloud import build_word_cloud_pic

__doc__ = "词云"

jieba.initialize()

scheduler.add_job(
    reset_database,
    'cron',
    hour=00,
    minute=00,
    misfire_grace_time=30,
)


@deco.ignore_botself
@deco.these_msgtypes(MsgTypes.TextMsg)
async def receive_group_msg(ctx: GroupMsg):
    if ctx.Content == '词云':
        # word_cloud_pic_b64 = build_word_cloud_pic(ctx.FromGroupId)
        loop = asyncio.get_event_loop()
        word_cloud_pic_b64 = await loop.run_in_executor(None, build_word_cloud_pic, ctx.FromGroupId)
        await S.aimage(word_cloud_pic_b64)
        logger.success('词云')
    else:
        words = jieba.lcut(re.sub(r'\[表情\d+]', '', ctx.Content))  # 过滤表情,并分词
        logger.success(f"[{ctx.FromGroupName}:{ctx.FromGroupId}] ; [{ctx.FromNickName}:{ctx.FromUserId}] 分词-->{words}")
        log_words(ctx.FromGroupId, words)
