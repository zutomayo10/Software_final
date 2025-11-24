"""
Política de asistencia mínima requerida.
Determina si un estudiante cumple con los requisitos de asistencia para aprobar.
"""

from typing import Dict, Any


class AttendancePolicy:
    """
    Gestiona la política de asistencia mínima requerida (RF02).
    
    Un estudiante debe cumplir con la asistencia mínima establecida por el reglamento
    académico de UTEC para poder aprobar el curso.
    """
    
    # Variable de clase que define si los docentes están de acuerdo con la política
    # RF03: allYearsTeachers con valores True/False
    _all_years_teachers_agree: bool = True
    
    @classmethod
    def set_teachers_agreement(cls, agreement: bool) -> None:
        """
        Establece si todos los docentes del curso están de acuerdo en otorgar
        puntos extra (RF03).
        
        Args:
            agreement: True si todos están de acuerdo, False si no
            
        Raises:
            ValueError: Si el valor no es booleano
        """
        if not isinstance(agreement, bool):
            raise ValueError("El acuerdo de docentes debe ser un valor booleano")
        cls._all_years_teachers_agree = agreement
    
    @classmethod
    def get_teachers_agreement(cls) -> bool:
        """
        Obtiene el estado del acuerdo de docentes.
        
        Returns:
            True si todos los docentes están de acuerdo, False si no
        """
        return cls._all_years_teachers_agree
    
    @staticmethod
    def check_minimum_attendance(has_minimum_attendance: bool) -> Dict[str, Any]:
        """
        Verifica si el estudiante cumple con la asistencia mínima requerida.
        
        Args:
            has_minimum_attendance: Indica si el estudiante alcanzó la asistencia mínima
            
        Returns:
            Diccionario con el resultado de la verificación:
                - 'meets_requirement': bool indicando si cumple
                - 'penalty': float indicando la penalización (0 si cumple)
                - 'message': str con el mensaje descriptivo
                
        Raises:
            ValueError: Si el parámetro no es booleano
        """
        if not isinstance(has_minimum_attendance, bool):
            raise ValueError("El parámetro de asistencia debe ser booleano")
        
        if has_minimum_attendance:
            return {
                'meets_requirement': True,
                'penalty': 0.0,
                'message': 'Cumple con asistencia mínima requerida'
            }
        else:
            # Si no cumple con asistencia mínima, la nota final debe considerar
            # esta falta como factor determinante
            return {
                'meets_requirement': False,
                'penalty': 0.0,  # La penalización se aplica en la lógica de negocio
                'message': 'NO cumple con asistencia mínima requerida (factor determinante para aprobación)'
            }
    
    @staticmethod
    def validate_attendance_record(attendance_percentage: float) -> bool:
        """
        Valida si un porcentaje de asistencia cumple el mínimo requerido.
        Esta es una función auxiliar para cuando se tiene el porcentaje exacto.
        
        Args:
            attendance_percentage: Porcentaje de asistencia (0-100)
            
        Returns:
            True si cumple con el mínimo (generalmente >= 70%), False si no
            
        Raises:
            ValueError: Si el porcentaje está fuera de rango
        """
        if not isinstance(attendance_percentage, (int, float)):
            raise ValueError("El porcentaje de asistencia debe ser un número")
        
        if attendance_percentage < 0 or attendance_percentage > 100:
            raise ValueError("El porcentaje de asistencia debe estar entre 0 y 100")
        
        # Criterio típico: 70% de asistencia mínima
        MINIMUM_ATTENDANCE_PERCENTAGE = 70.0
        return attendance_percentage >= MINIMUM_ATTENDANCE_PERCENTAGE
