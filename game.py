# 1 - Import library
import math
import random

import pygame

# 2 - Initialize the game
pygame.init()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]

player_pos = [100, 100]
acc = [0, 0]
arrows = []
bad_timer = 100
bad_timer1 = 0
bad_guys = [[640, 100]]
health_value = 194

pygame.mixer.init()

# 3 - Load image
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
bad_guy_img1 = pygame.image.load("resources/images/badguy.png")
bad_guy_img = bad_guy_img1
health_bar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
game_over = pygame.image.load("resources/images/gameover.png")
you_win = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 4 - keep looping through
running = 1
exitcode = 0
while running:
    bad_timer -= 1

    # 5 - clear the screen before drawing it again
    screen.fill(0)

    # 6 - draw the player on the screen at X:100, Y:100
    for x in range(width // grass.get_width() + 1):
        for y in range(height // grass.get_height() + 1):
            screen.blit(grass, (x * 100, y * 100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # 6.1 - Set player position and rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1] - (player_pos[1] + 32), position[0] - (player_pos[0] + 26))
    player_rot = pygame.transform.rotate(player, 360 - angle * 57.29)
    player_pos1 = (player_pos[0] - player_rot.get_rect().width / 2, player_pos[1] - player_rot.get_rect().height / 2)
    screen.blit(player_rot, player_pos1)
    # 6.2 - Draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360 - projectile[0] * 57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    # 6.3 - Draw badgers
    if bad_timer == 0:
        bad_guys.append([640, random.randint(50, 430)])
        bad_timer = 100 - (bad_timer1 * 2)
        if bad_timer1 >= 35:
            bad_timer1 = 35
        else:
            bad_timer1 += 5
    index = 0
    for bad_guy in bad_guys:
        if bad_guy[0] < -64:
            bad_guys.pop(index)
        bad_guy[0] -= 7

        # 6.3.1 - Attack castle
        bad_rect = pygame.Rect(bad_guy_img.get_rect())
        bad_rect.top = bad_guy[1]
        bad_rect.left = bad_guy[0]
        if bad_rect.left < 64:
            hit.play()
            health_value -= random.randint(5, 20)
            bad_guys.pop(index)

        # 6.3.2 - Check for collisions
        index1 = 0
        for bullet in arrows:
            bull_rect = pygame.Rect(arrow.get_rect())
            bull_rect.left = bullet[1]
            bull_rect.top = bullet[2]
            if bad_rect.colliderect(bull_rect):
                enemy.play()
                acc[0] += 1
                bad_guys.pop(index)
                arrows.pop(index1)
            index1 += 1

        # 6.3.3 - Next bad guy
        index += 1
    for bad_guy in bad_guys:
        screen.blit(bad_guy_img, bad_guy)

    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    survived_text = font.render(
        str((90000 - pygame.time.get_ticks()) / 60000) + ":" + str((90000 - pygame.time.get_ticks()) / 1000 % 60).zfill(
            2), True, (0, 0, 0))

    textRect = survived_text.get_rect()
    textRect.topright = [635, 5]
    screen.blit(survived_text, textRect)

    # 6.5 - Draw health bar
    screen.blit(health_bar, (5, 5))
    for health1 in range(health_value):
        screen.blit(health, (health1 + 8, 8))

    # 7 - update the screen
    pygame.display.flip()

    # 8 - loop through the events
    for event in pygame.event.get():
        # check if the event is the X button 
        if event.type == pygame.QUIT:
            # if it is quit the game
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            elif event.key == pygame.K_a:
                keys[1] = True
            elif event.key == pygame.K_s:
                keys[2] = True
            elif event.key == pygame.K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append(
                [math.atan2(position[1] - (player_pos1[1] + 32), position[0] - (player_pos1[0] + 26)),
                 player_pos1[0] + 32,
                 player_pos1[1] + 32])

    # 9 - Move player
    if keys[0]:
        player_pos[1] -= 5
    elif keys[2]:
        player_pos[1] += 5
    if keys[1]:
        player_pos[0] -= 5
    elif keys[3]:
        player_pos[0] += 5

    # 10 - Win/Lose check
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if health_value <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0

# 11 - Win/lose display
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (255, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(game_over, (0, 0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: " + str(accuracy) + "%", True, (0, 255, 0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(you_win, (0, 0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
