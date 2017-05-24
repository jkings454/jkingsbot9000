class CommandParser():
    def __init__(self, prefix):
        if len(prefix) > 1:
            raise InvalidPrefixError

        self.prefix = prefix

    def parse(self, message):
        tokenized = message.split()
        if tokenized[0].startswith(self.prefix):
            command = tokenized[0][1:]
        else:
            return None

        args = None

        if len(tokenized) > 1:
            args = tokenized[1:]

        return Command(command, args)

class Command():
    """
    Represents a bot command
    """
    def __init__(self, command, args):
        self.command = command
        self.args = args


class InvalidPrefixError(RuntimeError):
    def __init__(self):
        super(InvalidPrefixError, self).__init__("The prefix provided is invalid")