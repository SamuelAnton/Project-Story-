import pygame
import sys
import os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.imagef = load_image('HeroFront.png', -1)
        self.imageb = load_image('HeroBack.png', -1)
        self.imager = load_image('HeroRight.png', -1)
        self.imagel = load_image('HeroLeft.png', -1)
        self.image = self.imagef
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, place):
        super().__init__(door_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.place = place
        self.x = pos_x
        self.y = pos_y


class Use(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, text):
        super().__init__(use_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
        self.text = text


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = (255, 255, 255, 255)
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()
            elif event1.type == pygame.KEYDOWN or \
                    event1.type == pygame.MOUSEBUTTONDOWN:
                return first_scene()
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, *aa):
    new_player, x, y = None, None, None
    ii = 0
    doorss = []
    use = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '1':
                Tile('frontwall', x, y)
            elif level[y][x] == '2':
                Tile('leftwall', x, y)
            elif level[y][x] == '3':
                Tile('rightwall', x, y)
            elif level[y][x] == '4':
                Tile('backwall', x, y)
            elif level[y][x] == '5':
                Tile('cornerlwall', x, y)
            elif level[y][x] == '6':
                Tile('cornerrwall', x, y)
            elif level[y][x] == '7':
                Tile('frontwall', x, y)
                use.append(Use('mirror', x, y,
                               ['Ты посмотрел на отражение в зеркале...',
                                'Отражение посмотрело на тебя...', 'Неловко...']))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                doorss.append(Door('door', x, y, aa[ii]))
                Tile('empty', x, y)
                ii += 1
            elif level[y][x] == '=':
                use.append(Use('bed', x, y, ['Хотя вы и устали, спать на этом совсем не хочется']))
            elif level[y][x] == '-':
                Tile('empty', x, y)
            elif level[y][x] == 's':
                Tile('empty', x, y)
                use.append(Use('prisoner1', x, y, ['* И что ты смотришь?']))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, doorss, use


def new_level(lv):
    if lv != '':
        screen.fill((0, 0, 0))
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        use_group.empty()
        door_group.empty()
        global cur_level, player, level_x, level_y, door, lvl, useful
        cur_level = load_level(lv)
        player, level_x, level_y, door, useful = generate_level(cur_level, *doors[lv])
        if lvl == 'PrisonCorridorMap.txt' and lv == 'PrisonRoomMap.txt':
            player.pos_x += 2
        elif lvl == 'PrisonHallMap.txt' and lv == 'PrisonCorridorMap.txt':
            player.pos_x += 7
            player.pos_y -= 1
        all_sprites.draw(screen)
        door_group.draw(screen)
        lvl = lv


def dialog(text):
    global talk
    talk = True
    pygame.draw.rect(screen, (255, 255, 255), ((80, 440), (1120, 240)))
    pygame.draw.rect(screen, (0, 0, 0), ((85, 445), (1110, 230)))
    font = pygame.font.Font(None, 50)
    for iii in range(len(text)):
        string_rendered = font.render(text[iii], True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 450 + iii * 60
        intro_rect.x = 100
        screen.blit(string_rendered, intro_rect)


def first_scene():
    for yy in range(1, 7):
        tic = pygame.transform.scale(load_image(str(yy) + '.jpg'), (WIDTH, HEIGHT))
        screen.blit(tic, (0, 0))
        pygame.display.flip()
        for q in range(2):
            clock.tick(1)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (160, 160, 960, 160), 1)
    font = pygame.font.Font(None, 80)
    string_rendered = font.render('Введите имя:', True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 40
    intro_rect.x = 160
    screen.blit(string_rendered, intro_rect)
    name = ''
    inputt = True
    font = pygame.font.Font(None, 200)
    while inputt:
        pygame.draw.rect(screen, (0, 0, 0), (160, 160, 960, 160))
        pygame.draw.rect(screen, (255, 255, 255), (160, 160, 960, 160), 1)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    terminate()
                if e.key == 13:
                    inputt = False
                if e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if len(name) < 6 and e.unicode in 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ':
                    name += e.unicode
        string_rendered = font.render(name, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 165
        intro_rect.x = 165
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    return name


# print('Выберите разрешение (цифру): 1)1280х720  2)1920х1080  3)2560х1440')
# a = input()
a = '1'
pygame.init()
if a == '1':
    size = WIDTH, HEIGHT = 1280, 720
    tile_width = tile_height = 80
elif a == '2':
    size = WIDTH, HEIGHT = 1920, 1080
    tile_width = tile_height = 120
else:
    size = WIDTH, HEIGHT = 2560, 1440
    tile_width = tile_height = 160
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50

tile_images = {
    'frontwall': load_image('PrisonWallFront.png'),
    'empty': load_image('PrisonGround.png'),
    'door': load_image('PrisonDoor.png', -1),
    'leftwall': load_image('PrisonWallLeft.png', -1),
    'rightwall': load_image('PrisonWallRight.png', -1),
    'backwall': load_image('PrisonWallBack.png', -1),
    'cornerlwall': load_image('PrisonWallCornerL.png', -1),
    'cornerrwall': load_image('PrisonWallCornerR.png', -1),
    'mirror': load_image('Mirror.png', -1),
    'bed': load_image('PrisonBed.png', -1),
    'prisoner1': load_image('PrisonerFront1.png', -1)
}
doors = {
    'PrisonRoomMap.txt': ['PrisonCorridorMap.txt'],
    'PrisonCorridorMap.txt': ['', '', 'PrisonHallMap.txt', 'PrisonRoomMap.txt', ''],
    'PrisonHallMap.txt': ['PrisonCorridorMap.txt', '']
}
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
use_group = pygame.sprite.Group()
cur_level = load_level('PrisonRoomMap.txt')
lvl = 'PrisonRoomMap.txt'
player, level_x, level_y, door, useful = generate_level(cur_level, 'PrisonCorridorMap.txt')
can = '.@'
talk = True
t = True
NAME = start_screen()
screen.fill((0, 0, 0))
tiles_group.draw(screen)
door_group.draw(screen)
use_group.draw(screen)
player_group.draw(screen)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not talk:
                player.image = player.imagel
                if player.pos_x > 0 and cur_level[player.pos_y][player.pos_x - 1] in can:
                    player.pos_x -= 1
            if event.key == pygame.K_RIGHT and not talk:
                player.image = player.imager
                if cur_level[player.pos_y][player.pos_x + 1] in can:
                    if player.pos_x < level_x:
                        player.pos_x += 1
            if event.key == pygame.K_UP and not talk:
                player.image = player.imageb
                if cur_level[player.pos_y - 1][player.pos_x] in can:
                    if player.pos_y > 0:
                        player.pos_y -= 1
            if event.key == pygame.K_DOWN and not talk:
                player.image = player.imagef
                if cur_level[player.pos_y + 1][player.pos_x] in can:
                    if player.pos_y < level_y:
                        player.pos_y += 1
            if event.key == pygame.K_ESCAPE:
                terminate()
            if event.key == 13:
                if talk:
                    talk = not talk
                    screen.fill((0, 0, 0))
                elif player.image == player.imageb:
                    for i in door:
                        if i.x == player.pos_x and i.y == player.pos_y - 1:
                            new_level(i.place)
                    for y in useful:
                        if y.x == player.pos_x and y.y == player.pos_y - 1:
                            dialog(y.text)
                elif player.image == player.imagef:
                    for i in door:
                        if i.x == player.pos_x and i.y == player.pos_y + 1:
                            new_level(i.place)
                    for y in useful:
                        if y.x == player.pos_x and y.y == player.pos_y + 1:
                            dialog(y.text)
                elif player.image == player.imagel:
                    for i in door:
                        if i.x == player.pos_x - 1 and i.y == player.pos_y:
                            new_level(i.place)
                    for y in useful:
                        if y.x == player.pos_x - 1 and y.y == player.pos_y:
                            dialog(y.text)
                elif player.image == player.imager:
                    for i in door:
                        if i.x == player.pos_x + 1 and i.y == player.pos_y:
                            new_level(i.place)
                    for y in useful:
                        if y.x == player.pos_x + 1 and y.y == player.pos_y:
                            dialog(y.text)
    if t:
        dialog([NAME + ' значит...'])
        t = False
    elif not talk:
        player_group.update()
        tiles_group.draw(screen)
        door_group.draw(screen)
        use_group.draw(screen)
        player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
