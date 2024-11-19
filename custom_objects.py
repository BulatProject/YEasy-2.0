class MessageDataObject:
    def __init__(self, message: str) -> None:
        self.type = 'трек'
        message_parts: list[str] = message.split(',')

        for element in message_parts:
            element = element.strip()

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
