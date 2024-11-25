def event(cls):

    def apply(self):
        return self.payload.apply()

    if not getattr(cls, "payload", False):
        raise Exception("No payload defined")
    if not getattr(cls, "topic", False):
        cls.topic = ""

    cls.apply = apply
    cls.is_event = True
    return cls
