from math import fsum
import json


students_list = []

def moyenne_notes(notes: list) -> float:
    """ Calculate the average of a list of grades.
    Returns 0.0 if the list is empty. Raises TypeError if any element is not numeric. """
    if not notes:
        return 0.0

    vals = []
    for n in notes:
        try:
            vals.append(float(n))
        except (TypeError, ValueError):
            raise TypeError(f"Note non numérique détectée : {n!r}")

    avg = fsum(vals) / len(vals)
    return round(avg, 2)

def find_student_by_id(students: list[dict], searched_id: int) -> dict | None:
    """ Return the student dict matching searched_id or None if not found.
    Tolerant to IDs stored as strings or ints. """
    try:
        target = int(searched_id)
    except (TypeError, ValueError):
        return None

    for student in students:
        sid = student.get("id")
        try:
            sid_int = int(sid)
        except (TypeError, ValueError):
            continue
        if sid_int == target:
            return student
    return None


def display_students(students: list[dict]) -> None:
    """Display students' list """
    if not students:
        print("\nAucun étudiant enrégistré.")
        return

    for student in students:
        notes = student.get("notes", [])
        m = moyenne_notes(notes)
        print(
            f'ID: {student.get("id")} | Nom: {student.get("nom")} | '
            f'Email: {student.get("email")} | Notes: {notes} | Moyenne: {m}'
        )


def generate_new_id(students: list[dict]) -> int:
    """Generate a new unique student ID based on the existing list (robust to str/int)."""
    if not students:
        return 1
    max_id = 0
    for s in students:
        sid = s.get("id", 0)
        try:
            sid_int = int(sid)
        except (TypeError, ValueError):
            continue
        if sid_int > max_id:
            max_id = sid_int
    return max_id + 1


def parse_notes_input(notes_str: str) -> list[float]:
    """Converts a string like "15, 12, 18" into a list of floats validated between 0 and 20.
    Raises ValueError if any element is invalid."""
    if not notes_str.strip():
        return []
    parts = [p.strip() for p in notes_str.split(",")]
    notes = []
    for p in parts:
        if p == "":
            continue
        try:
            notes_float = float(p)
        except ValueError:
            raise ValueError(f"Impossible de convertir en nombre : '{p}'")
        if not (0 <= notes_float <= 20):
            raise ValueError(f"Note hors intervalle [0, 20] : {notes_float}")
        notes.append(notes_float)
    return notes

def save_json(students: list[dict], filepath: str = "etudiants.json") -> None:
    """Save the students' list in a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(students, file, ensure_ascii=False, indent=2)
        print(f"Sauvegarde effectuée: {filepath}")
    except IOError as exc:
        print(f"Erreur lors de la sauvegarde : {exc}")


def load_json(filepath: str = "etudiants.json") -> list[dict]:
    """Load students list from JSON file. Returns [] if file not found or invalid."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        normalized = []
        for student in data:
            if not isinstance(student, dict):
                continue
            if "id" in student:
                try:
                    student["id"] = int(student["id"])
                except (TypeError, ValueError):
                    continue
            if "notes" in student and not isinstance(student["notes"], list):
                student["notes"] = list(student["notes"]) if student["notes"] else []
            normalized.append(student)
        return normalized
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, IOError) as exc:
        print("Erreur lors du chargement du fichier JSON :", exc)
        return []

students_list = load_json("etudiants.json")

def check_email_validity(email: str) -> bool:
    """Check if an email address looks valid."""
    if not email:
        print("\nAdresse email vide !")
        print("Exemple d'une adresse électronique valide : 'jeanjacques@yahoo.fr'")
        return False

    if "@" not in email or "." not in email.split("@")[-1]:
        print("\nAdresse email invalide !")
        print("Exemple d'une adresse électronique valide : 'jeanjacques@yahoo.fr'")
        return False

    if email.startswith("@") or email.endswith("."):
        print("\nAdresse email invalide !")
        print("Exemple d'une adresse électronique valide : 'jeanjacques@yahoo.fr'")
        return False

    return True


students_list = []


def menu():
    """Main interactive menu (infinite loop until 'Quit')."""

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
            if not check_email_validity(email_input):
                print("Opération annulée — veuillez réessayer avec un email valide.")
                continue
            email = email_input

            notes_str = input(
                "Notes (séparées par des virgules, ex: 15,12.5,18) — laissez vide si aucune : "
            )
            try:
                notes = parse_notes_input(notes_str)
            except ValueError as exc:
                print(f"Erreur dans les notes : {exc}. Opération annulée.")
                continue

            new_id = generate_new_id(students_list)
            new_student = {"id": new_id, "nom": nom, "email": email, "notes": notes}
            students_list.append(new_student)
            print(f"\nÉtudiant ajouté avec ID {new_id}.")

        elif choix == "2":
            display_students(students_list)

        elif choix == "3":            
            id_str = input("ID recherché : ").strip()
            if not id_str.isdigit():
                print("ID invalide : doit être un entier positif.")
                continue
            ident = int(id_str)
            e = find_student_by_id(students_list, ident)
            if not e:
                print(f"\nAucun étudiant avec l'ID {ident}.")
            else:
                print(
                    f"\nID: {e['id']} | Nom: {e['nom']} | Email: {e['email']} | Notes: {e.get('notes', [])} | Moyenne: {moyenne_notes(e.get('notes', []))}"
                )

        elif choix == "4":
            save_json(students_list)

        elif choix == "5":
            confirm = input("Quitter ? (o/N) : ").strip().lower()
            if confirm == "o":
                print("Au revoir.")
                break
            else:
                print("Annulé, retour au menu.")

        else:
            print("Choix invalide — entre 1 et 5.")


if __name__ == "__main__":
    menu()
