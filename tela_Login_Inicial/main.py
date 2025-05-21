# Entry point of the game: creates and runs the main game instance

from tela_Login_Inicial.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()