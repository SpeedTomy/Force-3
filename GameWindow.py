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
        self.selected_squares = []  # Track two squares for 2-square moves
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
        self.move_two_squares_button = QPushButton("Déplacer 2 carrés")

        self.place_pawn_button.clicked.connect(lambda: self.select_action("Placer un pion"))
        self.move_pawn_button.clicked.connect(lambda: self.select_action("Déplacer un pion"))
        self.move_square_button.clicked.connect(lambda: self.select_action("Déplacer un carré"))
        self.move_two_squares_button.clicked.connect(lambda: self.select_action("Déplacer 2 carrés"))

        # Initially hide move buttons
        self.move_pawn_button.hide()
        self.move_square_button.hide()
        self.move_two_squares_button.hide()  # Hide by default

        self.action_buttons_layout.addWidget(self.place_pawn_button)
        self.action_buttons_layout.addWidget(self.move_pawn_button)
        self.action_buttons_layout.addWidget(self.move_square_button)
        self.action_buttons_layout.addWidget(self.move_two_squares_button)

        main_layout.addLayout(self.action_buttons_layout)

    def get_player_color(self):
        return "Blanc" if self.current_player == 0 else "Noir"

    def select_action(self, action):
        self.selected_action = action
        if action == "Déplacer 2 carrés":
            # Show two-square button only if board allows them
            if not self.board.isMove2SquarePawnsPossible():
                QMessageBox.information(self, "Info", "Vous ne pouvez pas déplacer 2 carrés maintenant.")
                return
            self.selected_squares.clear()
        else:
            self.remaining_moves = 1 if action != "Déplacer un carré" else 2 if self.board.isMove2SquarePawnsPossible() else 1
        if action in ["Déplacer un carré", "Déplacer 2 carrés"]:
            self.highlight_all_movable_squares()
        else:
            self.clear_highlight()
        self.update_action_buttons()

    def highlight_all_movable_squares(self):
        movable = self.board.getAllMovableSquares()
        for (i, j), btn in self.buttons.items():
            if (i, j) in movable:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: none;")

    def update_action_buttons(self):
        self.place_pawn_button.setStyleSheet("background-color: none")
        self.move_pawn_button.setStyleSheet("background-color: none")
        self.move_square_button.setStyleSheet("background-color: none")
        self.move_two_squares_button.setStyleSheet("background-color: none")

        if self.selected_action == "Placer un pion":
            self.place_pawn_button.setStyleSheet("background-color: yellow")
        elif self.selected_action == "Déplacer un pion":
            self.move_pawn_button.setStyleSheet("background-color: yellow")
        elif self.selected_action == "Déplacer un carré":
            self.move_square_button.setStyleSheet("background-color: yellow")
        elif self.selected_action == "Déplacer 2 carrés":
            self.move_two_squares_button.setStyleSheet("background-color: yellow")

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
            if action_success:
                self.update_board()
                # Show move buttons once both players have at least one pawn
                if all(len(p.pawns) >= 1 for p in self.board.players):
                    self.move_pawn_button.show()
                    self.move_square_button.show()
                # Hide "Placer un pion" if both players have 3
                if all(len(p.pawns) >= 3 for p in self.board.players):
                    self.place_pawn_button.hide()
                self.clear_highlight()
                self.selected_action = None
                self.update_action_buttons()
                # Vérifie si un joueur a gagné
                winner = self.board.checkIfWinner()
                if winner != -1:
                    QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
                    self.reset_game()
                else:
                    # Change de joueur
                    self.current_player = 1 - self.current_player
                    self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
            return
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
                    self.selected_action = None
                    self.update_action_buttons()
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
            return
        elif self.selected_action == "Déplacer un carré":
            # One-click approach: if (x, y) is in getAllMovableSquares, move immediately
            movable = self.board.getAllMovableSquares()
            if (x, y) not in movable:
                QMessageBox.information(self, "Info", "Case non déplaçable.")
                return
            result = self.board.moveSquarePawn(x, y)
            if result == 0:
                self.update_board()
                self.clear_highlight()
                self.selected_action = None
                self.update_action_buttons()
                # Check winner
                winner = self.board.checkIfWinner()
                if winner != -1:
                    QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
                    self.reset_game()
                else:
                    self.current_player = 1 - self.current_player
                    self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
            else:
                QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                self.update_board()
            return
        elif self.selected_action == "Déplacer 2 carrés":
            tile = self.board._get_board_by_coordinate(x, y)
            if tile.isSquarePawnSet() and not tile.isCircularPawnSet():
                self.selected_squares.append((x, y))
                if len(self.selected_squares) == 1:
                    self.clear_highlight()
                    first_btn = self.buttons[(x, y)]
                    first_btn.setStyleSheet("background-color: yellow;")
                    # Highlight all other movable squares in green
                    possible_second_moves = self.board.getAllMovableSquares()
                    if (x, y) in possible_second_moves:
                        possible_second_moves.remove((x, y))
                    for (xx, yy) in possible_second_moves:
                        self.buttons[(xx, yy)].setStyleSheet("background-color: green;")
                elif len(self.selected_squares) == 2:
                    sx = [self.selected_squares[0][0], self.selected_squares[1][0]]
                    sy = [self.selected_squares[0][1], self.selected_squares[1][1]]
                    result = self.board.move2SquarePawns(sx, sy)
                    if result == 0:
                        self.update_board()
                        self.clear_highlight()
                        self.selected_action = None
                        self.update_action_buttons()
                    else:
                        QMessageBox.warning(self, "Erreur",
                                            "Déplacement de 2 carrés invalide ! Vérifiez la fonction move2SquarePawns.")
                    self.selected_squares.clear()
            else:
                QMessageBox.information(self, "Info", "Veuillez sélectionner un carré vide.")
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
        valid_moves = self.board.getValidSquareMoves(x, y)
        # Only color valid moves in green, do not highlight anything in yellow or red
        for (i, j), btn in self.buttons.items():
            if (i, j) in valid_moves:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: none;")

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
            elif state[x][y] == "square_with_pawn":
                btn.setText("▢⚪" if self.board._get_circularPawn_by_board(x, y).color else "▢⚫")
        if self.board.isMove2SquarePawnsPossible():
            self.move_two_squares_button.show()
        else:
            self.move_two_squares_button.hide()

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