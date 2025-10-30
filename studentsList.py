import json

students = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "age": 20,
        "email": "alice@exemple.com",
        "notes": [15.5, 12.0, 18.0]
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "age": 22,
        "email": "bob@exemple.com",
        "notes": [14.0, 16.0, 13.5]
    }
]

def moyenne_notes(notes):
    """
    Return the average of a list of numeric notes
    :Args: 
        list of numeric notes
    :return:
        average of notes or None if notes is empty
    """
    if not notes:
        return None

    return sum(float(n) for n in notes) / len(notes)

def display():
    """
    To display student and her mean
    """
    for student in students:
        print(f"{student['name']}\t{student['age']} ans\t{student['email']}\nNotes: {student['notes']}\nMoyenne: {moyenne_notes(student['notes'])}")

def find_student_by_id(search_id: int):
    for student in students:
        if student.get('id') == search_id:
            return student
    return None

def save_students(filepath: str):
    """Save students list as a simple text representation (JSON style)."""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=2)

##Menu
def menu():
    """
        Interactive menu to add student data to the global students list.
    """
    choice: int = 0
    next_id = max((student.get('id', 0) for student in students)) + 1   

    while choice != 5:
        print('1. Ajouter un étudiant ')
        print('2. Afficher tous les étudiants (avec moyennes).')
        print('3. Rechercher par ID ')
        print('4. Sauvegarder ')
        print('5. Quitter: ')

        try:
            choice = int(input('Choix: '))
        except ValueError:
            print('Veuillez entrer un nombre valide (1-5).')
            continue

        match choice:
            case 1:
                name = input('Veuillez entrer votre nom et prenom: \n').strip()

                try:
                    age = int(input('Veuillez entrer votre age: \n'))
                    if age < 0:
                        print("L'âge doit être positif.")
                        continue
                except ValueError:
                    print("L'âge n'est pas valide.\n")
                    continue
                    
                email = input('Veuillez entrer votre email: \n').strip()
                notes_input = input('Veuillez entrer vos notes (séparées par des virgules): \n').strip()

                if not notes_input:
                    print("Aucune note fournie. Étudiant non ajouté.")
                    continue

                try:
                    parsed_notes = [float(n.strip()) for n in notes_input.split(',')]
                    for n in parsed_notes:
                        if n < 0 or n > 20:
                            print('La note doit être comprise entre 0 et 20.')
                            raise ValueError("Note invalide détectée.")
                except ValueError as e:
                    print(f"Erreur dans les notes: {e}. Étudiant non ajouté.")
                    continue

                student = {
                    'id': next_id,
                    'name': name,
                    'age': age,
                    'email': email,
                    'notes': parsed_notes,
                }
                students.append(student)
                print(f"Étudiant ajouté avec ID {next_id}.")
                next_id += 1

            case 2:
                display()
            case 3:
                try:
                    student_id = int(input('Veuillez entrer l\'ID de l\'étudiant: '))
                    student = find_student_by_id(student_id)
                    if student:
                        print(f"Étudiant trouvé: {student['name']}, {student['age']} ans, {student['email']}")
                        print(f"Notes: {student['notes']}")
                        print(f"Moyenne: {moyenne_notes(student['notes'])}")
                    else:
                        print("Aucun étudiant trouvé avec cet ID.")
                except ValueError:
                    print('ID invalide.')
            case 4:
                path = 'students.json'
                save_students(path)
                print(f'Etudiants enregistrés dans {path}')
            case 5:
                print('Au revoir !')
                break 

if __name__ == "__main__":
    menu()