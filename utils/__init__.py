"""
Módulo de utilidades.
Contiene clases y funciones de apoyo para el sistema.
"""

from .exceptions import (
    GradeCalculationError,
    InvalidEvaluationError,
    MaxEvaluationsExceededError,
    InvalidWeightError,
    AttendanceRequirementError,
    CalculationTimeoutError,
    InvalidStudentDataError
)

__all__ = [
    'GradeCalculationError',
    'InvalidEvaluationError',
    'MaxEvaluationsExceededError',
    'InvalidWeightError',
    'AttendanceRequirementError',
    'CalculationTimeoutError',
    'InvalidStudentDataError'
]
