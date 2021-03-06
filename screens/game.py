import pygame
import time
import random

from models.ship import Player, Enemy
from utils.collide import collide

from constants import WIDTH, HEIGHT, BG, CANVAS, heartImage, score_list

def game():
    run = True
    FPS = 60
    lives = 5
    level = 0
    player_vel = 5
    laser_vel = 10

    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 70)
    win_font = pygame.font.SysFont('comicsans', 70)

    enemies = []
    wave_length = 0
    enemy_vel = 1

    player = Player(300, 585)

    clock = pygame.time.Clock()

    lost = False
    win = False
    boss_entry = True

    def redraw_window():
        CANVAS.blit(BG, (0, 0))

        # Lives
        for index in range(1, lives + 1):
            CANVAS.blit(heartImage, (37 * index - 10, 20))

        # Draw Text
        level_label = main_font.render(f'{level} / 10', 1, (0, 255, 255))
        score_label = main_font.render(f'{player.get_score()}', 1, (0, 255, 0))

        CANVAS.blit(level_label, (30, 75))
        CANVAS.blit(score_label, (WIDTH - score_label.get_width() - 30, 20))

        player.draw(CANVAS)

        for enemyShip in enemies:
            enemyShip.draw(CANVAS)

        if win:
            score_list.append(player.get_score())
            win_label = win_font.render('WINNER :)', 1, (0, 209, 0))
            CANVAS.blit(win_label, (WIDTH//2 - win_label.get_width()//2, 350))

        if lost:
            score_list.append(player.get_score())
            lost_label = lost_font.render('GAME OVER :(', 1, (255, 0, 0))
            CANVAS.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, 350))

        if level >= 10 and boss_entry:
            last_label = lost_font.render('BOSS LEVEL!!', 1, (255, 0, 0))
            CANVAS.blit(last_label, (WIDTH//2 - last_label.get_width()//2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives > 0:
            if player.health <= 0:
                lives -= 1
                player.health = 100
        else:
            lost = True
            redraw_window()
            time.sleep(3)
            run = False

        if level == 10 and boss_entry:
            redraw_window()
            time.sleep(2)
            boss_entry = False
        elif level > 10:
            win = True
            redraw_window()
            time.sleep(3)
            run = False

        if len(enemies) == 0:
            level += 1
            wave_length += 4

            for i in range(wave_length if level < 10 else 1):
                enemies.append(Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easy', 'medium', 'hard']) if level < 10 else 'boss')
                )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        # Return to main page
        if keys[pygame.K_BACKSPACE]:
            run = False

        # Left Key
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (player.x - player_vel) > 0:
            player.x -= player_vel
        # Right Key
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (player.x + player_vel + player.get_width()) < WIDTH:
            player.x += player_vel
        # Up Key
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and (player.y - player_vel) > 0:
            player.y -= player_vel
        # Down Key
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (player.y + player_vel + player.get_height()) < HEIGHT:
            player.y += player_vel
        # Shoot Laser
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.SCORE += 50
                if enemy.ship_type == 'boss':
                    if enemy.boss_max_health - 5 <= 0:
                        enemies.remove(enemy)
                        enemy.boss_max_health = 100
                        player.health -= 100
                    else:
                        enemy.boss_max_health -= 5
                        player.health -= 100
                else:
                    player.health -= 10
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)