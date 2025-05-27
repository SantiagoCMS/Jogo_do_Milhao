# Ponto de entrada do jogo: inicia o loop principal do jogo.

from jogo.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()