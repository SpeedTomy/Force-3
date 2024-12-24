from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QSize

class GameWindow(QMainWindow):
    def __init__(self, board):
        super().__init__()
        self.board = board  # Plateau de jeu
        self.current_player = 0  # Joueur actuel (0 ou 1)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Force 3")
        self.setFixedSize(QSize(800, 800))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Grille pour le plateau
        self.layout = QGridLayout(central_widget)
        self.buttons = {}  # Stocker les boutons pour chaque case

        for i in range(3):
            for j in range(3):
                btn = QPushButton(" ")
                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, i, j)
                self.buttons[(i, j)] = btn
                btn.clicked.connect(lambda _, x=i, y=j: self.handle_click(x, y))

    def handle_click(self, x, y):
        """
        Gère les clics sur le plateau, en fonction de l'état actuel du jeu.
        Tente de placer ou de déplacer des pions circulaires ou carrés, et met à jour l'interface.
        """
        # Détermine l'action à effectuer
        action_success = False

        # Tente de placer un pion circulaire
        if len(self.board.players[self.current_player].pawns) < 3:
            action_success = self.board.placeCircularPawn(self.current_player, x, y) == 0

        # Si le joueur a déjà 3 pions, tente de déplacer un pion circulaire
        if not action_success and len(self.board.players[self.current_player].pawns) >= 3:
            # Par défaut, le premier pion est déplacé (ajuste en fonction des choix réels)
            action_success = self.board.moveCircularPawn(self.current_player, 1, x, y) == 0

        # Si ni un placement ni un déplacement circulaire n'est valide, tente de déplacer un carré
        if not action_success:
            action_success = self.board.moveSquarePawn(x, y) == 0

        # Si une action est effectuée, met à jour le plateau
        if action_success:
            self.update_board()

            # Vérifie si un joueur a gagné
            winner = self.board.checkIfWinner()
            if winner != -1:
                QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
                self.reset_game()
            else:
                # Change de joueur
                self.current_player = 1 - self.current_player

        else:
            # Action non valide, affiche un message d'erreur
            QMessageBox.warning(self, "Erreur", "Action non valide !")

    def reset_game(self):
        """
        Réinitialise le plateau et l'état du jeu après une victoire.
        """
        from Board import Board
        from Player import Player
        from Constants import WHITE_PAWN, BLACK_PAWN

        # Réinitialise les joueurs et le plateau
        player1 = Player(0, WHITE_PAWN)
        player2 = Player(1, BLACK_PAWN)
        self.board = Board(player1, player2)

        # Met à jour l'interface
        self.update_board()

    def update_board(self):
        state = self.board.get_board_state()
        for (x, y), btn in self.buttons.items():
            if state[x][y] == "empty":
                btn.setText("")
            elif state[x][y] == "white":
                btn.setText("⚪")
            elif state[x][y] == "black":
                btn.setText("⚫")
            elif state[x][y] == "square":
                btn.setText("■")

if __name__ == "__main__":
    import sys
    from Board import Board
    from Player import Player
    from Constants import WHITE_PAWN, BLACK_PAWN

    app = QApplication(sys.argv)
    player1 = Player(0, WHITE_PAWN)
    player2 = Player(1, BLACK_PAWN)
    board = Board(player1, player2)

    window = GameWindow(board)
    window.show()
    sys.exit(app.exec_())
