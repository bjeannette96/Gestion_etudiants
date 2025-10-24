etudiants = [
    {
        "id": 1,
        "nom": "Alice Dupont",
        "email": "alice@exemple.com",
        "notes": [15.5, 12.0, 18.0],
    },
    {
        "id": 2,
        "nom": "Bob Martin",
        "email": "bob@exemple.com",
        "notes": [10.0, 14.5, 16.0],
    },
]


def calculer_moyenne(notes):
    "This function returns the average of a list"
    if not notes:
        return 0
    return float(sum(notes) / len(notes))


def affichez(students):
    "This function returns the list of students with their average"
    try:
        if not students:
            return None
        for dictionnaire in students:
            nom = dictionnaire["nom"]
            mean = calculer_moyenne(dictionnaire["notes"])
            print(f"L'étudiant {nom} a pour moyenne : {mean}")
    except:
        print("An exception occurred")


# affichez(etudiants)


def add_student():
    student = {}
    student["id"] = len(etudiants) + 1
    print("Veuillez entrer les données de l'étudiant")
    student["name"] = input("Entrer le nom complet de l'étudiant:")
    student["email"] = input("Entrer le mail:")
    student["notes"] = []

    y = "Y"
    while y == "Y":
        note = input("Entrer une note de l'étudiant : ")
        try:
            note = float(note)
            Invalid_Number = note < 0 or note > 20
            student["notes"].append(note)
            y = input("Ajouter une note? Y/N : ").upper()
            etudiants.append(student)
        except Invalid_Number:
            print("Wrong input, please try again.")
        except:
            print("Wrong input, please try again.")
        finally:
            return print("Thank you!\n")


# def search_by_ID(id):
#     try:
        
#     except:
#         print("Wrong input, please try again.")



def menu(choice):
    
    match int(choice):
        case 1:
            add_student()
        case 2:
            affichez(etudiants)
        case 3:
            search_by_ID(id)
        case 4:
            print("Thursday")
        case _:
            print("No match")


def display_menu():
    print("****************MENU*************\n")
    print('1 - Ajouter un étudiant')
    print('2 - Afficher tous les étudiants')
    print('3 - Recherchez un étudiant')
    print('4 - Sauvegarder et quitter \n')
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
        except:
            print("Wrong input, please try again.")
        finally:
            return print("Thank you! Good Bye ... \n")
        
    return

main()