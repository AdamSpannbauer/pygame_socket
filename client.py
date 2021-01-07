import sys
import pygame
from network import Network

WIDTH = 500
HEIGHT = 500

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.vel = 3

    @property
    def rect(self):
        return self.x, self.y, self.width, self.height

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

    def read_pos(self, pos_str):
        if pos_str:
            x, y = pos_str.split(",")
            self.x, self.y = int(x), int(y)
        else:
            print("Bad Pos Str")

    def encode_pos(self):
        return f"{self.x},{self.y}"


def redraw_window(window, player1, player2):
    window.fill((255, 255, 255))
    player1.draw(window)
    player2.draw(window)
    pygame.display.update()


def main():
    network = Network()

    p1 = Player(0, 0, 100, 100, (0, 255, 0))
    p2 = Player(0, 0, 100, 100, (255, 0, 0))

    p1.read_pos(network.get_pos())

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        p2_pos = network.send(p1.encode_pos())
        p2.read_pos(p2_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit(1)

        p1.move()
        redraw_window(win, p1, p2)


main()
