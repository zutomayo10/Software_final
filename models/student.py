from typing import List, Optional
from .evaluation import Evaluation

class Student:
    
    def __init__(self, student_id: str, name: str):
        
        if not student_id or not isinstance(student_id, str):
            raise ValueError("El ID del estudiante debe ser un string no vacío")
        if not name or not isinstance(name, str):
            raise ValueError("El nombre del estudiante debe ser un string no vacío")
            
        self._student_id = student_id.strip()
        self._name = name.strip()
        self._evaluations: List[Evaluation] = []
        self._has_minimum_attendance: bool = False
        
    @property
    def student_id(self) -> str:
        
        return self._student_id
    
    @property
    def name(self) -> str:
        
        return self._name
    
    @property
    def evaluations(self) -> List[Evaluation]:
        
        return self._evaluations.copy()
    
    @property
    def has_minimum_attendance(self) -> bool:
        
        return self._has_minimum_attendance
    
    @has_minimum_attendance.setter
    def has_minimum_attendance(self, value: bool):
        
        if not isinstance(value, bool):
            raise ValueError("El valor de asistencia mínima debe ser booleano")
        self._has_minimum_attendance = value
    
    def add_evaluation(self, evaluation: Evaluation) -> None:
        
        if not isinstance(evaluation, Evaluation):
            raise TypeError("Debe proporcionar una instancia de Evaluation")
            
        if len(self._evaluations) >= 10:
            raise ValueError(
                f"El estudiante {self._student_id} ya tiene el máximo de 10 evaluaciones (RNF01)"
            )
        
        self._evaluations.append(evaluation)
    
    def get_evaluation_count(self) -> int:
        
        return len(self._evaluations)
    
    def __str__(self) -> str:
        return f"Student(ID: {self._student_id}, Name: {self._name}, Evaluations: {len(self._evaluations)})"
    
    def __repr__(self) -> str:
        return self.__str__()
