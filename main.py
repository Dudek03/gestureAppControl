"""import pygame as pg

from Game import Game
from Screen_helper import Screen_helper
from UI_settings import UI_settings

pg.init()
screen = pg.display.set_mode(UI_settings.get_screen_start_size(), pg.RESIZABLE)
screen_size = pg.display.get_window_size()
Screen_helper.set_screen(screen)
Screen_helper.set_screen_size(screen_size)
clock = pg.time.Clock()
running = True
dt = 0
min_screen_size = (700, 400)

if __name__ == "__main__":
    game = Game(mode="normal")
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.VIDEORESIZE:
                screen_size = pg.display.get_window_size()
                Screen_helper.set_screen_size(((max(screen_size[0],min_screen_size[0])),(max(screen_size[1],min_screen_size[1]))))
                screen = pg.display.set_mode(Screen_helper.get_size(), pg.RESIZABLE)
                game.on_display_resize()
        screen.fill(UI_settings.get_screen_fill_color())
        game.update()

        pg.display.flip()

        dt = clock.tick(60) / 1000

    pg.quit()"""

import pygame as pg
import sys
from stable_baselines3 import PPO
from air_hockey_env import AirHockeyEnv

# Twoje stare, dobre importy:
from Screen_helper import Screen_helper
from UI_settings import UI_settings
from handTracking import HandTracker

# --- KONFIGURACJA KOLORÓW MENU ---
BG_COLOR = (30, 30, 30)
COLOR_UNSELECTED = (100, 100, 100)
COLOR_SELECTED = (46, 204, 113)
COLOR_HOVER = (130, 130, 130)
COLOR_START = (52, 152, 219)
COLOR_START_HOVER = (41, 128, 185)
TEXT_COLOR = (255, 255, 255)


def draw_text(surface, text, font, color, center):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=center)
    surface.blit(text_obj, text_rect)


