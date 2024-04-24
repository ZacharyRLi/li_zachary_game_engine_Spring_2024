import pygame
import random

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Particle:
    def __init__(self, position, velocity, color, size):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.size = size

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def create_particle(self, position):
        velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        size = random.randint(5, 10)
        self.particles.append(Particle(position, velocity, color, size))

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, particle.color, [int(particle.position[0]), int(particle.position[1])], particle.size)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

particle_system = ParticleSystem()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                particle_system.create_particle(event.pos)

    screen.fill(BLACK)

    particle_system.update()
    particle_system.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()