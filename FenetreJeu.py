from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDialog, QDialogButtonBox, QInputDialog
from PyQt5.QtCore import QSize, Qt, QTimer
from Main import choixIA

class FenetreJeu(QMainWindow):
    def __init__(self, plateau, mode, couleur_joueur):
        super().__init__()
        self.plateau = plateau
        self.joueur_actuel = 0 if couleur_joueur == "Blanc" else 1
        self.mode = mode
        self.joueur_ia = 1 if couleur_joueur == "Blanc" else 0
        self.action_selectionnee = None
        self.deplacements_restants = 1
        self.pion_selectionne = None
        self.carre_selectionne = None
        self.carres_selectionnes = []
        self.bouton_placer_pion = None
        self.bouton_deplacer_pion = None
        self.bouton_deplacer_carre = None
        self.bouton_retour_menu = None
        self.bouton_etape_suivante = None
        self.compteur_deplacements_carres = 0
        self.cooldown_deplacement_deux_carres = False
        self.initUI()

        if self.mode == 2:
            self.joueur_ia = 0

        if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
            self.jouer_ia()

    def initUI(self):
        self.setWindowTitle("Force 3")
        self.setMinimumSize(QSize(800, 800))

        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_principal = QVBoxLayout(widget_central)

        self.label_joueur_actuel = QLabel(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
        self.label_joueur_actuel.setAlignment(Qt.AlignCenter)
        self.label_joueur_actuel.setStyleSheet("font-size: 24px;")
        layout_principal.addWidget(self.label_joueur_actuel)

        self.layout = QGridLayout()
        self.boutons = {}

        for i in range(3):
            for j in range(3):
                btn = QPushButton(" ")
                btn.setFixedSize(100, 100)
                self.layout.addWidget(btn, i, j)
                self.boutons[(i, j)] = btn
                btn.clicked.connect(lambda _, x=i, y=j: self.gerer_clic(x, y))

        layout_principal.addLayout(self.layout)

        self.layout_boutons_actions = QHBoxLayout()
        self.bouton_placer_pion = QPushButton("Placer un pion")
        self.bouton_deplacer_pion = QPushButton("Déplacer un pion")
        self.bouton_deplacer_carre = QPushButton("Déplacer un carré")
        self.bouton_deplacer_deux_carres = QPushButton("Déplacer 2 carrés")

        self.bouton_placer_pion.clicked.connect(lambda: self.selectionner_action("Placer un pion"))
        self.bouton_deplacer_pion.clicked.connect(lambda: self.selectionner_action("Déplacer un pion"))
        self.bouton_deplacer_carre.clicked.connect(lambda: self.selectionner_action("Déplacer un carré"))
        self.bouton_deplacer_deux_carres.clicked.connect(lambda: self.selectionner_action("Déplacer 2 carrés"))

        self.bouton_deplacer_pion.hide()
        self.bouton_deplacer_carre.hide()
        self.bouton_deplacer_deux_carres.hide()

        if self.mode in [0, 1]:
            self.bouton_placer_pion.show()
        else:
            self.bouton_placer_pion.hide()

        self.layout_boutons_actions.addWidget(self.bouton_placer_pion)
        self.layout_boutons_actions.addWidget(self.bouton_deplacer_pion)
        self.layout_boutons_actions.addWidget(self.bouton_deplacer_carre)
        if self.mode != 2:
            self.layout_boutons_actions.addWidget(self.bouton_deplacer_deux_carres)

        layout_principal.addLayout(self.layout_boutons_actions)

        if self.mode == 2:
            self.bouton_etape_suivante = QPushButton("Étape suivante")
            self.bouton_etape_suivante.clicked.connect(self.etape_ia_vs_ia)
            layout_principal.addWidget(self.bouton_etape_suivante)

        self.bouton_retour_menu = QPushButton("Retour au menu")
        self.bouton_retour_menu.clicked.connect(self.retour_menu)
        layout_principal.addWidget(self.bouton_retour_menu)

    def obtenir_couleur_joueur(self):
        return "Blanc" if self.joueur_actuel == 0 else "Noir"

    def selectionner_action(self, action):
        if self.cooldown_deplacement_deux_carres and action == "Déplacer 2 carrés":
            QMessageBox.information(self, "Info", "Vous ne pouvez pas déplacer 2 carrés ce tour-ci.")
            return
        self.action_selectionnee = action
        if action == "Déplacer 2 carrés":
            if not self.plateau.estDeplacement2CarrePionsPossible():
                QMessageBox.information(self, "Info", "Vous ne pouvez pas déplacer 2 carrés maintenant.")
                return
            self.carres_selectionnes.clear()
            self.desactiver_boutons_actions()
        else:
            self.deplacements_restants = 1 if action != "Déplacer un carré" else 2 if self.plateau.estDeplacement2CarrePionsPossible() else 1
        if action in ["Déplacer un carré", "Déplacer 2 carrés"]:
            self.surligner_tous_carres_deplacables()
        else:
            self.effacer_surlignage()
        self.mettre_a_jour_boutons_actions()

    def surligner_tous_carres_deplacables(self):
        deplacables = self.plateau.obtenirTousCarresDeplacables()
        for (i, j), btn in self.boutons.items():
            if (i, j) in deplacables:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: none;")

    def mettre_a_jour_boutons_actions(self):
        self.bouton_placer_pion.setStyleSheet("background-color: none")
        self.bouton_deplacer_pion.setStyleSheet("background-color: none")
        self.bouton_deplacer_carre.setStyleSheet("background-color: none")
        self.bouton_deplacer_deux_carres.setStyleSheet("background-color: none")

        if self.action_selectionnee == "Placer un pion":
            self.bouton_placer_pion.setStyleSheet("background-color: yellow")
        elif self.action_selectionnee == "Déplacer un pion":
            self.bouton_deplacer_pion.setStyleSheet("background-color: yellow")
        elif self.action_selectionnee == "Déplacer un carré":
            self.bouton_deplacer_carre.setStyleSheet("background-color: yellow")
        elif self.action_selectionnee == "Déplacer 2 carrés":
            self.bouton_deplacer_deux_carres.setStyleSheet("background-color: yellow")

    def gerer_clic(self, x, y):
        if not self.action_selectionnee:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une action d'abord !")
            return

        if self.action_selectionnee == "Déplacer un pion":
            if len(self.plateau.joueurs[self.joueur_actuel].pions) == 0:
                QMessageBox.warning(self, "Erreur", "Aucun pion à déplacer !")
                return
        elif self.action_selectionnee == "Déplacer un carré":
            if not any(tuile.estCarrePionDefini() for ligne in self.plateau.plateau for tuile in ligne):
                QMessageBox.warning(self, "Erreur", "Aucune case vide à déplacer pour l'instant !")
                return

        action_reussie = False

        if self.action_selectionnee == "Placer un pion":
            if len(self.plateau.joueurs[self.joueur_actuel].pions) >= 3:
                QMessageBox.warning(self, "Erreur", "Vous ne pouvez pas placer plus de 3 pions !")
                return
            if len(self.plateau.joueurs[self.joueur_actuel].pions) < 3:
                action_reussie = self.plateau.placerRondPion(self.joueur_actuel, x, y) == 0
            if action_reussie:
                self.mettre_a_jour_plateau()
                if self.mode == 0 and all(len(p.pions) >= 1 for p in self.plateau.joueurs):
                    self.bouton_deplacer_pion.show()
                    self.bouton_deplacer_carre.show()
                elif self.mode == 1 and len(self.plateau.joueurs[self.joueur_actuel].pions) >= 1:
                    self.bouton_deplacer_pion.show()
                    self.bouton_deplacer_carre.show()
                if all(len(p.pions) >= 3 for p in self.plateau.joueurs):
                    self.bouton_placer_pion.hide()
                self.effacer_surlignage()
                self.action_selectionnee = None
                self.mettre_a_jour_boutons_actions()
                gagnant = self.plateau.verifierSiGagnant()
                if gagnant != -1:
                    QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
                    self.close()
                    self.redemarrer_application()
                else:
                    self.plateau.finTour()
                    self.joueur_actuel = 1 - self.joueur_actuel
                    self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
                    if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
                        self.jouer_ia()
            return
        elif self.action_selectionnee == "Déplacer un pion":
            if self.pion_selectionne is None:
                if any(pion.posX == x and pion.posY == y for pion in self.plateau.joueurs[self.joueur_actuel].pions):
                    self.pion_selectionne = (x, y)
                    self.surligner_deplacements_possibles(x, y)
                else:
                    QMessageBox.information(self, "Info", "Cette case ne contient pas votre pion.")
                return
            else:
                px, py = self.pion_selectionne
                id_pion = None
                for p in self.plateau.joueurs[self.joueur_actuel].pions:
                    if p.posX == px and p.posY == py:
                        id_pion = p.id
                        break
                if id_pion and self.plateau.deplacerRondPion(self.joueur_actuel, id_pion, x, y) == 0:
                    self.mettre_a_jour_plateau()
                    self.effacer_surlignage()
                    self.pion_selectionne = None
                    self.action_selectionnee = None
                    self.mettre_a_jour_boutons_actions()
                    gagnant = self.plateau.verifierSiGagnant()
                    if gagnant != -1:
                        QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
                        self.close()
                        self.redemarrer_application()
                    else:
                        self.plateau.finTour()
                        self.joueur_actuel = 1 - self.joueur_actuel
                        self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
                        if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
                            self.jouer_ia()
                else:
                    QMessageBox.warning(self, "Erreur", "Déplacement invalide !")
                    self.effacer_surlignage()
                    self.pion_selectionne = None
            return
        elif self.action_selectionnee == "Déplacer un carré":
            deplacables = self.plateau.obtenirTousCarresDeplacables()
            if (x, y) not in deplacables:
                QMessageBox.information(self, "Info", "Case non déplaçable.")
                return
            resultat = self.plateau.deplacerCarrePion(x, y)
            if resultat == 0:
                self.mettre_a_jour_plateau()
                self.effacer_surlignage()
                self.action_selectionnee = None
                self.mettre_a_jour_boutons_actions()
                gagnant = self.plateau.verifierSiGagnant()
                if gagnant != -1:
                    QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
                    self.close()
                    self.redemarrer_application()
                else:
                    self.plateau.finTour()
                    self.joueur_actuel = 1 - self.joueur_actuel
                    self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
                    if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
                        self.jouer_ia()
            else:
                QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                self.mettre_a_jour_plateau()
            return
        elif self.action_selectionnee == "Déplacer 2 carrés":
            tuile = self.plateau.obtenir_plateau_par_coordonnees(x, y)
            if tuile.estCarrePionDefini():
                self.carres_selectionnes.append((x, y))
                if len(self.carres_selectionnes) == 1:
                    self.effacer_surlignage()
                    premier_btn = self.boutons[(x, y)]
                    premier_btn.setStyleSheet("background-color: yellow;")
                    deplacements_possibles = self.plateau.obtenirTousCarresDeplacables()
                    if (x, y) in deplacements_possibles:
                        deplacements_possibles.remove((x, y))
                    for (xx, yy) in deplacements_possibles:
                        self.boutons[(xx, yy)].setStyleSheet("background-color: green;")
                elif len(self.carres_selectionnes) == 2:
                    sx = [self.carres_selectionnes[0][0], self.carres_selectionnes[1][0]]
                    sy = [self.carres_selectionnes[0][1], self.carres_selectionnes[1][1]]
                    resultat = self.plateau.deplacerCarrePion(sx[0], sy[0])
                    if resultat == 0:
                        self.mettre_a_jour_plateau()
                        self.effacer_surlignage()
                        self.carres_selectionnes = [(sx[1], sy[1])]
                        self.compteur_deplacements_carres += 1
                        self.surligner_tous_carres_deplacables()
                        deplacements_possibles = self.plateau.obtenirTousCarresDeplacables()
                        if (sx[1], sy[1]) in deplacements_possibles:
                            deplacements_possibles.remove((sx[1], sy[1]))
                        for (xx, yy) in deplacements_possibles:
                            self.boutons[(xx, yy)].setStyleSheet("background-color: green;")
                        if not deplacements_possibles or self.compteur_deplacements_carres == 2:
                            self.desactiver_boutons_actions()
                            self.action_selectionnee = None
                            self.mettre_a_jour_boutons_actions()
                            self.plateau.finTour()
                            self.joueur_actuel = 1 - self.joueur_actuel
                            self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
                            self.compteur_deplacements_carres = 0
                            self.cooldown_deplacement_deux_carres = True
                            self.effacer_surlignage()
                            self.activer_boutons_actions()
                            if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
                                self.jouer_ia()
                    else:
                        QMessageBox.warning(self, "Erreur", "Déplacement de carré invalide !")
                        self.mettre_a_jour_plateau()
                    self.carres_selectionnes.clear()
            else:
                QMessageBox.information(self, "Info", "Veuillez sélectionner un carré.")
            return

        if action_reussie:
            self.mettre_a_jour_plateau()

            if self.action_selectionnee == "Placer un pion" and action_reussie:
                if all(len(p.pions) >= 1 for p in self.plateau.joueurs):
                    self.bouton_deplacer_pion.show()
                    self.bouton_deplacer_carre.show()

                if all(len(p.pions) >= 3 for p in self.plateau.joueurs):
                    self.bouton_placer_pion.hide()

            gagnant = self.plateau.verifierSiGagnant()
            if gagnant != -1:
                QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
                self.close()
                self.redemarrer_application()
            else:
                self.plateau.finTour()
                self.joueur_actuel = 1 - self.joueur_actuel
                self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")

    def jouer_ia(self):
        choixIA(self.plateau.joueurs[self.joueur_actuel], self.plateau.joueurs[1 - self.joueur_actuel], self.plateau)
        self.mettre_a_jour_plateau()
        gagnant = self.plateau.verifierSiGagnant()
        if gagnant != -1:
            QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
            self.close()
            self.redemarrer_application()
        else:
            self.joueur_actuel = 1 - self.joueur_actuel
            self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
            if self.mode == 1 and self.joueur_actuel == self.joueur_ia:
                self.jouer_ia()
        self.effacer_surlignage()
        self.activer_boutons_actions()

    def etape_ia_vs_ia(self):
        if self.plateau.verifierSiGagnant() == -1:
            choixIA(self.plateau.joueurs[self.joueur_actuel], self.plateau.joueurs[1 - self.joueur_actuel], self.plateau)
            self.mettre_a_jour_plateau()
            gagnant = self.plateau.verifierSiGagnant()
            if gagnant != -1:
                QMessageBox.information(self, "Victoire", f"Joueur {gagnant + 1} a gagné !")
                self.close()
                self.redemarrer_application()
            else:
                self.joueur_actuel = 1 - self.joueur_actuel
                self.label_joueur_actuel.setText(f"Joueur actuel: {self.obtenir_couleur_joueur()}")
        self.effacer_surlignage()
        self.activer_boutons_actions()

    def surligner_deplacements_possibles(self, x, y):
        deplacements_possibles = self.plateau.obtenirDeplacementsRondsValides(x, y)
        for (i, j), btn in self.boutons.items():
            if (i, j) == (x, y):
                btn.setStyleSheet("background-color: yellow;")
            elif (i, j) in deplacements_possibles:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: red;")

    def surligner_carres_possibles(self, x, y):
        deplacements_valides = self.plateau.obtenirDeplacementsCarreValides(x, y)
        for (i, j), btn in self.boutons.items():
            if (i, j) in deplacements_valides:
                btn.setStyleSheet("background-color: green;")
            else:
                btn.setStyleSheet("background-color: none;")

    def effacer_surlignage(self):
        for btn in self.boutons.values():
            btn.setStyleSheet("background-color: none;")

    def mettre_a_jour_plateau(self):
        etat = self.plateau.obtenir_etat_plateau()
        for (x, y), btn in self.boutons.items():
            if etat[x][y] == "vide":
                btn.setText("✖")
                btn.setStyleSheet("color: red;")
            elif etat[x][y] == "blanc":
                btn.setText("⚪")
            elif etat[x][y] == "noir":
                btn.setText("⚫")
            elif etat[x][y] == "carre":
                btn.setText("")
            else:
                btn.setText(" ")
        if self.mode != 2 and self.plateau.estDeplacement2CarrePionsPossible():
            self.bouton_deplacer_deux_carres.show()
        else:
            self.bouton_deplacer_deux_carres.hide()
        if self.mode == 0:
            if all(len(p.pions) >= 1 for p in self.plateau.joueurs):
                self.bouton_deplacer_pion.show()
                self.bouton_deplacer_carre.show()
            if all(len(p.pions) >= 3 for p in self.plateau.joueurs):
                self.bouton_placer_pion.hide()
        elif self.mode == 1:
            if len(self.plateau.joueurs[0].pions) >= 1:
                self.bouton_deplacer_pion.show()
                self.bouton_deplacer_carre.show()
            if len(self.plateau.joueurs[0].pions) >= 3:
                self.bouton_placer_pion.hide()
        self.cooldown_deplacement_deux_carres = False
        self.effacer_surlignage()
        self.activer_boutons_actions()

    def desactiver_boutons_actions(self):
        self.bouton_placer_pion.setEnabled(False)
        self.bouton_deplacer_pion.setEnabled(False)
        self.bouton_deplacer_carre.setEnabled(False)
        self.bouton_deplacer_deux_carres.setEnabled(False)

    def activer_boutons_actions(self):
        self.bouton_placer_pion.setEnabled(True)
        self.bouton_deplacer_pion.setEnabled(True)
        self.bouton_deplacer_carre.setEnabled(True)
        self.bouton_deplacer_deux_carres.setEnabled(True)

    def retour_menu(self):
        self.close()
        self.redemarrer_application()

    def redemarrer_application(self):
        import sys
        from PyQt5.QtWidgets import QApplication

        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        self.dialog = BoiteDialogueSelectionMode()
        if self.dialog.exec_() == QDialog.Accepted:
            mode = self.dialog.obtenir_mode_selectionne()

            if mode == 1:
                dialog_couleur = BoiteDialogueSelectionCouleur()
                if dialog_couleur.exec_() == QDialog.Accepted:
                    couleur_joueur = dialog_couleur.obtenir_couleur_selectionnee()
                else:
                    self.redemarrer_application()
                    return
            else:
                couleur_joueur = "Blanc"

            joueur1 = Joueur(0, PION_BLANC)
            joueur2 = Joueur(1, PION_NOIR)
            plateau = Plateau(joueur1, joueur2)

            self.fenetre = FenetreJeu(plateau, mode, couleur_joueur)
            self.fenetre.show()
            self.fenetre.mettre_a_jour_plateau()
        else:
            self.quitter_application()

    def quitter_application(self):
        import sys
        sys.exit()

class BoiteDialogueSelectionMode(QDialog):
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

    def obtenir_mode_selectionne(self):
        return self.comboBox.currentIndex()

class BoiteDialogueSelectionCouleur(QDialog):
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

    def obtenir_couleur_selectionnee(self):
        return self.colorComboBox.currentText()

if __name__ == "__main__":
    import sys
    from Plateau import Plateau
    from Joueur import Joueur
    from Constantes import PION_BLANC, PION_NOIR

    app = QApplication(sys.argv)

    dialog = BoiteDialogueSelectionMode()
    if dialog.exec_() == QDialog.Accepted:
        mode = dialog.obtenir_mode_selectionne()

        if mode == 1:
            dialog_couleur = BoiteDialogueSelectionCouleur()
            if dialog_couleur.exec_() == QDialog.Accepted:
                couleur_joueur = dialog_couleur.obtenir_couleur_selectionnee()
            else:
                sys.exit()

        else:
            couleur_joueur = "Blanc"

        joueur1 = Joueur(0, PION_BLANC)
        joueur2 = Joueur(1, PION_NOIR)
        plateau = Plateau(joueur1, joueur2)

        fenetre = FenetreJeu(plateau, mode, couleur_joueur)
        fenetre.show()
        fenetre.mettre_a_jour_plateau()
        sys.exit(app.exec_())