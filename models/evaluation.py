from typing import Optional

class Evaluation:
    
    def __init__(self, name: str, score: float, weight: float):
        
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
        
        return self._name
    
    @property
    def score(self) -> float:
        
        return self._score
    
    @property
    def weight(self) -> float:
        
        return self._weight
    
    def calculate_weighted_score(self) -> float:
        
        return (self._score * self._weight) / 100.0
    
    def __str__(self) -> str:
        return f"Evaluation(Name: {self._name}, Score: {self._score}, Weight: {self._weight}%)"
    
    def __repr__(self) -> str:
        return self.__str__()
