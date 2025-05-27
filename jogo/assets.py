import pygame
from button import Button

class Assets:
    # Manages loading/scaling of game assets
    def __init__(self):
        self.load_fonts()
        self.load_images()
        self.load_sounds()
        pygame.mixer.music.set_volume(0.1)
        self.click_sound.set_volume(0.1)

    def load_images(self):
        # Load background and UI images
        self.background = pygame.image.load("images/background.png").convert()
        self.logo_img = pygame.image.load("images/logo.png").convert_alpha()
        self.matematica_img = self.load_scaled("images/matematica.png", scale=0.4)
        self.portugues_img = self.load_scaled("images/portugues.png", scale=0.4)
        self.ingles_img = self.load_scaled("images/ingles.png", scale=0.4)
        self.humanas_img = self.load_scaled("images/humanas.png", scale=0.4)
        self.naturais_img = self.load_scaled("images/naturais.png", scale=0.4)
        self.start_img = self.load_scaled("images/botao_iniciar.png", scale=0.18)
        self.start_disabled_img = self.load_scaled("images/start_disabled.png", scale=0.18)
        self.ranking_img = self.load_scaled("images/ranking.png", scale=0.18)
        self.back_img = self.load_scaled("images/botao_voltar.png", scale=0.18)
        self.options_img = self.load_scaled("images/botao_opcoes.png")
        self.exit_img = self.load_scaled("images/botao_sair.png")
        self.music_img = self.load_scaled("images/botao_musica.png")
        self.sound_img = self.load_scaled("images/botao_som.png")
        self.fullscreen_img = self.load_scaled("images/botao_tela.png")
        self.fundamental_img = self.load_scaled("images/fundamental.png", scale=0.5)
        self.medio_img = self.load_scaled("images/medio.png", scale=0.5)
        self.right_arrow_img = self.load_scaled("images/right_arrow.png", width=104, height=104)
        self.left_arrow_img = self.load_scaled("images/left_arrow.png", width=104, height=104)
        self.tip_box_img = self.load_scaled("images/tip_box.png")
        self.rankingblock_img = self.load_scaled("images/rankingblock.png")
        self.botao_dica0_img = self.load_scaled("images/botao_dica0.png", width=180, height=80)
        self.botao_dica1_img = self.load_scaled("images/botao_dica1.png", width=180, height=80)
        self.botao_dica2_img = self.load_scaled("images/botao_dica2.png", width=180, height=80)
        self.botao_dica3_img = self.load_scaled("images/botao_dica3.png", width=180, height=80)
        self.botao_eliminar0_img = self.load_scaled("images/botao_eliminar0.png", width=180, height=80)
        self.botao_eliminar1_img = self.load_scaled("images/botao_eliminar1.png", width=180, height=80)
        self.botao_eliminar2_img = self.load_scaled("images/botao_eliminar2.png", width=180, height=80)
        self.botao_eliminar3_img = self.load_scaled("images/botao_eliminar3.png", width=180, height=80)
        self.botao_pular0_img = self.load_scaled("images/botao_pular0.png", width=180, height=80)
        self.botao_pular1_img = self.load_scaled("images/botao_pular1.png", width=180, height=80)
        self.botao_pular2_img = self.load_scaled("images/botao_pular2.png", width=180, height=80)
        self.botao_pular3_img = self.load_scaled("images/botao_pular3.png", width=180, height=80)
        self.jogar_img = self.load_scaled("images/botao_jogar.png")
        self.answer_a_img = self.load_scaled("images/answer_a.png", width=445, height=77)
        self.answer_b_img = self.load_scaled("images/answer_b.png", width=445, height=77)
        self.answer_c_img = self.load_scaled("images/answer_c.png", width=445, height=77)
        self.answer_d_img = self.load_scaled("images/answer_d.png", width=445, height=77)
        self.question_box_img = self.load_scaled("images/question_box.png", width=968, height=156)
        self.tip_box_img = self.load_scaled("images/tip_box.png", width=518, height=346)
        self.checkbox_on = self.load_scaled("images/checkbox_on.png", width=50, height=50)
        self.checkbox_off = self.load_scaled("images/checkbox_off.png", width=50, height=50)

    def load_sounds(self):
        # Load music and sound effects
        pygame.mixer.music.load("assets/mainmenu.mp3")
        pygame.mixer.music.play(-1)  # loop music
        self.click_sound = pygame.mixer.Sound("assets/button.mp3")

    def load_fonts(self):
        # Load fonts
        self.font = pygame.font.Font("assets/Font.ttf", 74)
        self.volume_font = pygame.font.Font("assets/Font.ttf", 48)
        self.small_font = pygame.font.Font("assets/Font.ttf", 24)
        self.medium_font = pygame.font.Font("assets/Font.ttf", 36)
        self.large_font = pygame.font.Font("assets/Font.ttf", 48)

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