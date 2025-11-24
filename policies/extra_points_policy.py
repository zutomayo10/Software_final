"""
Política de puntos extra que pueden otorgar los docentes.
Maneja las bonificaciones adicionales según criterios académicos.
"""

from typing import Dict, Any, List


class ExtraPointsPolicy:
    """
    Gestiona la política de puntos extra otorgados por docentes (RF03).
    
    Los docentes pueden otorgar puntos extra a estudiantes que cumplan
    ciertos criterios académicos, siempre que todos los docentes del curso
    estén de acuerdo.
    """
    
    # Lista que simula la configuración de docentes que participan
    # RF03: allYearsTeachers - lista de docentes
    _all_years_teachers: List[str] = []
    
    @classmethod
    def set_all_years_teachers(cls, teachers: List[str]) -> None:
        """
        Establece la lista de docentes que participan en la decisión de puntos extra.
        
        Args:
            teachers: Lista con los IDs o nombres de los docentes
            
        Raises:
            ValueError: Si no es una lista o está vacía
        """
        if not isinstance(teachers, list):
            raise ValueError("Debe proporcionar una lista de docentes")
        if not teachers:
            raise ValueError("La lista de docentes no puede estar vacía")
        cls._all_years_teachers = teachers.copy()
    
    @classmethod
    def get_all_years_teachers(cls) -> List[str]:
        """
        Obtiene la lista de docentes configurados.
        
        Returns:
            Lista de docentes
        """
        return cls._all_years_teachers.copy()
    
    @staticmethod
    def calculate_extra_points(
        base_grade: float,
        extra_points: float,
        teachers_agree: bool
    ) -> Dict[str, Any]:
        """
        Calcula los puntos extra que se aplicarán a la nota base.
        
        Args:
            base_grade: Nota base calculada (antes de puntos extra)
            extra_points: Cantidad de puntos extra a otorgar
            teachers_agree: Si todos los docentes están de acuerdo (RF03)
            
        Returns:
            Diccionario con:
                - 'extra_points_applied': float - puntos efectivamente aplicados
                - 'final_grade': float - nota final con puntos extra
                - 'capped': bool - si la nota fue limitada a 20
                - 'message': str - mensaje descriptivo
                
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        # Validaciones
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
        
        # Si los docentes no están de acuerdo, no se aplican puntos extra
        if not teachers_agree:
            return {
                'extra_points_applied': 0.0,
                'final_grade': base_grade,
                'capped': False,
                'message': 'Puntos extra NO aplicados: docentes no están de acuerdo'
            }
        
        # Aplicar puntos extra
        final_grade = base_grade + extra_points
        capped = False
        
        # La nota final no puede exceder 20
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
        """
        Valida que los puntos extra no excedan el máximo permitido.
        
        Args:
            extra_points: Puntos extra a validar
            max_allowed: Máximo de puntos extra permitidos (default: 2.0)
            
        Returns:
            True si es válido, False si excede el máximo
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        if not isinstance(extra_points, (int, float)):
            raise ValueError("Los puntos extra deben ser un número")
        
        if not isinstance(max_allowed, (int, float)):
            raise ValueError("El máximo permitido debe ser un número")
        
        if extra_points < 0:
            raise ValueError("Los puntos extra no pueden ser negativos")
        
        if max_allowed < 0:
            raise ValueError("El máximo permitido no puede ser negativo")
        
        return extra_points <= max_allowed
