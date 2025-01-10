import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()
pygame.mixer.init()  # Inisialisasi mixer untuk suara

# Konstanta
WIDTH, HEIGHT = 1500, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burung Terbang")

background_image = pygame.image.load("bg.jpg")  # Ganti dengan nama file latar belakang Anda
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Ubah ukuran gambar

# Muat suara
jump_sound = pygame.mixer.Sound("lompat.mp3")  # Suara ketika melompat
nabrak_sound = pygame.mixer.Sound("nabrak.wav")  # Suara ketika nabrak
die_sound = pygame.mixer.Sound("die.wav")  # Suara ketika kalah

# Kelas untuk burung
class Bird:
    def __init__(self):
        self.image = pygame.image.load("bird.png")  # Muat gambar burung
        self.rect = self.image.get_rect(center=(50, HEIGHT // 2))  # Posisi awal burung
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH
        jump_sound.play()  # Mainkan suara ketika melompat

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def draw(self):
        screen.blit(self.image, self.rect)  # Gambar burung menggunakan gambar

# Kelas untuk rintangan
class Pipe:
    def __init__(self):
        self.height = random.randint(150, 450)
        self.top = pygame.Rect(WIDTH, 0, 50, self.height)
        self.bottom = pygame.Rect(WIDTH, self.height + 150, 50, HEIGHT - self.height - 150)

    def move(self):
        self.top.x -= 5
        self.bottom.x -= 5

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.top)
        pygame.draw.rect(screen, BLACK, self.bottom)

# Fungsi utama
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()  # Melompat
                if event.key == pygame.K_r and game_over:
                    main()  # Restart game

        if not game_over:
            bird.move()

            # Cek tabrakan dengan rintangan
            for pipe in pipes:
                pipe.move()
                if pipe.top.x < 0:
                    pipes.remove(pipe)
                    pipes.append(Pipe())
                    score += 1  # Tambah skor saat melewati rintangan

                if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                    nabrak_sound.play()  # Mainkan suara ketika nabrak
                    game_over = True

            # Cek jika burung jatuh
            if bird.rect.y > HEIGHT or bird.rect.y < 0:
                die_sound.play()  # Mainkan suara ketika kalah
                game_over = True

            # Menggambar
            screen.blit(background_image, (0, 0))  # Gambar latar belakang
            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Tampilkan skor
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(text, (10, 10))

        else:
            # Tampilkan pesan Game Over
            font = pygame.font.Font(None, 48)
            text = font.render('Game Over! Press R to Restart', True, BLACK)
            screen.blit(text, (50, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()