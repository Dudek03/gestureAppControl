class Screen_helper:
    _screen = None
    _size = None

    @classmethod
    def set_screen(cls, screen):
        cls._screen = screen

    @classmethod
    def set_screen_size(cls, screen_size):
        cls._size = screen_size

    @classmethod
    def get_screen(cls):
        if cls._screen is None:
            raise Exception("Screen not initialized! Call set_screen first.")
        return cls._screen

    @classmethod
    def get_size(cls):
        if cls._size is None:
            raise Exception("Screen size not set!")
        return cls._size
