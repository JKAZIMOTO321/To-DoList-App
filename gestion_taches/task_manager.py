import datetime

class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        self._next_id = self._get_next_id()

    def _get_next_id(self):
        if not self.tasks:
            return 1
        return max(task.get("id", 0) for task in self.tasks) + 1

    def get_tasks(self, filtre_statut=None, filtre_priorite=None):
        tasks = self.tasks
        if filtre_statut:
            tasks = [t for t in tasks if t["statut"] == filtre_statut]
        if filtre_priorite:
            tasks = [t for t in tasks if t["priorite"] == filtre_priorite]
        return tasks

    def add_task(self, titre, description, priorite, date_limite):
        task = {
            "id": self._next_id,
            "titre": titre,
            "description": description,
            "priorite": priorite,
            "date_limite": date_limite,
            "statut": "À faire"
        }
        self.tasks.append(task)
        self._next_id += 1
        self.storage.save_tasks(self.tasks)
        return task

    def update_task(self, task_id, titre=None, description=None, priorite=None, date_limite=None, statut=None):
        for task in self.tasks:
            if task["id"] == task_id:
                if titre is not None:
                    task["titre"] = titre
                if description is not None:
                    task["description"] = description
                if priorite is not None:
                    task["priorite"] = priorite
                if date_limite is not None:
                    task["date_limite"] = date_limite
                if statut is not None:
                    task["statut"] = statut
                self.storage.save_tasks(self.tasks)
                return task
        return None

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.storage.save_tasks(self.tasks)

    def mark_task_done(self, task_id):
        return self.update_task(task_id, statut="Terminée")

# Exemple d'utilisation :
# from storage import Storage
# storage = Storage('data/tasks.json')
# manager = TaskManager(storage)
# manager.add_task("Titre", "Desc", "Normale", "2025-01-01")
