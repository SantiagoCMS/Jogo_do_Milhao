import pygame

# Generic button class for handling click interactions
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False  # Tracks if the button was already clicked
        self.x = x
        self.y = y

    # Draws the button and handles click detection
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        # Check if mouse is over button and left mouse is clicked
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True  # Only returns True once per click
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False  # Reset click state when mouse is released

        # Draw button image
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action