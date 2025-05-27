import pygame
from jogo.button import Button

# Tela do menu principal
class MainMenu:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.options_clicked = False
        self.exit_clicked = False

        self.jogar_button = Button(427, 260, assets.jogar_img)
        self.options_button = Button(427, 410, assets.options_img)
        self.exit_button = Button(427, 560, assets.exit_img)

    def update(self):
        jogar = self.jogar_button.draw(self.screen)
        options = self.options_button.draw(self.screen)
        exit_ = self.exit_button.draw(self.screen)

        self.options_clicked = options
        self.exit_clicked = exit_
        return jogar

# Tela de opções
class OptionsMenu:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.music_playing = True
        self.sound_on = True
        self.is_fullscreen = False  # Estado desejado de tela cheia
        self.volume = 0.2

        self.music_button = Button(427, 230, assets.music_img)
        self.sound_button = Button(427, 380, assets.sound_img)
        self.back_button = Button(10, 650, assets.back_img)
        self.fullscreen_button = Button(427, 530, assets.fullscreen_img)

        pygame.mixer.music.set_volume(self.volume)
        self.assets.click_sound.set_volume(self.volume if self.sound_on else 0)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        print(f"OptionsMenu: Intencao de fullscreen alterada para {self.is_fullscreen}")

    def show(self):
        action_to_return = None

        # Aguarda o clique anterior ser solto
        while pygame.mouse.get_pressed()[0]:
            pygame.event.pump()
            pygame.time.wait(10)

        running = True
        while running:
            self.screen.blit(self.assets.background, (0, 0))
            text = self.assets.font.render("Opções", True, (0, 227, 197))
            self.screen.blit(text, (540 - text.get_width() // 2, 50))

            self._draw_checkbox(self.music_playing, 680, 245)
            self._draw_checkbox(self.sound_on, 680, 395)
            self._draw_checkbox(self.is_fullscreen, 680, 545)

            if self.music_button.draw(self.screen):
                self.assets.click_sound.play()
                self.toggle_music()

            if self.sound_button.draw(self.screen):
                self.assets.click_sound.play()
                self.toggle_sound()

            if self.fullscreen_button.draw(self.screen):
                self.assets.click_sound.play()
                pygame.time.wait(100)
                self.toggle_fullscreen()
                action_to_return = "TOGGLE_FULLSCREEN"
                running = False

            if self.back_button.draw(self.screen):
                self.assets.click_sound.play()
                pygame.time.wait(100)
                action_to_return = None
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    action_to_return = "QUIT"
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Clique na barra de volume
                    if 340 < event.pos[0] < 740 and 300 < event.pos[1] < 320:
                        self.volume = (event.pos[0] - 340) / 400
                        pygame.mixer.music.set_volume(self.volume)
                        if self.sound_on:
                            self.assets.click_sound.set_volume(self.volume)

            pygame.display.update()

        return action_to_return

    def _draw_checkbox(self, state, x, y):
        img = self.assets.checkbox_on if state else self.assets.checkbox_off
        self.screen.blit(img, (x, y))

    def toggle_music(self):
        if self.music_playing:
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.volume)
        self.music_playing = not self.music_playing

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.assets.click_sound.set_volume(self.volume if self.sound_on else 0)