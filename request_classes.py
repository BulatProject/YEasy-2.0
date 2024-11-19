from pytubefix import YouTube
from pytubefix.cli import on_progress
 
from base_classes import BaseRequestType
from custom_objects import CustomException
from TEXTS import Errors, MP3, Result


class TrackRequestType(BaseRequestType):
    "Класс для комманды \"трек\""

    def download(self) -> str:
        youtube_object = YouTube(self.url, on_progress_callback=on_progress)

        try:
            youtube_stream = youtube_object.streams.get_audio_only()

            if not self.file_name:
                self.author = youtube_object.author
                self.title = youtube_object.title

            title_result = self.make_title()
            
            youtube_stream.download(mp3=True,
                                    output_path=self.user_id,
                                    filename=self.file_name)

            tag_set_result = self.set_mp3_tags()

            return title_result + '\n' + self.file_name

        except Exception as ex:
            raise CustomException(
                Errors.DOWNLOAD_FAILED.value.format('песню', self.url)
                + '\n'
                + str(ex))


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
