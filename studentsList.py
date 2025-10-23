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

def moyenne_notes(notes) :
    """
    Return the average of a list of numeric notes
    :Args: 
        list of numeric notes
    :return:
        average of notes or None if notes is empty
    """
    if not notes:
        return None

    total = 0.0
    count = 0
    for n in notes:
        total += float(n)
        count += 1

    if count == 0:
        return None
    
    return total / count

def display() :
    """
    To display student and her mean
    """
    for student in students:
        print(f"{student['name']}\t{student['age']} ans\t{student['email']}\nNotes: {student['notes']}\nMoyenne: {moyenne_notes(student['notes'])}")

def find_student_by_id(search_id: int) :
    for student in students :
        if(student['id'] == search_id) :
            return student
    return 0
##Menu
def menu():
    """
        Interactive menu to add student data to the global students list.
    """

    choice: int = 0
    n: int = 0
    id : int = 0

    while choice != 5 :
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
            name = input('Veuillez entrer votre nom et prenom: \n')
            students.append({'id': id})
            students.append({'name': name})
            age = input('Veuillez entrer votre age: \n')
            students.append({'age': age})
            email = input('Veuillez entrer votre email: \n')
            students.append({'email': email})
            notes = input('Veuillez entrer vos notes (séparées par des virgules): \n')
            parsed = [n.strip() for n in notes.split(',')]
            for n in parsed :
                if (int(n) < 0 or int(n) > 20) :
                   print('La note doit etre comprise entre 0 et 20')
                else :
                    students.append({'notes': parsed})
         case 2:
            display()
         case 3:
            id = input('Veuillez entrer l\'ID de l\'étudiant: ')
            find_student_by_id(id)
         case 5:
            print ('Au revoir !')

if __name__ == "__main__":
    menu()