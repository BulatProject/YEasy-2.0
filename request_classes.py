from pytubefix import YouTube
from pytubefix.cli import on_progress
 
from base_classes import BaseRequestType
from custom_objects import CustomException, logger
from TEXTS import Errors, Result, MediaTypes


class TrackRequestType(BaseRequestType):
    "Класс для комманды \"трек\""

    def download(self) -> None:
        youtube_object = YouTube(self.url, on_progress_callback=on_progress)

        try:
            youtube_stream = youtube_object.streams.get_audio_only()

            if not self.file_name:
                self.author = youtube_object.author
                self.title = youtube_object.title
            logger.info('Корректировка названия начинается')
            title_result = self.make_title()
            logger.info(title_result)

            youtube_stream.download(
                output_path=self.user_id,
                filename=MediaTypes.M4A.value.format(self.fixed_file_name))

            logger.info(Result.DOWNLOAD.value.format(self.file_name))

            logger.info('Конвертация файла начинается')
            self.convert_to_mp3()

            logger.info('Переименование файла начинается')
            self.rename_file()

            tag_set_result = self.set_mp3_tags()
            logger.info(tag_set_result)

        except Exception as ex:
            logger.info(str(ex))
            raise CustomException(
                Errors.DOWNLOAD_FAILED.value.format('песню', self.url))


class ListRequestType(BaseRequestType):
    "Класс для комманды \"лист\""

    def __init__(self, user_id: str, range: str, url: str, file_name: str = None) -> None:
        self.type = 'Лист'
        self.user_id = user_id
        self.range = range.strip()
        self.url = url.strip()
        self.file_name = file_name.strip()


class VideoRequestType(BaseRequestType):
    "Класс для комманды \"видео\""

    def check_for_youtube(self) -> None:    # Зачем вообще проверять? А, чтобы выбрать, pytube или dlp
        self.url
