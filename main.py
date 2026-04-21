import pygame as pg
import sys
from stable_baselines3 import PPO
from air_hockey_env import AirHockeyEnv

from Screen_helper import Screen_helper
from UI_settings import UI_settings

BG_COLOR = (30, 30, 30)
COLOR_UNSELECTED = (100, 100, 100)
COLOR_SELECTED = (46, 204, 113)
COLOR_HOVER = (130, 130, 130)
COLOR_START = (52, 152, 219)
COLOR_START_HOVER = (41, 128, 185)
TEXT_COLOR = (255, 255, 255)

min_screen_size = (700, 400)


def draw_text(surface, text, font, color, center):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=center)
    surface.blit(text_obj, text_rect)


def main_menu(screen, w, h, clock):
    # Czcionki zostawiamy stałe, by uniknąć zniekształceń, ale możesz je też skalować!
    font_title = pg.font.SysFont("Arial", 50, bold=True)
    font_subtitle = pg.font.SysFont("Arial", 25, bold=True)
    font_btn = pg.font.SysFont("Arial", 22)

    opponent_mode = "AI"
    control_mode = "MOUSE"
    hand_model_mode = "MEDIAPIPE"

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pg.mouse.get_pos()

        curr_w, curr_h = screen.get_size()

        btn_w = max(200, int(curr_w * 0.35))
        btn_h = max(40, int(curr_h * 0.08))
        gap = int(curr_w * 0.02)

        y_title = int(curr_h * 0.10)  # Tytuł na 10% wysokości

        y_g1_title = int(curr_h * 0.22)  # Grupa 1 na 22%
        y_g1_btns = int(curr_h * 0.28)  # Przyciski G1 na 28%

        y_g2_title = int(curr_h * 0.42)  # Grupa 2 na 42%
        y_g2_btns = int(curr_h * 0.48)

        y_g3_title = int(curr_h * 0.62)  # Grupa 3 (Ręka) na 62%
        y_g3_btns = int(curr_h * 0.68)

        y_start = int(curr_h * 0.85)  # Przycisk start na samym dole (85%)
        start_h = max(60, int(curr_h * 0.1))

        # ==========================================
        # TWORZENIE RESPONSYWNYCH HITBOXÓW (RECT)
        # ==========================================
        btn_ai_rect = pg.Rect(curr_w // 2 - btn_w - gap, y_g1_btns, btn_w, btn_h)
        btn_bot_rect = pg.Rect(curr_w // 2 + gap, y_g1_btns, btn_w, btn_h)

        btn_mouse_rect = pg.Rect(curr_w // 2 - btn_w - gap, y_g2_btns, btn_w, btn_h)
        btn_hand_rect = pg.Rect(curr_w // 2 + gap, y_g2_btns, btn_w, btn_h)

        btn_mp_rect = pg.Rect(curr_w // 2 - btn_w - gap, y_g3_btns, btn_w, btn_h)
        btn_own_rect = pg.Rect(curr_w // 2 + gap, y_g3_btns, btn_w, btn_h)

        btn_start_rect = pg.Rect(
            curr_w // 2 - int(curr_w * 0.3), y_start, int(curr_w * 0.6), start_h
        )

        # ==========================================
        # RYSOWANIE MENU
        # ==========================================
        draw_text(screen, "AIR HOCKEY", font_title, TEXT_COLOR, (curr_w // 2, y_title))

        # --- WYBÓR PRZECIWNIKA ---
        draw_text(
            screen,
            "Wybierz przeciwnika:",
            font_subtitle,
            TEXT_COLOR,
            (curr_w // 2, y_g1_title),
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
            screen,
            "Wybierz sterowanie:",
            font_subtitle,
            TEXT_COLOR,
            (curr_w // 2, y_g2_title),
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

        # --- WYBÓR MODELU RĘKI ---
        if control_mode == "HAND":
            draw_text(
                screen,
                "Model detekcji dłoni:",
                font_subtitle,
                (200, 200, 200),
                (curr_w // 2, y_g3_title),
            )

            c_mp = (
                COLOR_SELECTED
                if hand_model_mode == "MEDIAPIPE"
                else (
                    COLOR_HOVER
                    if btn_mp_rect.collidepoint(mouse_pos)
                    else COLOR_UNSELECTED
                )
            )
            pg.draw.rect(screen, c_mp, btn_mp_rect, border_radius=10)
            draw_text(screen, "MediaPipe", font_btn, TEXT_COLOR, btn_mp_rect.center)

            c_own = (
                COLOR_SELECTED
                if hand_model_mode == "OWN_MODEL"
                else (
                    COLOR_HOVER
                    if btn_own_rect.collidepoint(mouse_pos)
                    else COLOR_UNSELECTED
                )
            )
            pg.draw.rect(screen, c_own, btn_own_rect, border_radius=10)
            draw_text(screen, "Własny Model", font_btn, TEXT_COLOR, btn_own_rect.center)

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

            if event.type == pg.VIDEORESIZE:
                screen_size = (event.w, event.h)
                min_screen_size = (700, 400)
                Screen_helper.set_screen_size(
                    (
                        (max(screen_size[0], min_screen_size[0])),
                        (max(screen_size[1], min_screen_size[1])),
                    )
                )
                screen = pg.display.set_mode(Screen_helper.get_size(), pg.RESIZABLE)
                w, h = Screen_helper.get_size()

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
                    # Zwracamy wszystkie TRZY zmienne!
                    return opponent_mode, control_mode, hand_model_mode

                # Przyciski modelu klikalne tylko jeśli aktywna jest Ręka
                if control_mode == "HAND":
                    if btn_mp_rect.collidepoint(mouse_pos):
                        hand_model_mode = "MEDIAPIPE"
                    elif btn_own_rect.collidepoint(mouse_pos):
                        hand_model_mode = "OWN_MODEL"

        clock.tick(60)


def play_game(opponent_mode, control_mode, hand_model_mode, screen, clock):
    env = AirHockeyEnv()
    obs, _ = env.reset()

    env.human_playing = True
    env.game.opponent.is_ai = False

    tracker = None
    if control_mode == "HAND":
        if hand_model_mode == "MEDIAPIPE":
            print("Inicjalizacja kamery: MediaPipe...")
            from gesture_controll import HandTracker
        else:
            print("Inicjalizacja kamery: Własny Model...")
            from gesture_controll_own_model import HandTracker

        tracker = HandTracker()
        pg.time.wait(1000)
    else:
        print("Sterowanie myszką gotowe.")
        pg.mouse.set_visible(True)

    model = None
    if opponent_mode == "AI":
        print("Przeciwnik: Wyuczone AI")
        model_path = "3900000.zip "
        model = PPO.load(model_path, env=env)
    else:
        print("Przeciwnik: Skryptowany Bot")

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.VIDEORESIZE:
                screen_size = pg.display.get_window_size()
                Screen_helper.set_screen_size(
                    (
                        (max(screen_size[0], min_screen_size[0])),
                        (max(screen_size[1], min_screen_size[1])),
                    )
                )
                screen = pg.display.set_mode(Screen_helper.get_size(), pg.RESIZABLE)
                env.game.on_display_resize()

        screen_w, screen_h = Screen_helper.get_size()

        # Wspólny kod dla HandTrackera (obie klasy mają te same metody!)
        if control_mode == "HAND" and tracker:
            if tracker.get_hand_visible():
                env.current_hand_pos = tracker.get_position(
                    target_width=screen_w, target_height=screen_h
                )
            else:
                env.current_hand_pos = env.game.opponent.get_player_pos()
        else:
            env.current_hand_pos = None

        if opponent_mode == "AI":
            action, _ = model.predict(obs, deterministic=True)
        else:
            action = env.game._move_player_script()

        obs, reward, terminated, truncated, info = env.step(action)

        screen.fill(UI_settings.get_screen_fill_color())

        env.render()
        pg.display.flip()

        if terminated or truncated:
            obs, _ = env.reset()

        clock.tick(60)

    pg.mouse.set_visible(True)
    env.close()
    if tracker:
        tracker.stop()


def main():
    pg.init()

    screen = pg.display.set_mode(UI_settings.get_screen_start_size(), pg.RESIZABLE)
    screen_size = pg.display.get_window_size()
    Screen_helper.set_screen(screen)
    Screen_helper.set_screen_size(screen_size)

    pg.display.set_caption("Air Hockey AI")
    clock = pg.time.Clock()

    w, h = Screen_helper.get_size()

    # Odbieramy trzy zmienne z menu
    opp_mode, ctrl_mode, hand_mode = main_menu(screen, w, h, clock)

    # Przekazujemy je dalej
    play_game(opp_mode, ctrl_mode, hand_mode, screen, clock)


if __name__ == "__main__":
    main()
