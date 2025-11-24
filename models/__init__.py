"""
Módulo de modelos de dominio.
Contiene las clases principales del sistema de cálculo de notas.
"""

from .student import Student
from .teacher import Teacher
from .evaluation import Evaluation

__all__ = ['Student', 'Teacher', 'Evaluation']
