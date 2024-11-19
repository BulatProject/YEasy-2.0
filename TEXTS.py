import enum

EXAMPLES = ('https://youtu.be/', 'youtu.be/', 'https://www.youtube.com/watch?', 'youtube.com/watch?', 'https://youtube.com/playlist?', 'youtube.com/playlist?')

CLEAN_LINK = f'Ссылка на видео должна начинаться как один из примеров и быть не длиннее 130 символов:\n"{EXAMPLES[0]}"\n"{EXAMPLES[1]}"\n"{EXAMPLES[2]}"\n"{EXAMPLES[3]}"\n"{EXAMPLES[4]}"\n"{EXAMPLES[5]}"'

class Errors(enum.Enum):
    BAD_LINK = f"Ссылка не соответстует требованиям:\n{CLEAN_LINK}"
    DOWNLOAD_FAILED = r'Не удалось загрузить {} по ссылке: {}'
    COMMA_MESSAGE_ERROR = 'Нет запятой - диапазон не распознан.'
    HYPHEN = 'Нет дефиса - диапазон не распознан.'
    SYMBOLS_ERROR = 'В диапазоне есть лишние символы - диапазон не распознан.'
    RANGE_ERROR = 'Количество песен, которое вы хотите скачать: {}. Это не соответствует правилам.'
    INSTRUCTION_ERROR = 'Сообщение должно начинаться с символов "трек," или "лист,".'
    LENGHT_ERROR = f'Ошибка.\nПроверьте свою команду:\n{INSTRUCTION_ERROR}'
    NO_FIRST_NUM_ERROR = 'Вы пропустили первое число диапазона.'
    RANGE_TOO_BIG = 'Диапазон не может быть больше размера плейлиста.'
    WRONG_COMMAND = "Эта комманда не поддерживается."
    TAGS = 'Композиции {} не были присвоены теги.\nОшибка: {}'


class BanList(enum.Enum):
    SYSTEM_SYMBOLS = "(\s)?[\/\\:*?<>|\"'@#]"
    TITLE_EXESSIVE_DATA = "([\[\(]?(official|lyric(s)?)(\s)*(lyric(s)?)?(\s)*(music|hd|hq)?(\s)*(video|audio)?(\s)?(by.*)?[\]\)]?|\[cc\]|[\[\(](video|audio|hd|hq)(\s)?(by.*)?[\]\)]|[\[\(]?(music video|high quality)[\]\)]?)"
    AUTHOR_EXESSIVE_DATA = "(- topic|vevo|official|music)"


class Result(enum.Enum):
    MESSAGE_PROCESSED = 'Сообщение было успешно помещено в объект и обработано'
    DATA_STORED = 'Данные инициализированы'
    LENGTH = 'Длина ссылки {} менее 131 символа'
    TITLES = 'Название композиции {} было успешно изменено'
    TAGS = 'Композиции {} были присвоены теги'
    DOWNLOAD = 'Файл {} был успешно скачан'
    SENT = 'Файл {} был успешно отправлен'
    DELETED = 'Файл {} был успешно удалён'
    MOVED = 'Файл {} был успешно перемещён'


class ResponseMessages(enum.Enum):
    REQUEST_RECIEVED = 'Запрос обрабатывается, ожидайте.'


class LogMessages(enum.Enum):
    REQUEST_WAS_RECIEVED = "Сообщение \"{}\" было получено"
    RESPONSE_WAS_SENT = "Сообщение \"{}\" было отправлено пользователю"


