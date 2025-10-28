import json

with open('student_list.json', 'r') as fichier_json:
    students = json.load(fichier_json)
    print(students)




def calculer_moyenne(grades):
    "This function returns the average of a list"
    if not grades:
        return 0
    return float(sum(grades) / len(grades))


def afficher():
    "This function returns the list of students with their average"
    try:
        if not students:
            return None
        for dictionnaire in students:
            name = dictionnaire["name"]
            mean = calculer_moyenne(dictionnaire["grades"])
            print(f"{name}'smean is: {mean}")
    except:
        print("An exception occurred")


# affichez(students)


def add_student():
    student = {}
    student["id"] = len(students) + 1
    print("Veuillez entrer les données de l'étudiant")
    student["name"] = input("Entrer le name complet de l'étudiant:")
    student["mail"] = input("Entrer le mail:")
    student["grades"] = []

    y = "Y"
    while y == "Y":
        note = input("Entrer une note de l'étudiant : ")
        try:
            note = float(note)
            Invalid_Number = note < 0 or note > 20
            student["grades"].append(note)
            y = input("Ajouter une note? Y/N : ").upper()
            students.append(student)
        except Invalid_Number:
            print("Wrong input, please try again.")
        except:
            print("Wrong input, please try again.")
        finally:
            return print("Thank you!\n")


def search_by_ID():
    try:
        id = input("Entrer l'id de l'étudiant : ")
        
        for student in students:
            right_id=student.get("id")
            if right_id == int(id):
                return print(f"L'étudiant trouvé : {student}")
        print("Student not found !!!")
    except:
        print("Wrong input, please try again.")

def save_students_list():
    try:
        with open('student_list.json', 'w') as fichier_json:
            json.dump(students, fichier_json)
            print("Liste des étudiants sauvegardée avec succès.")
    except:
        print("Erreur lors de la sauvegarde de la liste des étudiants.")


def menu(choice):
    
    match int(choice):
        case 1:
            add_student()
        case 2:
            afficher()
        case 3:
            search_by_ID()
        case 4:
            save_students_list()
        case _:
            exit()


def display_menu():
    print("\n ****************MENU*************\n")
    print('1 - Ajouter un étudiant')
    print('2 - Afficher tous les étudiants')
    print('3 - Recherchez un étudiant')
    print('4 - Sauvegarder')
    return


def main():
    
    y = "Y"
    while y == "Y":
        display_menu()
        note = input("Que desirez-vous faire? Choisissez un chiffre parmi les options du menu: ")
        try:
            Invalid_options = note not in range(1, 4)
            menu(note)
            y = input("Continuer? Y/N : ").upper()
        except Invalid_options:
            print("Wrong choice, please try again.")
            return
        except:
            print("Wrong input, please try again.")
    
    return print("Thank you! Good Bye ... \n")
        

main()