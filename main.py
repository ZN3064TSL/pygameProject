import pygame
# Импорт pygame

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
# Определение групп спрайтов

class Border(pygame.sprite.Sprite):
    '''
    Класс реализующий работу границ уровня
    '''

    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Platform(pygame.sprite.Sprite):
    '''
    Класс реализующий работу платформ
    '''

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('data/platforms/platform.png'), (300, 50))
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    '''
    Класс реализующий работу персонажа
    '''

    def __init__(self):
        super().__init__()
        self.model = pygame.transform.scale(pygame.image.load('data/spaceman/spaceman.png'), (55, 90))
        self.model_reversed = pygame.transform.flip(self.model, True, False)
        self.run_model = pygame.transform.scale(pygame.image.load('data/spaceman/spaceman_run.png'), (55, 90))
        self.run_model_reversed = pygame.transform.flip(self.run_model, True, False)
        self.jump_model = pygame.transform.scale(pygame.image.load('data/spaceman/spaceman_jump.png'), (70, 90))
        self.jump_model_reversed = pygame.transform.flip(self.jump_model, True, False)
        self.image = self.model
        self.rect = self.image.get_rect()
        self.direction = 'right'
        self.rect.x = 0
        self.rect.y = 200
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.5
        self.speed = 5
        self.moving_left = False
        self.moving_right = False
        self.health = 150

    def update(self):
        '''
        Метод необходимый для обновления состояния спрайта персонажа
        '''

        self.velocity.y += self.gravity
        self.rect.y += self.velocity.y

        if self.rect.bottom >= height - 70:
            self.rect.bottom = height - 70
            self.velocity.y = 0

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.velocity.y = -1
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if self.rect.x < 3600 // 2:
                self.rect.x = 0
            else:
                self.rect.x = 3600 - 150

        platform_collision = pygame.sprite.spritecollideany(self, platform_list)
        if platform_collision and self.velocity.y > 0:
            self.rect.bottom = platform_collision.rect.top
            self.velocity.y = 0

        if self.velocity.y != 0:
            if self.direction == 'right':
                self.image = self.jump_model
            else:
                self.image = self.jump_model_reversed
            self.can_jump = False
        elif self.moving_left:
            self.image = self.run_model_reversed
            self.direction = 'left'
            self.can_jump = True
        elif self.moving_right:
            self.image = self.run_model
            self.direction = 'right'
            self.can_jump = True
        else:
            if self.direction == 'right':
                self.image = self.model
            else:
                self.image = self.model_reversed
            self.can_jump = True

    def jump(self):
        '''
        Метод реализующий прыжок персонажа
        '''

        if self.can_jump:
            self.velocity.y = -15
            self.can_jump = False

    def move_left(self):
        '''
        Метод реализующий движение персонажа влево
        '''

        self.rect.x -= self.speed
        self.moving_left = True

    def move_right(self):
        '''
        Метод реализующий движение персонажа вправо
        '''

        self.rect.x += self.speed
        self.moving_right = True

    def stop_moving_left(self):
        '''
        Метод реализующий остановку персонажа при движении влево
        '''

        self.moving_left = False

    def stop_moving_right(self):
        '''
        Метод реализующий остановку персонажа при движении вправо
        '''

        self.moving_right = False


class Bullet(pygame.sprite.Sprite):
    '''
    Класс реализует работу пули
    '''

    def __init__(self, x, y, direction, enemies_group):
        super().__init__(bullets)
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
        self.speed = 10
        self.enemies_group = enemies_group

    def update(self):
        '''
        Метод реализует обновление положения спрайта пули
        '''

        if self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'right':
            self.rect.x += self.speed
        if self.rect.x < -200 or self.rect.x > 3600:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    '''
    Класс реализует работу противника
    '''

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.model = pygame.transform.scale(pygame.image.load("data/tvar'/tvar'.png"), (180, 90))
        self.model_reversed = pygame.transform.flip(self.model, True, False)
        self.model_run = pygame.transform.scale(pygame.image.load("data/tvar'/tvar'_run.png"), (180, 90))
        self.model_run_reversed = pygame.transform.flip(self.model_run, True, False)
        self.model_run2 = pygame.transform.scale(pygame.image.load("data/tvar'/tvar'_run1.png"), (180, 90))
        self.model_run2_reversed = pygame.transform.flip(self.model_run2, True, False)
        self.model_type_run = 'run2'
        self.model_type = 'reversed'
        self.image = self.model_reversed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 20
        self.step = 100
        self.to_time_out = 10
        self.time_out = 0
        self.health = 500

    def update(self):
        '''
        Метод реализует обновление положения спрайта противника
        '''

        if self.rect.left < 0 or self.rect.right > 3600:
            self.speed *= -1
        if self.time_out == 0:
            if self.step != 0:
                self.step -= 1
            else:
                self.step = 100
                self.rect.x += self.speed
                if self.model_type_run == 'run1':
                    if self.model_type == 'reversed':
                        self.image = self.model_run2_reversed
                    elif self.model_type == 'not reversed':
                        self.image = self.model_run2
                    self.model_type_run = 'run2'
                elif self.model_type_run == 'run2':
                    if self.model_type == 'reversed':
                        self.image = self.model_run_reversed
                    elif self.model_type == 'not reversed':
                        self.image = self.model_run
                    self.model_type_run = 'run1'
                self.to_time_out -= 1
                if self.to_time_out == 0:
                    self.to_time_out = 10
                    self.time_out = 500
                    self.image = self.model
                    self.speed *= -1
                    if self.model_type == 'reversed':
                        self.image = self.model
                        self.model_type = 'not reversed'
                    elif self.model_type == 'not reversed':
                        self.image = self.model_reversed
                        self.model_type = 'reversed'
        else:
            self.time_out -= 1

        if pygame.sprite.collide_rect(self, player):
            if self.alive():
                player.health -= 1
                if player.health == 0:
                    player.kill()

        if pygame.sprite.spritecollide(self, bullets, True):
            self.health -= 50
            if self.health == 0:
                self.kill()


