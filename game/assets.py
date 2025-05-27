import pygame
from game.button import Button

class Assets:
    # Manages loading/scaling of game assets
    def __init__(self):
        self.load_fonts()
        self.load_images()
        self.load_sounds()
        pygame.mixer.music.set_volume(0.1)
        self.click_sound.set_volume(0.1)

        # Keep bigger buttons scaled properly (default size ~225x90)
        self.matematica_img = self.load_scaled("images/matematica.png", scale=0.4)
        self.portugues_img = self.load_scaled("images/portugues.png", scale=0.4)
        self.ingles_img = self.load_scaled("images/ingles.png", scale=0.4)
        self.humanas_img = self.load_scaled("images/humanas.png", scale=0.4)
        self.naturais_img = self.load_scaled("images/naturais.png", scale=0.4)
        self.start_img = self.load_scaled("images/botao_iniciar.png", scale=0.18)
        self.ranking_img = self.load_scaled("images/ranking.png", scale=0.18)
        self.back_img = self.load_scaled("images/botao_voltar.png", scale=0.18)

        # Reduce larger buttons proportionally
        self.fundamental_img = self.load_scaled("images/fundamental.png", scale=0.5)
        self.medio_img = self.load_scaled("images/medio.png", scale=0.5)

    def load_images(self):
        # Load background and UI images
        self.background = pygame.image.load("images/background.png").convert()
        self.logo_img = pygame.image.load("images/logo.png").convert_alpha()
        self.start_img = self.load_scaled("images/botao_iniciar.png")
        self.options_img = self.load_scaled("images/botao_opcoes.png")
        self.exit_img = self.load_scaled("images/botao_sair.png")
        self.music_img = self.load_scaled("images/botao_musica.png")
        self.sound_img = self.load_scaled("images/botao_som.png")
        self.back_img = self.load_scaled("images/botao_voltar.png")
        self.fullscreen_img = self.load_scaled("images/botao_tela.png")
        self.fundamental_img = self.load_scaled("images/fundamental.png")
        self.medio_img = self.load_scaled("images/medio.png")
        self.humanas_img = self.load_scaled("images/humanas.png")
        self.naturais_img = self.load_scaled("images/naturais.png")
        self.matematica_img = self.load_scaled("images/matematica.png")
        self.ingles_img = self.load_scaled("images/ingles.png")
        self.portugues_img = self.load_scaled("images/portugues.png")
        self.right_arrow_img = self.load_scaled("images/right_arrow.png")
        self.left_arrow_img = self.load_scaled("images/left_arrow.png")
        self.tip_box_img = self.load_scaled("images/tip_box.png")
        self.ranking_img = self.load_scaled("images/ranking.png")
        self.rankingblock_img = self.load_scaled("images/rankingblock.png")
        self.botao_dica0_img = self.load_scaled("images/botao_dica0.png")
        self.botao_dica1_img = self.load_scaled("images/botao_dica1.png")
        self.botao_dica2_img = self.load_scaled("images/botao_dica2.png")
        self.botao_dica3_img = self.load_scaled("images/botao_dica3.png")
        self.botao_eliminar0_img = self.load_scaled("images/botao_eliminar0.png")
        self.botao_eliminar1_img = self.load_scaled("images/botao_eliminar1.png")
        self.botao_eliminar2_img = self.load_scaled("images/botao_eliminar2.png")
        self.botao_eliminar3_img = self.load_scaled("images/botao_eliminar3.png")
        self.botao_pular0_img = self.load_scaled("images/botao_pular0.png")
        self.botao_pular1_img = self.load_scaled("images/botao_pular1.png")
        self.botao_pular2_img = self.load_scaled("images/botao_pular2.png")
        self.botao_pular3_img = self.load_scaled("images/botao_pular3.png")
        self.jogar_img = self.load_scaled("images/botao_jogar.png")

        self.checkbox_on = pygame.transform.scale(
            pygame.image.load("images/checkbox_on.png").convert_alpha(), (50, 50)
        )
        self.checkbox_off = pygame.transform.scale(
            pygame.image.load("images/checkbox_off.png").convert_alpha(), (50, 50)
        )

    def load_sounds(self):
        # Load music and sound effects
        pygame.mixer.music.load("assets/mainmenu.mp3")
        pygame.mixer.music.play(-1)  # loop music
        self.click_sound = pygame.mixer.Sound("assets/button.mp3")

    def load_fonts(self):
        # Load fonts
        self.font = pygame.font.Font("assets/Font.ttf", 74)
        self.volume_font = pygame.font.Font("assets/Font.ttf", 48)

    def load_scaled(self, path, width=None, height=None, scale=None):
        # Load image and scale (proportional or fixed)
        img = pygame.image.load(path).convert_alpha()
        if scale is not None:
            width = int(img.get_width() * scale)
            height = int(img.get_height() * scale)
        elif width is not None and height is not None:
            pass  # fixed size
        else:
            width, height = 225, 90  # default size
        return pygame.transform.scale(img, (width, height))


def create_button(x, y, text):
    # Create a semi-transparent button with centered text
    font = pygame.font.Font("assets/Font.ttf", 48)
    text_surf = font.render(text, True, (255, 255, 255))
    surface = pygame.Surface((225, 90), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 150))
    surface.blit(text_surf, ((225 - text_surf.get_width()) // 2, (90 - text_surf.get_height()) // 2))
    return Button(x, y, surface)