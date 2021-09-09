import pygame
import neat
import random
import os
import time
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('assets', 'bird3.png')))
]
PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'pipe.png')))
BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'bg.png')))
BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join('assets', 'base.png')))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25  # passaro mira pra cima qd pressiona tecla, e mira pra baixo quando cai. Isso diz quantos graus a imagem do passaro gira
    ROTATION_VEL = 20  # velocidade de rotacao da imagem
    ANIMATION_TIME = 5  # tempo de animacao

    def __init__(self, x, y):  # posicao inicial do passaro
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        # pra ir pra cima, a velocidade eh negativa ja que o (0,0) eh no canto superior esquerdo
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # d = v*t + a*t^2
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        # impedir de acelerar demais
        if d >= 16:
            d = 16

        # pulo um pouco mais alto
        elif d < 0:
            d -= 2

        # muda a posicao do passaro
        self.y += d

        # se ele tiver subindo
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                # impede q o passaro gire dms, ele mira pra cima meio inclinado
                self.tilt = self.MAX_ROTATION
        else:
            # rotacionar pra baixo, bico do passaro completamente pra baixo
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VEL

    def draw(self, win):
        self.img_count += 1

        # se tiver mirado pra baixo, escolhe a segunda imagem
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        else:
            # quanto tempo ele fica em cada imagem
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = self.IMGS[1]
            else:
                self.img = self.IMGS[0]
                self.img_count = 0

        # rotaciona a imagem em torno do eixo
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(
            center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)

    # sistema de colisao
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 160  # distancia entra os canos
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, int(round(self.top - bird.y)))
        bottom_offset = (self.x - bird.x, int(round(self.bottom - bird.y)))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

# monta a janela


def draw_window(win, birds, pipes, base, score, generation):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Pontos: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 20 - text.get_width(), 10))

    genText = STAT_FONT.render(
        "Geração: " + str(generation), 1, (255, 255, 255))
    win.blit(genText, (10, 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()


class Game:
    def __init__(self):
        self.generation = -1

    def main(self, genomes, config):
        self.generation += 1
        nets = []
        ge = []
        birds = []
        base = Base(730)
        pipes = [Pipe(600)]
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        score = 0

        for _, g in genomes:
            ge.append(g)
            g.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(230, 350))

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_ind = 1
            else:
                run = False
                break

            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.1
                output = nets[x].activate((bird.y, abs(
                    bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
                if output[0] > 0.5:
                    bird.jump()

            rem = []
            add_pipe = False
            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        ge[x].fitness -= 1
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)

            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            base.move()
            draw_window(win, birds, pipes, base, score, self.generation)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    game = Game()
    winner = p.run(game.main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
