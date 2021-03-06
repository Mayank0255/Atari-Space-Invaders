import pygame

from constants import WIDTH, BG, CANVAS, score_list, trophyImage

def score_board():
    run = True

    score_title_font = pygame.font.SysFont('comicsans', 60)
    score_font = pygame.font.SysFont('comicsans', 55)

    score_list.sort()
    score_list.reverse()

    while run:
        CANVAS.blit(BG, (0, 0))

        score_title_label = score_title_font.render('Score Board', 1, (0, 229, 0))
        CANVAS.blit(score_title_label, (WIDTH//2 - score_title_label.get_width()//2 - 30, 175))
        CANVAS.blit(trophyImage, (WIDTH//2 + score_title_label.get_width()//2 - 10, 163))

        i = 0
        for score in score_list[:5]:
            score_label = score_font.render(str(score), 1, (0, 255, 255))
            CANVAS.blit(score_label, (WIDTH//2 - score_label.get_width() + 20, 250 + i * 40))
            i += 1

        back_label = score_font.render('[Backspace]', 1, (255, 255, 255))
        CANVAS.blit(back_label, (30, 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            run = False