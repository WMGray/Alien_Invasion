# 创建一个用于跟踪游戏统计信息的类

class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 游戏刚启动时处于不活动状态
        self.game_active = False

        # 任何情况下都不应重置最高分
        self.high_score = 0


    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit  # 飞船剩余数量
        self.score = 0  # 初始化分数为0
        self.level = 1  # 初始化等级为1
