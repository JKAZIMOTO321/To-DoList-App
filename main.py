import sys
from PyQt5.QtWidgets import QApplication
from gestion_taches.ui import TaskManagerUI
from gestion_taches.storage import Storage
from gestion_taches.task_manager import TaskManager
from PyQt5.QtCore import QDate

class MainApp(TaskManagerUI):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.selected_task_id = None
        self.refresh_table()
        self.status_filter.currentIndexChanged.connect(self.refresh_table)
        self.priority_filter.currentIndexChanged.connect(self.refresh_table)
        # Connexions des boutons
        self.add_btn.clicked.connect(self.show_add_form)
        self.edit_btn.clicked.connect(self.show_edit_form)
        self.delete_btn.clicked.connect(self.delete_task)
        self.in_progress_btn.clicked.connect(self.mark_task_in_progress)
        self.done_btn.clicked.connect(self.mark_task_done)
        self.save_btn.clicked.connect(self.save_task)
        self.table.cellClicked.connect(self.select_task)
        # Afficher la liste au démarrage
        self.show_list_panel()

    def mark_task_in_progress(self):
        if self.selected_task_id is None:
            self.show_message("Aucune sélection", "Veuillez sélectionner une tâche à mettre en cours.")
            return
        self.manager.update_task(self.selected_task_id, statut="En cours")
        self.show_message("Succès", "Tâche marquée comme en cours d'exécution.")
        self.refresh_table()

    def refresh_table(self):
        statut = self.status_filter.currentText()
        priorite = self.priority_filter.currentText()
        
        filtre_statut = None if statut == "Tous les statuts" else statut
        filtre_priorite = None if priorite == "Toutes les priorités" else priorite
        
        tasks = self.manager.get_tasks(filtre_statut=filtre_statut, filtre_priorite=filtre_priorite)
        self.table.setRowCount(len(tasks))
        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, self._item(task["titre"]))
            self.table.setItem(row, 1, self._item(task["priorite"]))
            self.table.setItem(row, 2, self._item(task["date_limite"]))
            self.table.setItem(row, 3, self._item(task["statut"]))
            self.table.setItem(row, 4, self._item(task["description"]))
        self.selected_task_id = None
        self.table.clearSelection()

    def _item(self, value):
        from PyQt5.QtWidgets import QTableWidgetItem
        item = QTableWidgetItem(str(value))
        item.setFlags(item.flags() ^ 2)  # Non-editable
        return item

    def select_task(self, row, column):
        titre = self.table.item(row, 0).text()
        for task in self.manager.get_tasks():
            if task["titre"] == titre:
                self.selected_task_id = task["id"]
                break

    def show_add_form(self):
        self.selected_task_id = None
        self.show_form_panel(edit=False)

    def show_edit_form(self):
        if self.selected_task_id is None:
            self.show_message("Aucune sélection", "Veuillez sélectionner une tâche à modifier.")
            return
        task = next((t for t in self.manager.get_tasks() if t["id"] == self.selected_task_id), None)
        if not task:
            self.show_message("Erreur", "Tâche introuvable.")
            return
        self.titre_input.setText(task["titre"])
        self.description_input.setPlainText(task["description"])
        self.priorite_input.setCurrentText(task["priorite"])
        self.date_input.setDate(QDate.fromString(task["date_limite"], "yyyy-MM-dd"))
        self.show_form_panel(edit=True)

    def save_task(self):
        titre = self.titre_input.text().strip()
        description = self.description_input.toPlainText().strip()
        priorite = self.priorite_input.currentText()
        date_limite = self.date_input.date().toString("yyyy-MM-dd")
        if not titre:
            self.show_message("Erreur", "Le titre est obligatoire.")
            return
        if self.selected_task_id is None:
            self.manager.add_task(titre, description, priorite, date_limite)
            self.show_message("Succès", "Tâche ajoutée.")
        else:
            self.manager.update_task(self.selected_task_id, titre, description, priorite, date_limite)
            self.show_message("Succès", "Tâche modifiée.")
        self.show_list_panel()
        self.refresh_table()

    def delete_task(self):
        if self.selected_task_id is None:
            self.show_message("Aucune sélection", "Veuillez sélectionner une tâche à supprimer.")
            return
        self.manager.delete_task(self.selected_task_id)
        self.show_message("Succès", "Tâche supprimée.")
        self.refresh_table()

    def mark_task_done(self):
        if self.selected_task_id is None:
            self.show_message("Aucune sélection", "Veuillez sélectionner une tâche à terminer.")
            return
        self.manager.mark_task_done(self.selected_task_id)
        self.show_message("Succès", "Tâche marquée comme terminée.")
        self.refresh_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    storage = Storage("data/tasks.json")
    manager = TaskManager(storage)
    window = MainApp(manager)
    window.show()
    sys.exit(app.exec_())
