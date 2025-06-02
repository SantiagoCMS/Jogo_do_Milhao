import pygame
from jogo.menus import MainMenu, OptionsMenu
from jogo.assets import Assets
from jogo.subjects_menu import SubjectsMenu # Presume que esta é a versão que retorna (nível, matérias)
from jogo.game_screen import GameScreen     # Presume que esta é a versão que aceita (nível, matérias) no __init__
from jogo.ranking_screen import RankingScreen

class Game:
    """Controlador principal do jogo (inicializa Pygame, menus e gerencia a troca de telas)."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Tamanho da janela
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Code Milionário")

        # Carrega imagens, sons, fontes, etc.
        self.assets = Assets()

        # Inicializa as telas que são persistentes ou chamadas sem parâmetros dinâmicos
        self.main_menu = MainMenu(self.screen, self.assets)
        self.options_menu = OptionsMenu(self.screen, self.assets)
        self.subjects_menu = SubjectsMenu(self.screen, self.assets)
        self.ranking_screen = RankingScreen(self.screen, self.assets)

        # self.game_screen = GameScreen(self.screen, self.assets) # << REMOVIDO DAQUI
        # GameScreen será instanciada sob demanda com os filtros corretos.

        self.running = True  # Loop principal

    def run(self):
        """Executa o loop principal do jogo."""
        while self.running:
            # Fundo e logo (desenhados a cada frame, antes da tela específica)
            self.screen.blit(self.assets.background, (0, 0))
            logo_x = (self.SCREEN_WIDTH - self.assets.logo_img.get_width()) // 2
            self.screen.blit(self.assets.logo_img, (logo_x, 30))

            # Lógica do Menu Principal
            # self.main_menu.update() é chamado e desenha os botões do menu principal.
            # Ele retorna True se "Jogar" for clicado, e também pode setar
            # self.main_menu.options_clicked ou self.main_menu.exit_clicked.

            # Ação padrão é mostrar o menu principal e suas opções
            # Se uma ação levar a outra tela, o loop principal continua e a nova tela é mostrada.

            if self.main_menu.update(): # Assume que update() retorna True se "Jogar" foi clicado
                self.assets.click_sound.play()

                # Chama SubjectsMenu.show() que agora é bloqueante e retorna as seleções
                # (selected_level, selected_subjects_list) ou (None, None)
                selected_level, selected_subjects_list = self.subjects_menu.show()

                if selected_level and selected_subjects_list:
                    # Se o usuário selecionou nível e matérias e clicou em "Iniciar"
                    # Cria uma NOVA instância de GameScreen com os filtros
                    current_game_instance = GameScreen(self.screen, self.assets, selected_level, selected_subjects_list)
                    current_game_instance.show() # Roda a tela do jogo (bloqueante)

                    # Após o jogo terminar (GameScreen.show() retornar), o loop principal continua.
                    # O MainMenu será desenhado novamente na próxima iteração.
                    # É bom limpar eventos de mouse para evitar cliques residuais no menu.
                    pygame.event.clear(pygame.MOUSEBUTTONDOWN)
                    pygame.event.clear(pygame.MOUSEBUTTONUP)
                # else: O usuário clicou em "Voltar" no SubjectsMenu ou fechou a janela.
                # O loop continua, e o MainMenu será processado/desenhado na próxima iteração.

            elif self.main_menu.options_clicked: # Usar elif para garantir que apenas uma ação principal do menu seja processada por vez
                self.assets.click_sound.play()

                # Assume que options_menu.show() é bloqueante e lida com a lógica de tela cheia internamente,
                # atualizando self.options_menu.is_fullscreen e potencialmente recriando self.screen.
                # A flag 'tela_foi_alterada' no seu código original precisaria ser retornada por options_menu.show()
                # ou a lógica de recriação da tela principal precisa estar aqui.

                # Para simplificar, vamos supor que options_menu.show() pode retornar um status ou lidar com a mudança
                self.options_menu.show()

                # Se o OptionsMenu mudou o modo da tela, precisamos atualizar a referência 'self.screen'
                # e passá-la para as outras telas se elas não pegarem a referência global do Pygame.
                # A sua lógica original de recriar self.screen:
                fullscreen_status_after_options = getattr(self.options_menu, 'is_fullscreen', pygame.display.is_fullscreen())

                current_flags = self.screen.get_flags()
                is_currently_fullscreen = bool(current_flags & pygame.FULLSCREEN)

                if fullscreen_status_after_options and not is_currently_fullscreen:
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.FULLSCREEN)
                elif not fullscreen_status_after_options and is_currently_fullscreen:
                    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

                # Atualiza a referência da tela nas outras telas persistentes
                # Se a instância da tela foi recriada (como self.screen acima), as outras precisam saber.
                # Esta abordagem de reatribuir self.screen é um pouco incomum; geralmente,
                # os objetos de tela pegam a superfície principal na sua criação.
                # Se você recria self.screen, você PRECISA atualizar todas as suas instâncias de tela.
                self.main_menu.screen = self.screen
                self.options_menu.screen = self.screen
                self.subjects_menu.screen = self.screen
                self.ranking_screen.screen = self.screen
                # self.game_screen.screen = self.screen # GameScreen é instanciada sob demanda, então pegará a tela atual.

                self.main_menu.options_clicked = False # Reseta a flag

            elif self.main_menu.exit_clicked:
                self.assets.click_sound.play()
                self.running = False

            # Eventos globais (como fechar a janela principal)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        pygame.quit()

# Para iniciar o jogo:
if __name__ == '__main__':
    game = Game()
    game.run()