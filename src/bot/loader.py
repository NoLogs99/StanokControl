from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.config.config import config
from src.utils.logger import logger

logger.info("Инициализация бота и диспетчера")
logger.debug("Используется ParseMode: {}", ParseMode.HTML)

bot = Bot(token=config.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

logger.success("Bot и Dispatcher успешно созданы")
