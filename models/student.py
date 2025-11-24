"""
Clase Student: Representa un estudiante en el sistema.
"""

from typing import List, Optional
from .evaluation import Evaluation


class Student:
    """
    Representa un estudiante con su información básica y evaluaciones.
    
    Attributes:
        student_id (str): Identificador único del estudiante
        name (str): Nombre completo del estudiante
        evaluations (List[Evaluation]): Lista de evaluaciones del estudiante
        has_minimum_attendance (bool): Indica si cumple con asistencia mínima
    """
    
    def __init__(self, student_id: str, name: str):
        """
        Inicializa un estudiante.
        
        Args:
            student_id: Identificador único del estudiante
            name: Nombre completo del estudiante
            
        Raises:
            ValueError: Si el ID o nombre están vacíos
        """
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
        """Obtiene el ID del estudiante."""
        return self._student_id
    
    @property
    def name(self) -> str:
        """Obtiene el nombre del estudiante."""
        return self._name
    
    @property
    def evaluations(self) -> List[Evaluation]:
        """Obtiene la lista de evaluaciones del estudiante."""
        return self._evaluations.copy()
    
    @property
    def has_minimum_attendance(self) -> bool:
        """Indica si el estudiante cumple con la asistencia mínima."""
        return self._has_minimum_attendance
    
    @has_minimum_attendance.setter
    def has_minimum_attendance(self, value: bool):
        """
        Establece si el estudiante cumple con la asistencia mínima.
        
        Args:
            value: True si cumple, False si no cumple
            
        Raises:
            ValueError: Si el valor no es booleano
        """
        if not isinstance(value, bool):
            raise ValueError("El valor de asistencia mínima debe ser booleano")
        self._has_minimum_attendance = value
    
    def add_evaluation(self, evaluation: Evaluation) -> None:
        """
        Agrega una evaluación al estudiante.
        
        Args:
            evaluation: La evaluación a agregar
            
        Raises:
            ValueError: Si ya tiene 10 evaluaciones (RNF01)
            TypeError: Si el argumento no es una Evaluation
        """
        if not isinstance(evaluation, Evaluation):
            raise TypeError("Debe proporcionar una instancia de Evaluation")
            
        # RNF01: Máximo 10 evaluaciones por estudiante
        if len(self._evaluations) >= 10:
            raise ValueError(
                f"El estudiante {self._student_id} ya tiene el máximo de 10 evaluaciones (RNF01)"
            )
        
        self._evaluations.append(evaluation)
    
    def get_evaluation_count(self) -> int:
        """Retorna el número de evaluaciones registradas."""
        return len(self._evaluations)
    
    def __str__(self) -> str:
        return f"Student(ID: {self._student_id}, Name: {self._name}, Evaluations: {len(self._evaluations)})"
    
    def __repr__(self) -> str:
        return self.__str__()
