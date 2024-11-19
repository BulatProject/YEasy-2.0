import os.path as path
import re
from os import remove, replace

import eyed3

from custom_objects import CustomException
from TEXTS import Errors, BanList, MP3, Result


class BaseRequestType():
    "Базовый класс для всех типов комманд"

    def __init__(self, user_id: str, url: str, file_name: str = None) -> None:
        self.user_id = user_id
        self.url = url
        if file_name:
            self.author, self.title = file_name.split(' - ', 1)
        self.file_name = file_name

    def check_url_length(self) -> None:
        "Проверка длины url из сообщения пользователя"
        if len(self.url) > 131:
            raise CustomException(Errors.BAD_LINK.value)

        return Result.LENGTH.value.format(self.url)

    def make_title(self) -> str:
        system_symbols = BanList.SYSTEM_SYMBOLS.value

        # Если в названии видео нет тире,
        # вместо автора указываем название канала
        if ' - ' not in self.title:
            # Проверяем название канала и видео на наличие специальных символов:
            pre_author: str = re.sub(pattern=system_symbols,
                                     repl='',
                                     string=self.author,
                                     flags=re.IGNORECASE).strip()

            pre_title: str = re.sub(pattern=system_symbols,
                                    repl='',
                                    string=self.title,
                                    flags=re.IGNORECASE).strip()

        else:
            # Если в названии видео есть тире,
            # левая часть станет названием исполнителя
            altered_title: str = re.sub(pattern=system_symbols,
                                        repl='',
                                        string=self.title,
                                        flags=re.IGNORECASE).strip()

            pre_author, pre_title = altered_title.split(' - ', 1)

        # Очищенные от спецсимволов названия по отдельности очищаем от
        # лишних описаний и добавляем в атрибуты объекта
        self.author = re.sub(pattern=BanList.AUTHOR_EXESSIVE_DATA.value,
                             repl='',
                             string=pre_author,
                             flags=re.IGNORECASE).strip()

        self.title = re.sub(pattern=BanList.TITLE_EXESSIVE_DATA.value,
                            repl='',
                            string=pre_title,
                            flags=re.IGNORECASE).strip()

        # Очищенные названия объединяем в название файла
        self.file_name = ' - '.join((self.author, self.title))

        return Result.TITLES.value.format(self.file_name)

    def set_mp3_tags(self) -> str:
        mp3_file_name = MP3.format(self.file_name)

        try:
            base = eyed3.load(path.join(self.user_id, mp3_file_name))

            base.tag.title = self.title
            base.tag.artist = self.author

            base.tag.save()
            return Result.TAGS.value.format(self.file_name)

        except Exception as err:
            return Errors.TAGS.value.format(self.file_name, str(err))

    def delete_file(self) -> None:
        remove(path.join(self.user_id, MP3.format(self.file_name)))

    def move_file(self) -> None:
        replace(MP3.format(self.file_name), path.join('Songs', MP3.format(self.file_name)))