SYSTEM_SYMBOLS = ('/', '\\', ':', '*', '?', '<', '>', '|', '"', "'", '@', '#')
BAN_LIST = ('(Official Video)', '(Official Music Video)', '(Official Audio)', '(Music Video)', 
    '(OFFICIAL VIDEO)', '(OFFICIAL MUSIC VIDEO)', '(OFFICIAL AUDIO)', '(MUSIC VIDEO)',
    '[Official Video]', '[Official Music Video]', '[Official Audio]', '[Music Video]',
    '[OFFICIAL VIDEO]', '[OFFICIAL MUSIC VIDEO]', '[OFFICIAL AUDIO]', '[MUSIC VIDEO]',
    'Official Video', 'Official Music Video', 'Official Audio', 'Music Video',
    'OFFICIAL VIDEO', 'OFFICIAL MUSIC VIDEO', 'OFFICIAL AUDIO', 'MUSIC VIDEO',
    '(Official HD Video)', '(Official HQ Video)', '(High Quality)', '(HIGH QUALITY)', 
    '(OFFICIAL HD VIDEO)', '(OFFICIAL HQ VIDEO)', '(Video)', '(Audio)', '[Audio]',
    '(Official Lyrics Video)', '(Lyric Video)', '(VIDEO)', '(AUDIO)', '[AUDIO]',
    '[Official Lyrics Video]', '[Lyric Video]',
    '(lyrics)', '(Lyrics)', '(LYRICS)',
    '[lyrics]', '[Lyrics]', '[LYRICS]',
    'Lyrics', 'lyrics', 'LYRICS',
    '(hd)', '(hq)', '[hd]', '[hq]',
    '(HD)', '(HQ)', '[HD]', '[HQ]', '[CC]')

MP3 = r"{}.mp3"

START = 'Перед использованием ОБЯЗАТЕЛЬНО прочтите описание и инструкцию по использованию бота, введя: "/help" и "/info".'
HELP = '''\
Данный бот предназначен для скачивания песен с YouTube, но его можно использовать и для скачивания аудиоряда из любого видео.

Скачивать песни можно как по одной, так группой из плейлистов.

Воздержитесь от скачивания видео с нестандартными символами в названии.

ВАЖНО!
Бот автоматически убирает из названия песни следующие символы (в теги они тоже не попадут):
'/', '\\', ':', '*', '?', '<', '>', '|', '"', "'", '@', '#'.
Также из названия песни будут убраны упоминания о том, что это официальное/HD видео/аудио.
Пример:
'official video', 'official music video', 'official audio', 'music video', \
(high quality), (video)', '(Audio)', '[audio]', \
'(lyrics)', '(hd)', '(hq)', '[CC]'.

Также он заполняет теги "исполнители" и "название".
Если в названии видео нет символа "-", то название видео становится названием трека, а название канала - именем исполнителя.
В противном случае он делит название видео пополам, и левая часть становится именем исполнителя, а правая - названием трека.

После скачивания, соответственно, советую подкорректировать теги, если это имеет для вас значение.

Чтобы посмотреть доступные команды, наберите /commands.\
'''

COMMANDS = \
'''
/start - запустить бота.
/info - инструкция по работе с ботом.
/help - узнать основную информацию о боте (перед использование ОБЯЗАТЕЛЬНО ознакомьтесь).
/commands - получить эту инструкцию.\
'''

INFO = \
f'''ВАЖНО. Если видео, аудиоряд которого вы хотите скачать, имеет возрастные или иные ограничения, то видео скачано не будет!

Использовать бота просто:
Введите: "Трек, ССЫЛКА_НА_ВИДЕО", - и отправьте сообщение, если хотите скачать аудиоряд из одного видео.

Пример:
Трек, https://youtu.be/Z6kNQEzQJpA

{CLEAN_LINK}

Если же вы хотите скачать видео из плейлиста, то инструкция следующая:
Введите: "Лист, ДИАПАЗОН, ССЫЛКА_НА_ППЛЕЙЛИСТ".
Диапазон, в котором находятся треки, должен быть не больше 20.

Пример:
Лист, 1-21, https://youtube.com/playlist?list=КОДПЛЕЙЛИСТА

В данном случае скачаны будут первые 20 песен из указанного плейлиста.
Если в вашем диапазоне больше 20 песен, то песни скачаны не будут.
Если в плейлисте меньше песен, нежели в диапазоне, что вы указали, песни скачаны не будут.

К сожалению, каждый раз вам придётся присылать ссылку и диапазон заново.
Возможно, в будущем это неудобство будет устранено.\
'''


ILOVEYOU = 'Обнимаю и целую. =3'

