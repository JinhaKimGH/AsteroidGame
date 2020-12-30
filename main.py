import pygame
import random
import mysql.connector

pygame.init()


#COLORS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0,255, 0)
BLUE = (0, 0, 255)
PALE_RED = (226, 82, 82)
PALE_BLUE = (66, 66, 238)
PALE_GREEN = (84, 226, 84)
LIGHT_BLUE = (135, 206, 235)
hover_color = (255, 255, 255)
hover_color_exit = (255, 255, 255)
BROWN = (139,69,19)
pale_white = (220, 223, 227)

screen_h = 600
screen_w = 600

#SHIP VARIABLES
ship_x = screen_w//2
ship_y = screen_h - 100
ship_dx = 7
ship_dy = 7
ship_l = 20
ship_w = 20

#Ammo Variables
pellet_x = ship_x
pellet_y = ship_y
pellet_r = ship_l - 15
pellet_dy = 25
shoot = False

#Enemy Variables
enemy_x = screen_w//2
enemy_y = screen_h//2
enemy_w = 40
enemy_l = 40
enemy_dx = 5
enemy_color = PALE_GREEN
enemy = None

#Miscellaneous
score = 0
health_bar_one = GREEN
health_bar_two = GREEN
health_bar_three = GREEN

screen = pygame.display.set_mode((screen_h, screen_w))

pygame.display.set_caption('Asteroids')

title = pygame.font.Font('freesansbold.ttf', 90)
play = pygame.font.Font('freesansbold.ttf', 30)
scoreboard = pygame.font.Font('freesansbold.ttf', 30)
start = False
hit = 0
enter_name = False
string = ""
first_entry = True

def connect(string):
    cnx = mysql.connector.connect(
        user='root',
        password='jinha0704',
        database='asteroidhighscore')
    mycursor = cnx.cursor()

    sql = "INSERT into score(name, score) VALUES (%s, %s)"
    val = (string, score)
    mycursor.execute(sql, val)
    cnx.commit()
    print(mycursor.rowcount, "record inserted.")
    mycursor.close()
    cnx.close()

class Enemy:
    def __init__(self, enemy_x, enemy_y, enemy_dy=enemy_dx, enemy_w=enemy_w, enemy_l=enemy_l, hit=False, kill=False):
        self.x = enemy_x
        self.y = enemy_y
        self.dy = enemy_dy
        self.w = enemy_w
        self.l = enemy_l
        self.hit = hit
        self.kill = kill


    def event(self, pellet_list):
        global score
        pygame.draw.rect(screen, enemy_color, (self.x, self.y, self.w, self.l))
        pygame.display.update()
        for pellet in pellet_list:
            if self.x <= pellet.x <= self.x + self.l and self.y <= pellet.y <= self.y + self.w:
                score += 10
                self.hit = True


        if self.hit == True:
            del self
            return True

        else:
            self.y += self.dy
            return False


    def check(self):
        if self.hit == True:
            return True

        else:
            return False

    def enemy_damage(self):
        if self.y >= 500 and self.kill == False:
            self.kill = True
            return True

        return False


class Pellet:
    pellet_list = []
    def __init__(self, pellet_x, pellet_y, pellet_r=ship_l-15, pellet_dy=15):
        self.x = pellet_x
        self.y = pellet_y
        self.r = pellet_r
        self.dy = pellet_dy
        Pellet.append_pellet(self)

    @classmethod
    def append_pellet(cls, pellet):
        cls.pellet_list.append(pellet)

    @classmethod
    def event(cls):
        temp = cls.pellet_list.copy()
        for pellet in cls.pellet_list:
            pellet.y -= pellet.dy
            if pellet.y <= 0:
                temp.remove(pellet)
                del pellet
                continue

            else:
                pygame.draw.circle(screen, LIGHT_BLUE, (pellet.x + 10, pellet.y - 10), pellet.r)
                pygame.display.update()

        cls.pellet_list = temp


class Ship:
    def __init__(self, ship_x=ship_x, ship_y = ship_y, ship_dx = ship_dx, ship_dy = ship_dy, ship_l=ship_l, ship_w = ship_w, hit=3):
        self.x = ship_x
        self.y = ship_y
        self.dx = ship_dx
        self.dy = ship_dy
        self.l = ship_l
        self.w = ship_w
        self.hp = hit

    def event(self):
        global health_bar_one, health_bar_two, health_bar_three
        if 0 <= self.hp:
            key = pygame.key.get_pressed()
            pygame.draw.rect(screen, WHITE, (self.x, self.y, self.w, self.l))
            pygame.draw.rect(screen, health_bar_one, (self.x - 25, self.y + self.w + 10, 15, 5))
            pygame.draw.rect(screen, health_bar_two, (self.x, self.y + self.w + 10, 15, 5))
            pygame.draw.rect(screen, health_bar_three, (self.x + 25, self.y + self.w + 10, 15, 5))
            screen.blit(board, boardRect)
            pygame.display.update()

            if key[pygame.K_d]:
                self.x += self.dx
                if self.x + self.l >= screen_w:
                    self.x = screen_w + self.l

            if key[pygame.K_a]:
                self.x -= self.dx
                if self.x <= 0:
                    self.x = 0

            if key[pygame.K_SPACE] and len(Pellet.pellet_list) <= 1:
                temp = Pellet(self.x, self.y)

            if self.hp == 0:
                health_bar_one = health_bar_three = health_bar_two = GREEN

            if self.hp == 2:
                health_bar_one = RED

            if self.hp == 1:
                health_bar_two = RED

