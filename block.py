import os
import random
import math
import sys
import time
import pygame as pg

# --- 定数定義 ---
WIDTH = 1100   # 画面の幅
HEIGHT = 650   # 画面の高さ
FPS = 60       # フレームレート（1秒あたりの更新回数）
PADDLE_Y_OFFSET = 50  # 下からバーを上げる量



# 作業ディレクトリをスクリプトのある場所に変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

class Background:
    def __init__(self, path="fig/0.png"):
        raw = pg.image.load(path).convert()
        self.img = pg.transform.scale(raw, (WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.img, (0, 0))
        

class Paddle:
    def __init__(self, pos):
        # バー画像の読み込み
        img = pg.image.load("fig/bar.png").convert_alpha()
        self.img = pg.transform.scale(img, (100, 15))
        self.rect = self.img.get_rect(midbottom=pos)
        self.speed = 12

        # こうかとん画像の準備
        raw = pg.image.load("fig/fly.png").convert_alpha()
        char_w = self.rect.width // 2
        char_h = int(char_w * raw.get_height() / raw.get_width())
        self.char_img = pg.transform.scale(raw, (char_w, char_h))
        self.dir = 1

    def update(self, keys):
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dir = 1
        if keys[pg.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.dir = -1

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        char = self.char_img
        if self.dir < 0:
            char = pg.transform.flip(self.char_img, True, False)
        # バー下への描画位置を少し上にずらす
        mx, my = self.rect.midbottom
        char_rect = char.get_rect(midtop=(mx, my - 5))  # 5px 上にオフセット
        screen.blit(char, char_rect)


        

class Ball:
    def __init__(self, pos, radius=10):
        self.pos = pg.math.Vector2(pos)
        angle = random.uniform(-math.pi/4, -3*math.pi/4)
        speed = 10
        self.vel = pg.math.Vector2(
            speed * math.cos(angle),
            speed * math.sin(angle)
        )
        self.radius = radius
        self.color = (255, 100, 100)

    def update(self):
        self.pos += self.vel
        if self.pos.x - self.radius <= 0 or self.pos.x + self.radius >= WIDTH:
            self.vel.x *= -1
        if self.pos.y - self.radius <= 0:
            self.vel.y *= -1
        

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def get_rect(self) -> pg.Rect:
        return pg.Rect(
            int(self.pos.x - self.radius),
            int(self.pos.y - self.radius),
            self.radius * 2, self.radius * 2
        )

class Ringo:  #りんごのクラス
    def __init__(self,ap_x,ap_y,ap_rad):
        self.ap_x = ap_x
        self.ap_y = ap_y
        self.color = (255,0,0)
        self.ap_rad = ap_rad
        #座標と半径、色
        
    def update(self):
        
        self.ap_y += 2
        
            
    def draw(self,screen):
        
        # pg.draw.circle(screen,self.color,(self.ap_x, int(self.ap_y)),self.ap_rad)
        app_img = pg.image.load("fig/apple.png")
        app_img = pg.transform.scale(app_img,(60,60))
        screen.blit(app_img,(self.ap_x, int(self.ap_y)))
        
            

    def get_rect(self) -> pg.Rect:
        return pg.Rect(
            int(self.ap_x - self.ap_rad),
            int(self.ap_y - self.ap_rad),
            self.ap_rad * 2, self.ap_rad * 2
        )

class HUD:
    def __init__(self, font):
        self.font = font
        self.hp = 3
        self.mp = 5

    def draw(self, screen):
        hp_s = self.font.render(f"HP: {self.hp}/3", True, (255,255,255))
        mp_s = self.font.render(f"MP: {self.mp}/5", True, (255,255,255))
        screen.blit(hp_s, (10, 10))
        screen.blit(mp_s, (10, 40))

class Game:
    def __init__(self):
        pg.display.set_caption("ブロック崩し")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.bg = Background()
        # バーとキャラをより上に配置
        self.paddle = Paddle((WIDTH//2, HEIGHT - PADDLE_Y_OFFSET))
        self.ball = Ball((self.paddle.rect.centerx, self.paddle.rect.top - 10))
        self.app = Ringo(100,-500,30)
        self.font = pg.font.Font(None, 36)
        self.hud = HUD(self.font)
        self.running = True
        self.game_over_font = pg.font.Font(None, 100)

    def run(self):
        while self.running:

            self.clock.tick(FPS)
            self._events()
            self._update()
            self._draw()
            

            if self.hud.hp <= 0:
                self._draw_game_over()
                pg.display.flip()
                pg.time.delay(3000)
                self.running = False
            

        pg.quit()
        sys.exit()

    def _events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def _update(self):
        keys = pg.key.get_pressed()
        self.paddle.update(keys)
        self.ball.update()
        self.app.update()

        if self.ball.get_rect().colliderect(self.paddle.rect):
            self.ball.vel.y *= -1
        
        if self.app.get_rect().colliderect(self.paddle.rect):
            if self.hud.hp < 3 :
                self.hud.hp += 1
            else :
                None
            self.app.ap_x = random.randint(100,2300)
            self.app.ap_y = -200
        

        if self.ball.pos.y - self.ball.radius > HEIGHT:
            self.hud.hp -= 1
            pg.time.delay(500)
            self.ball = Ball((self.paddle.rect.centerx, self.paddle.rect.top - 10))
            self.app.ap_y = -400
            self.app.ap_x = random.randint(100,2300)
            #リンゴが落ちたときに再度落ちてくる
        if self.app.ap_y >= 700:
            self.app.ap_y = -400
            self.app.ap_x = random.randint(100,2300)

    def _draw(self):
        self.screen.fill((0, 0, 0))
        self.bg.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.hud.draw(self.screen)
        self.app.draw(self.screen)
        pg.display.flip()
        

    def _draw_game_over(self):
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        game_over_surf = self.game_over_font.render("Game Over", True, (255, 0, 0))
        rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(game_over_surf, rect)
        


def main():
    pg.init()
    Game().run()

if __name__ == "__main__":
    main()
