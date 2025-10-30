from __future__ import annotations
from math import fsum
import json


class Student:
    """
    Represents a student.
    Attributes:
        id (int): Unique identifier.
        nom (str): Full name.
        email (str): Email address.
        notes (List[float]): List of grades (as floats).
    """

    def __init__(
        self, id: int, nom: str, email: str, notes: list[float] | None = None
    ) -> None:
        """
        Initializes a new Student object.
        Args:
            id (int): Unique identifier.
            nom (str): Full name of the student.
            email (str): Email address.
            notes (List[float] | None): Initial list of grades.
        """

        self.id = int(id)
        self.nom = nom
        self.email = email
        self.notes: list[float] = list(notes) if notes else []

    def moyenne(self) -> float:
        """
        Calculates and returns the average of the grades, rounded to 2 decimal places.
        Returns:
            float: The average rounded to 2 decimal places. Returns 0.0 if no grades are provided.
        Raises:
            TypeError: If any element in the grades list cannot be converted to a float.
        """

        if not self.notes:
            return 0.0

        vals: list[float] = []
        for note in self.notes:
            try:
                vals.append(float(note))
            except (TypeError, ValueError):
                raise TypeError(f"Note non numérique détectée : {note!r}")
        avg = fsum(vals) / len(vals)
        return round(avg, 2)

    def to_dict(self) -> dict[str, any]:
        """
        Returns a dictionary representation serializable to JSON.
        Returns:
            dict: A dictionary containing id, name, email, and grades.
        """

        return {
            "id": self.id,
            "nom": self.nom,
            "email": self.email,
            "notes": list(self.notes),
        }

    def valid_email(self) -> bool:
        """
        Checks if the email has a reasonable format.
        Minimal criteria:
          - contains '@'
          - the part after '@' contains a dot
          - does not start with '@' and does not end with '.'
        Returns:
            bool: True if the email appears valid, False otherwise.
        """

        if not self.email or "@" not in self.email:
            return False
        local, _, domain = self.email.partition("@")
        if not local or not domain or "." not in domain:
            return False
        if self.email.startswith("@") or self.email.endswith("."):
            return False
        return True

    def __str__(self) -> str:
        """
        Readable string representation of the student.
        Example: "ID: 1 | Name: Alice Dupont | Email: alice@example.com | Average: 15.25"
        """

        try:
            m = self.moyenne()
        except TypeError:
            m = "err"
        return f"ID: {self.id} | Nom: {self.nom} | Email: {self.email} | Moyenne: {m}"

    @classmethod
    def from_dict(cls, data: dict[str, any]) -> "Student":
        """
        Creates a Student instance from a dictionary (useful for JSON loading).
        Args:
            data (dict): A dictionary containing 'id', 'nom', 'email', and optionally 'notes'.
        Returns:
            Student: The created instance.
        Notes:
            - Invalid values may raise exceptions or be ignored depending on the case.
        """

        id_val = data.get("id")
        nom = data.get("nom", "")
        email = data.get("email", "")
        notes = data.get("notes", [])

        try:
            id_int = int(id_val)
        except (TypeError, ValueError):
            raise ValueError(f"ID invalide dans le dict: {id_val!r}")
        if not isinstance(notes, list):
            notes = list(notes) if notes else []
        return cls(id_int, nom, email, notes)


def parse_notes_input(notes_str: str) -> list[float]:
    """
    Converts a string like "15, 12.5, 18" into a list of floats validated between 0 and 20.
    Args:
        notes_str (str): string entered by the user.
    Returns:
        list[float]: list of converted grades.
    Raises:
        ValueError: if a value cannot be converted to float or is outside the [0, 20] range.
    """

    if not notes_str or not notes_str.strip():
        return []
    parts = [p.strip() for p in notes_str.split(",")]
    notes: list[float] = []
    for p in parts:
        if p == "":
            continue
        try:
            f = float(p)
        except ValueError:
            raise ValueError(f"Impossible de convertir en nombre : '{p}'")
        if not (0 <= f <= 20):
            raise ValueError(f"Note hors intervalle [0, 20] : {f}")
        notes.append(f)
    return notes


def generate_new_id(students: list[Student]) -> int:
    """
    Generates a new unique ID (maximum existing ID + 1), tolerant to IDs stored as int or str.
    Args:
        students (list[Student]): list of Student objects.
    Returns:
        int: new identifier.
    """

    if not students:
        return 1
    max_id = 0
    for s in students:
        try:
            sid = int(s.id)
        except (TypeError, ValueError):
            continue
        if sid > max_id:
            max_id = sid
    return max_id + 1


