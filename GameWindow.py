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
        self.selected_pawn = None  # <-- added to track the selected pawn
        self.selected_square = None  # Track selected square tile
        self.place_pawn_button = None
        self.move_pawn_button = None
        self.move_square_button = None
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

        # Initially hide move buttons
        self.move_pawn_button.hide()
        self.move_square_button.hide()

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

        # Check if there's at least one pawn or square to move
        if self.selected_action == "Déplacer un pion":
            if len(self.board.players[self.current_player].pawns) == 0:
                QMessageBox.warning(self, "Erreur", "Aucun pion à déplacer !")
                return
        elif self.selected_action == "Déplacer un carré":
            if not any(tile.isSquarePawnSet() for row in self.board.board for tile in row):
                QMessageBox.warning(self, "Erreur", "Aucune case vide à déplacer pour l'instant !")
                return

        # Détermine l'action à effectuer
        action_success = False

        if self.selected_action == "Placer un pion":
            if len(self.board.players[self.current_player].pawns) >= 3:
                QMessageBox.warning(self, "Erreur", "Vous ne pouvez pas placer plus de 3 pions !")
                return
            # Tente de placer un pion circulaire
            if len(self.board.players[self.current_player].pawns) < 3:
                action_success = self.board.placeCircularPawn(self.current_player, x, y) == 0
        elif self.selected_action == "Déplacer un pion":
            if self.selected_pawn is None:
                # First click: select the pawn
                # Remove or rename this message so it doesn't wrongly appear:
                if any(pawn.x == x and pawn.y == y for pawn in self.board.players[self.current_player].pawns):
                    self.selected_pawn = (x, y)
                    self.highlight_possible_moves(x, y)
                else:
                    # ...example change:
                    QMessageBox.information(self, "Info", "Cette case ne contient pas votre pion.")
                return
            else:
                # Second click: attempt move
                px, py = self.selected_pawn
                pawn_id = None
                for p in self.board.players[self.current_player].pawns:
                    if p.x == px and p.y == py:
                        pawn_id = p.id
                        break
                if pawn_id and self.board.moveCircularPawn(self.current_player, pawn_id, x, y) == 0:
                    self.update_board()
                    self.clear_highlight()
                    self.selected_pawn = None
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
                    # Only show a warning here if it's truly invalid
                    QMessageBox.warning(self, "Erreur", "Déplacement invalide !")
                    self.clear_highlight()
                    self.selected_pawn = None
        elif self.selected_action == "Déplacer un carré":
            # Replicate the two-click approach for squares
            if self.selected_square is None:
                # First click: choose a square tile
                tile = self.board._get_board_by_coordinate(x, y)
                if tile.isSquarePawnSet() and not tile.isCircularPawnSet():
                    self.selected_square = (x, y)
                    self.highlight_possible_squares(x, y)
                else:
                    QMessageBox.information(self, "Info", "Cliquez sur une case contenant un carré.")
                return
            else:
                # Second click: attempt the move
                sx, sy = self.selected_square
                result = self.board.moveSquarePawn(sx, sy)
                if result == 0:
                    action_success = True
                    self.clear_highlight()
                    self.selected_square = None
                else:
                    QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                    self.clear_highlight()
                    self.selected_square = None

            if action_success and self.remaining_moves == 2:
                self.remaining_moves -= 1
                self.update_action_buttons()
                return

        # Si une action est effectuée, met à jour le plateau
        if action_success:
            self.update_board()

            # After placing a pawn, check if all 3 pions are placed for both players
            if self.selected_action == "Placer un pion" and action_success:
                # Once both players have at least 1 pawn, show move buttons
                if all(len(p.pawns) >= 1 for p in self.board.players):
                    self.move_pawn_button.show()
                    self.move_square_button.show()

                # Once both players have 3 pions, hide place button
                if all(len(p.pawns) >= 3 for p in self.board.players):
                    self.place_pawn_button.hide()

            # Vérifie si un joueur a gagné
            winner = self.board.checkIfWinner()
            if winner != -1:
                QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
                self.reset_game()
            else:
                # Change de joueur
                self.current_player = 1 - self.current_player
                self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")

    def highlight_possible_moves(self, x, y):
        possible_moves = self.board.getValidCircularMoves(x, y)
        for (i, j), btn in self.buttons.items():
            if (i, j) == (x, y):
                btn.setStyleSheet("background-color: yellow;")
            elif (i, j) in possible_moves:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: red;")

    def highlight_possible_squares(self, x, y):
        # Similar to highlight_possible_moves but for squares
        valid_moves = self.board.getValidSquareMoves(x, y)
        for (i, j), btn in self.buttons.items():
            if (i, j) == (x, y):
                btn.setStyleSheet("background-color: yellow;")
            elif (i, j) in valid_moves:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: red;")

    def clear_highlight(self):
        for btn in self.buttons.values():
            btn.setStyleSheet("background-color: none;")

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
