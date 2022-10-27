import pygame, sys, random, os

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.WIDTH = 544
        self.HEIGHT = 888
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.loop = True
        self.time = 30
        self.tick = 3
        self.score = 0
        self.gameover = True

    class Bird(pygame.sprite.Sprite):
        def __init__(self) -> None:
            super().__init__()
            self.Animation1 = pygame.image.load("yellowbird-downflap.png")
            self.Animation2 = pygame.image.load("yellowbird-midflap.png")
            self.Animation3 = pygame.image.load("yellowbird-upflap.png")
            self.image = self.Animation2
            self.rect = self.image.get_rect(center = (game.WIDTH / 4, game.HEIGHT / 2))  
            self.gravity = 0.75
            self.velocity = 0  
            self.switch = False   
        def update(self):
            if not game.gameover:
                self.velocity -= self.gravity
                self.rect.y -= self.velocity
            if game.time % 10 == 0:
                self.image = self.Animation1
            if game.time % 20 == 0:
                self.image = self.Animation2
            if game.time % 30 == 0:
                self.image = self.Animation3
            if self.velocity > 0:
                if not self.image.get_rect().bottomright[0] > 34 and not self.image.get_rect().bottomright[1] > 24:
                    self.image = pygame.transform.rotate(self.image, 30)
            elif self.velocity == 0:
                self.image = pygame.transform.rotate(self.image, 0)
            else:
                if not self.image.get_rect().bottomright[0] > 34 and not self.image.get_rect().bottomright[1] > 24:
                    self.image = pygame.transform.rotate(self.image, -30)
        def jump(self):
            self.velocity = 15

    class ScoreAir(pygame.sprite.Sprite):
        def __init__(self, y) -> None:
            super().__init__()
            self.image = pygame.image.load("pipe-mid.png")
            self.image = pygame.transform.scale(self.image, (52, 185))
            self.rect = self.image.get_rect(topleft = (game.WIDTH + 100, y))
            self.speed = 4
            pipeGroup.add(self)
        def update(self):
            if not game.gameover:
                self.rect.x -= self.speed 
            if self.rect.colliderect(bird.rect):
                self.kill()
                game.score += 1

    class BottomPipe(pygame.sprite.Sprite):
        def __init__(self, y) -> None:
            super().__init__()
            self.image = pygame.image.load("pipe-green.png")
            self.image = pygame.transform.scale(self.image, (self.image.get_width(),game.HEIGHT))
            self.rect = self.image.get_rect(topleft = (game.WIDTH + 100, y))
            self.speed = 4
            pipeGroup.add(self)
        def update(self):
            if not game.gameover:
                self.rect.x -= self.speed
            if self.rect.right < -5:
                self.kill()
            if self.rect.colliderect(bird):
                game.gameover = True

    class TopPipe(pygame.sprite.Sprite):
        def __init__(self, y) -> None:
            super().__init__()
            self.image = pygame.image.load("pipe-green.png")
            self.image = pygame.transform.scale(self.image, (self.image.get_width(),game.HEIGHT))
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(bottomleft = (game.WIDTH + 100, y))
            self.speed = 4
            pipeGroup.add(self)
        def update(self):
            if not game.gameover:
                self.rect.x -= self.speed
            if self.rect.right < -5:
                self.kill()
            if self.rect.colliderect(bird):
                game.gameover = True
    def update(self):
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
                    self.gameover = False
                    global startgame
                    startgame = False
            if event.type == pygame.QUIT:
                self.loop = False

    def spawnPipe(self):
        if self.time == 30:
            self.tick += 1
            self.time = 0
        if self.tick == 4 and not game.gameover:
            y = random.randint(220, self.HEIGHT - 200)
            self.BottomPipe(y)
            self.TopPipe(y - 185)
            self.ScoreAir(y - 185)
        if self.tick == 4:
            self.tick = 0

game = Game()
bird = game.Bird()
pygame.display.set_caption("FlappyBird Game")
icon = pygame.image.load("favicon.ico")
pygame.display.set_icon(icon)

background = pygame.image.load("background-day.png")
background = pygame.transform.scale(background,(game.WIDTH,game.HEIGHT))

birdGroup = pygame.sprite.Group()
birdGroup.add(bird)
pipeGroup = pygame.sprite.Group()

base = pygame.image.load("base.png")
base = pygame.transform.scale(base,(game.WIDTH * 2, base.get_height() * 1.5))
baserect = base.get_rect(center = (game.WIDTH / 2 - 42, game.HEIGHT - base.get_height() * 0.75))

font = pygame.font.Font(os.path.join("C:\\Users\\user\\Desktop","flappybird", 'FlappyBirdRegular-9Pq0.ttf'), 132)
score = font.render("{}".format(game.score), True, (255,255,255))

startgame = True
startgamepic = pygame.image.load("message.png")
startgamepic = pygame.transform.scale(startgamepic, (game.WIDTH, game.HEIGHT))


gameoverpic = pygame.image.load("gameover.png")
gameoverpic = pygame.transform.scale(gameoverpic, (game.WIDTH, gameoverpic.get_height() * 2))


if __name__ == "__main__":
    while game.loop:
        game.screen.blit(background, (0,0))
        if startgame:
            game.screen.blit(startgamepic, (0,0))
        game.spawnPipe()
        score = font.render("{}".format(game.score),True, (255,255,255))
        game.screen.blit(score, (game.WIDTH / 2, game.HEIGHT / 4))
        pipeGroup.draw(game.screen)
        pipeGroup.update()
        game.screen.blit(base, (baserect.x, game.HEIGHT - base.get_height() * 0.75))
        if not game.gameover:
            baserect.x -= 4
        if baserect.centerx < 0:
            baserect.centerx = game.WIDTH / 2 - 42
        if game.gameover and not startgame:
            game.screen.blit(gameoverpic, (0, game.HEIGHT / 4))
        birdGroup.update()
        birdGroup.draw(game.screen)      
        if bird.rect.bottom >= baserect.centery:
            game.gameover = True
        game.update()
        game.clock.tick(game.FPS)
        game.time += 1

pygame.quit()
sys.exit()
