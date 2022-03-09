
# 创建一个表示游戏的类 以创建空的pygame窗口

import sys
from time import sleep

import pygame

from alien import Alien           # 导入外星人类
from bullet import Bullet         # 导入子弹类
from game_stats import GameStats  # 导入统计信息类
from settings import Settings     # 导入设置类
from ship import Ship             # 导入飞船类
from button import Button         # 导入按钮类
from scoreboard import Scoreboard # 导入记分牌类



class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        """
        # 初始化一个准备显示的窗口或屏幕
        self.screen = pygame.display.set_mode((1200, 800)) 
        # 设置窗口背景
        self.bg_color = (150, 150, 200)
        # 全屏模式
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        """
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 设置窗口标题
        pygame.display.set_caption("外星人入侵!!")
        # 创建Ship实例
        self.ship = Ship(self)
        # 创建用于存储子弹的编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人编组
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        # 创建Play按钮
        self.play_button = Button(self, "Play")
        # 创建记分牌实例
        self.scoreboard = Scoreboard(self)


    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人
        alien = Alien(self)

        # 计算一行可容纳多少个外星人
        available_space_x = self.settings.screen_width - (
                    1.5 * alien.rect.width)
        number_alien_x = available_space_x // (1.5 * alien.rect.width)

        # 计算一列可以容纳多少个外星人
        available_space_y = self.settings.screen_height - (
                    2.2 * alien.rect.height)
        number_alien_y = available_space_y // (2.2 * alien.rect.height)

        # 创建外星人群
        for alien_number in range(int(number_alien_x)):
            self._create_alien(alien_number, 1)
        '''for row_number in range(int(number_alien_y)):
        for alien_number in range(int(number_alien_x)):
          self._create_alien(alien_number, row_number)'''

    def _create_alien(self, alien_number, row_number):
        '''创建一个外星人并肩齐放在当前行'''
        # 创建一个外星人并加入当前行
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien.rect.width + 1.5 * alien.rect.width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_events(self):
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # 接收到退出事件后退出游戏
            elif event.type == pygame.KEYDOWN:  # 检测按下按键
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:  # 检测到松开按键
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_botton(mouse_pos)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:  # q--退出
            sys.exit()
        if event.key == pygame.K_RIGHT:  # 检测按键是否是右箭头
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 检测按键是否是左箭头
            # 向左移动飞船
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:  # 空格--开火
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:  # 右箭头--移动
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:  # 左箭头--移动
            self.ship.moving_left = False

    def _check_play_botton(self, mouse_pos):
        """在玩家单击Pkay按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.scoreboard.prep_ships()
            # 清空余下的子弹和外行星
            self.bullets.empty()
            self.aliens.empty()
            # 创建新的外星人，并让飞船剧中
            self._create_fleet()
            self.ship.center_ship()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_fleet_edges(self):
        '''有外星人到达边缘时采取相应的措施'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整群外星人下移，并改变他们的方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        '''检查是否有外星人到达了屏幕底端'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens:
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞一样处理
                self._ship_hit()
                break

    def _fire_bullet(self):
        '''创建一颗子弹，并将其加入编组bullets中'''
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        '''响应飞船和外星人碰撞'''
        if self.stats.ships_left > 0:
            # 将ships_left - 1 并更新飞船图像
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()

            # 清空余下的外星人和子弹
            self.bullets.empty()
            self.aliens.empty()

            # 创建新的外星人和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)  # 游戏结束 显示鼠标光标

    def _update_bullets(self):
        '''更新子弹位置并删除消失的子弹'''
        self.bullets.update()
        # 删除消失的子弹
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''响应子弹和外星人碰撞'''
        # 检查是否有子弹击中外星人
        # 如果是这样，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens, True, True)
        # 如果击中，更新分数
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_score * len(aliens)
                self.scoreboard.prep_score()
                self.scoreboard.check_high_score()
        # 如果外星人全部消灭，就重新创建一群外星人,并更新游戏等级
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            # 加快游戏节奏
            self.settings.increase_speed()
            # 提高游戏等级
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _update_aliens(self):
        '''更新外星人群中所有外星人的位置'''
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达了屏幕底端
        self._check_aliens_bottom()

    def _update_screen(self):
        ''''更新频幕上的图像，并切换到新屏幕'''
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw_bullet()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 绘制记分牌
        self.scoreboard.show_score()
        # 如果游戏处于非活动状态-->绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()


if __name__ == "__main__":
    # 创建一个游戏实例
    alien_invasion = AlienInvasion()
    # 调用run_game()方法开始游戏
    alien_invasion.run_game()
