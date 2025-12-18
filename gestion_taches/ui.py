from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
            QTableWidget, QTableWidgetItem, QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QMessageBox,
            QStackedWidget, QMenuBar, QAction
        )

class TaskManagerUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestionnaire de tâches")
        self.setGeometry(100, 100, 800, 600)


        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        # Menu de navigation
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_navigation = self.menu_bar.addMenu("Navigation")
        self.action_afficher_taches = QAction("Liste des tâches", self)
        self.action_ajouter_tache = QAction("Ajouter une tâche", self)
        self.menu_navigation.addAction(self.action_afficher_taches)
        self.menu_navigation.addAction(self.action_ajouter_tache)

        # Connexion des actions de menu
        self.action_afficher_taches.triggered.connect(self.show_list_panel)
        self.action_ajouter_tache.triggered.connect(lambda: self.show_form_panel(edit=False))

        # Panneau liste des tâches
        self.panel_liste = QWidget()
        self.liste_layout = QVBoxLayout()
        self.panel_liste.setLayout(self.liste_layout)
        # Filtre par statut (doit être après la création de self.liste_layout)
        self.filter_layout = QHBoxLayout()
        self.status_filter = QComboBox()
        self.status_filter.addItem("Tous les statuts")
        self.status_filter.addItems(["À faire", "En cours", "Terminée"])
        
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("Toutes les priorités")
        self.priority_filter.addItems(["Faible", "Normale", "Urgente"])
        
        self.filter_layout.addWidget(QLabel("Statut : "))
        self.filter_layout.addWidget(self.status_filter)
        self.filter_layout.addWidget(QLabel("  Priorité : "))
        self.filter_layout.addWidget(self.priority_filter)
        self.liste_layout.insertLayout(0, self.filter_layout)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Titre", "Priorité", "Date limite", "Statut", "Description"
        ])
        self.liste_layout.addWidget(self.table)
        self.button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ajouter")
        self.edit_btn = QPushButton("Modifier")
        self.delete_btn = QPushButton("Supprimer")
        self.in_progress_btn = QPushButton("En cours")
        self.done_btn = QPushButton("Terminer")
        self.button_layout.addWidget(self.add_btn)
        self.button_layout.addWidget(self.edit_btn)
        self.button_layout.addWidget(self.delete_btn)
        self.button_layout.addWidget(self.in_progress_btn)
        self.button_layout.addWidget(self.done_btn)
        self.liste_layout.addLayout(self.button_layout)

        # Panneau formulaire
        self.panel_form = QWidget()
        self.form_layout = QVBoxLayout()
        self.panel_form.setLayout(self.form_layout)
        self.titre_input = QLineEdit()
        self.description_input = QTextEdit()
        self.priorite_input = QComboBox()
        self.priorite_input.addItems(["Faible", "Normale", "Urgente"])
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        self.save_btn = QPushButton("Enregistrer")
        self.form_layout.addWidget(QLabel("Titre :"))
        self.form_layout.addWidget(self.titre_input)
        self.form_layout.addWidget(QLabel("Description :"))
        self.form_layout.addWidget(self.description_input)
        self.form_layout.addWidget(QLabel("Priorité :"))
        self.form_layout.addWidget(self.priorite_input)
        self.form_layout.addWidget(QLabel("Date limite :"))
        self.form_layout.addWidget(self.date_input)
        self.form_layout.addWidget(self.save_btn)

        # StackedWidget pour la navigation
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.panel_liste)  # index 0
        self.stacked.addWidget(self.panel_form)   # index 1
        self.central_layout.addWidget(self.stacked)
        self.setCentralWidget(self.central_widget)

        # Connexions des boutons (slots à connecter dans main.py)
        # self.add_btn.clicked.connect(...)
        # self.edit_btn.clicked.connect(...)
        # self.delete_btn.clicked.connect(...)
        # self.done_btn.clicked.connect(...)
        # self.save_btn.clicked.connect(...)
        # self.add_btn.clicked.connect(...)
        # self.edit_btn.clicked.connect(...)
        # self.delete_btn.clicked.connect(...)
        # self.done_btn.clicked.connect(...)
        # self.save_btn.clicked.connect(...)


    def show_form_panel(self, edit=False):
        self.stacked.setCurrentIndex(1)
        if not edit:
            self.titre_input.clear()
            self.description_input.clear()
            self.priorite_input.setCurrentIndex(1)
            self.date_input.setDate(QDate.currentDate())

    def show_list_panel(self):
        self.stacked.setCurrentIndex(0)


    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerUI()
    window.show()
    sys.exit(app.exec_())
