import pygame
import os
from random import randint
from abc import ABC, abstractmethod

NUMBERS = {"0" : pygame.image.load(os.path.join('assets/UI/Numbers', '0.png')),
           "1" : pygame.image.load(os.path.join('assets/UI/Numbers', '1.png')),
           "2" : pygame.image.load(os.path.join('assets/UI/Numbers', '2.png')),
           "3" : pygame.image.load(os.path.join('assets/UI/Numbers', '3.png')),
           "4" : pygame.image.load(os.path.join('assets/UI/Numbers', '4.png')),
           "5" : pygame.image.load(os.path.join('assets/UI/Numbers', '5.png')),
           "6" : pygame.image.load(os.path.join('assets/UI/Numbers', '6.png')),
           "7" : pygame.image.load(os.path.join('assets/UI/Numbers', '7.png')),
           "8" : pygame.image.load(os.path.join('assets/UI/Numbers', '8.png')),
           "9" : pygame.image.load(os.path.join('assets/UI/Numbers', '9.png'))}

# Global variables
FPS = 60
WHITE = (255, 255, 255)
HEIGHT = 600
WIDTH = 400
GAP = 150

PIPE_WIDTH = 65
PIPE_HEIGHT = 400
BIRD_WIDTH = 42
BIRD_HEIGHT = 29
NUMBER_HEIGHT = 36
NUMBER_WIDTH = 24

PIPE_HIT = pygame.USEREVENT + 1

class Score:
    def __init__(self, score = 0):
        self.score = score
        self.number = NUMBERS['0']

    def update_score(self):
        self.score += 1
        self.number = self.generate_number()

    def generate_number(self):
        num = str(self.score)

        images = []  # Lista obrazów reprezentujących cyfry składające liczbę

        for digit in num:
            image = NUMBERS[digit].convert_alpha()  # Konwersja na format z alfą
            image.set_alpha(255)  # Ustawienie maksymalnej wartości przezroczystości
            images.append(image)
    
        # Tworzenie jednego obrazu zawierającego wszystkie cyfry obok siebie
        number_surface = pygame.Surface((len(num) * NUMBER_WIDTH, NUMBER_HEIGHT), pygame.SRCALPHA)
        x_offset = 0
        for image in images:
            number_surface.blit(image, (x_offset, 0))
            x_offset += image.get_width()

        return number_surface

    def display_score(self, WIN):
        WIN.blit(self.number, (WIDTH // 2, 50))

# Klasa abstrakcyjna reprezentująca obiekt w grze
class GameObject(ABC):
    def __init__(self, x = 0, y = 0, width = WIDTH, height = HEIGHT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @abstractmethod
    def display(self, WIN):
        pass

    @abstractmethod
    def get_rect(self):
        pass

# Klasa reprezentująca tło
class Background(GameObject):
    def __init__(self, x = 0, y = 0, back_width = WIDTH, back_height = HEIGHT):
        super().__init__(x, y, back_width, back_height)
        self.back_image = pygame.transform.scale(pygame.image.load(
            os.path.join('assets/GameObjects', 'background.png')), (self.width, self.height))
        
    def display(self, WIN):
        WIN.blit(self.back_image, (self.x, self.y))

    def get_rect(self):
        pass

class Base(GameObject):
    def __init__(self, x, y, base_width = WIDTH, base_height = 100):
        super().__init__(x, y , base_width, base_height)
        self.base_image = pygame.transform.scale(pygame.image.load(
            os.path.join('assets/GameObjects', 'base.png')), (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def display(self, WIN):
        WIN.blit(self.base_image, (self.x, self.y))

    def get_rect(self):
        return self.rect

# Klasa reprezentująca ptaka
class Bird(GameObject):

    def __init__(self, x, y, bird_width = BIRD_WIDTH, bird_height = BIRD_HEIGHT):
        super().__init__(x, y, bird_width, bird_height)

        self.bird_image = pygame.transform.scale(
            pygame.image.load(os.path.join('assets/GameObjects', 'bird-midflip.png')), (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = 0
    
    def jump(self):
        if self.y > 0:
            self.vel = -8
    
    def update(self):
        self.y += self.vel
        self.vel += 0.5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def display(self, WIN):
        WIN.blit(self.bird_image, (self.x, self.y))

    def get_rect(self):
        return self.rect

class Pipe(GameObject):
    def __init__(self, x, y, rotate = False, pipe_width = PIPE_WIDTH, pipe_height = PIPE_HEIGHT):
        super().__init__(x, y, pipe_width, pipe_height)
        self.rotate = rotate
        self.pipe_image = pygame.transform.scale(
            pygame.image.load(os.path.join('assets/GameObjects', 'pipe.png')), (self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, WIN):
        if self.rotate:
            WIN.blit(pygame.transform.rotate(self.pipe_image, 180), (self.x, self.y))
        else:
            WIN.blit(self.pipe_image, (self.x, self.y))

    def move(self):
        self.x -= 1.5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_rect(self):
        return self.rect


# Główna klasa gry
class Main:
    def __init__(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = Background(0, 0)
        self.bird = Bird(WIDTH // 2 - 21, HEIGHT // 2)
        self.base = Base(0, HEIGHT - 100)
        self.pipes = []
        self.generate_pipes()
        self.score = Score()
    
    def generate_pipes(self):
        i_top = randint(-350, -100)
        i_bot = i_top + GAP + PIPE_HEIGHT
        self.pipes.append((Pipe(WIDTH, i_top, True), Pipe(WIDTH, i_bot)))
        # tworzymy parę złożoną z górnej i dolnej rury
    
    def handle_hits(self, bird_rect):
        for pipe_pair in self.pipes:
            pipe_top, pipe_bot = pipe_pair
            pipe_top_rect = pipe_top.get_rect()
            pipe_bot_rect = pipe_bot.get_rect()
                
            if bird_rect.colliderect(pipe_top_rect):
                pass
            if bird_rect.colliderect(pipe_bot_rect):
                pass
        if bird_rect.colliderect(self.base.get_rect()):
            pass

    def display(self):
        self.background.display(self.WIN)
        self.bird.display(self.WIN)
        for pipe_pair in self.pipes:
            pipe_pair[0].display(self.WIN)
            pipe_pair[1].display(self.WIN)
        self.base.display(self.WIN)
        self.score.display_score(self.WIN)

    def handle_pipes(self):
        pipes_to_remove = []

        for i in range(len(self.pipes)):
            if self.pipes[i][0].x == WIDTH // 2 - 1:
                self.generate_pipes()
                self.score.update_score()
            elif self.pipes[i][0].x < -65:
                pipes_to_remove.append(self.pipes[i])

        for pipe in pipes_to_remove:
            self.pipes.remove(pipe)    
        

    def main(self):

        pygame.init()
        pygame.display.set_caption("Flappy Bird")

        clock = pygame.time.Clock()

        run = True

        while run:
            bird_rect = self.bird.get_rect()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #bird_rect = pygame.Rect()
                        self.bird.jump()

            for pipe_pair in self.pipes:
                pipe_pair[0].move()
                pipe_pair[1].move()
            
            self.handle_hits(bird_rect)            
            self.handle_pipes()
            self.bird.update()
            self.display()

            pygame.display.update()
            clock.tick(FPS)

game = Main()
game.main()