def main_menu(screen, w, h, clock):
    font_title = pg.font.SysFont("Arial", 60, bold=True)
    font_subtitle = pg.font.SysFont("Arial", 30, bold=True)
    font_btn = pg.font.SysFont("Arial", 25)

    opponent_mode = "AI"
    control_mode = "MOUSE"

    btn_w, btn_h = 280, 50
    btn_ai_rect = pg.Rect(w // 2 - btn_w - 20, 220, btn_w, btn_h)
    btn_bot_rect = pg.Rect(w // 2 + 20, 220, btn_w, btn_h)
    btn_mouse_rect = pg.Rect(w // 2 - btn_w - 20, 380, btn_w, btn_h)
    btn_hand_rect = pg.Rect(w // 2 + 20, 380, btn_w, btn_h)
    btn_start_rect = pg.Rect(w // 2 - 200, 500, 400, 70)

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pg.mouse.get_pos()

        draw_text(screen, "AIR HOCKEY", font_title, TEXT_COLOR, (w // 2, 80))

        # --- WYBÓR PRZECIWNIKA ---
        draw_text(
            screen, "Wybierz przeciwnika:", font_subtitle, TEXT_COLOR, (w // 2, 180)
        )
        c_ai = (
            COLOR_SELECTED
            if opponent_mode == "AI"
            else (
                COLOR_HOVER if btn_ai_rect.collidepoint(mouse_pos) else COLOR_UNSELECTED
            )
        )
        pg.draw.rect(screen, c_ai, btn_ai_rect, border_radius=10)
        draw_text(screen, "Wyuczone AI", font_btn, TEXT_COLOR, btn_ai_rect.center)

        c_bot = (
            COLOR_SELECTED
            if opponent_mode == "BOT"
            else (
                COLOR_HOVER
                if btn_bot_rect.collidepoint(mouse_pos)
                else COLOR_UNSELECTED
            )
        )
        pg.draw.rect(screen, c_bot, btn_bot_rect, border_radius=10)
        draw_text(screen, "Skryptowany Bot", font_btn, TEXT_COLOR, btn_bot_rect.center)

        # --- WYBÓR STEROWANIA ---
        draw_text(
            screen, "Wybierz sterowanie:", font_subtitle, TEXT_COLOR, (w // 2, 340)
        )
        c_mouse = (
            COLOR_SELECTED
            if control_mode == "MOUSE"
            else (
                COLOR_HOVER
                if btn_mouse_rect.collidepoint(mouse_pos)
                else COLOR_UNSELECTED
            )
        )
        pg.draw.rect(screen, c_mouse, btn_mouse_rect, border_radius=10)
        draw_text(screen, "Myszka", font_btn, TEXT_COLOR, btn_mouse_rect.center)

        c_hand = (
            COLOR_SELECTED
            if control_mode == "HAND"
            else (
                COLOR_HOVER
                if btn_hand_rect.collidepoint(mouse_pos)
                else COLOR_UNSELECTED
            )
        )
        pg.draw.rect(screen, c_hand, btn_hand_rect, border_radius=10)
        draw_text(screen, "Ręka (Kamera)", font_btn, TEXT_COLOR, btn_hand_rect.center)

        # --- START ---
        c_start = (
            COLOR_START_HOVER if btn_start_rect.collidepoint(mouse_pos) else COLOR_START
        )
        pg.draw.rect(screen, c_start, btn_start_rect, border_radius=15)
        draw_text(screen, "START MECZU", font_title, TEXT_COLOR, btn_start_rect.center)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Obsługa zmiany rozmiaru okna w menu
            if event.type == pg.VIDEORESIZE:
                screen_size = pg.display.get_window_size()
                min_screen_size = (700, 400)
                Screen_helper.set_screen_size(
                    (
                        (max(screen_size[0], min_screen_size[0])),
                        (max(screen_size[1], min_screen_size[1])),
                    )
                )
                screen = pg.display.set_mode(Screen_helper.get_size(), pg.RESIZABLE)
                w, h = Screen_helper.get_size()
                # (Opcjonalnie: można tu ponownie przeliczyć pozycje prostokątów, ale dla uproszczenia centrujemy)

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if btn_ai_rect.collidepoint(mouse_pos):
                    opponent_mode = "AI"
                elif btn_bot_rect.collidepoint(mouse_pos):
                    opponent_mode = "BOT"
                elif btn_mouse_rect.collidepoint(mouse_pos):
                    control_mode = "MOUSE"
                elif btn_hand_rect.collidepoint(mouse_pos):
                    control_mode = "HAND"
                elif btn_start_rect.collidepoint(mouse_pos):
                    return opponent_mode, control_mode

        clock.tick(60)  # Menu też nie powinno smażyć procesora!


def play_game(opponent_mode, control_mode, screen, clock):
    env = AirHockeyEnv()
    obs, _ = env.reset()

    env.human_playing = True
    env.game.opponent.is_ai = False

    tracker = None
    if control_mode == "HAND":
        print("Inicjalizacja kamery i MediaPipe...")
        tracker = HandTracker()
        pg.time.wait(1000)
    else:
        print("Sterowanie myszką gotowe.")
        pg.mouse.set_visible(False)

    model = None
    if opponent_mode == "AI":
        print("Przeciwnik: Wyuczone AI")
        model_path = "models/PPO/14000000.zip"  # PODMIEŃ NA SWÓJ MODEL!
        model = PPO.load(model_path, env=env)
    else:
        print("Przeciwnik: Skryptowany Bot")
        env.game.player.is_ai = False

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            # Obsługa zmiany rozmiaru okna w trakcie gry
            if event.type == pg.VIDEORESIZE:
                screen_size = pg.display.get_window_size()
                min_screen_size = (700, 400)
                Screen_helper.set_screen_size(
                    (
                        (max(screen_size[0], min_screen_size[0])),
                        (max(screen_size[1], min_screen_size[1])),
                    )
                )
                screen = pg.display.set_mode(Screen_helper.get_size(), pg.RESIZABLE)
                env.game.on_display_resize()

        # Aktualny rozmiar okna dla Trackera
        screen_w, screen_h = Screen_helper.get_size()

        # Pobieranie pozycji dłoni
        if control_mode == "HAND" and tracker:
            if tracker.get_hand_visible():
                env.current_hand_pos = tracker.get_position(
                    target_width=screen_w, target_height=screen_h
                )
            else:
                env.current_hand_pos = env.game.opponent.get_player_pos()
        else:
            env.current_hand_pos = None

        # Ruch przeciwnika
        if opponent_mode == "AI":
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, info = env.step(action)
        else:
            dummy_action = [0, 0]
            obs, reward, terminated, truncated, info = env.step(dummy_action)
            env.game._move_opponent_script()

        # Rysowanie tła przed renderem gry (pobierane z UI_settings!)
        screen.fill(UI_settings.get_screen_fill_color())

        env.render()
        pg.display.flip()

        if terminated or truncated:
            obs, _ = env.reset()

        # ZEGAR Z TWOJEGO STAREGO MAIN! Pilnuje stałych 60 FPS.
        clock.tick(60)

    pg.mouse.set_visible(True)
    env.close()
    if tracker:
        tracker.stop()


def main():
    pg.init()

    # Inicjalizacja z Twojego starego main.py
    screen = pg.display.set_mode(UI_settings.get_screen_start_size(), pg.RESIZABLE)
    screen_size = pg.display.get_window_size()
    Screen_helper.set_screen(screen)
    Screen_helper.set_screen_size(screen_size)

    pg.display.set_caption("Air Hockey AI")
    clock = pg.time.Clock()

    w, h = Screen_helper.get_size()
    opp_mode, ctrl_mode = main_menu(screen, w, h, clock)

    play_game(opp_mode, ctrl_mode, screen, clock)


if __name__ == "__main__":
    main()
