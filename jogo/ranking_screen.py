import pygame
import json
import os

class RankingScreen:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

        # Fontes usadas na tela
        self.small_font = assets.small_font
        self.medium_font = assets.font
        self.large_font = assets.large_font

        # Caminho do arquivo JSON onde o ranking é salvo
        self.file_path = "jogo/ranking_data.json"

        self.running = True

        # Carrega e redimensiona a imagem de fundo para preencher a tela
        self.bg_image = pygame.image.load("images/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        # Configura o botão "Voltar" com sua imagem e posição fixa
        self.botao_voltar_img = self.assets.back_img
        self.botao_voltar_rect = self.botao_voltar_img.get_rect(topleft=(10, self.screen.get_height() - 70))

        # Carrega os dados do ranking do arquivo
        self.load_ranking()

    def load_ranking(self):
        # Tenta carregar o ranking do arquivo JSON, caso não exista, inicializa com dado padrão
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.ranking_data = json.load(file)
        else:
            self.ranking_data = {"teste": 0}  # Dado padrão caso o arquivo não exista

    def save_ranking(self):
        # Salva os dados do ranking no arquivo JSON (não usado aqui, mas útil para atualizações)
        with open(self.file_path, "w") as file:
            json.dump(self.ranking_data, file)

    def draw(self):
        # Desenha o fundo da tela
        self.screen.blit(self.bg_image, (0, 0))

        # Renderiza o título centralizado no topo da tela
        title_surface = self.medium_font.render("Ranking", True, (1, 227, 197))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Ordena o ranking por pontuação decrescente para exibição
        sorted_ranking = sorted(self.ranking_data.items(), key=lambda x: x[1], reverse=True)
        for i, (user, score) in enumerate(sorted_ranking):
            # Formata o texto do ranking, substituindo vírgulas por pontos para o padrão local
            text = f"{i+1}. {user}: P$ {score:,.0f}".replace(",", ".")
            score_surface = self.small_font.render(text, True, (255, 50, 94))
            # Desenha cada linha do ranking na vertical, com espaçamento de 40 pixels
            self.screen.blit(score_surface, (100, 120 + i * 40))

        # Desenha o botão "Voltar" na tela
        self.screen.blit(self.botao_voltar_img, self.botao_voltar_rect)

        # Atualiza a tela com tudo que foi desenhado
        pygame.display.update()

    def run(self):
        # Loop principal da tela de ranking
        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Fecha o jogo ao clicar no X da janela
                    self.running = False
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Detecta clique no botão "Voltar"
                    if self.botao_voltar_rect.collidepoint(event.pos):
                        self.assets.click_sound.play()  # Toca som do clique
                        self.running = False
                        return "subjects_menu"  # Retorna para a tela de seleção de matérias
