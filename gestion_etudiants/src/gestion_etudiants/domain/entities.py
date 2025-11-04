from dataclasses import dataclass
from typing import List, Optional
from math import fsum





@dataclass
class Etudiant:
    """Represents a student with identifying information and grades."""
    id_etudiant:int | None
    nom:str
    email:str
    notes: Optional[List[float]] =None

    def moyenne(self)->float:
        """
        Calculates and returns the average of the grades, rounded to 2 decimal places.
        Returns:
            float: The average rounded to 2 decimal places. Returns 0.0 if no grades are provided.
        Raises:
            TypeError: If any element in the grades list cannot be converted to a float.
        """
        if not self.notes:
            return 0.0

        vals: List[float] = []
        for n in self.notes:
            try:
                vals.append(float(n))
            except (TypeError, ValueError) as exc:
                raise TypeError(f"Note non numérique détectée : {n!r}") from exc
        avg = fsum(vals) / len(vals)
        return round(avg, 2)


stud=Etudiant(12,"Jean","j@exemple.fr",[12,13,14])
print(stud)
print(stud.moyenne())

