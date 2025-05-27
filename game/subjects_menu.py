import pygame
from game.button import Button

class SubjectsMenu:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.selected_subjects = []
        self.running = True

        # Create buttons
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
        self.running = True
        while self.running:
            self.screen.fill((255, 255, 255))  # White background
            self.screen.blit(self.assets.background, (0, 0))
            text = self.assets.font.render("Escolha matérias", True, (0, 227, 197))
            self.screen.blit(text, (540 - text.get_width() // 2, 10))

            # Draw buttons and handle clicks
            for name, button in self.buttons.items():
                if button.draw(self.screen):
                    self.assets.click_sound.play()
                    if name == "voltar":
                        self.running = False
                    elif name in self.selected_subjects:
                        self.selected_subjects.remove(name)
                    elif name == "fundamental":
                        # Remove "medio" if selected and add "fundamental"
                        self.selected_subjects = [s for s in self.selected_subjects if s != "medio"]
                        self.selected_subjects.append("fundamental")
                    elif name == "medio":
                        # Remove "fundamental" if selected and add "medio"
                        self.selected_subjects = [s for s in self.selected_subjects if s != "fundamental"]
                        self.selected_subjects.append("medio")
                    elif name not in ["start", "voltar"]:
                        self.selected_subjects.append(name)

            # Draw checkboxes below buttons
            for name, button in self.buttons.items():
                if name in ["fundamental", "medio", "matematica", "portugues", "ingles", "naturais", "humanas"]:
                    checkbox_img = (
                        self.assets.checkbox_on if name in self.selected_subjects else self.assets.checkbox_off
                    )
                    checkbox_x = button.x + (button.image.get_width() // 2) - (checkbox_img.get_width() // 2)
                    checkbox_y = button.y + button.image.get_height() + 5
                    self.screen.blit(checkbox_img, (checkbox_x, checkbox_y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()