class UI_settings:
    _board_pos_mul = 0.1
    _board_size_mul = 0.8
    _middle_line_color = "pink"
    _board_line_color = "pink"
    _player_size_mul = 0.05
    _player_circle_color = "pink"
    _screen_start_size = (1280, 720)
    _screen_fill_color = "black"
    _puck_size_mul = 0.05
    _puck_color = "pink"
    _score_font = (None,100)

    @classmethod
    def get_board_pos_mul(cls):
        return cls._board_pos_mul
    
    @classmethod
    def get_board_size_mul(cls):
        return cls._board_size_mul 
    
    @classmethod
    def get_middle_line_color(cls):
        return cls._middle_line_color
    
    @classmethod
    def get_board_line_color(cls):
        return cls._board_line_color
    
    @classmethod
    def get_player_size_mul(cls):
        return cls._player_size_mul
    
    @classmethod
    def get_player_circle_color(cls):
        return cls._player_circle_color
    
    @classmethod
    def get_screen_start_size(cls):
        return cls._screen_start_size

    @classmethod
    def get_screen_fill_color(cls):
        return cls._screen_fill_color

    @classmethod 
    def get_puck_size_mul(cls):
        return cls._puck_size_mul    
    
    @classmethod
    def get_puck_color(cls):
        return cls._puck_color
    
    @classmethod
    def get_score_font(cls):
        return cls._score_font