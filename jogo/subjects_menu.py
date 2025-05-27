import pygame
from jogo.button import Button
from jogo.ranking_screen import RankingScreen

class SubjectsMenu:
    """
    Tela onde o jogador escolhe o módulo (fundamental ou médio) e as matérias para o quiz.
    """
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

        self.selected_subjects = []  # Lista com os nomes das opções selecionadas.
        self.start_clicked = False  # Informa ao Game.py que o botão Iniciar foi clicado.

        self.subject_categories = ["matematica", "portugues", "ingles", "naturais", "humanas"]

        # Cria os botões com suas respectivas imagens.
        self.buttons = {
            "fundamental": Button(150, 140, assets.fundamental_img),
            "medio": Button(600, 140, assets.medio_img),
            "matematica": Button(55, 390, assets.matematica_img),
            "portugues": Button(405, 390, assets.portugues_img),
            "ingles": Button(755, 390, assets.ingles_img),
            "naturais": Button(230, 540, assets.naturais_img),
            "humanas": Button(580, 540, assets.humanas_img),
            "start": Button(910, 650, assets.start_img),
            "ranking": Button(470, 650, assets.ranking_img),
            "voltar": Button(10, 650, assets.back_img),
        }

    def show(self):
        """Exibe a tela e lida com os cliques até sair ou iniciar o jogo."""
        self.running = True
        self.start_clicked = False

        # Prepara imagens do botão "Iniciar" (ativa e desativada).
        original_start_button_image = self.assets.start_img
        disabled_start_button_image = getattr(self.assets, 'start_disabled_img', getattr(self.assets, 'start_inactive_img', None))

        while self.running:
            self.screen.blit(self.assets.background, (0, 0))  # Fundo da tela.

            # Título centralizado.
            text_surface = self.assets.font.render("Escolha matérias", True, (0, 227, 197))
            self.screen.blit(text_surface, (540 - text_surface.get_width() // 2, 10))

            # Verifica se "Iniciar" deve estar habilitado.
            module_selected = ("fundamental" in self.selected_subjects or "medio" in self.selected_subjects)
            actual_subject_selected = any(s_cat in self.selected_subjects for s_cat in self.subject_categories)
            start_button_can_be_activated = module_selected and actual_subject_selected

            # Troca a imagem do botão Iniciar se estiver desabilitado.
            if disabled_start_button_image:
                self.buttons["start"].image = original_start_button_image if start_button_can_be_activated else disabled_start_button_image

            for name, button in self.buttons.items():
                if button.draw(self.screen):  # Se foi clicado:
                    if name == "start" and start_button_can_be_activated:
                        self.assets.click_sound.play()
                        self.start_clicked = True
                        self.running = False

                    elif name == "voltar":
                        self.assets.click_sound.play()
                        self.running = False

                    elif name == "ranking":
                        self.assets.click_sound.play()
                        ranking_screen = RankingScreen(self.screen, self.assets)
                        ranking_screen.run()

                    else:
                        self.assets.click_sound.play()
                        if name in self.selected_subjects:
                            self.selected_subjects.remove(name)
                        else:
                            if name == "fundamental":
                                self.selected_subjects = [s for s in self.selected_subjects if s != "medio"]
                            elif name == "medio":
                                self.selected_subjects = [s for s in self.selected_subjects if s != "fundamental"]
                            self.selected_subjects.append(name)

            # Exibe os checkboxes abaixo dos botões selecionáveis.
            for name, button_obj in self.buttons.items():
                if name in ["fundamental", "medio"] + self.subject_categories:
                    is_selected = name in self.selected_subjects
                    checkbox_image = self.assets.checkbox_on if is_selected else self.assets.checkbox_off
                    cb_x = button_obj.rect.centerx - checkbox_image.get_width() // 2
                    cb_y = button_obj.rect.bottom + 5
                    self.screen.blit(checkbox_image, (cb_x, cb_y))

            # Fecha janela.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        # Restaura imagem original do botão "Iniciar" caso o menu seja reusado.
        if disabled_start_button_image:
            self.buttons["start"].image = original_start_button_image