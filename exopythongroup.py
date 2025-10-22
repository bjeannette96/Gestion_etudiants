studentslist=[]

#dictionnaire avec : id (int), nom (str), email (str), notes (liste de float)
studentslist=[
    {"id":1100223344,
     "nom":'ALAIN Jean',
     "email":"alainjean@email.com", 
     "notes":[13,12.5,11]
     },

    {"id":1100556677,
     "nom":'BEAUVIN Marc',
     "email":"beauvinmarc@email.com", 
     "notes":[14,15.5,16.5]
     }]

for s in studentslist:
    print(s)

def moyenne_notes(notes):
     '''This function collects each student's grades, 
        calculates their sum, 
        and divides it by the number of grades. '''
     return sum(notes) / len(notes)

for student in studentslist:
    moyenne = moyenne_notes(student["notes"])
    print(f"{student['nom']} : {moyenne:.2f}")

