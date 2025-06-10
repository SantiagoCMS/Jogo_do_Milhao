import pygame
from jogo.menus import MainMenu, OptionsMenu
from jogo.assets import Assets
from jogo.subjects_menu import SubjectsMenu  # Tela para escolher nível e matérias
from jogo.game_screen import GameScreen      # Tela do jogo principal, recebe nível e matérias
from jogo.ranking_screen import RankingScreen

class Game:
    """Controlador principal do jogo, inicializa Pygame, carrega assets, menus e gerencia troca de telas."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Configura tamanho da janela
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Code Milionário")

        # Carrega imagens, sons, fontes, etc.
        self.assets = Assets()

        # Inicializa as telas persistentes (sem parâmetros dinâmicos)
        self.main_menu = MainMenu(self.screen, self.assets)
        self.options_menu = OptionsMenu(self.screen, self.assets)
        self.subjects_menu = SubjectsMenu(self.screen, self.assets)
        self.ranking_screen = RankingScreen(self.screen, self.assets)

        # GameScreen será criado sob demanda, com nível e matérias selecionados
        self.running = True  # Flag do loop principal

    def run(self):
        """Loop principal do jogo que gerencia exibição e troca de telas."""
        while self.running:
            # Desenha fundo e logo a cada frame (antes da tela específica)
            self.screen.blit(self.assets.background, (0, 0))
            logo_x = (self.SCREEN_WIDTH - self.assets.logo_img.get_width()) // 2
            self.screen.blit(self.assets.logo_img, (logo_x, 30))

            # Atualiza o menu principal e verifica se o botão "Jogar" foi clicado
            if self.main_menu.update():  # Retorna True se "Jogar" foi clicado
                self.assets.click_sound.play()

                # Mostra tela de seleção de nível e matérias (bloqueante)
                selected_level, selected_subjects_list = self.subjects_menu.show()

                if selected_level and selected_subjects_list:
                    # Se seleção válida, instancia GameScreen com os filtros
                    current_game_instance = GameScreen(self.screen, self.assets, selected_level, selected_subjects_list)
                    current_game_instance.show()  # Executa o jogo (bloqueante)

                    # Após sair do jogo, limpa eventos para evitar cliques acumulados no menu
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    pygame.event.clear(pygame.MOUSEBUTTONUP)
                # Se usuário cancelou ou voltou, retorna ao menu principal

            elif self.main_menu.options_clicked:
                self.assets.click_sound.play()

                # Mostra tela de opções (bloqueante)
                self.options_menu.show()

                # Ajusta modo fullscreen se foi alterado
                fullscreen_status_after_options = getattr(self.options_menu, 'is_fullscreen', pygame.display.is_fullscreen())
                current_flags = self.screen.get_flags()
                is_currently_fullscreen = bool(current_flags & pygame.FULLSCREEN)

                if fullscreen_status_after_options and not is_currently_fullscreen:
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
                elif not fullscreen_status_after_options and is_currently_fullscreen:
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                # Atualiza a referência da tela nas outras telas para a nova janela criada
                self.main_menu.screen = self.screen
                self.options_menu.screen = self.screen
                self.subjects_menu.screen = self.screen
                self.ranking_screen.screen = self.screen

                self.main_menu.options_clicked = False  # Reseta flag após processar

            elif self.main_menu.exit_clicked:
                self.assets.click_sound.play()
                self.running = False  # Sai do loop principal e fecha o jogo

            # Eventos globais, como fechar a janela principal
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()  # Atualiza a tela a cada frame

        pygame.quit()  # Encerra Pygame ao sair do loop

# Executa o jogo se for o arquivo principal
if __name__ == '__main__':
    game = Game()
    game.run()
