"""
Clase Evaluation: Representa una evaluación de un estudiante.
"""

from typing import Optional


class Evaluation:
    """
    Representa una evaluación con su nota y peso académico.
    
    Attributes:
        name (str): Nombre de la evaluación (ej: "Parcial 1", "Lab 3")
        score (float): Nota obtenida (0-20)
        weight (float): Peso de la evaluación sobre la nota final (0-100)
    """
    
    def __init__(self, name: str, score: float, weight: float):
        """
        Inicializa una evaluación.
        
        Args:
            name: Nombre de la evaluación
            score: Nota obtenida (escala 0-20)
            weight: Peso porcentual (0-100)
            
        Raises:
            ValueError: Si los valores están fuera de rango o son inválidos
        """
        if not name or not isinstance(name, str):
            raise ValueError("El nombre de la evaluación debe ser un string no vacío")
        
        if not isinstance(score, (int, float)):
            raise ValueError("La nota debe ser un número")
        
        if not isinstance(weight, (int, float)):
            raise ValueError("El peso debe ser un número")
        
        if score < 0 or score > 20:
            raise ValueError("La nota debe estar entre 0 y 20")
        
        if weight < 0 or weight > 100:
            raise ValueError("El peso debe estar entre 0 y 100")
        
        self._name = name.strip()
        self._score = float(score)
        self._weight = float(weight)
    
    @property
    def name(self) -> str:
        """Obtiene el nombre de la evaluación."""
        return self._name
    
    @property
    def score(self) -> float:
        """Obtiene la nota de la evaluación."""
        return self._score
    
    @property
    def weight(self) -> float:
        """Obtiene el peso de la evaluación."""
        return self._weight
    
    def calculate_weighted_score(self) -> float:
        """
        Calcula la contribución de esta evaluación a la nota final.
        
        Returns:
            Nota ponderada (score * weight / 100)
        """
        return (self._score * self._weight) / 100.0
    
    def __str__(self) -> str:
        return f"Evaluation(Name: {self._name}, Score: {self._score}, Weight: {self._weight}%)"
    
    def __repr__(self) -> str:
        return self.__str__()
