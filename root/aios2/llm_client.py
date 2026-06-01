    def __call__(self, messages: list, tools: dict = None, stream: bool = True) -> dict:
        """Make instance callable - forwards stream parameter to chat()."""
        return self.chat(messages, tools, stream=stream)
