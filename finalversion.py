"""
Student management system.

This module defines the Student class and helper functions
for managing student data, calculating averages, validating emails,
and saving/loading data to and from JSON files.
It also includes an interactive menu for user interaction.
"""

from math import fsum
import json
from typing import Any


class Student:
    """
    Represents a student.
    Attributes:
        student_id (int): Unique identifier.
        name (str): Full name.
        email (str): Email address.
        grades (list[float]): List of grades (as floats).
    """

    def __init__(
        self, student_id: int, name: str, email: str, grades: list[float] | None = None
    ) -> None:
        """
        Initializes a new Student object.
        Args:
            student_id (int): Unique identifier.
            name (str): Full name of the student.
            email (str): Email address.
            grades (List[float] | None): Initial list of grades.
        """
        self.student_id = int(student_id)
        self.name = name
        self.email = email
        # copy to avoid aliasing
        self.grades: list[float] = list(grades) if grades else []

    def average(self) -> float:
        """
        Calculates and returns the average of the grades, rounded to 2 decimal places.
        Returns:
            float: The average rounded to 2 decimal places. Returns 0.0 if no grades are provided.
        Raises:
            TypeError: If any element in the grades list cannot be converted to a float.
        """
        if not self.grades:
            return 0.0

        vals: list[float] = []
        for n in self.grades:
            try:
                vals.append(float(n))
            except (TypeError, ValueError) as exc:
                raise TypeError(f"Note non numérique détectée : {n!r}") from exc
        avg = fsum(vals) / len(vals)
        return round(avg, 2)

    def to_dict(self) -> dict[str, Any]:
        """
        Returns a dictionary representation serializable to JSON.
        Returns:
            dict: A dictionary containing student_id, name, email, and grades.
        """
        return {
            "id": self.student_id,
            "nom": self.name,
            "email": self.email,
            "notes": list(self.grades),
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
            m = self.average()
        except TypeError:
            m = "err"
        return f"ID: {self.student_id} | Nom: {self.name} | Email: {self.email} | Moyenne: {m}"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Student":
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
        name = data.get("nom", "")
        email = data.get("email", "")
        grades = data.get("notes", [])

        try:
            id_int = int(id_val)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"ID invalide dans le dict: {id_val!r}") from exc
        if not isinstance(grades, list):
            grades = list(grades) if grades else []
        return cls(id_int, name, email, grades)


def parse_grades_input(grades_str: str) -> list[float]:
    """
    Converts a string like "15, 12.5, 18" into a list of floats validated between 0 and 20.
    Args:
        grades_str (str): string entered by the user.
    Returns:
        list[float]: list of converted grades.
    Raises:
        ValueError: if a value cannot be converted to float or is outside the [0, 20] range.
    """
    if not grades_str or not grades_str.strip():
        return []
    parts = [p.strip() for p in grades_str.split(",")]
    grades: list[float] = []
    for p in parts:
        if p == "":
            continue
        try:
            f = float(p)
        except ValueError as exc:
            raise ValueError(f"Impossible de convertir en nombre : '{p}'") from exc
        if not 0 <= f <= 20:
            raise ValueError(f"Note hors intervalle [0, 20] : {f}")
        grades.append(f)
    return grades


def generate_new_id(students: list[Student]) -> int:
    """
    Generates a new unique ID (maximum existing ID + 1), tolerant to IDs stored as int or str.
    Args:
        students (list[Student]): list of Student objects.
    Returns:
        int: new identifier.
    """
    try:
        max_id = max((int(s.student_id) for s in students), default=0)
    except Exception:
        max_id = 0
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
            sid = int(s.student_id)
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
            json_list = [s.to_dict() for s in students]
            json.dump(json_list, f, ensure_ascii=False, indent=2)
        print(f"Sauvegarde effectuée dans le fichier: {fichier}")
    except IOError as exc:
        print(f"Erreur lors de la sauvegarde : {exc}")


def load(fichier: str = "etudiants.json") -> list[Student]:
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
            print("Fichier JSON mal formaté : la racine doit être une liste.")
            return []
        for item in raw:
            if not isinstance(item, dict):
                continue
            try:
                st = Student.from_dict(item)
            except ValueError as exc:
                print(f"Ignoré lors du chargement: {exc}")
                continue
            loaded.append(st)
        return loaded
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError) as exc:
        print(f"Erreur lors du chargement du fichier JSON : {exc}")
        return []


def display_students(students: list[Student]) -> None:
    """
    Displays all students (uses Student's __str__ method).
    """

    if not students:
        print("\nAucun étudiant enregistré.")
        return
    for s in students:
        print(s)


