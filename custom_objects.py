import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger("YEasy 2.0")


class MessageDataObject:
    def __init__(self, message: str) -> None:
        message_parts: list[str] = message.split(',')

        for i in range(len(message_parts)):
            message_parts[i] = message_parts[i].strip()

        self.command_type: str = message_parts[0].lower()

        if message_parts[-1].lower() != 'да':
            self.command_data: list = message_parts[1:]
            self.delete_after_sending: bool = True

        else:
            self.command_data: list = message_parts[1:-1]
            self.delete_after_sending: bool = False


class CustomException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
