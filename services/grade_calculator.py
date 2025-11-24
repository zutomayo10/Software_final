"""
Servicio principal para el cálculo de notas finales.
Implementa todos los requerimientos funcionales (RF01-RF05) y no funcionales (RNF01-RNF04).
"""

import time
from typing import Dict, Any, List
from datetime import datetime

from models import Student, Teacher, Evaluation
from policies import AttendancePolicy, ExtraPointsPolicy
from utils.exceptions import (
    GradeCalculationError,
    InvalidWeightError,
    CalculationTimeoutError,
    AttendanceRequirementError
)


class GradeCalculator:
    """
    Calculadora de notas finales que implementa la lógica de negocio completa.
    
    Responsabilidades:
    - RF01: Registrar evaluaciones de estudiantes
    - RF02: Verificar asistencia mínima
    - RF03: Aplicar puntos extra según política de docentes
    - RF04: Calcular nota final
    - RF05: Generar detalle del cálculo
    
    Cumple con:
    - RNF03: Cálculo determinista (mismos datos -> misma nota)
    - RNF04: Tiempo de cálculo < 300ms
    """
    
    # RNF04: Tiempo máximo de cálculo en segundos
    MAX_CALCULATION_TIME = 0.3  # 300 ms
    
    def __init__(self, teacher: Teacher):
        """
        Inicializa el calculador de notas para un docente.
        
        Args:
            teacher: El docente que utilizará el calculador
            
        Raises:
            ValueError: Si el docente no es válido
        """
        if not isinstance(teacher, Teacher):
            raise ValueError("Debe proporcionar un docente válido")
        
        self._teacher = teacher
        self._calculation_history: List[Dict[str, Any]] = []
    
    @property
    def teacher(self) -> Teacher:
        """Obtiene el docente asociado al calculador."""
        return self._teacher
    
    def register_evaluations(
        self,
        student: Student,
        evaluations: List[Evaluation]
    ) -> Dict[str, Any]:
        """
        RF01: Registra las evaluaciones de un estudiante.
        
        Args:
            student: El estudiante al que se le registran las evaluaciones
            evaluations: Lista de evaluaciones a registrar
            
        Returns:
            Diccionario con el resultado del registro
            
        Raises:
            ValueError: Si los parámetros son inválidos
            MaxEvaluationsExceededError: Si se excede el límite de evaluaciones
        """
        if not isinstance(student, Student):
            raise ValueError("Debe proporcionar un estudiante válido")
        
        if not isinstance(evaluations, list):
            raise ValueError("Las evaluaciones deben ser una lista")
        
        result = {
            'success': True,
            'student_id': student.student_id,
            'evaluations_added': 0,
            'total_evaluations': student.get_evaluation_count(),
            'errors': []
        }
        
        for evaluation in evaluations:
            try:
                student.add_evaluation(evaluation)
                result['evaluations_added'] += 1
            except Exception as e:
                result['success'] = False
                result['errors'].append(str(e))
        
        result['total_evaluations'] = student.get_evaluation_count()
        
        return result
    
    def register_attendance(
        self,
        student: Student,
        has_minimum_attendance: bool
    ) -> Dict[str, Any]:
        """
        RF02: Registra si el estudiante cumplió con la asistencia mínima requerida.
        
        Args:
            student: El estudiante
            has_minimum_attendance: Si cumple con asistencia mínima
            
        Returns:
            Diccionario con el resultado del registro
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        if not isinstance(student, Student):
            raise ValueError("Debe proporcionar un estudiante válido")
        
        if not isinstance(has_minimum_attendance, bool):
            raise ValueError("El estado de asistencia debe ser booleano")
        
        student.has_minimum_attendance = has_minimum_attendance
        
        attendance_check = AttendancePolicy.check_minimum_attendance(
            has_minimum_attendance
        )
        
        return {
            'success': True,
            'student_id': student.student_id,
            'has_minimum_attendance': has_minimum_attendance,
            'message': attendance_check['message']
        }
    
    def register_extra_points_policy(
        self,
        teachers_agree: bool,
        teachers_list: List[str] = None
    ) -> Dict[str, Any]:
        """
        RF03: Registra si los docentes están de acuerdo en otorgar puntos extra.
        
        Args:
            teachers_agree: Si todos los docentes están de acuerdo
            teachers_list: Lista opcional de IDs de docentes participantes
            
        Returns:
            Diccionario con el resultado del registro
            
        Raises:
            ValueError: Si los parámetros son inválidos
        """
        if not isinstance(teachers_agree, bool):
            raise ValueError("El acuerdo de docentes debe ser booleano")
        
        AttendancePolicy.set_teachers_agreement(teachers_agree)
        
        if teachers_list:
            ExtraPointsPolicy.set_all_years_teachers(teachers_list)
        
        return {
            'success': True,
            'teachers_agree': teachers_agree,
            'teachers_count': len(teachers_list) if teachers_list else 0,
            'message': f'Política de puntos extra configurada: {"APROBADA" if teachers_agree else "RECHAZADA"}'
        }
    
    def calculate_final_grade(
        self,
        student: Student,
        extra_points: float = 0.0
    ) -> Dict[str, Any]:
        """
        RF04: Calcula la nota final de un estudiante.
        
        El cálculo considera:
        - Evaluaciones ponderadas
        - Asistencia mínima (factor determinante)
        - Puntos extra (si aplica)
        
        Args:
            student: El estudiante
            extra_points: Puntos extra a aplicar (default: 0)
            
        Returns:
            Diccionario con la nota final y detalles del cálculo
            
        Raises:
            GradeCalculationError: Si hay errores en el cálculo
            CalculationTimeoutError: Si excede el tiempo límite (RNF04)
        """
        # RNF04: Medir tiempo de cálculo
        start_time = time.time()
        
        try:
            # Validaciones
            if not isinstance(student, Student):
                raise ValueError("Debe proporcionar un estudiante válido")
            
            if not isinstance(extra_points, (int, float)):
                raise ValueError("Los puntos extra deben ser un número")
            
            if extra_points < 0:
                raise ValueError("Los puntos extra no pueden ser negativos")
            
            # Verificar que tiene evaluaciones
            if student.get_evaluation_count() == 0:
                raise GradeCalculationError(
                    f"El estudiante {student.student_id} no tiene evaluaciones registradas"
                )
            
            # Validar que los pesos suman aproximadamente 100%
            total_weight = sum(eval.weight for eval in student.evaluations)
            if abs(total_weight - 100.0) > 0.01:  # Tolerancia de 0.01%
                raise InvalidWeightError(
                    f"Los pesos de las evaluaciones deben sumar 100%, actualmente suman {total_weight}%"
                )
            
            # Calcular nota base (promedio ponderado)
            base_grade = sum(
                eval.calculate_weighted_score() 
                for eval in student.evaluations
            )
            
            # Verificar asistencia mínima
            attendance_check = AttendancePolicy.check_minimum_attendance(
                student.has_minimum_attendance
            )
            
            # Aplicar puntos extra (solo si cumple asistencia y docentes aprueban)
            teachers_agree = AttendancePolicy.get_teachers_agreement()
            
            extra_points_result = ExtraPointsPolicy.calculate_extra_points(
                base_grade=base_grade,
                extra_points=extra_points if student.has_minimum_attendance else 0,
                teachers_agree=teachers_agree
            )
            
            final_grade = extra_points_result['final_grade']
            
            # RNF03: Si no cumple asistencia mínima, la nota podría verse afectada
            # pero el cálculo en sí es determinista
            passes_course = student.has_minimum_attendance and final_grade >= 10.5
            
            # Verificar tiempo de cálculo (RNF04)
            calculation_time = time.time() - start_time
            if calculation_time > self.MAX_CALCULATION_TIME:
                raise CalculationTimeoutError(
                    f"El cálculo excedió el tiempo máximo de {self.MAX_CALCULATION_TIME * 1000}ms "
                    f"(tomó {calculation_time * 1000:.2f}ms) - RNF04"
                )
            
            # Construir resultado
            result = {
                'success': True,
                'student_id': student.student_id,
                'student_name': student.name,
                'base_grade': round(base_grade, 2),
                'extra_points_applied': extra_points_result['extra_points_applied'],
                'final_grade': final_grade,
                'has_minimum_attendance': student.has_minimum_attendance,
                'passes_course': passes_course,
                'grade_capped': extra_points_result['capped'],
                'calculation_time_ms': round(calculation_time * 1000, 2),
                'timestamp': datetime.now().isoformat()
            }
            
            # Guardar en historial
            self._calculation_history.append(result.copy())
            
            return result
            
        except Exception as e:
            calculation_time = time.time() - start_time
            raise GradeCalculationError(
                f"Error al calcular nota final: {str(e)} "
                f"(tiempo: {calculation_time * 1000:.2f}ms)"
            ) from e
    
    def get_calculation_detail(
        self,
        student: Student,
        extra_points: float = 0.0
    ) -> Dict[str, Any]:
        """
        RF05: Visualiza el detalle del cálculo de la nota final.
        
        Proporciona un desglose completo del cálculo paso a paso,
        incluyendo cada evaluación, su peso, la asistencia y los puntos extra.
        
        Args:
            student: El estudiante
            extra_points: Puntos extra a considerar
            
        Returns:
            Diccionario con el detalle completo del cálculo
            
        Raises:
            GradeCalculationError: Si hay errores en el cálculo
        """
        if not isinstance(student, Student):
            raise ValueError("Debe proporcionar un estudiante válido")
        
        # Calcular nota final
        calculation_result = self.calculate_final_grade(student, extra_points)
        
        # Construir detalle de evaluaciones
        evaluations_detail = []
        for i, evaluation in enumerate(student.evaluations, 1):
            evaluations_detail.append({
                'number': i,
                'name': evaluation.name,
                'score': evaluation.score,
                'weight': evaluation.weight,
                'weighted_score': round(evaluation.calculate_weighted_score(), 2),
                'contribution': f"{evaluation.weight}% de {evaluation.score} = {evaluation.calculate_weighted_score():.2f} puntos"
            })
        
        # Detalle de asistencia
        attendance_detail = AttendancePolicy.check_minimum_attendance(
            student.has_minimum_attendance
        )
        
        # Detalle de puntos extra
        teachers_agree = AttendancePolicy.get_teachers_agreement()
        extra_points_detail = ExtraPointsPolicy.calculate_extra_points(
            base_grade=calculation_result['base_grade'],
            extra_points=extra_points if student.has_minimum_attendance else 0,
            teachers_agree=teachers_agree
        )
        
        # Construir resultado detallado
        detail = {
            'student_info': {
                'id': student.student_id,
                'name': student.name,
                'evaluations_count': student.get_evaluation_count()
            },
            'evaluations_detail': evaluations_detail,
            'base_calculation': {
                'total_weight': sum(e.weight for e in student.evaluations),
                'base_grade': calculation_result['base_grade'],
                'formula': 'Suma de (nota × peso/100) para cada evaluación'
            },
            'attendance': {
                'meets_requirement': attendance_detail['meets_requirement'],
                'message': attendance_detail['message'],
                'impact': 'Requisito obligatorio para aprobar el curso'
            },
            'extra_points': {
                'requested': extra_points,
                'applied': extra_points_detail['extra_points_applied'],
                'teachers_agree': teachers_agree,
                'message': extra_points_detail['message']
            },
            'final_result': {
                'final_grade': calculation_result['final_grade'],
                'passes_course': calculation_result['passes_course'],
                'grade_capped': calculation_result['grade_capped'],
                'approval_threshold': 10.5
            },
            'metadata': {
                'calculated_by': self._teacher.name,
                'teacher_id': self._teacher.teacher_id,
                'calculation_time_ms': calculation_result['calculation_time_ms'],
                'timestamp': calculation_result['timestamp']
            }
        }
        
        return detail
    
    def get_calculation_history(self) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de cálculos realizados.
        
        Returns:
            Lista de cálculos históricos
        """
        return self._calculation_history.copy()
    
    def clear_history(self) -> None:
        """Limpia el historial de cálculos."""
        self._calculation_history.clear()