main = Ship()

run = True
while run:
    if enter_name == False:
        screen.fill(BLACK)
    board = scoreboard.render(str(score), True, WHITE)
    boardRect = board.get_rect()
    boardRect.center = (550, 20)
    caption = title.render('Asteroids', True, WHITE)
    captionRect = caption.get_rect()
    captionRect.center = (300, 200)
    title_bg = title.render('Asteroids', True, pale_white)
    titleRect = title_bg.get_rect()
    titleRect.center = (304, 204)
    home = play.render('Home', True, hover_color)
    homeRect = home.get_rect()
    homeRect.center = (300, 450)
    text = play.render('Play', True, hover_color)
    textRect = text.get_rect()
    textRect.center = (300, 300)
    exit = play.render('Exit', True, hover_color_exit)
    exitRect = exit.get_rect()
    exitRect.center = (300, 350)
    key = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if not start:
        screen.blit(title_bg, titleRect)
        screen.blit(caption, captionRect)
        screen.blit(text, textRect)
        screen.blit(exit, exitRect)
        pygame.display.update()

        if 269 <= pos[0] <= 332 and 336 <= pos[1] <= 360:
            hover_color_exit = RED
            if click[0] == 1:
                run = False

        if 331 < pos[0] or pos[0] < 268 or 361 < pos[1] or pos[1] < 335:
            hover_color_exit = WHITE

        if 269 <= pos[0] <= 332 and 284 <= pos[1] <= 306:
            hover_color = GREEN
            if click[0] == 1:
                start = True
                hit = 0

        if 331 < pos[0] or pos[0] < 268 or 307 < pos[1] or pos[1] < 283:
            hover_color = WHITE

    if start:
        if main.hp != 0:
            if not enemy:
                enemy = Enemy(random.randint(100, 500), random.randint(1, 100))

            screen.fill(BLACK)
            main.event()
            Pellet.event()
            if enemy:
                enemy.event(Pellet.pellet_list)
                if enemy.check() == True:
                    enemy = Enemy(random.randint(100, 500), random.randint(1, 100))

                if enemy.kill == True:
                    del enemy
                    enemy = Enemy(random.randint(100, 500), random.randint(1, 100))


                if enemy.enemy_damage() == True:
                    main.hp -= 1
                    score -= 10

        if main.hp == 0:
            health_bar_three = RED
            enemy_dx = 0
            screen.fill(BLACK)
            end_screen = title.render('GAME OVER', True, WHITE)
            end_screen_bg = title.render('GAME OVER', True, pale_white)
            end_screenRect = end_screen.get_rect()
            end_screen_bgRect = end_screen_bg.get_rect()
            end_screenRect.center = (300, 200)
            end_screen_bgRect.center = (304, 204)
            score_one = scoreboard.render('Score:', True, WHITE)
            score_numbers = scoreboard.render(str(score), True, WHITE)
            scoreRect = score_one.get_rect()
            score_numbersRect = score_numbers.get_rect()
            scoreRect.center = (250, 400)
            score_numbersRect.center = (350, 400)
            screen.blit(score_one, scoreRect)
            screen.blit(score_numbers, score_numbersRect)
            screen.blit(end_screen_bg, end_screen_bgRect)
            screen.blit(end_screen, end_screenRect)
            pygame.display.update()
            enter_name = True

        if enter_name == True:

            if key[pygame.K_a]:
                string += "a"

            if key[pygame.K_b]:
                string += "b"

            if key[pygame.K_c]:
                string += "c"

            if key[pygame.K_d]:
                string += "d"

            if key[pygame.K_e]:
                string += "e"

            if key[pygame.K_f]:
                string += "f"

            if key[pygame.K_g]:
                string += "g"

            if key[pygame.K_h]:
                string += "h"

            if key[pygame.K_i]:
                string += "i"

            if key[pygame.K_j]:
                string += "j"

            if key[pygame.K_k]:
                string += "k"

            if key[pygame.K_l]:
                string += "l"

            if key[pygame.K_m]:
                string += "m"

            if key[pygame.K_n]:
                string += "n"

            if key[pygame.K_o]:
                string += "o"

            if key[pygame.K_p]:
                string += "p"

            if key[pygame.K_q]:
                string += "q"

            if key[pygame.K_r]:
                string += "r"

            if key[pygame.K_s]:
                string += "s"

            if key[pygame.K_t]:
                string += "t"

            if key[pygame.K_u]:
                string += "u"

            if key[pygame.K_v]:
                string += "v"

            if key[pygame.K_w]:
                string += "w"

            if key[pygame.K_x]:
                string += "x"

            if key[pygame.K_y]:
                string += "y"

            if key[pygame.K_z]:
                string += "z"

            if key[pygame.K_BACKSPACE]:
                string = string[:len(string)-1]

            if key[pygame.K_RETURN]:
                if first_entry == True:
                    first_entry = False
                    connect(string)

            name = play.render(string, True, WHITE)
            nameRect = caption.get_rect()
            nameRect.center = (300, 350)

            screen.blit(name, nameRect)
            pygame.display.update()
            pygame.time.delay(80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

quit()


