from typing import Dict, Any

class AttendancePolicy:
    
    _all_years_teachers_agree: bool = True
    
    @classmethod
    def set_teachers_agreement(cls, agreement: bool) -> None:
        
        if not isinstance(agreement, bool):
            raise ValueError("El acuerdo de docentes debe ser un valor booleano")
        cls._all_years_teachers_agree = agreement
    
    @classmethod
    def get_teachers_agreement(cls) -> bool:
        
        return cls._all_years_teachers_agree
    
    @staticmethod
    def check_minimum_attendance(has_minimum_attendance: bool) -> Dict[str, Any]:
        
        if not isinstance(has_minimum_attendance, bool):
            raise ValueError("El parámetro de asistencia debe ser booleano")
        
        if has_minimum_attendance:
            return {
                'meets_requirement': True,
                'penalty': 0.0,
                'message': 'Cumple con asistencia mínima requerida'
            }
        else:
            return {
                'meets_requirement': False,
                'penalty': 0.0,  # La penalización se aplica en la lógica de negocio
                'message': 'NO cumple con asistencia mínima requerida (factor determinante para aprobación)'
            }
    
    @staticmethod
    def validate_attendance_record(attendance_percentage: float) -> bool:
        
        if not isinstance(attendance_percentage, (int, float)):
            raise ValueError("El porcentaje de asistencia debe ser un número")
        
        if attendance_percentage < 0 or attendance_percentage > 100:
            raise ValueError("El porcentaje de asistencia debe estar entre 0 y 100")
        
        MINIMUM_ATTENDANCE_PERCENTAGE = 70.0
        return attendance_percentage >= MINIMUM_ATTENDANCE_PERCENTAGE
