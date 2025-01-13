import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Membuat layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burung Terbang")

# Inisialisasi suara
flap_sound = pygame.mixer.Sound("flappy_whoosh-43099.mp3")
game_over_sound = pygame.mixer.Sound("resources/game_over.wav")

# Memuat gambar latar belakang
background_image = pygame.image.load("resources/background.png")

# Kelas untuk burung
class Bird:
    def __init__(self):
        self.image = pygame.image.load("resources/bird.png")  # Gambar burung dari file
        self.rect = self.image.get_rect(center=(50, HEIGHT // 2))
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def draw(self):
        screen.blit(self.image, self.rect)  # Menggambar burung menggunakan gambar

# Kelas untuk pipa
class Pipe:
    def __init__(self):
        self.height = random.randint(150, 450)
        self.width = 50
        self.top = pygame.Rect(WIDTH, 0, self.width, self.height)
        self.bottom = pygame.Rect(WIDTH, self.height + 150, self.width, HEIGHT - self.height - 150)

    def move(self):
        self.top.x -= 5
        self.bottom.x -= 5

    def draw(self):
        # Menggambar pipa atas dengan warna kuning
        pygame.draw.rect(screen, (255, 255, 0), self.top)  # Warna kuning
        # Menggambar pipa bawah dengan warna kuning
        pygame.draw.rect(screen, (255, 255, 0), self.bottom)  # Warna kuning

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
                    bird.flap()
                    flap_sound.play()  # Memutar suara flap
                if event.key == pygame.K_r and game_over:
                    game_over_sound.play()  # Memutar suara game over
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
                    game_over = True

            # Cek jika burung jatuh
            if bird.rect.y > HEIGHT or bird.rect.y < 0:
                game_over = True

            # Menggambar
            screen.blit(background_image, (0, 0))  # Menggambar latar belakang
            bird.draw()
            for pipe in pipes:
                pipe.draw()

            # Tampilkan skor
            font = pygame.font.Font(None, 36)
            text = font.render(f'Score: {score}', True, (0, 0, 0))
            screen.blit(text, (10, 10))

        else:
            # Tampilkan pesan Game Over
            font = pygame.font.Font(None, 48)
            text = font.render('Game Over! Press R to Restart', True, (0, 0, 0))
            screen.blit(text, (50, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()