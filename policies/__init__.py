"""
Módulo de políticas para el cálculo de notas.
Contiene las políticas de asistencia y puntos extra.
"""

from .attendance_policy import AttendancePolicy
from .extra_points_policy import ExtraPointsPolicy

__all__ = ['AttendancePolicy', 'ExtraPointsPolicy']
