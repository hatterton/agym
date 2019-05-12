class Config:
    def __init__(self):
        self.window_screen_width = 600
        self.window_screen_height = 600

        self.env_width = 450
        self.env_height = 500

        self.mb_width = 150
        self.mb_height = 60
        self.menu_height = 400

        self.space_target = 60
        self.target_width = 62
        self.target_height = 22
        self.width_target_wall = 8

        self.cirle_color = (200, 50, 50)
        self.bg_color = (130, 130, 130)
        self.ga_bg_color = (130, 160, 230)

        self.max_lives = 1
        self.default_reward = 10
        self.catch_reward = 250


        self.max_fps = 100

        self.length_of_log = 100
