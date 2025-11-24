from typing import Dict, Any, List

class ExtraPointsPolicy:
    
    _all_years_teachers: List[str] = []
    
    @classmethod
    def set_all_years_teachers(cls, teachers: List[str]) -> None:
        
        if not isinstance(teachers, list):
            raise ValueError("Debe proporcionar una lista de docentes")
        if not teachers:
            raise ValueError("La lista de docentes no puede estar vacía")
        cls._all_years_teachers = teachers.copy()
    
    @classmethod
    def get_all_years_teachers(cls) -> List[str]:
        
        return cls._all_years_teachers.copy()
    
    @staticmethod
    def calculate_extra_points(
        base_grade: float,
        extra_points: float,
        teachers_agree: bool
    ) -> Dict[str, Any]:
        
        if not isinstance(base_grade, (int, float)):
            raise ValueError("La nota base debe ser un número")
        
        if not isinstance(extra_points, (int, float)):
            raise ValueError("Los puntos extra deben ser un número")
        
        if not isinstance(teachers_agree, bool):
            raise ValueError("El acuerdo de docentes debe ser booleano")
        
        if base_grade < 0 or base_grade > 20:
            raise ValueError("La nota base debe estar entre 0 y 20")
        
        if extra_points < 0:
            raise ValueError("Los puntos extra no pueden ser negativos")
        
        if not teachers_agree:
            return {
                'extra_points_applied': 0.0,
                'final_grade': base_grade,
                'capped': False,
                'message': 'Puntos extra NO aplicados: docentes no están de acuerdo'
            }
        
        final_grade = base_grade + extra_points
        capped = False
        
        if final_grade > 20:
            final_grade = 20.0
            capped = True
        
        message = f'Puntos extra aplicados: +{extra_points:.2f}'
        if capped:
            message += ' (nota limitada a 20)'
        
        return {
            'extra_points_applied': extra_points,
            'final_grade': round(final_grade, 2),
            'capped': capped,
            'message': message
        }
    
    @staticmethod
    def validate_extra_points(extra_points: float, max_allowed: float = 2.0) -> bool:
        
        if not isinstance(extra_points, (int, float)):
            raise ValueError("Los puntos extra deben ser un número")
        
        if not isinstance(max_allowed, (int, float)):
            raise ValueError("El máximo permitido debe ser un número")
        
        if extra_points < 0:
            raise ValueError("Los puntos extra no pueden ser negativos")
        
        if max_allowed < 0:
            raise ValueError("El máximo permitido no puede ser negativo")
        
        return extra_points <= max_allowed
