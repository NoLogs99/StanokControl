from loguru import logger
import sys


def setup_logging(config):
    config.LOGS_PATH.mkdir(parents=True, exist_ok=True)

    logger.remove()

    logger.add(
        sys.stdout,
        level="DEBUG" if config.DEBUG else "INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
        enqueue=True,
        catch=True,
    )

    logger.add(
        config.LOGS_PATH / "bot.log",
        rotation="10 MB",
        retention="14 days",
        compression="zip",
        level="DEBUG" if config.DEBUG else "INFO",
        encoding="utf-8",
        enqueue=True,
    )

    logger.add(
        config.LOGS_PATH / "errors.log",
        level="ERROR",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        enqueue=True,
    )

    if not config.DEBUG:
        logger.add(
            config.LOGS_PATH / "bot.jsonl",
            serialize=True,
            rotation="500 MB",
            retention="90 days",
            level="INFO",
            enqueue=True,
        )

    return logger
