# Подключаем библиотеки
import pygame
import sys
import os
import random


# Класс плитки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        # Добавляем в группы спрайтов
        super().__init__(tiles_group, all_sprites)
        # Загружаем изображение из словаря
        self.image = tile_images[tile_type]
        # Ставим на место на экране
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        # Добавляем в группы спрайтов
        super().__init__(player_group, all_sprites)
        # Загружаем 4 возможных состояния поворота игрока
        self.imagef = pygame.transform.scale(load_image('HeroFront.png', -1), (tile_width, tile_height))
        self.imageb = pygame.transform.scale(load_image('HeroBack.png', -1), (tile_width, tile_height))
        self.imager = pygame.transform.scale(load_image('HeroRight.png', -1), (tile_width, tile_height))
        self.imagel = pygame.transform.scale(load_image('HeroLeft.png', -1), (tile_width, tile_height))
        # Изначальный поворот
        self.image = self.imagef
        # Записываем позицию по x и y
        self.pos_x, self.pos_y = pos_x, pos_y
        # Ставим на место на экране
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    # Метод обновляющий положение игрока на экране
    def update(self):
        self.rect = self.image.get_rect().move(
            tile_width * self.pos_x, tile_height * self.pos_y)


# Класс дверей
class Door(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, place):
        # Добовляем в группы спрайтов
        super().__init__(door_group, all_sprites)
        # Загружаем изображения из словаря
        self.image = tile_images[tile_type]
        # Ставим на место на экране
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        # Записываем место, куда ведёт эта дверь
        self.place = place
        # Записываем координаты двери
        self.x = pos_x
        self.y = pos_y


# Класс объектов, с которыми можно взаимодейстовать
class Use(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, text):
        # добавляем в группы спрайтов
        super().__init__(use_group, all_sprites)
        # Загружаем изображение из словаря
        self.image = tile_images[tile_type]
        # Ставим на место на экране
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        # Записываем координаты
        self.x = pos_x
        self.y = pos_y
        # Записываем сообщение, которое предмет выведет на экран при взаимодейтвии
        self.text = text
        self.phrase = -1

    def return_text(self, next=False):
        global quest, sec2, sec3
        if self.phrase < len(self.text) - 1 and next:
            if self.text[0][0] == '          Вульферн':
                for w in useful:
                    if w.text[0][0] == '          Вульферн':
                        w.phrase += 1
            elif self.text[0][0] == 'Под кроватью вы нашли мешок с вещами:':
                for w in useful:
                    if w.text[0][0] == 'Под кроватью вы нашли мешок с вещами:':
                        w.phrase += 1
            else:
                self.phrase += 1
        if self.text[0][0] == '          Охраник?':
            sec2 = False
            if self.text[self.phrase][1] == 'Можешь идти, разберись с тем, что там происходит':
                sec3 = False
        if self.phrase >= len(self.text) - 1:
            self.phrase = len(self.text) - 1
        if self.image == tile_images['prisoner3']:
            if self.text[self.phrase][1] == 'Спасибо большое!':
                doors['PrisonCorridorMap.txt'] = ['wolf', 'mark', 'PrisonHallMap.txt',
                                                  'PrisonRoomMap.txt', 'PrisonRoomMap2.txt']
            if quest:
                doors['PrisonHallMap.txt'] = ['PrisonCorridorMap.txt', 'endofpart1']
                for ww in door:
                    if ww.place == 'closed':
                        ww.place = 'endofpart1'
        if self.text[self.phrase] == ['Под кроватью вы нашли мешок с вещами:',
                                      'Пара старых журналов и фотографий, а так же немного еды.',
                                      'На упаковке от еды вы замечаете логотип...',
                                      'Он кажется вам очень знакомым']:
            quest = True
            texts['PrisonHallMap.txt'][0] = 0
        return self.text[self.phrase]


# Класс изображения для атаки во время битвы
class Pow(pygame.sprite.Sprite):
    def __init__(self, *group):
        # Загружаем изображение
        self.image = pygame.transform.scale(load_image("pow.png", -1), (tile_width * 2, tile_height * 2))
        self.rect = self.image.get_rect()
        # Расставляем на экран так, чтобы не косались друг друга и не выходили за экран
        while True:
            self.rect.x = random.randrange(WIDTH - tile_width * 2)
            self.rect.y = random.randrange(HEIGHT - tile_width * 2)
            if pygame.sprite.spritecollideany(self, pow_group):
                continue
            else:
                break
        # Флажок показывающий нажали или нет на объект
        self.tap = False
        super().__init__(*group)

    # Метод обновляющий объект
    def update(self, *args):
        # Если на объект нажали, он становится невидимым и флажок нажатия меняем на True
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = load_image('White.png', -1)
            self.tap = True


# Функция загружающая объект из папки data с возможностью сделать фон невидимым
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


# Функция закрывающая игру
def terminate():
    pygame.quit()
    sys.exit()


# Функция начала игры
def start_screen():
    # Запускаем фоновую музыку
    fon_theme.play(loops=-1)
    # загружаем фоновое избражение и выводим его на экран
    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    # игровой цикл с возможностью выйти и нажать Enter
    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                terminate()
            elif event1.type == pygame.KEYDOWN or \
                    event1.type == pygame.MOUSEBUTTONDOWN:
                fon_theme.stop()
                # При нажатии возвращаем работу функции first_scene()
                return first_scene()
        pygame.display.flip()
        clock.tick(FPS)


