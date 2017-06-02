class CommandBase:

    def __init__(self, *args, **kwargs):
        self.sdk = kwargs['sdk']
