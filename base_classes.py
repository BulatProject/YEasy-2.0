import os.path as path
import re
import subprocess
from os import remove, replace, rename

import eyed3

from custom_objects import CustomException, logger
from TEXTS import Errors, BanList, MediaTypes, Result, SubprocessCommands



class BaseRequestType():
    "Базовый класс для всех типов комманд"

    def __init__(self, user_id: str, url: str, file_name: str = None) -> None:
        self.user_id = user_id
        self.url = url
        if file_name:
            self.author, self.title = file_name.split(' - ', 1)
        self.file_name = file_name
        self.m4a = MediaTypes.M4A.value
        self.file_type = MediaTypes.MP3.value

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

        logger.info('Подготовка названия начинается')
        self.replace_spaces()

        return Result.TITLES.value.format(self.file_name)

    def replace_spaces(self) -> None:
        self.fixed_file_name = self.file_name.replace(" ", "_").replace("(", "").replace(")", "")
        logger.info(f'Файл {self.file_name} готов к конвертации в mp3')

    def convert_to_mp3(self) -> str:
        input_file = path.join(self.user_id, self.fixed_file_name)
        output_file = path.join(self.user_id, self.fixed_file_name)

        command = SubprocessCommands.CONVERSION.value.format(input_file, output_file)

        try:
            logger.info(f'Конвертация файла\
                {self.fixed_file_name}.m4a в mp3 начата')

            converting = subprocess.run(command, shell=True)

            if converting.returncode == 0:
                logger.info(f'Файл {self.file_name}.m4a\
                    был успешно конвертирован в mp3')

                remove(self.m4a.format((input_file)))
                logger.info(f'Файл {self.fixed_file_name}.m4a был удалён')
                return None

            else:
                logger.info(f'Файл {self.fixed_file_name}.m4a\
                    не был конвертирован в mp3-формат')
                remove(self.m4a.format((input_file)))
                logger.info(f'Файл {self.fixed_file_name}.m4a был удалён')

        except Exception as err:
            logger.exception(err)
            remove(input_file)
            logger.info(f'Файл {self.fixed_file_name}.m4a был удалён')

            raise CustomException(f'При конвертации файла\
                {self.fixed_file_name}.m4a возникла ошибка')

    def rename_file(self):
        rename(path.join(self.user_id, self.file_type.format(self.fixed_file_name)),
               path.join(self.user_id, 
                         self.file_type.format(self.file_name)))

        logger.info('Файл был переименован')

    def set_mp3_tags(self) -> str:
        mp3_file_name = self.file_type.format(self.file_name)

        try:
            logger.info('Изменение тегов начинается')
            base = eyed3.load(path.join(self.user_id, mp3_file_name))

            base.tag.title = self.title
            base.tag.artist = self.author

            base.tag.save()
            return Result.TAGS.value.format(self.file_name)

        except Exception as err:
            logger.exception(err)
            return Errors.TAGS.value.format(self.file_name, str(err))

    def delete_file(self) -> None:
        remove(path.join(self.user_id,
                         self.file_type.format(self.file_name)))

    def move_file(self) -> None:
        replace(path.join(self.user_id,
                          self.file_type.format(self.file_name)),
                path.join(self.user_id, 
                          'Songs', self.file_type.format(self.file_name)))