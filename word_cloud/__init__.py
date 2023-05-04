import re
from pathlib import Path

import jieba
from botoy import async_scheduler
from botoy import ctx, mark_recv, logger, S, contrib, jconfig

from .database import log_words, reset_database
from .word_cloud import build_word_cloud_pic, send_to_all_group

curFileDir = Path(__file__).parent

# jieba.initialize()
stopwords = [
    line.strip()
    for line in open(curFileDir / "stopwords.txt", encoding="UTF-8").readlines()
]
jieba.load_userdict(str(curFileDir / "dict.txt"))

for t_s in jconfig.get("wordCloud.sendtime"):
    t_s_ = t_s.split(".")
    async_scheduler.add_job(
        send_to_all_group,
        "cron",
        hour=t_s_[0],
        minute=t_s_[1],
        misfire_grace_time=30,
    )  # 每天21点把词云发送到所有群
    logger.warning(f"词云将在[{t_s_[0]}:{t_s_[1]}]发送到所有群")

for t_r in jconfig.get("wordCloud.resettime"):
    t_r_ = t_r.split(".")
    async_scheduler.add_job(
        reset_database,
        "cron",
        hour=t_r_[0],
        minute=t_r_[1],
        misfire_grace_time=30,
    )  # reset_database
    logger.warning(f"词云将在[{t_r_[0]}:{t_r_[1]}]重置数据库")


# from datetime import datetime, timedelta, timezone\
# utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
# beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
#
# async_scheduler.add_job(
#     reset_database,
#     next_run_time=beijing_time + timedelta(seconds=15),
#     misfire_grace_time=30,
# )  # 每天4点重置数据库
#
# async_scheduler.add_job(
#     send_to_all_group,
#     next_run_time=beijing_time + timedelta(seconds=10),
#     misfire_grace_time=30,
# )  # 每天4点重置数据库


async def main():
    if m := ctx.group_msg:
        if m.is_from_self:
            return
        if m.text == "词云":
            await S.text("正在合成词云...")
            await S.image(await build_word_cloud_pic(m.from_group))
            logger.success("词云")
        else:
            if msg := m.text:
                msg_finish = re.sub(r"[^\u4e00-\u9fa5^a-zA-Z0-9]", '',
                                    re.sub(r"\[表情\d+]", "", msg))  # 只保留字符串中的中英文和数字+过滤表情,
                words = await contrib.async_run(
                    jieba.lcut, msg_finish
                )  # 分词
                words_finish = [
                    word for word in words if word not in stopwords and not word.isspace() and word.isprintable()
                ]  # 去除stopwords
                logger.success(
                    f"[{m.from_group_name}:{m.from_group}] ; [{m.from_user}:{m.from_user_name}] 分词-->{words_finish}"
                )
                if words_finish:
                    await log_words(m.from_group, m.bot_qq, words_finish)


mark_recv(main, author='yuban10703', name="词云", usage='发送"词云"')
