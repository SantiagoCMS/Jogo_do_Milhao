# Dentro da sua classe SubjectsMenu
import pygame
from jogo.button import Button
from jogo.ranking_screen import RankingScreen # Mantido, caso você o use

class SubjectsMenu:
    """
    Tela onde o jogador escolhe o módulo (fundamental ou médio) e as matérias para o quiz.
    """
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.selected_level = None # Novo: para armazenar o nível explicitamente
        self.selected_actual_subjects = [] # Novo: para armazenar apenas as matérias

        # Mantendo selected_subjects para a lógica de seleção dos botões visuais
        self.selected_subjects_ui = []  # Renomeado de self.selected_subjects para clareza

        self.subject_categories = ["matematica", "portugues", "ingles", "naturais", "humanas"]

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
        """Exibe a tela e lida com os cliques.
        Retorna (selected_level, selected_subjects_list) se 'Iniciar' for clicado,
        ou (None, None) se 'Voltar' ou fechar janela.
        """
        self.running = True
        # Resetar seleções ao mostrar o menu novamente
        self.selected_level = None
        self.selected_actual_subjects = []
        self.selected_subjects_ui = []


        original_start_button_image = self.assets.start_img
        disabled_start_button_image = getattr(self.assets, 'start_disabled_img', getattr(self.assets, 'start_inactive_img', self.assets.start_img)) # Fallback para original se não houver desabilitada

        # Limpa cliques pendentes
        pygame.event.clear(pygame.MOUSEBUTTONDOWN)
        pygame.event.clear(pygame.MOUSEBUTTONUP)


        while self.running:
            self.screen.blit(self.assets.background, (0, 0))
            text_surface = self.assets.large_font.render("Escolha o nível e as matérias", True, (0, 227, 197)) # Título ajustado
            self.screen.blit(text_surface, (self.screen.get_width() // 2 - text_surface.get_width() // 2, 40)) # Y ajustado

            # Lógica para habilitar o botão Iniciar
            level_is_selected = self.selected_level is not None
            at_least_one_subject_is_selected = bool(self.selected_actual_subjects)
            start_button_can_be_activated = level_is_selected and at_least_one_subject_is_selected

            if disabled_start_button_image:
                self.buttons["start"].image = original_start_button_image if start_button_can_be_activated else disabled_start_button_image

            mouse_clicked_this_frame = False # Para tratar apenas um clique por frame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    if disabled_start_button_image: self.buttons["start"].image = original_start_button_image
                    return None, None # Retorna None se fechar

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Processar no soltar do mouse
                    mouse_clicked_this_frame = True

            for name, button in self.buttons.items():
                # Atualiza o estado visual do botão (hover, etc.)
                # O button.draw() não deve mais manipular o clique para seleção de matéria aqui,
                # faremos isso com base no mouse_clicked_this_frame e collidepoint.
                button.draw(self.screen) # Apenas desenha

                if mouse_clicked_this_frame and button.rect.collidepoint(pygame.mouse.get_pos()):
                    if name == "start" and start_button_can_be_activated:
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                        self.running = False
                        if disabled_start_button_image: self.buttons["start"].image = original_start_button_image
                        return self.selected_level, self.selected_actual_subjects

                    elif name == "voltar":
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                        self.running = False
                        if disabled_start_button_image: self.buttons["start"].image = original_start_button_image
                        return None, None # Retorna None para indicar 'voltar'

                    elif name == "ranking":
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()
                        ranking_screen = RankingScreen(self.screen, self.assets)
                        ranking_screen.run()
                        # Após o ranking, é bom limpar cliques para evitar ações acidentais
                        pygame.event.clear(pygame.MOUSEBUTTONUP)
                        mouse_clicked_this_frame = False # Evita reprocessar clique no ranking

                    elif name in ["fundamental", "medio"] + self.subject_categories: # Botões de seleção
                        if hasattr(self.assets, 'click_sound'): self.assets.click_sound.play()

                        if name == "fundamental":
                            self.selected_level = "fundamental"
                            if "fundamental" not in self.selected_subjects_ui: self.selected_subjects_ui.append("fundamental")
                            if "medio" in self.selected_subjects_ui: self.selected_subjects_ui.remove("medio")
                        elif name == "medio":
                            self.selected_level = "medio"
                            if "medio" not in self.selected_subjects_ui: self.selected_subjects_ui.append("medio")
                            if "fundamental" in self.selected_subjects_ui: self.selected_subjects_ui.remove("fundamental")
                        elif name in self.subject_categories:
                            if name in self.selected_actual_subjects:
                                self.selected_actual_subjects.remove(name)
                                if name in self.selected_subjects_ui: self.selected_subjects_ui.remove(name) # UI sync
                            else:
                                self.selected_actual_subjects.append(name)
                                if name not in self.selected_subjects_ui: self.selected_subjects_ui.append(name) # UI sync

                    # Após um clique ser processado, idealmente não processar mais cliques neste frame
                    mouse_clicked_this_frame = False # Reseta para o próximo frame, ou use break se o loop de botões for problemático


            # Exibe os checkboxes (baseado em selected_subjects_ui para visual e selected_level/selected_actual_subjects para lógica)
            for name, button_obj in self.buttons.items():
                if name in ["fundamental", "medio"] + self.subject_categories:
                    is_selected = False
                    if name == "fundamental" and self.selected_level == "fundamental": is_selected = True
                    elif name == "medio" and self.selected_level == "medio": is_selected = True
                    elif name in self.subject_categories and name in self.selected_actual_subjects: is_selected = True

                    checkbox_image = self.assets.checkbox_on if is_selected else self.assets.checkbox_off
                    cb_x = button_obj.rect.centerx - checkbox_image.get_width() // 2
                    cb_y = button_obj.rect.bottom + 5
                    self.screen.blit(checkbox_image, (cb_x, cb_y))

            pygame.display.update()

        # Se o loop terminar por outra razão (ex: self.running se tornou False por QUIT)
        if disabled_start_button_image: self.buttons["start"].image = original_start_button_image
        return None, None