def crop_image(image, x, y, width, height):
    '''
    Функция необходима для обрезки изображения фона
    '''

    cropped_rect = pygame.Rect(x, y, width, height)
    cropped_image = image.subsurface(cropped_rect)
    return cropped_image


def draw_restart_button(screen):
    '''
    Функция необходима для отрисовки надписи Press Enter to Restart после смерти персонажа
    '''
    font = pygame.font.Font(None, 36)
    text = font.render('Press Enter to Restart', True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    return text_rect


level = 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('2D spaceman simulator')
    size = width, height = 1000, 587
    screen = pygame.display.set_mode(size)
    # Инициализация pygame и установка параметров окна игры

    pygame.mouse.set_visible(False)
    # Курсор пропадает при попадании в зону окна игры

    background_image = pygame.image.load('data/bacgrounds/firstlvl.jpg').convert()
    background_image = pygame.transform.scale(background_image, (600, 600))
    background_image_reversed = pygame.transform.flip(background_image, True, False)
    ground_image = pygame.image.load('data/ground/ground.png').convert()
    ground_image = pygame.transform.scale(ground_image, (600, 600))
    ground_image = crop_image(ground_image, 0, 0, 600, 600)
    # Установка изображений земли и фона в переменные

    pygame.display.flip()
    # Обновление изображения окна

    moving_left = False
    moving_right = False
    # Определение переменных направления персонажа

    platform_list = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    # Определение спрайтов персонажа и платформ

    Border(0, 600, 3600, 600)
    Border(0, 0, 0, 600)
    Border(3600, 0, 3600, 600)
    # Определение спрайтов границ уровня

    camera = pygame.Rect(0, 0, width, height)
    # Определение камеры

    levels = [
        {
            'platforms': [(100, 450), (600, 350), (1100, 250), (1600, 350), (2100, 450)],
            'enemies': [(850, 430), (2700, 430)]
        },
        {
            'platforms': [(100, 500), (300, 400), (500, 300), (700, 200), (900, 100)],
            'enemies': [(500, 430), (900, 30), (2700, 430)]
        },
        {
            'platforms': [(100, 500), (800, 500), (1500, 500), (2200, 500), (3200, 500)],
            'enemies': [(1900, 430), (500, 400), (2000, 200)]
        },
        {
            'platforms': [(200, 300), (700, 300), (1200, 300), (1700, 300), (2200, 300)],
            'enemies': [(400, 200), (900, 200), (1400, 200), (1900, 200), (2400, 200)]
        },
        {
            'platforms': [(100, 500), (400, 400), (700, 300), (1000, 200), (1300, 100)],
            'enemies': [(140, 430), (450, 320), (770, 225), (1190, 30), (1140, 430), (1450, 430), (1770, 430),
                        (2190, 430)]
        },
        {
            'platforms': [(100, 90), (400, 90), (700, 90), (1000, 90), (1300, 90),
                          (1500, 500), (1700, 400), (1680, 100), (2200, 200)],
            'enemies': [(1200, -15), (600, -15), (900, -15), (200, -15)]
        },
        {
            'platforms': [(100, 100), (300, 200), (500, 300), (700, 400), (900, 500)],
            'enemies': [(1000, 420), (400, 120), (600, 220), (800, 320), (200, 20)]
        },
    ]

    for platform in levels[level]['platforms']:
        block = Platform()
        block.rect.x = platform[0] - camera.x
        block.rect.y = platform[1] - camera.y
        platform_list.add(block)

    for enemy in levels[level]['enemies']:
        enemy = Enemy(enemy[0], enemy[1])
        enemy_group = pygame.sprite.Group()
        enemy_group.add(enemy)
    # Установка платформ и противников

    running = True
    clock = pygame.time.Clock()
    fps = 75
    restart_text_shown = False
    # Определение необходимых переменных
    while running:
        # Запуск основного цикла событий
        for event in pygame.event.get():
            # Запуск цикла обработки событий
            if event.type == pygame.QUIT:
                running = False
            if player.alive():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                    elif event.key == pygame.K_a:
                        moving_left = True
                    elif event.key == pygame.K_d:
                        moving_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        moving_left = False
                    elif event.key == pygame.K_d:
                        moving_right = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if player.direction == 'right':
                        bullet = Bullet(player.rect.x + 30, player.rect.y + 40, 'right', enemy_group)
                    else:
                        bullet = Bullet(player.rect.x, player.rect.y + 40, 'left', enemy_group)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        background_image = pygame.image.load('data/bacgrounds/firstlvl.jpg').convert()
                        background_image = pygame.transform.scale(background_image, (600, 600))
                        background_image_reversed = pygame.transform.flip(background_image, True, False)
                        ground_image = pygame.image.load('data/ground/ground.png').convert()
                        ground_image = pygame.transform.scale(ground_image, (600, 600))
                        ground_image = crop_image(ground_image, 0, 0, 600, 600)

                        pygame.display.flip()

                        moving_left = False
                        moving_right = False

                        platform_list = pygame.sprite.Group()
                        all_sprites = pygame.sprite.Group()
                        player = Player()
                        all_sprites.add(player)

                        Border(0, 600, 3600, 600)
                        Border(0, 0, 0, 600)
                        Border(3600, 0, 3600, 600)

                        camera = pygame.Rect(0, 0, width, height)

                        for platform in levels[level]['platforms']:
                            block = Platform()
                            block.rect.x = platform[0] - camera.x
                            block.rect.y = platform[1] - camera.y
                            platform_list.add(block)

                        for enemy in levels[level]['enemies']:
                            enemy = Enemy(enemy[0], enemy[1])
                            enemy_group = pygame.sprite.Group()
                            enemy_group.add(enemy)

        camera.x = -player.rect.x + width / 2 - 100
        camera.y = -player.rect.y + height / 2 + 110

        if len(enemy_group) == 0:
            # Реализация перехода на новый уровень
            if level < 6:
                level += 1
            else:
                font = pygame.font.Font(None, 48)
                text = font.render("You Win", True, (255, 0, 0))
                text_rect = text.get_rect(center=(width // 2, height // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.wait(5000)
                pygame.quit()
                quit()
            background_image = pygame.image.load('data/bacgrounds/firstlvl.jpg').convert()
            background_image = pygame.transform.scale(background_image, (600, 600))
            background_image_reversed = pygame.transform.flip(background_image, True, False)
            ground_image = pygame.image.load('data/ground/ground.png').convert()
            ground_image = pygame.transform.scale(ground_image, (600, 600))
            ground_image = crop_image(ground_image, 0, 0, 600, 600)

            pygame.display.flip()

            moving_left = False
            moving_right = False

            platform_list = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)

            Border(0, 600, 3600, 600)
            Border(0, 0, 0, 600)
            Border(3600, 0, 3600, 600)

            camera = pygame.Rect(0, 0, width, height)

            for platform in levels[level]['platforms']:
                block = Platform()
                block.rect.x = platform[0] - camera.x
                block.rect.y = platform[1] - camera.y
                platform_list.add(block)

            for enemy in levels[level]['enemies']:
                enemy = Enemy(enemy[0], enemy[1])
                enemy_group = pygame.sprite.Group()
                enemy_group.add(enemy)

        for i in range(-600, 3600, 1200):
            screen.blit(background_image, [i + camera.x, camera.y - 600])
            screen.blit(background_image_reversed, [i + 600 + camera.x, camera.y - 600])
            screen.blit(background_image, [i + camera.x, camera.y])
            screen.blit(background_image_reversed, [i + 600 + camera.x, camera.y])
            screen.blit(ground_image, [i + camera.x, 65 + camera.y])
            screen.blit(ground_image, [i + 600 + camera.x, 65 + camera.y])

        for sprite in all_sprites:
            screen.blit(sprite.image, sprite.rect.move(camera.topleft))
        # Отрисовка спрайтов

        bullets.update()
        # Обновление положения спрайтов пуль

        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect.move(camera.topleft))
        # Отрисовка пуль

        enemy.update()
        # Обновление положения спрайтов противников

        for platform in platform_list:
            screen.blit(platform.image, platform.rect.move(camera.topleft))
            platform.rect.x += -player.velocity.x
        # Отрисовка платформ

        if player.health <= 0:
            # Реализация смерти и респавна персонажа
            if not restart_text_shown:
                restart_text_rect = draw_restart_button(screen)
                restart_text_shown = True
        else:
            if restart_text_shown:
                restart_text_shown = False

        if moving_left:
            player.move_left()
        else:
            player.stop_moving_left()
        if moving_right:
            player.move_right()
        else:
            player.stop_moving_right()
        # Реализация движения персонажа

        keys = pygame.key.get_pressed()
        # Получение информации о всех нажатых кнопках в данный момент
        all_sprites.update()
        # Обновление спрайтов

        clock.tick(fps)
        pygame.display.flip()
        # Обновление изображения в окне игры

    pygame.quit()
    # Выход из игры
