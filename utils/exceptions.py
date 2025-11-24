"""
Excepciones personalizadas del sistema de cálculo de notas.
"""


class GradeCalculationError(Exception):
    """Excepción base para errores de cálculo de notas."""
    pass


class InvalidEvaluationError(GradeCalculationError):
    """Excepción para evaluaciones inválidas."""
    pass


class MaxEvaluationsExceededError(GradeCalculationError):
    """Excepción cuando se excede el máximo de evaluaciones permitidas (RNF01)."""
    pass


class InvalidWeightError(GradeCalculationError):
    """Excepción para pesos de evaluación inválidos."""
    pass


class AttendanceRequirementError(GradeCalculationError):
    """Excepción cuando no se cumple con la asistencia mínima."""
    pass


class CalculationTimeoutError(GradeCalculationError):
    """Excepción cuando el cálculo excede el tiempo límite (RNF04)."""
    pass


class InvalidStudentDataError(GradeCalculationError):
    """Excepción para datos de estudiante inválidos."""
    pass
