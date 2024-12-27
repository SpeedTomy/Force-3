from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialog, QDialogButtonBox, QInputDialog
from PyQt5.QtCore import QSize, Qt

class GameWindow(QMainWindow):
    def __init__(self, board, mode):
        super().__init__()
        self.board = board  # Plateau de jeu
        self.current_player = 0  # Joueur actuel (0 ou 1)
        self.mode = mode  # Mode de jeu
        self.selected_action = None  # Action sélectionnée
        self.remaining_moves = 1  # Nombre de déplacements restants pour les carrés
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Force 3")
        self.setMinimumSize(QSize(800, 800))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # Affichage du joueur actuel
        self.current_player_label = QLabel(f"Joueur actuel: {self.get_player_color()}")
        self.current_player_label.setAlignment(Qt.AlignCenter)
        self.current_player_label.setStyleSheet("font-size: 24px;")
        main_layout.addWidget(self.current_player_label)

        # Grille pour le plateau
        self.layout = QGridLayout()
        self.buttons = {}  # Stocker les boutons pour chaque case

        for i in range(3):
            for j in range(3):
                btn = QPushButton(" ")
                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, i, j)
                self.buttons[(i, j)] = btn
                btn.clicked.connect(lambda _, x=i, y=j: self.handle_click(x, y))

        main_layout.addLayout(self.layout)

        # Boutons pour les actions disponibles
        self.action_buttons_layout = QHBoxLayout()
        self.place_pawn_button = QPushButton("Placer un pion")
        self.move_pawn_button = QPushButton("Déplacer un pion")
        self.move_square_button = QPushButton("Déplacer un carré")

        self.place_pawn_button.clicked.connect(lambda: self.select_action("Placer un pion"))
        self.move_pawn_button.clicked.connect(lambda: self.select_action("Déplacer un pion"))
        self.move_square_button.clicked.connect(lambda: self.select_action("Déplacer un carré"))

        self.action_buttons_layout.addWidget(self.place_pawn_button)
        self.action_buttons_layout.addWidget(self.move_pawn_button)
        self.action_buttons_layout.addWidget(self.move_square_button)

        main_layout.addLayout(self.action_buttons_layout)

    def get_player_color(self):
        return "Blanc" if self.current_player == 0 else "Noir"

    def select_action(self, action):
        self.selected_action = action
        self.remaining_moves = 1 if action != "Déplacer un carré" else 2 if self.board.isMove2SquarePawnsPossible() else 1
        self.update_action_buttons()

    def update_action_buttons(self):
        self.place_pawn_button.setStyleSheet("background-color: none")
        self.move_pawn_button.setStyleSheet("background-color: none")
        self.move_square_button.setStyleSheet("background-color: none")

        if self.selected_action == "Placer un pion":
            self.place_pawn_button.setStyleSheet("background-color: yellow")
        elif self.selected_action == "Déplacer un pion":
            self.move_pawn_button.setStyleSheet("background-color: yellow")
        elif self.selected_action == "Déplacer un carré":
            self.move_square_button.setStyleSheet("background-color: yellow")

    def handle_click(self, x, y):
        """
        Gère les clics sur le plateau, en fonction de l'état actuel du jeu.
        Tente de placer ou de déplacer des pions circulaires ou carrés, et met à jour l'interface.
        """
        if not self.selected_action:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une action d'abord !")
            return

        # Détermine l'action à effectuer
        action_success = False

        if self.selected_action == "Placer un pion":
            # Tente de placer un pion circulaire
            if len(self.board.players[self.current_player].pawns) < 3:
                action_success = self.board.placeCircularPawn(self.current_player, x, y) == 0
        elif self.selected_action == "Déplacer un pion":
            # Si le joueur a déjà 3 pions, tente de déplacer un pion circulaire
            if len(self.board.players[self.current_player].pawns) >= 3:
                for pawn in self.board.players[self.current_player].pawns:
                    if pawn.x != x or pawn.y != y:
                        action_success = self.board.moveCircularPawn(self.current_player, pawn.id, x, y) == 0
                        if action_success:
                            break
        elif self.selected_action == "Déplacer un carré":
            # Tente de déplacer un carré
            if self.remaining_moves == 2:
                action_success = self.board.moveSquarePawn(x, y) == 0
                if action_success:
                    self.remaining_moves -= 1
                    self.update_action_buttons()
                    return
            else:
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
                self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")

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
        self.current_player = 0
        self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")

    def update_board(self):
        state = self.board.get_board_state()
        for (x, y), btn in self.buttons.items():
            if state[x][y] == "empty":
                btn.setText("■")
            elif state[x][y] == "white":
                btn.setText("⚪")
            elif state[x][y] == "black":
                btn.setText("⚫")
            elif state[x][y] == "square":
                btn.setText("▢")

class ModeSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection du mode de jeu")
        self.setFixedSize(QSize(300, 200))

        layout = QVBoxLayout()

        self.label = QLabel("Choisissez un mode de jeu:")
        layout.addWidget(self.label)

        self.comboBox = QComboBox()
        self.comboBox.addItems(["Player vs Player", "Player vs IA", "IA vs IA"])
        layout.addWidget(self.comboBox)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def get_selected_mode(self):
        return self.comboBox.currentIndex()

if __name__ == "__main__":
    import sys
    from Board import Board
    from Player import Player
    from Constants import WHITE_PAWN, BLACK_PAWN

    app = QApplication(sys.argv)

    dialog = ModeSelectionDialog()
    if dialog.exec_() == QDialog.Accepted:
        mode = dialog.get_selected_mode()

        player1 = Player(0, WHITE_PAWN)
        player2 = Player(1, BLACK_PAWN)
        board = Board(player1, player2)

        window = GameWindow(board, mode)
        window.show()
        sys.exit(app.exec_())