def handle_add_student(students: list[Student]) -> None:
    """
    Interactive flow to add a new student to the `students` list.

    Behaviour:
      - User can cancel at any prompt by entering 'q' (case-insensitive).
      - Validates email via Student.valid_email().
      - Validates grades via parse_grades_input().
      - Prevents duplicate emails.
      - Appends a new Student on success and prints the new ID.
    """
    print("\n-- Ajoutez un nouvel étudiant (entrez 'q' pour annuler l'opération) --")

    while True:
        name = input("Nom complet : ").strip()
        if name.lower() == "q":
            print("L'ajout d'un nouvel étudiant annulé.")
            return
        if not name:
            print("Le nom ne peut pas être vide. Réessayez ou entrez 'q' pour annuler.")
            continue

        email_input = input("Email: ").strip()
        if email_input.lower() == "q":
            print("L'ajout d'un nouvel étudiant annulé.")
            return

        # Check duplicate email
        if any(s.email == email_input for s in students):
            print(
                "Cet email existe déjà. "
                "Entrez une autre adresse mail ou entrez 'q' pour annuler."
            )
            continue

        # Validate email using Student.valid_email
        temp = Student(0, name, email_input, [])
        if not temp.valid_email():
            print(
                "Format de l'adresse mail invalide. "
                "Réessayez ou entrez 'q' pour annuler."
            )
            continue

        grades_str = input(
            "Notes (séparées par des virgules, ex: 15,12.5,18) — laissez vide si aucune : "
        ).strip()
        if grades_str.lower() == "q":
            print("L'ajout d'un nouvel étudiant annulé.")
            return

        try:
            grades = parse_grades_input(grades_str)
        except ValueError as exc:
            print(
                f"Erreur dans les notes : {exc}. Réessayez ou entrez 'q' pour annuler."
            )
            continue

        # All validations passed -> create and append student
        new_id = generate_new_id(students)
        new_student = Student(new_id, name, email_input, grades)
        students.append(new_student)
        print(f"\nÉtudiant ajouté avec ID {new_id}.")
        return


def handle_search(students: list[Student]) -> None:
    """
    Handles the user interaction for searching a student by ID.

    Asks the user to input an ID, validates it, calls find_student_by_id(),
    and displays the result (or an error message if not found).

    Args:
        students (list[Student]): The current list of students.
    """
    id_str = input("ID recherché : ").strip()

    # Validate user input
    if not id_str or not id_str.isdigit():
        print(" ID invalide : doit être un entier positif.")
        return

    ident = int(id_str)

    try:
        found = find_student_by_id(students, ident)
        print(
            f"Étudiant trouvé :\n"
            f"ID: {found.student_id}\n"
            f"Nom: {found.name}\n"
            f"Email: {found.email}\n"
            f"Notes: {found.grades}\n"
            f"Moyenne: {found.average()}\n"
        )
    except ValueError as exc:
        print(f" {exc}")


def handle_exit(students: list[Student]) -> bool:
    """
    Handles the exit process: asks for confirmation, saves data, and returns
    whether the program should exit.

    Args:
        students (list[Student]): The current list of students.

    Returns:
        bool: True if the user confirmed exit, False otherwise.
    """
    confirm = input("Quitter ? (o/N) : ").strip().lower()
    if confirm == "o":
        try:
            save(students, "etudiants.json")
            print("Sauvegarde effectuée avant fermeture.")
        except (OSError, IOError) as exc:
            print(f"Erreur lors de la sauvegarde : {exc}")
        print("A bientôt!")
        return True
    else:
        print("Retour au menu principal.")
        return False


# ------------------------
# Interactive menu
# ------------------------


def menu():
    """
    Main interactive menu.
    Handles adding, displaying, searching, saving, and exiting.
    """
    students = load("etudiants.json")  # charger au démarrage
    exiting = False
    try:
        while True:
            print("\n--- MENU ---")
            print("1. Ajouter un étudiant")
            print("2. Afficher tous les étudiants")
            print("3. Rechercher par ID")
            print("4. Sauvegarder")
            print("5. Quitter")
            choice = input("Choix (1-5) : ").strip()

            if choice == "1":
                handle_add_student(students)

            elif choice == "2":
                display_students(students)

            elif choice == "3":
                handle_search(students)

            elif choice == "4":
                save(students, "etudiants.json")

            elif choice == "5":
                if handle_exit(students):
                    exiting = True
                    break
            else:
                print("Choix invalide — entre 1 et 5.")
    finally:
        if not exiting:
            try:
                save(students, "etudiants.json")
            except (OSError, IOError):
                pass


if __name__ == "__main__":
    menu()
