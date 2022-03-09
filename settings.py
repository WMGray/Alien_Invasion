# 创建设置类
class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏静态设置"""
        # 屏幕设置
        self.screen_width = 1200  # 屏幕宽度
        self.screen_height = 800  # 屏幕高度
        self.bg_color = (150, 150, 200)  # 屏幕背景色

        # 飞船设置
        self.ship_speed = 0.5  # 飞船速度
        self.ship_limit = 3  # 飞船数量限制

        # 子弹设置
        self.bullet_speed = 3  # 子弹速度
        self.bullet_width = 3  # 子弹宽度
        self.bullet_height = 15  # 子弹高度
        self.bullet_color = (60, 100, 60)   # 子弹颜色
        self.bullet_allowed = 4  # 子弹数量

        # 外星人设置
        self.alien_speed = 1  # 外星人移动速度
        self.fleet_drop_speed = 10  # 外星人下降速度
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.05

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 0.5
        self.bullet_speed = 3
        self.alien_speed = 1.0
        self.alien_score = 100   # 外星人分数

        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed += self.ship_speed * self.speedup_scale
        self.bullet_speed += self.bullet_speed * self.speedup_scale
        self.alien_speed += self.alien_speed * self.speedup_scale
        self.alien_score += int(self.alien_score * self.speedup_scale)


