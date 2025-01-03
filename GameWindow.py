from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialog, QDialogButtonBox, QInputDialog
from PyQt5.QtCore import QSize, Qt, QTimer
from Main import IAChoices

class GameWindow(QMainWindow):
    def __init__(self, board, mode, player_color):
        super().__init__()
        self.board = board  # Plateau de jeu
        self.current_player = 0 if player_color == "Blanc" else 1  # Joueur actuel (0 ou 1)
        self.mode = mode  # Mode de jeu
        self.ia_player = 1 if player_color == "Blanc" else 0  # IA joue en second si le joueur est blanc
        self.selected_action = None  # Action sélectionnée
        self.remaining_moves = 1  # Nombre de déplacements restants pour les carrés
        self.selected_pawn = None  # <-- added to track the selected pawn
        self.selected_square = None  # Track selected square tile
        self.selected_squares = []  # Track two squares for 2-square moves
        self.place_pawn_button = None
        self.move_pawn_button = None
        self.move_square_button = None
        self.back_to_menu_button = None  # Bouton pour revenir au menu
        self.next_step_button = None  # Bouton pour avancer d'une étape en mode IA vs IA
        self.square_moves_count = 0  # Counter for square moves
        self.two_square_move_cooldown = False  # Cooldown flag for two-square moves
        self.initUI()

        if self.mode == 2:  # IA vs IA
            self.ia_player = 0
            # Désactiver le timer pour permettre un contrôle manuel
            # self.ia_vs_ia_timer = QTimer(self)
            # self.ia_vs_ia_timer.timeout.connect(self.ia_vs_ia_step)
            # self.ia_vs_ia_timer.start(1000)  # Step every second

        # Si le joueur est noir, l'IA commence
        if self.mode == 1 and self.current_player == self.ia_player:
            self.ia_play()

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

        # Show place pawn button only for Player vs Player and Player vs IA modes
        if self.mode in [0, 1]:
            self.place_pawn_button.show()
        else:
            self.place_pawn_button.hide()

        self.action_buttons_layout.addWidget(self.place_pawn_button)
        self.action_buttons_layout.addWidget(self.move_pawn_button)
        self.action_buttons_layout.addWidget(self.move_square_button)
        if self.mode != 2:  # Hide "Déplacer 2 carrés" button in IA vs IA mode
            self.action_buttons_layout.addWidget(self.move_two_squares_button)

        main_layout.addLayout(self.action_buttons_layout)

        if self.mode == 2:  # IA vs IA
            self.next_step_button = QPushButton("Next Step")
            self.next_step_button.clicked.connect(self.ia_vs_ia_step)
            main_layout.addWidget(self.next_step_button)

        # Bouton pour revenir au menu principal
        self.back_to_menu_button = QPushButton("Retour au menu")
        self.back_to_menu_button.clicked.connect(self.back_to_menu)
        main_layout.addWidget(self.back_to_menu_button)

    def get_player_color(self):
        return "Blanc" if self.current_player == 0 else "Noir"

    def select_action(self, action):
        if self.two_square_move_cooldown and action == "Déplacer 2 carrés":
            QMessageBox.information(self, "Info", "Vous ne pouvez pas déplacer 2 carrés ce tour-ci.")
            return
        self.selected_action = action
        if action == "Déplacer 2 carrés":
            # Show two-square button only if board allows them
            if not self.board.isMove2SquarePawnsPossible():
                QMessageBox.information(self, "Info", "Vous ne pouvez pas déplacer 2 carrés maintenant.")
                return
            self.selected_squares.clear()
            self.disable_action_buttons()
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
                if self.mode == 0 and all(len(p.pawns) >= 1 for p in self.board.players):
                    self.move_pawn_button.show()
                    self.move_square_button.show()
                elif self.mode == 1 and len(self.board.players[self.current_player].pawns) >= 1:
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
                    self.close()  # Close the current window
                    self.restart_application()  # Restart application to return to the menu
                else:
                    # Change de joueur
                    self.board.endTurn()  # Réduire le cooldown à la fin du tour
                    self.current_player = 1 - self.current_player
                    self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
                    if self.mode == 1 and self.current_player == self.ia_player:
                        self.ia_play()
            return
        elif self.selected_action == "Déplacer un pion":
            if self.selected_pawn is None:
                # First click: select the pawn
                if any(pawn.x == x and pawn.y == y for pawn in self.board.players[self.current_player].pawns):
                    self.selected_pawn = (x, y)
                    self.highlight_possible_moves(x, y)
                else:
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
                        self.close()  # Close the current window
                        self.restart_application()  # Restart application to return to the menu
                    else:
                        # Change de joueur
                        self.board.endTurn()  # Réduire le cooldown à la fin du tour
                        self.current_player = 1 - self.current_player
                        self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
                        if self.mode == 1 and self.current_player == self.ia_player:
                            self.ia_play()
                else:
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
                    self.close()  # Close the current window
                    self.restart_application()  # Restart application to return to the menu
                else:
                    self.board.endTurn()  # Réduire le cooldown à la fin du tour
                    self.current_player = 1 - self.current_player
                    self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
                    if self.mode == 1 and self.current_player == self.ia_player:
                        self.ia_play()
            else:
                QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                self.update_board()
            return
        elif self.selected_action == "Déplacer 2 carrés":
            tile = self.board._get_board_by_coordinate(x, y)
            if tile.isSquarePawnSet():
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
                    result = self.board.moveSquarePawn(sx[0], sy[0])
                    if result == 0:
                        self.update_board()
                        self.clear_highlight()
                        self.selected_squares = [(sx[1], sy[1])]
                        self.square_moves_count += 1
                        self.highlight_all_movable_squares()
                        possible_second_moves = self.board.getAllMovableSquares()
                        if (sx[1], sy[1]) in possible_second_moves:
                            possible_second_moves.remove((sx[1], sy[1]))
                        for (xx, yy) in possible_second_moves:
                            self.buttons[(xx, yy)].setStyleSheet("background-color: green;")
                        if not possible_second_moves or self.square_moves_count == 2:
                            self.disable_action_buttons()
                            self.selected_action = None
                            self.update_action_buttons()
                            self.board.endTurn()
                            self.current_player = 1 - self.current_player
                            self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
                            self.square_moves_count = 0  # Reset counter
                            self.two_square_move_cooldown = True  # Set cooldown
                            self.clear_highlight()  # Clear highlight when switching to the next player
                            self.enable_action_buttons()  # Re-enable action buttons for the next player
                            if self.mode == 1 and self.current_player == self.ia_player:
                                self.ia_play()
                    else:
                        QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                        self.update_board()
                    self.selected_squares.clear()
            else:
                QMessageBox.information(self, "Info", "Veuillez sélectionner un carré.")
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
                self.close()  # Close the current window
                self.restart_application()  # Restart application to return to the menu
            else:
                # Change de joueur
                self.board.endTurn()  # Réduire le cooldown à la fin du tour
                self.current_player = 1 - self.current_player
                self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")

    def ia_play(self):
        IAChoices(self.board.players[self.current_player], self.board.players[1 - self.current_player], self.board)
        self.update_board()
        winner = self.board.checkIfWinner()
        if winner != -1:
            QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
            self.close()  # Close the current window
            self.restart_application()  # Restart application to return to the menu
        else:
            self.current_player = 1 - self.current_player
            self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
            if self.mode == 1 and self.current_player == self.ia_player:
                self.ia_play()
        self.clear_highlight()  # Clear highlight when IA plays
        self.enable_action_buttons()  # Re-enable action buttons when IA plays

    def ia_vs_ia_step(self):
        """
        Avance d'une étape en mode IA vs IA.
        """
        if self.board.checkIfWinner() == -1:
            IAChoices(self.board.players[self.current_player], self.board.players[1 - self.current_player], self.board)
            self.update_board()
            winner = self.board.checkIfWinner()
            if winner != -1:
                QMessageBox.information(self, "Victoire", f"Joueur {winner + 1} a gagné !")
                self.close()  # Close the current window
                self.restart_application()  # Restart application to return to the menu
            else:
                self.current_player = 1 - self.current_player
                self.current_player_label.setText(f"Joueur actuel: {self.get_player_color()}")
        self.clear_highlight()  # Clear highlight when IA vs IA step occurs
        self.enable_action_buttons()  # Re-enable action buttons when IA vs IA step occurs

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

    def update_board(self):
        state = self.board.get_board_state()
        for (x, y), btn in self.buttons.items():
            if state[x][y] == "empty":
                btn.setText("✖")  # Croix rouge pour les tuiles vides
                btn.setStyleSheet("color: red;")  # Couleur rouge pour la croix
            elif state[x][y] == "white":
                btn.setText("⚪")
            elif state[x][y] == "black":
                btn.setText("⚫")
            elif state[x][y] == "square":
                btn.setText("")  # Rien pour les carrés
            else:
                btn.setText(" ")  # Par défaut, texte vide
        if self.mode != 2 and self.board.isMove2SquarePawnsPossible():  # Hide "Déplacer 2 carrés" button in IA vs IA mode
            self.move_two_squares_button.show()
        else:
            self.move_two_squares_button.hide()
        # Ensure buttons visibility based on mode and player actions
        if self.mode == 0:  # Player vs Player
            if all(len(p.pawns) >= 1 for p in self.board.players):
                self.move_pawn_button.show()
                self.move_square_button.show()
            if all(len(p.pawns) >= 3 for p in self.board.players):
                self.place_pawn_button.hide()
        elif self.mode == 1:  # Player vs IA
            if len(self.board.players[0].pawns) >= 1:
                self.move_pawn_button.show()
                self.move_square_button.show()
            if len(self.board.players[0].pawns) >= 3:
                self.place_pawn_button.hide()
        self.two_square_move_cooldown = False  # Reset cooldown at the start of each turn
        self.clear_highlight()  # Clear highlight when updating the board
        self.enable_action_buttons()  # Re-enable action buttons when updating the board

    def disable_action_buttons(self):
        self.place_pawn_button.setEnabled(False)
        self.move_pawn_button.setEnabled(False)
        self.move_square_button.setEnabled(False)
        self.move_two_squares_button.setEnabled(False)

    def enable_action_buttons(self):
        self.place_pawn_button.setEnabled(True)
        self.move_pawn_button.setEnabled(True)
        self.move_square_button.setEnabled(True)
        self.move_two_squares_button.setEnabled(True)

    def back_to_menu(self):
        """
        Retourne au menu principal en redémarrant l'application.
        """
        self.close()
        self.restart_application()

    def restart_application(self):
        """
        Redémarre l'application pour revenir au menu principal.
        """
        import sys
        from PyQt5.QtWidgets import QApplication

        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        self.dialog = ModeSelectionDialog()
        if self.dialog.exec_() == QDialog.Accepted:
            mode = self.dialog.get_selected_mode()

            if mode == 1:  # Player vs IA
                color_dialog = ColorSelectionDialog()
                if color_dialog.exec_() == QDialog.Accepted:
                    player_color = color_dialog.get_selected_color()
                else:
                    self.restart_application()  # Retourne au menu principal si l'utilisateur clique sur "Retour au menu"
                    return
            else:
                player_color = "Blanc"  # Default color for other modes

            player1 = Player(0, WHITE_PAWN)
            player2 = Player(1, BLACK_PAWN)
            board = Board(player1, player2)

            self.window = GameWindow(board, mode, player_color)
            self.window.show()
            self.window.update_board()  # Mettre à jour le plateau dès le lancement du jeu
        else:
            self.quit_application()  # Quitte l'application si l'utilisateur clique sur "Quitter" dans la boîte de dialogue de sélection de mode

    def quit_application(self):
        """
        Quitte l'application.
        """
        import sys
        sys.exit()

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

        self.buttonBox = QDialogButtonBox()
        self.okButton = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.quitButton = self.buttonBox.addButton("Quitter", QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def get_selected_mode(self):
        return self.comboBox.currentIndex()

class ColorSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choisissez votre couleur")
        self.setFixedSize(QSize(300, 100))

        layout = QVBoxLayout()

        self.label = QLabel("Choisissez votre couleur:")
        layout.addWidget(self.label)

        self.colorComboBox = QComboBox()
        self.colorComboBox.addItems(["Blanc", "Noir"])
        layout.addWidget(self.colorComboBox)

        self.buttonBox = QDialogButtonBox()
        self.okButton = self.buttonBox.addButton(QDialogButtonBox.Ok)
        self.backToMenuButton = self.buttonBox.addButton("Retour au menu", QDialogButtonBox.RejectRole)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def get_selected_color(self):
        return self.colorComboBox.currentText()

if __name__ == "__main__":
    import sys
    from Board import Board
    from Player import Player
    from Constants import WHITE_PAWN, BLACK_PAWN

    app = QApplication(sys.argv)

    dialog = ModeSelectionDialog()
    if dialog.exec_() == QDialog.Accepted:
        mode = dialog.get_selected_mode()

        if mode == 1:  # Player vs IA
            color_dialog = ColorSelectionDialog()
            if color_dialog.exec_() == QDialog.Accepted:
                player_color = color_dialog.get_selected_color()
            else:
                sys.exit()

        else:
            player_color = "Blanc"  # Default color for other modes

        player1 = Player(0, WHITE_PAWN)
        player2 = Player(1, BLACK_PAWN)
        board = Board(player1, player2)

        window = GameWindow(board, mode, player_color)
        window.show()
        window.update_board()  # Mettre à jour le plateau dès le lancement du jeu
        sys.exit(app.exec_())