# Функция загрузки уровня
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Функция генерации уровня
def generate_level(level, *aa):
    # Задаём начальные значения
    new_player, x, y = None, None, None
    # Счётчик дверей
    ii = 0
    # Список дверей на уровне
    doorss = []
    # Список интерактивных объектов
    use = []
    global under
    # Цикл загружающий уровень и создающий объекты по символам
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
                               [['Ты посмотрел на отражение в зеркале...',
                                'Отражение посмотрело на тебя...', 'Неловко...'], ['Это просто зеркало'],
                                ['memory1'], ['Это просто зеркало']]))
            elif level[y][x] == '@':
                Tile(under, x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                doorss.append(Door('door', x, y, aa[ii]))
                Tile('empty', x, y)
                ii += 1
            elif level[y][x] == '=':
                Tile('empty', x, y)
                use.append(Use('bed', x, y, [['Хотя вы и устали, спать на этом совсем не хочется']]))
            elif level[y][x] == '-':
                use.append(Use('white', x, y, [['Хотя вы и устали, спать на этом совсем не хочется']]))
            elif level[y][x] == 's':
                Tile('empty', x, y)
                use.append(Use('prisoner1', x, y,
                               [['          Вульферн', 'И что ты смотришь?', 'Смешно, да?'],
                                ['          Вульферн', 'Этот офицер Дин...', 'Надо его проучить...',
                                 'Не хочешь помочь мне?'],
                                ['          Вульферн', 'Нет? Ну и хорошо.', 'Ты главное не сдавай меня.'],
                                ['          Вульферн', 'Проходи. Они могут догадаться о моей задумке!']]))
            elif level[y][x] == 'd':
                Tile('empty', x, y)
                use.append(Use('prisondin', x, y, [['         Офицер Дин', 'Не подходи ко мне приступное отребье!',
                                                                           'Или хочешь чтобы я и тебе навалял?']]))
            elif level[y][x] == 'a':
                Tile('empty', x, y)
                use.append(Use('prisoner2', x, y, [['         Маркус', 'Надзиратель Дин как всегда не в духе...'],
                                                   ['         Маркус', 'Ты такое пропустил!'],
                                                   ['         Маркус', 'Бедный Вульф...']]))
            elif level[y][x] == '#':
                Tile('road', x, y)
            elif level[y][x] == '*':
                Tile('roadmid', x, y)
            elif level[y][x] == ',':
                Tile('ground', x, y)
            elif level[y][x] == '+':
                Tile('ground', x, y)
                Tile('rock', x, y)
            elif level[y][x] == 'C':
                Tile('roadmid', x, y)
                use.append(Use('car', x, y, [['Вы проверили остался ли кто нибудь живой', 'Там никого нет...'],
                                             ['Вы нашли переговорный пейджер в кабине водителя',
                                              'Там остались последние сообщения'],
                                             ['To: Мы почти приехали.', 'From: Хорошо.',
                                              'From: Внимание! Зазвучала сирена ядерной тревоги!',
                                              'To: Какая сирена? У нас всё чис...'],
                                             ['Последнее сообщение не было отправленно...'],
                                             ['Больше тут ничего нет.']]))
            elif level[y][x] == '_':
                Tile('road', x, y)
                use.append(Use('white', x, y, [['Вы проверили остался ли кто нибудь живой', 'Там никого нет...'],
                                               ['Вы нашли переговорный пейджер в кабине водителя',
                                                'Там остались последние сообщения'],
                                               ['To: Мы почти приехали.', 'From: Хорошо.',
                                                'From: Внимание! Зазвучала сирена ядерной тревоги!',
                                                'To: Какая сирена? У нас всё чис...'],
                                               ['Последнее сообщение не было отправленно...'],
                                               ['Больше тут ничего нет.']]))
            elif level[y][x] == '~':
                Tile('roadmid', x, y)
                use.append(Use('white', x, y, [['Вы проверили остался ли кто нибудь живой', 'Там никого нет...'],
                                               ['Вы нашли переговорный пейджер в кабине водителя',
                                                'Там остались последние сообщения'],
                                               ['To: Мы почти приехали.', 'From: Хорошо.',
                                                'From: Внимание! Зазвучала сирена ядерной тревоги!',
                                                'To: Какая сирена? У нас всё чис...'],
                                               ['Последнее сообщение не было отправленно...'],
                                               ['Больше тут ничего нет.']]))
            elif level[y][x] == '`':
                Tile('afterground', x, y)
            elif level[y][x] == '%':
                Tile('afterwall', x, y)
            elif level[y][x] == 'D':
                Tile('afterground', x, y)
                use.append(Use('afterdin', x, y, [['         ???', 'П-Помоги мне!', 'Он собирается меня убить!']]))
            elif level[y][x] == 'S':
                Tile('afterground', x, y)
                use.append(Use('enemy', x, y, [['fight']]))
            elif level[y][x] == ':':
                Tile('empty', x, y)
                use.append(Use('white', x, y,
                               [['          Вульферн', 'И что ты смотришь?', 'Смешно, да?'],
                                ['          Вульферн', 'Этот офицер Дин...', 'Надо его проучить...',
                                 'Не хочешь помочь мне?'],
                                ['          Вульферн', 'Нет? Ну и хорошо.', 'Ты главное не сдавай меня.'],
                                ['          Вульферн', 'Проходи. Они могут догадаться о моей задумке!!']]))
            elif level[y][x] == '!':
                Tile('afterground', x, y)
                use.append(Use('white', x, y, [['fight']]))
            elif level[y][x] == 'k' and not quest:
                Tile('empty', x, y)
                use.append(Use('prisoner3', x, y, [['          Кевин',
                                                    'Хей, братюнь, не мог бы ты немного помочь мне пожалуйста?'],
                                                   ['          Кевин',
                                                    'Я не могу отходить от офицера, а мы скоро уедем...',
                                                    'А я забыл свои вещи в камере!',
                                                    'Можешь пожалуйста принести их мне?'],
                                                   ['          Кевин', 'Спасибо большое!',
                                                    'Моя камера находится сразу слева от входа в коридор.'],
                                                   ['          Кевин',
                                                    'Моя камера находится сразу слева от входа в коридор.']]))
            elif level[y][x] == 'k' and quest:
                Tile('empty', x, y)
                use.append(Use('prisoner3', x, y, [['          Кевин', 'Спасибо тебе большое!',
                                                    'В качестве благодарности прими эту шоколадку!',
                                                    '* Вы получили шоколад!'], ['          Кевин',
                                                                                'Спасибо большо ещё раз!']]))
            elif level[y][x] == '8':
                Tile('frontwall', x, y)
                use.append(Use('mirror', x, y, [['Это просто зеркало...', 'Хотя оно какое-то грязное...']]))
            elif level[y][x] == '9':
                Tile('empty', x, y)
                use.append(Use('bed', x, y, [['Под кроватью вы нашли мешок с вещами:',
                                              'Пара старых журналов и фотографий, а так же немного еды.',
                                              'На упаковке от еды вы замечаете логотип...',
                                              'Он кажется вам очень знакомым'], ['Койка Кевина']]))
            elif level[y][x] == '0':
                use.append(Use('white', x, y, [['Под кроватью вы нашли мешок с вещами:',
                                                'Пара старых журналов и фотографий, а так же немного еды.',
                                                'На упаковке от еды вы замечаете логотип...',
                                                'Он кажется вам очень знакомым'], ['Койка Кевина']]))
            elif level[y][x] == 'O':
                Tile('empty', x, y)
                use.append(Use('security', x, y, [['          Охраник?',
                                                   'А ты чего тут делаешь? И ты вообще кто такой?',
                                                   '...Не знаешь что произошло?', 'Да я и сам то не очень понимаю'],
                                                  ['          Охраник?',
                                                   'ЭТО случилось в самый обычный день.'
                                                   ' Я пил чай и тут земля начала дрожать.',
                                                   'Я уронил чашку и уже наклонился её поднимать, как потерял сознание',
                                                   'А когда очнулся, был уже тут.'],
                                                  ['          Охраник',
                                                   'Заключенные устроили тут свою общину и я присоединился к ним.',
                                                   'Офицеров я тут больше не видел...'],
                                                  ['          Охраник',
                                                   'Я вижу, ты хороший малый. Ты можешь остаться с нами если хочешь',
                                                   'Кстати, я слышал шум из той "комнаты"',
                                                   'можешь пожалуйста проверить, что они там устроили.'],
                                                  ['          Охраник', 'Если тебе придётся драться, то помни:',
                                                   'Бить противника нужно в слабые с помощью МЫШКИ.',
                                                   'Так же противника можно уговорить престать сражаться.'],
                                                  ['          Охраник',
                                                   'Можешь идти, разберись с тем, что там происходит']]))
    # вернем игрока, размер поля в клеткахб двери и интерактивные объекты на уровне
    return new_player, x, y, doorss, use


# Функция переключающаяся на новый уровень
def new_level(lv):
    global lvl
    # При определённом значении перехрдим во вторую локацию
    if lv == 'endofpart1':
        if lvl == 'PrisonHallMap.txt':
            part2()
    elif lv == 'wolf':
        dialog(['Это комната Вольферна'])
    elif lv == 'mark':
        dialog(['Это комната Маркуса'])
    elif lv == 'kewin':
        dialog(['Это комната Кевина'])
    elif lv == 'closed':
        if lvl == 'PrisonHallMap.txt':
            dialog(['         Офицер Дин', 'Мы уже скоро поедем, не торопи события!'])
    elif lv != '':
        # Закрашиваем поле и опусташаем группы спрайтов
        screen.fill((0, 0, 0))
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        use_group.empty()
        door_group.empty()
        # загружаем нужные глобальные переменные
        global cur_level, player, level_x, level_y, door, useful
        # Загружаем уровень
        cur_level = load_level(lv)
        # генерируем уровень
        player, level_x, level_y, door, useful = generate_level(cur_level, *doors[lv])
        for www in range(len(useful)):
            useful[www].phrase += texts[lv][www]
        # При переходе из определённой локации в другую, двигаем игрока к двери, из которой он вышел
        if lvl == 'PrisonCorridorMap.txt' and lv == 'PrisonRoomMap.txt':
            player.pos_x += 2
        elif lvl == 'PrisonHallMap.txt' and lv == 'PrisonCorridorMap.txt':
            player.pos_x += 7
            player.pos_y -= 1
        elif lvl == 'PrisonRoomMap2.txt' and lv == 'PrisonCorridorMap.txt':
            player.pos_x += 6
        # прорисовываем уровень
        all_sprites.draw(screen)
        door_group.draw(screen)
        lvl = lv


# Функция диалогового окна
def dialog(text):
    if text == ['memory1']:
        text = ['Это просто зеркало']
    # Глобальная переменная показывающая находится ли игрок в диалоге
    global talk
    talk = True
    # Рисуем рамки окна
    pygame.draw.rect(screen, (255, 255, 255), ((tile_width, 5.5 * tile_height), (14 * tile_width, 3 * tile_height)))
    pygame.draw.rect(screen, (0, 0, 0), ((tile_width * 1.0625, tile_height * 5.5625),
                                         (tile_width * 13.875, 2.875 * tile_height)))
    # Загружаем построчно текст в окно
    font = pygame.font.Font(None, int(0.625 * tile_width))
    for iii in range(len(text)):
        string_rendered = font.render(text[iii], True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 5.625 * tile_width + iii * 0.75 * tile_height
        intro_rect.x = 1.25 * tile_width
        screen.blit(string_rendered, intro_rect)


# Функция первой кат-сцены и выбора имени
def first_scene():
    # Кат-сцена
    time = 0
    screen.fill((0, 0, 0))
    pygame.display.flip()
    scene = True
    scene1_theme.play()
    tic = None
    while scene:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    terminate()
                if ev.key == 13:
                    scene = False
        if time > 17:
            break
        if time > 13.6:
            tic = pygame.transform.scale(load_image('6.jpg'), (WIDTH, HEIGHT))
        elif time > 11.2:
            tic = pygame.transform.scale(load_image('5.jpg'), (WIDTH, HEIGHT))
        elif time > 9.5:
            tic = pygame.transform.scale(load_image('4.jpg'), (WIDTH, HEIGHT))
        elif time > 4.5:
            tic = pygame.transform.scale(load_image('3.jpg'), (WIDTH, HEIGHT))
        elif time > 4:
            tic = pygame.transform.scale(load_image('2.jpg'), (WIDTH, HEIGHT))
        elif time > 3:
            tic = pygame.transform.scale(load_image('1.jpg'), (WIDTH, HEIGHT))
        else:
            screen.fill((0, 0, 0))
        if tic is not None:
            screen.blit(tic, (0, 0))
        pygame.display.flip()
        time += clock.tick() / 1000
    scene1_theme.stop()
    # Экран выбора имени
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (2 * tile_width, 2 * tile_height, 12 * tile_width, 2 * tile_height), 1)
    font = pygame.font.Font(None, tile_height)
    string_rendered = font.render('Введите имя:', True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 0.5 * tile_height
    intro_rect.x = 2 * tile_width
    screen.blit(string_rendered, intro_rect)
    name = ''
    inputt = True
    font = pygame.font.Font(None, int(2.5 * tile_width))
    while inputt:
        pygame.draw.rect(screen, (0, 0, 0), (2 * tile_width, 2 * tile_width, 12 * tile_width, 2 * tile_width))
        pygame.draw.rect(screen, (255, 255, 255), (2 * tile_width, 2 * tile_width, 12 * tile_width, 2 * tile_width), 1)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    terminate()
                if e.key == 13 and name != '':
                    if name.lower() in names:
                        pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
                        dialog(names[name.lower()])
                    elif name.lower() == 'ammine' or name.lower() == 'аммайн':
                        terminate()
                    else:
                        inputt = False
                if e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                if len(name) < 7 and e.unicode in 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТ' \
                                                  'ЬБЮqwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM':
                    name += e.unicode
        string_rendered = font.render(name, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 2.0625 * tile_width
        intro_rect.x = 2.0625 * tile_width
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
    # Возвращаем введённое пользователем имя
    return name


# Вторая кат-сцена
def part2():
    # Переменная показывающая, что нужно рисовать под игроком
    global under
    under = 'ground'
    # Вторая кат-сцена
    prison_theme.stop()
    ww = True
    screen.fill((0, 0, 0))
    tim = 0
    font = pygame.font.Font(None, tile_height)
    scene2_theme.play()
    sh = True
    while ww:
        for w in pygame.event.get():
            if w.type == pygame.QUIT:
                terminate()
            if w.type == pygame.KEYDOWN:
                if w.key == 13:
                    if tim < 18:
                        tim = 18
                        scene2_theme.stop()
                    else:
                        ww = False
                if w.key == pygame.K_ESCAPE:
                    terminate()
        if tim < 4.5:
            fon = pygame.transform.scale(load_image('1.png'), (WIDTH, HEIGHT))
        elif tim < 9:
            fon = pygame.transform.scale(load_image('2.png'), (WIDTH, HEIGHT))
        elif tim < 10:
            fon = pygame.transform.scale(load_image('3.png'), (WIDTH, HEIGHT))
        elif tim < 16.5:
            fon = pygame.transform.scale(load_image('4.png'), (WIDTH, HEIGHT))
        else:
            fon = pygame.transform.scale(load_image('Logo.png'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        if tim > 30 and sh:
            fon_theme.play(loops=-1)
            sh = False
        if tim > 18:
            if int(tim) % 2 == 0:
                string_rendered = font.render('[Нажмите Enter]', True, pygame.Color('white'))
            else:
                string_rendered = font.render('[Нажмите Enter]', True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = 8 * tile_height
            intro_rect.x = 5 * tile_width
            screen.blit(string_rendered, intro_rect)
        tim += clock.tick() / 1000
        pygame.display.flip()
    # Запускаем новую локацию
    scene2_theme.stop()
    fon_theme.stop()
    after_theme.play(loops=-1)
    new_level('AroundPrison.txt')


# Функция боя с врагом
def fight1():
    after_theme.stop()
    fight_theme.play(loops=-1)
    btns = [pygame.color.Color('green'), (255, 255, 255)]
    font = pygame.font.Font(None, int(tile_height * 1.5))
    b1 = 'Атака'
    b2 = 'Действие'
    count = 0
    image = pygame.transform.scale(load_image('PrisonerFront3.png', -1), (int(tile_width * 5.5),
                                                                          int(tile_height * 5.5)))
    hp = 5
    enemyhp = 10
    while True:
        screen.fill((0, 0, 0))
        # Варианты сообщения
        if count == 0:
            dialog(['Перед вами грозный противник.',
                    'Ваше стремление помочь улетучивается, но уже поздно', 'отступать'])
        elif count == 1:
            dialog(['Вы молите противника не атаковать вас.', 'Противник засомневался...', 'Его атака снижена!'])
        elif count == 2:
            dialog(['Вы молите противника не атаковать вас.', '* Я не буду сражаться с тобой. Уйди с пути.'])
        elif count == 3:
            dialog(['Вы уговаривайте противника отступить.', '* Я не позволю ему уйти, я наконец-то могу отомстить!'])
        elif count == 4:
            dialog(['Вы уговаривайте противника отступить.', '* Возможно ты прав... Я дам ему уйти на этот раз.',
                    'Но если я увижу, что он продолжает делать ЭТО, ему конец!'])

        elif count == 5:
            dialog(['Вы аттакуете противника', '* Эй, если ты будешь аттаковать меня, то я не буду бездействовать!'])
        elif count == 6:
            dialog(['Вы пытались аттаковать противника...', 'У вас не очень получилось сделать это'])
        elif count == 7:
            dialog(['Вы аттакуете противника!', '* И это всё что ты можешь?'])
        for event in pygame.event.get():
            # Действие игрока
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_DOWN:
                    btns = btns[::-1]
                if event.key == pygame.K_UP:
                    btns = btns[::-1]
                if event.key == 13:
                    if b1 == 'Конец':
                        end()
                    elif b1 == 'Атака':
                        if btns[0] == (255, 255, 255):
                            b1 = 'Уговор'
                            b2 = 'Мольба'
                        else:
                            dmg = attack()
                            enemyhp -= dmg
                            if enemyhp <= 0:
                                end()
                            hp -= enemy_attack()
                            if count == 4:
                                count = 5
                            elif dmg == 0:
                                count = 6
                            else:
                                count = 7
                    else:
                        if btns[0] == (255, 255, 255):
                            if count == 0 or count == 3 or count >= 5:
                                count = 1
                                hp -= enemy_attack()
                            elif count == 1 or count == 3 or count >= 5:
                                count = 2
                                hp -= enemy_attack()
                        else:
                            if count == 0 or count == 1:
                                count = 3
                                hp -= enemy_attack()
                            elif count == 2:
                                count = 4
                        if count == 4:
                            b1 = 'Конец'
                        else:
                            b1 = 'Атака'
                            b2 = 'Действие'
                if event.key == 304 and count != 4:
                    b1 = 'Атака'
                    b2 = 'Действие'
        # Рисуем компоненты боя
        pygame.draw.rect(screen, btns[0], ((tile_width, 0.5 * tile_height),
                                           (5 * tile_width, 2 * tile_height)), int(1 / 16 * tile_height))
        string_rendered1 = font.render(b1, True, btns[0])
        intro_rect = string_rendered1.get_rect()
        intro_rect.top = tile_height * 1.025
        if b1 == 'Уговор':
            intro_rect.x = tile_width * 1.7
        else:
            intro_rect.x = tile_width * 2
        screen.blit(string_rendered1, intro_rect)
        if count != 4:
            pygame.draw.rect(screen, btns[1], ((tile_width, 3 * tile_height),
                                               (5 * tile_width, 2 * tile_height)), int(1 / 16 * tile_height))
            string_rendered1 = font.render(b2, True, btns[1])
            intro_rect = string_rendered1.get_rect()
            intro_rect.top = tile_height * 3.525
            if b2 == 'Мольба':
                intro_rect.x = tile_width * 1.7
            else:
                intro_rect.x = tile_width
        screen.blit(string_rendered1, intro_rect)
        # Проверка живы ли мы
        if hp <= 0:
            game_over()
        screen.blit(image, (tile_width * 8, 0))
        font1 = pygame.font.Font(None, int(0.625 * tile_width))
        string_rendered = font1.render('HP', True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = tile_height * 0.5
        intro_rect.x = int(6.5 * tile_width)
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(screen, pygame.color.Color('red'),
                         ((int(12.5 * tile_width), tile_height), (tile_width * 2, tile_height // 5)))
        pygame.draw.rect(screen, pygame.color.Color('green'),
                         ((int(12.5 * tile_width), tile_height), (tile_width * 0.2 * enemyhp, tile_height // 5)))
        string_rendered = font1.render('Enemy HP', True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = tile_height * 0.5
        intro_rect.x = int(12.5 * tile_width)
        screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(screen, pygame.color.Color('red'),
                         ((int(6.5 * tile_width), tile_height), (tile_width * 2, tile_height // 5)))
        pygame.draw.rect(screen, pygame.color.Color('green'),
                         ((int(6.5 * tile_width), tile_height), (tile_width * 0.4 * hp, tile_height // 5)))
        pygame.display.flip()


# Функция нашей атаки врага
def attack():
    screen.fill((0, 0, 0))
    time = 0
    hits = 0
    a = []
    for _ in range(random.choice([3, 4])):
        a.append(Pow(pow_group))
    run = True
    clock.tick()
    while run:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            pow_group.update(event)
        pow_group.draw(screen)
        time += clock.tick() / 1000
        pygame.display.flip()
        if time > 2:
            run = False
    for i in a:
        if i.tap:
            hits += 1
    pow_group.empty()
    # Возвращает количество попаданий
    return hits


# Функция атаки противника
def enemy_attack():
    hp = 0
    screen.fill((0, 0, 0))
    hero = pygame.transform.scale(load_image('HeroFront.png', -1), (tile_width, tile_height))
    coords = [7.5 * tile_height, 4 * tile_width]
    x = 0
    yy = 0
    enemy = pygame.transform.scale(load_image('atc1.png', -1), (tile_width, tile_height))
    var = random.choice([0, 1, 2, 3])
    # Варианты расположения атаки
    if var == 0:
        ecoords = [tile_width * 3.5, 0]
        move = [0.025 * tile_height, 0.025 * tile_height]
    elif var == 1:
        ecoords = [tile_width * 11.5, 0]
        move = [-0.025 * tile_height, 0.025 * tile_height]
    elif var == 3:
        ecoords = [tile_width * 3.5, tile_height * 8]
        move = [0.025 * tile_height, -0.025 * tile_height]
    else:
        ecoords = [tile_width * 11.5, tile_height * 8]
        move = [-0.025 * tile_height, -0.025 * tile_height]
    linecoords = ecoords[:]
    cooldown = 0
    tr = True
    while tr:
        a = [ecoords[0] + 0.1375 * tile_width, ecoords[1] + 0.0375 * tile_width,
             ecoords[0] + 0.7125 * tile_width, 0.825 * tile_width + ecoords[1]]
        b = [0.225 * tile_width + coords[0], coords[1] + 0.05 * tile_width,
             0.5875 * tile_width + coords[0], coords[1] + 0.9125 * tile_width]
        screen.fill((0, 0, 0))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                terminate()
            if i.type == pygame.KEYDOWN:
                # Движение игрока
                if i.key == pygame.K_UP:
                    yy = -0.0125 * tile_height
                if i.key == pygame.K_DOWN:
                    yy = 0.0125 * tile_height
                if i.key == pygame.K_LEFT:
                    x = -0.0125 * tile_height
                if i.key == pygame.K_RIGHT:
                    x = 0.0125 * tile_height
            if i.type == pygame.KEYUP:
                if i.key == pygame.K_UP and yy == -0.0125 * tile_height:
                    yy = 0
                if i.key == pygame.K_DOWN and yy == 0.0125 * tile_height:
                    yy = 0
                if i.key == pygame.K_LEFT and x == -0.0125 * tile_height:
                    x = 0
                if i.key == pygame.K_RIGHT and x == 0.0125 * tile_height:
                    x = 0
        coords[0] += x
        coords[1] += yy
        # Рамки поля
        if coords[1] < tile_height:
            coords[1] = tile_height
        if coords[1] > tile_height * 7:
            coords[1] = tile_height * 7
        if coords[0] < tile_width * 4.5:
            coords[0] = tile_width * 4.5
        if coords[0] > tile_width * 10.5:
            coords[0] = tile_width * 10.5
        pygame.draw.rect(screen, (255, 255, 255),
                         ((tile_width * 4.5, tile_height), (tile_width * 7, tile_height * 7)),
                         int(tile_height * 0.0625))
        screen.blit(hero, coords)
        ecoords[0] += move[0]
        ecoords[1] += move[1]
        # Функция движения атаки противника
        pygame.draw.line(screen, (255, 255, 255),
                         (linecoords[0] + 0.15 * tile_width, linecoords[1] + 0.35 * tile_width),
                         (ecoords[0] + 0.15 * tile_width, ecoords[1] + 0.35 * tile_width), int(tile_height * 0.0625))
        pygame.draw.line(screen, (255, 255, 255),
                         (linecoords[0] + 0.275 * tile_width, linecoords[1] + 0.1125 * tile_width),
                         (ecoords[0] + 0.275 * tile_width, ecoords[1] + 0.1125 * tile_width), int(tile_height * 0.0625))
        pygame.draw.line(screen, (255, 255, 255),
                         (linecoords[0] + 0.5 * tile_width, linecoords[1] + 0.0625 * tile_width),
                         (ecoords[0] + 0.5 * tile_width, ecoords[1] + 0.0625 * tile_width), int(tile_height * 0.0625))
        pygame.draw.line(screen, (255, 255, 255),
                         (linecoords[0] + 0.7 * tile_width, linecoords[1] + 0.1625 * tile_width),
                         (ecoords[0] + 0.7 * tile_width, ecoords[1] + 0.1625 * tile_width), int(tile_height * 0.0625))
        screen.blit(enemy, ecoords)
        if ecoords[1] < 0 or ecoords[1] > HEIGHT:
            tr = False
        if int(a[0]) > int(b[2]) + int(b[0]) or int(a[0]) + int(a[2]) < int(b[0]) or \
                int(a[1]) > int(b[1]) + int(b[3]) or int(a[3]) + int(a[1]) < int(b[1]):
            if cooldown <= 0:
                hp += 1
                cooldown = 0.5
        cooldown -= clock.tick() / 1000
        pygame.display.flip()
        clock.tick(FPS)
    # Возвращаем количество попаданий по игроку
    return hp


# Функция экрана конца игры если мы проиграли
def game_over():
    fight_theme.stop()
    fon_theme.play(loops=-1)
    fon = pygame.transform.scale(load_image('end_screen.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    pygame.display.flip()
    while True:
        for r in pygame.event.get():
            if r.type == pygame.QUIT:
                terminate()
            elif r.type == pygame.KEYDOWN:
                if r.key == pygame.K_ESCAPE:
                    terminate()
                if r.key == 13:
                    terminate()


# Функция экрана конца игры если мы прошли игру
def end():
    fight_theme.stop()
    fon_theme.play(loops=-1)
    screen.fill((0, 0, 0))
    dialog(['Вы прошли ДЕМО-версию игры!', 'Спасибо за то, что играли)'])
    pygame.display.flip()
    while True:
        for r in pygame.event.get():
            if r.type == pygame.QUIT:
                terminate()
            elif r.type == pygame.KEYDOWN:
                if r.key == pygame.K_ESCAPE:
                    terminate()
                if r.key == 13:
                    terminate()


def memory():
    z = True
    tim = 0
    clock.tick()
    prison_theme.stop()
    while z:
        for r in pygame.event.get():
            if r.type == pygame.QUIT:
                terminate()
            elif r.type == pygame.KEYDOWN:
                if r.key == pygame.K_ESCAPE:
                    terminate()
                if r.key == 13:
                    z = False
        if tim < 3:
            fon = pygame.transform.scale(load_image('6.jpg'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
        elif tim < 6:
            screen.fill((0, 0, 0))
        elif tim < 9:
            fon = pygame.transform.scale(load_image('тру.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
        elif tim < 12:
            fon = pygame.transform.scale(load_image('трудва.png'), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
        else:
            z = False
        tim += clock.tick() / 1000
        pygame.display.flip()
    screen.fill((0, 0, 0))
    prison_theme.play(loops=-1)


# Выбор разрешения экрана игры
print('Выберите разрешение (цифру): 1)1280х720  2)1920х1080  3)2560х1440')
a = input()
under = 'empty'
pygame.init()
pygame.display.set_caption('The Story DEMO')
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
FPS = 144
# Словарь объектов игры
tile_images = {
    'frontwall': pygame.transform.scale(load_image('PrisonWallFront.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(load_image('PrisonGround.png'), (tile_width, tile_height)),
    'door': pygame.transform.scale(load_image('PrisonDoor.png', -1), (tile_width, tile_height)),
    'leftwall': pygame.transform.scale(load_image('PrisonWallLeft.png', -1), (tile_width, tile_height)),
    'rightwall': pygame.transform.scale(load_image('PrisonWallRight.png', -1), (tile_width, tile_height)),
    'backwall': pygame.transform.scale(load_image('PrisonWallBack.png', -1), (tile_width, tile_height)),
    'cornerlwall': pygame.transform.scale(load_image('PrisonWallCornerL.png', -1), (tile_width, tile_height)),
    'cornerrwall': pygame.transform.scale(load_image('PrisonWallCornerR.png', -1), (tile_width, tile_height)),
    'mirror': pygame.transform.scale(load_image('Mirror.png', -1), (tile_width, tile_height * 2)),
    'bed': pygame.transform.scale(load_image('PrisonBed.png', -1), (tile_width * 2, tile_height)),
    'prisoner1': pygame.transform.scale(load_image('PrisonerFront1.png', -1), (int(tile_width * 1.5),
                                                                               int(tile_height * 1.5))),
    'prisondin': pygame.transform.scale(load_image('DinOfficerFront.png', -1), (tile_width, tile_height)),
    'prisoner2': pygame.transform.scale(load_image('PrisonerFront2.png', -1), (tile_width, tile_height)),
    'ground': pygame.transform.scale(load_image('Ground.png'), (tile_width, tile_height)),
    'road': pygame.transform.scale(load_image('Road.png'), (tile_width, tile_height)),
    'roadmid': pygame.transform.scale(load_image('RoadMid.png'), (tile_width, tile_height)),
    'rock': pygame.transform.scale(load_image('rock.png', -1), (tile_width, tile_height)),
    'car': pygame.transform.scale(load_image('Car.png', -1), (int(tile_width * 6.75), int(tile_height * 2.25))),
    'afterground': pygame.transform.scale(load_image('AfterPrisonGround.png'), (tile_width, tile_height)),
    'afterwall': pygame.transform.scale(load_image('AfterPrisonWallFront.png'), (tile_width, tile_height)),
    'afterdin': pygame.transform.scale(load_image('DinPrisonerFront.png', -1), (tile_width, tile_height)),
    'enemy': pygame.transform.scale(load_image('PrisonerFront3.png', -1), (int(tile_width * 1.5),
                                                                           int(tile_height * 1.5))),
    'white': pygame.transform.scale(load_image('White.png', -1), (tile_width, tile_height)),
    'prisoner3': pygame.transform.scale(load_image('PrisonerFront4.png', -1), (tile_width, tile_height)),
    'security': pygame.transform.scale(load_image('SecurityFront.png', -1), (tile_width, tile_height)),
}
# словарь дверей и куда они ведут
doors = {
    'PrisonRoomMap.txt': ['PrisonCorridorMap.txt'],
    'PrisonCorridorMap.txt': ['wolf', 'mark', 'PrisonHallMap.txt', 'PrisonRoomMap.txt', 'kewin'],
    'PrisonHallMap.txt': ['PrisonCorridorMap.txt', 'closed'],
    'AroundPrison.txt': [],
    'AfterPrison.txt': [],
    'PrisonRoomMap2.txt': ['PrisonCorridorMap.txt'],
    'PrisonEnter.txt': []
}
# Словарь особых имён
names = {
    'l': ['Ты не так умён как он'],
    'л': ['Ты не так умён как он'],
    'пикачу': ['Пика-пика!'],
    'pikachu': ['Пика-пика!'],
    'дискорд': ['Бог хаоса уже есть в этой вселеной'],
    'discord': ['Бог хаоса уже есть в этой вселеной'],
    'сайтама': ['Ты не так силён как он'],
    'saitama': ['Ты не так силён как он'],
    'рем': ['Прости, но я люблю Эмилию'],
    'rem': ['Прости, но я люблю Эмилию'],
    'темми': ['пРИВ!'],
    'temmie': ['пРИВ!'],
    'эсканор': ['Тот, кто стоит над всеми народами,',
                'один из семи смертных грехов - грех гордыни', 'Великий львиный грех - Эсканор'],
    'escanor': ['Тот, кто стоит над всеми народами,',
                ' один из семи смертных грехов - грех гордыни', 'Великий львиный грех - Эсканор'],
    'din': ['* Как ты посмел ко мне обратиться?!'],
    'дин': ['* Как ты посмел ко мне обратиться?!'],
}
# Словарь для диаологов
texts = {
    'PrisonRoomMap.txt': [0, 0, 0],
    'PrisonCorridorMap.txt': [],
    'PrisonHallMap.txt': [0, 0, 0, 0, 0, 0, 0],
    'AroundPrison.txt': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'AfterPrison.txt': [0, 0, 0, 0, 0],
    'PrisonRoomMap2.txt': [0, 0, 0],
    'PrisonEnter.txt': [0]
}
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
use_group = pygame.sprite.Group()
pow_group = pygame.sprite.Group()
cur_level = load_level('PrisonRoomMap.txt')
lvl = 'PrisonRoomMap.txt'
player, level_x, level_y, door, useful = generate_level(cur_level, 'PrisonCorridorMap.txt')
can = '.@,#*`'
talk = True
t = True
quest = False
sec = True
sec2 = True
sec3 = True
# Загружаем звуки в игре
prison_theme = pygame.mixer.Sound(file='data/prison_theme.wav')
scene1_theme = pygame.mixer.Sound(file='data/scene1.wav')
fon_theme = pygame.mixer.Sound(file='data/FonSound.wav')
after_theme = pygame.mixer.Sound(file='data/afterfall_theme.wav')
scene2_theme = pygame.mixer.Sound(file='data/scene2.wav')
fight_theme = pygame.mixer.Sound(file='data/fight_theme.wav')
prison_theme.set_volume(0.2)
scene1_theme.set_volume(0.2)
after_theme.set_volume(0.2)
scene2_theme.set_volume(0.2)
fight_theme.set_volume(0.2)
# Стартовое окно игры
NAME = start_screen()
screen.fill((0, 0, 0))
tiles_group.draw(screen)
door_group.draw(screen)
use_group.draw(screen)
player_group.draw(screen)
prison_theme.play(loops=-1)
# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            # Движение игрока
            if event.key == pygame.K_LEFT and not talk:
                player.image = player.imagel
                if player.pos_x > 0 and cur_level[player.pos_y][player.pos_x - 1] in can:
                    player.pos_x -= 1
            if event.key == pygame.K_RIGHT and not talk:
                player.image = player.imager
                if player.pos_x < level_x:
                    if cur_level[player.pos_y][player.pos_x + 1] in can:
                        player.pos_x += 1
            if event.key == pygame.K_UP and not talk:
                player.image = player.imageb
                if player.pos_y == 0 and lvl == 'PrisonEnter.txt' and not sec2 and not sec3:
                    new_level('AroundPrison.txt')
                    player.pos_x += 2
                    player.pos_y += 2
                elif player.pos_y == 0 and lvl == 'PrisonEnter.txt' and sec2:
                    dialog(['          Охраник?', 'Ты куда пошёл?', 'Я те говорю сюда подойди.',
                            'Не буду я стрелять, не боись'])
                elif player.pos_y == 0 and lvl == 'PrisonEnter.txt' and sec3:
                    dialog(['          Охраник?', 'Ты куда пошёл?', 'Мы ещё не договорили!'])
                elif player.pos_y == 0 and lvl == 'AfterPrison.txt':
                    dialog(['Мне нужно помочь!'])
                elif cur_level[player.pos_y - 1][player.pos_x] in can:
                    if player.pos_y > 0:
                        player.pos_y -= 1
            if event.key == pygame.K_DOWN and not talk:
                player.image = player.imagef
                try:
                    if cur_level[player.pos_y + 1][player.pos_x] in can:
                        if player.pos_y < level_y:
                            player.pos_y += 1
                except IndexError:
                    if lvl == 'AroundPrison.txt':
                        new_level('PrisonEnter.txt')
                    elif sec2:
                        dialog(['          Охраник?', 'Ты куда пошёл?', 'Я те говорю сюда подойди.',
                                'Не буду я стрелять, не боись'])
                    elif sec3:
                        dialog(['          Охраник?', 'Ты куда пошёл?', 'Мы ещё не договорили!'])
                    else:
                        new_level('AfterPrison.txt')
            if event.key == pygame.K_ESCAPE:
                terminate()
            if event.key == 13:
                # Пропуски диалога
                if talk:
                    talk = not talk
                    screen.fill((0, 0, 0))
                # Проверка всех дверей и предметов на взаимодействие
                elif player.image == player.imageb:
                    for i in door:
                        if i.x == player.pos_x and i.y == player.pos_y - 1:
                            new_level(i.place)
                    for y in range(len(useful)):
                        if useful[y].x == player.pos_x and useful[y].y == player.pos_y - 1:
                            if useful[y].return_text() == ['fight']:
                                fight1()
                            elif useful[y].return_text() == ['memory1']:
                                memory()
                                useful[y].return_text(next=True)
                            else:
                                dialog(useful[y].return_text(next=True))
                            if lvl == 'PrisonRoomMap.txt' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonRoomMap2' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonHallMap.txt' and y > 2:
                                texts[lvl][-1] += 1
                                texts[lvl][-2] += 1
                                texts[lvl][-3] += 1
                                texts[lvl][-4] += 1
                            elif lvl == 'AroundPrison.txt':
                                for wwww in range(len(texts[lvl])):
                                    texts[lvl][wwww] += 1
                            else:
                                texts[lvl][y] += 1
                elif player.image == player.imagef:
                    for i in door:
                        if i.x == player.pos_x and i.y == player.pos_y + 1:
                            new_level(i.place)
                    for y in range(len(useful)):
                        if useful[y].x == player.pos_x and useful[y].y == player.pos_y + 1:
                            if useful[y].return_text() == ['fight']:
                                fight1()
                            elif useful[y].return_text() == ['memory1']:
                                memory()
                                useful[y].return_text(next=True)
                            else:
                                dialog(useful[y].return_text(next=True))
                            if lvl == 'PrisonRoomMap.txt' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonRoomMap2' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonHallMap.txt' and y > 2:
                                texts[lvl][-1] += 1
                                texts[lvl][-2] += 1
                                texts[lvl][-3] += 1
                                texts[lvl][-4] += 1
                            elif lvl == 'AroundPrison.txt':
                                for wwww in range(len(texts[lvl])):
                                    texts[lvl][wwww] += 1
                            else:
                                texts[lvl][y] += 1
                elif player.image == player.imagel:
                    for i in door:
                        if i.x == player.pos_x - 1 and i.y == player.pos_y:
                            new_level(i.place)
                    for y in range(len(useful)):
                        if useful[y].x == player.pos_x - 1 and useful[y].y == player.pos_y:
                            if useful[y].return_text() == ['fight']:
                                fight1()
                            elif useful[y].return_text() == ['memory1']:
                                memory()
                                useful[y].return_text(next=True)
                            else:
                                dialog(useful[y].return_text(next=True))
                            if lvl == 'PrisonRoomMap.txt' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonRoomMap2' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonHallMap.txt' and y > 2:
                                texts[lvl][-1] += 1
                                texts[lvl][-2] += 1
                                texts[lvl][-3] += 1
                                texts[lvl][-4] += 1
                            elif lvl == 'AroundPrison.txt':
                                for wwww in range(len(texts[lvl])):
                                    texts[lvl][wwww] += 1
                            else:
                                texts[lvl][y] += 1
                elif player.image == player.imager:
                    for i in door:
                        if i.x == player.pos_x + 1 and i.y == player.pos_y:
                            new_level(i.place)
                    for y in range(len(useful)):
                        if useful[y].x == player.pos_x + 1 and useful[y].y == player.pos_y:
                            if useful[y].return_text() == ['fight']:
                                fight1()
                            elif useful[y].return_text() == ['memory1']:
                                memory()
                                useful[y].return_text(next=True)
                            else:
                                dialog(useful[y].return_text(next=True))
                            if lvl == 'PrisonRoomMap.txt' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonRoomMap2' and y >= 1:
                                texts[lvl][1] += 1
                                texts[lvl][2] += 1
                            elif lvl == 'PrisonHallMap.txt' and y > 2:
                                texts[lvl][-1] += 1
                                texts[lvl][-2] += 1
                                texts[lvl][-3] += 1
                                texts[lvl][-4] += 1
                            elif lvl == 'AroundPrison.txt':
                                for wwww in range(len(texts[lvl])):
                                    texts[lvl][wwww] += 1
                            else:
                                texts[lvl][y] += 1
    if t:
        dialog([NAME + ' значит...'])
        t = False
    elif not talk:
        # Рисуем спрайты
        player_group.update()
        tiles_group.draw(screen)
        door_group.draw(screen)
        use_group.draw(screen)
        player_group.draw(screen)
    if lvl == 'AfterPrison.txt' and t is False:
        dialog(['* П-Помогите!', ' Он хочет убить меня!'])
        t = None
    if sec and lvl == 'PrisonEnter.txt':
        dialog(['          Охраник?', 'Э, кто стрелять ид... Тфу... Кто идёт, стрелять буду!',
                'Ты хто такой?', 'Пади сюда, разберёмся сейчас.'])
        sec = False
    pygame.display.flip()
    clock.tick(FPS)
