from os import listdir, getenv
import os.path as path
import random

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from TEXTS import *
from custom_objects import MessageDataObject, CustomException, logger
from request_classes import TrackRequestType, ListRequestType, VideoRequestType


REQUEST_TYPE: set = {
    'трек': TrackRequestType,
    'лист': ListRequestType,
    'видео': VideoRequestType
}

load_dotenv()
TOKEN = getenv("TOKEN")


logger.info("Logging started")

RESPONSE = LogMessages.RESPONSE_WAS_SENT.value


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, disable_web_page_preview=True)

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INFO, disable_web_page_preview=True)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Errors.WRONG_COMMAND)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning("Update '%s' caused error '%s'", update, context.error)

# Easer egg
async def iloveyou(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text=ILOVEYOU)

# Easer egg
async def random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    memes = listdir('memes')
    i = random.randrange(len(memes))
    meme_to_post = path.join('memes', memes[i])
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=meme_to_post)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return None

    try:
        message = str(update.message.text)

        logger.info(LogMessages.REQUEST_WAS_RECIEVED.value.format(message))
        user_id = str(update.effective_chat.id)

        await context.bot.send_message(chat_id=user_id, text=ResponseMessages.REQUEST_RECIEVED.value)
        logger.info(RESPONSE.format(ResponseMessages.REQUEST_RECIEVED.value))

        # Обработка сообщения:
        message_parts = MessageDataObject(message)
        logger.info(Result.MESSAGE_PROCESSED.value)

        # Инициализация сообщения:
        request_type = REQUEST_TYPE[message_parts.command_type]

        data_object: TrackRequestType|ListRequestType|VideoRequestType = request_type(user_id, *message_parts.command_data)
        logger.info(Result.DATA_STORED.value)

        # Проверка длинны ссылки:
        logger.info('Проверка ссылки начата')
        url_check_result = data_object.check_url_length()
        logger.info(url_check_result)

        # Подготовка к скачиванию и скачивание:
        logger.info('Скачивание начато')
        data_object.download()
        logger.info(Result.DOWNLOAD.value.format(data_object.file_name))

        # Отправка файла пользователю:
        file_path = path.join(user_id, data_object.file_type.format(data_object.file_name))
        logger.info('Отправка файла начата')
        await context.bot.send_document(chat_id=update.effective_chat.id, document=file_path)
        logger.info(Result.SENT.value.format(data_object.file_name))

    except Exception as exception:
        logger.error(str(exception))
        await context.bot.send_message(chat_id=user_id, text=f'Произошла ошибка при скачивании {data_object.url}')
        logger.info(RESPONSE.format(f'Произошла ошибка при скачивании {data_object.url}'))

    finally:
        # Удаление или перемещение файла после отправки:
        try:
            if message_parts.delete_after_sending:
                data_object.delete_file()
                logger.info(Result.DELETED.value.format(data_object.file_name))
            else:
                data_object.move_file()
                logger.info(Result.MOVED.value.format(data_object.file_name))

        except Exception as ex:
            logger.error(ex)
            logger.error(f'Файл по ссылке {data_object.url} не был удалён или перемещён')


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    commands_handler = CommandHandler('commands', commands)
    info_handler = CommandHandler('info', info)
    love = CommandHandler('iloveyou', iloveyou)
    meme = CommandHandler('meme', random_meme)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(message_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(commands_handler)
    application.add_handler(info_handler)
    application.add_handler(love)
    application.add_handler(meme)
    application.add_handler(unknown_handler)
    application.add_error_handler(error)

    application.run_polling()


if __name__ == '__main__':
    main()
