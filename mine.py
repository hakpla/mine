import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import stat

class ErazCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Créateur d'Eraz")

        # Configuration de l'interface utilisateur
        tk.Label(root, text="Entrez l'ID de l'Eraz (multiple de 751953751953):").pack()

        self.eraz_id_entry = tk.Entry(root)
        self.eraz_id_entry.pack()

        tk.Button(root, text="Créer Eraz", command=self.create_eraz).pack()

        # Zone de texte pour afficher les IDs minés
        tk.Label(root, text="IDs des Eraz minés:").pack()
        self.mined_ids_text = scrolledtext.ScrolledText(root, height=10, width=50)
        self.mined_ids_text.pack()
        self.mined_ids_text.config(state=tk.DISABLED)  # Empêcher la modification directe

        # Chemin vers le fichier de log pour suivre les IDs d'Eraz
        self.log_file_path = "/media/aloys/ALOIS/Dev/mine/eraz_ids.txt"
        self.initialize_log_file()
        self.update_mined_ids_display()

    def initialize_log_file(self):
        """Crée le fichier de log s'il n'existe pas déjà."""
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, 'w') as f:
                pass

    def update_mined_ids_display(self):
        """Met à jour l'affichage des IDs minés."""
        with open(self.log_file_path, 'r') as f:
            mined_ids = f.read()
        self.mined_ids_text.config(state=tk.NORMAL)
        self.mined_ids_text.delete('1.0', tk.END)
        self.mined_ids_text.insert(tk.INSERT, mined_ids)
        self.mined_ids_text.config(state=tk.DISABLED)

    def is_id_valid_and_unique(self, eraz_id):
        """Vérifie si l'ID est valide et unique."""
        if eraz_id % 751953751953 != 0:
            return False

        with open(self.log_file_path, 'r') as f:
            used_ids = f.read().splitlines()
            if str(eraz_id) in used_ids:
                return False

        return True

    def create_eraz_file(self, eraz_id, directory):
        """Crée un fichier .eraz pour l'ID spécifié en lecture seule."""
        if not directory:  # Si aucun dossier n'est choisi, annuler la création
            return False

        filepath = os.path.join(directory, f"{eraz_id}.eraz")
        with open(filepath, 'w') as file:
            file.write(f"ID de l'eraz: {eraz_id}")
        os.chmod(filepath, stat.S_IRUSR)  # Rend le fichier en lecture seule

        # Ajoute l'ID au fichier de log
        with open(self.log_file_path, 'a') as f:
            f.write(f"{eraz_id}\n")

        return True

    def create_eraz(self):
        """Traite la demande de création d'un Eraz."""
        try:
            eraz_id = int(self.eraz_id_entry.get())
            if self.is_id_valid_and_unique(eraz_id):
                directory = filedialog.askdirectory()  # Laisse l'utilisateur choisir le dossier de sauvegarde
                if self.create_eraz_file(eraz_id, directory):
                    messagebox.showinfo("Succès", "L'Eraz a été créé avec succès.")
                    self.update_mined_ids_display()  # Mettre à jour l'affichage après chaque création réussie
                else:
                    messagebox.showinfo("Annulé", "Création de l'Eraz annulée.")
            else:
                messagebox.showwarning("Erreur", "ID invalide ou déjà utilisé.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ErazCreatorApp(root)
    root.mainloop()

