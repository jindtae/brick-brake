import pygame
import random

# 초기화
pygame.init()

# 화면 설정
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brick Breaker')

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128)
]

# 게임 속도
clock = pygame.time.Clock()
fps = 60

# 패들 클래스
class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 10
        self.x = (screen_width - self.width) // 2
        self.y = screen_height - 40
        self.speed = 15

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, dx):
        self.x += dx
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > screen_width:
            self.x = screen_width - self.width

# 공 클래스
class Ball:
    def __init__(self):
        self.radius = 10
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.dx = 5
        self.dy = -5

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x - self.radius < 0 or self.x + self.radius > screen_width:
            self.dx = -self.dx
        if self.y - self.radius < 0:
            self.dy = -self.dy

# 벽돌 클래스
class Brick:
    def __init__(self, x, y, width, height, color, durability):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.durability = durability

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def hit(self):
        self.durability -= 1
        if self.durability == 2:
            self.color = (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2)
        elif self.durability == 1:
            self.color = (self.color[0] // 4, self.color[1] // 4, self.color[2] // 4)

# 벽돌 배열 생성
bricks = []
rows = 6
cols = 10
brick_width = screen_width // cols
brick_height = 30

for row in range(rows):
    for col in range(cols):
        x = col * brick_width
        y = row * brick_height
        color = random.choice(COLORS)
        durability = random.randint(1, 3)
        bricks.append(Brick(x, y, brick_width, brick_height, color, durability))

# 게임 루프
paddle = Paddle()
ball = Ball()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move(-paddle.speed)
    if keys[pygame.K_RIGHT]:
        paddle.move(paddle.speed)

    ball.move()

    

    # 공과 패들의 충돌 검사
    if (paddle.y < ball.y + ball.radius < paddle.y + paddle.height and
        paddle.x < ball.x < paddle.x + paddle.width):
        ball.dy = -ball.dy

    # 공과 벽돌의 충돌 검사
    for brick in bricks[:]:
        if (brick.y < ball.y - ball.radius < brick.y + brick.height and
            brick.x < ball.x < brick.x + brick.width):
            ball.dy = -ball.dy
            brick.hit()
            if brick.durability <= 0:
                bricks.remove(brick)
            break

    screen.fill(BLACK)
    paddle.draw()
    ball.draw()
    for brick in bricks:
        brick.draw()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()