def find_student_by_id(students: list[Student], searched_id: int) -> Student:
    """
    Search for a student by ID and return the corresponding Student object.
    Args:
        students (list[Student]): list of students.
        searched_id (int): ID to search for.
    Returns:
        Student: the matching student object.
    Raises:
        ValueError: if no student with the given ID is found.
    """

    try:
        target = int(searched_id)
    except (TypeError, ValueError):
        raise ValueError("ID invalide fourni à la recherche")

    for s in students:
        try:
            sid = int(s.id)
        except (TypeError, ValueError):
            continue
        if sid == target:
            return s
    raise ValueError(f"Aucun étudiant avec l'ID {searched_id}.")


def save(students: list[Student], fichier: str = "etudiants.json") -> None:
    """
    Saves the list of students to a JSON file using to_dict().
    Args:
        students (list[Student]): list of Student objects.
        fichier (str): path to the output file.
    """

    try:
        with open(fichier, "w", encoding="utf-8") as f:
            json_list = [e.to_dict() for e in students]
            json.dump(json_list, f, ensure_ascii=False, indent=2)
        print(f"Sauvegarde effectuée: {fichier}")
    except IOError as exc:
        print(f"Erreur lors de la sauvegarde : {exc}")


def charger(fichier: str = "etudiants.json") -> list[Student]:
    """
    Loads the list of students from a JSON file.
    Returns an empty list if the file is missing or corrupted.
    Args:
        fichier (str): Path to the JSON file.
    Returns:
        list[Student]: A list of Student objects.
    """

    try:
        with open(fichier, "r", encoding="utf-8") as f:
            raw = json.load(f)
        loaded: list[Student] = []
        if not isinstance(raw, list):
            print("La racine doit être une liste.")
            return []
        for item in raw:
            if not isinstance(item, dict):
                continue
            try:
                et = Student.from_dict(item)
            except ValueError as exc:
                print(f"Ignoré lors du chargement: {exc}")
                continue
            loaded.append(et)
        return loaded
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError) as exc:
        print(f"Erreur lors du chargement du fichier JSON : {exc}")
        return []


def afficher_etudiants(students: list[Student]) -> None:
    """
    Displays all students (uses Student's __str__ method).
    """

    if not students:
        print("\nAucun étudiant enregistré.")
        return
    for e in students:
        print(e)


def menu():
    """
    Main interactive menu.
    Handles adding, displaying, searching, saving, and exiting.
    """

    students = charger("etudiants.json")  # charger au démarrage
    try:
        while True:
            print("\n--- MENU ---")
            print("1. Ajouter un étudiant")
            print("2. Afficher tous les étudiants")
            print("3. Rechercher par ID")
            print("4. Sauvegarder")
            print("5. Quitter")
            choix = input("Choix (1-5) : ").strip()

            if choix == "1":
                nom = input("Nom complet : ").strip()
                email_input = input("Email : ").strip()

                temp = Student(0, nom, email_input, [])
                if not temp.valid_email():
                    print("Email invalide. Opération annulée.")
                    continue

                notes_str = input(
                    "Notes (séparées par des virgules, ex: 15,12.5,18) — laissez vide si aucune : "
                ).strip()
                try:
                    notes = parse_notes_input(notes_str)
                except ValueError as exc:
                    print(f"Erreur dans les notes : {exc}. Opération annulée.")
                    continue

                new_id = generate_new_id(students)
                new_student = Student(new_id, nom, email_input, notes)
                students.append(new_student)
                print(f"\nÉtudiant ajouté avec ID {new_id}.")

            elif choix == "2":
                afficher_etudiants(students)

            elif choix == "3":
                id_str = input("ID recherché : ").strip()
                try:
                    if not id_str or not id_str.isdigit():
                        raise ValueError("ID invalide : doit être un entier positif.")
                    ident = int(id_str)
                    try:
                        found = find_student_by_id(students, ident)
                    except ValueError as exc:
                        print(exc)
                        continue
                    print(
                        f"ID: {found.id} | Nom: {found.nom} | Email: {found.email} | Notes: {found.notes} | Moyenne: {found.moyenne()}"
                    )
                except ValueError as exc:
                    print(exc)
                    continue

            elif choix == "4":
                save(students, "etudiants.json")

            elif choix == "5":
                confirm = input("Quitter ? (o/N) : ").strip().lower()
                if confirm == "o":
                    # sauvegarde finale avant de quitter
                    save(students, "etudiants.json")
                    print("Au revoir.")
                    break
                else:
                    print("Annulé, retour au menu.")

            else:
                print("Choix invalide — entre 1 et 5.")
    finally:
        # Au cas où une interruption survient, on sauvegarde quand même
        try:
            save(students, "etudiants.json")
        except Exception:
            pass


if __name__ == "__main__":
    menu()
