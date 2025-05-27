import pygame
import json
import os

class RankingScreen:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.small_font = assets.small_font
        self.medium_font = assets.font
        self.large_font = assets.large_font
        self.file_path = "ranking_data.json"
        self.running = True
        self.bg_image = pygame.image.load("images/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())

        self.load_ranking()

    def load_ranking(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.ranking_data = json.load(file)
        else:
            self.ranking_data = {"teste": 0}

    def save_ranking(self):
        with open(self.file_path, "w") as file:
            json.dump(self.ranking_data, file)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))

        # Título "Ranking"
        title_surface = self.medium_font.render("Ranking", True, (1, 227, 197))
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_surface, title_rect)

        # Exibir pontuações
        sorted_ranking = sorted(self.ranking_data.items(), key=lambda x: x[1], reverse=True)
        for i, (user, score) in enumerate(sorted_ranking):
            text = f"{i+1}. {user}: R$ {score:,.0f}".replace(",", ".")
            score_surface = self.small_font.render(text, True, (255, 50, 94))
            self.screen.blit(score_surface, (100, 120 + i * 40))

        pygame.display.update()

    def run(self):
        while self.running:
            self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.running = False  # volta pra tela anterior
