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
    
    MAX_CALCULATION_TIME = 0.3
    
    def __init__(self, teacher: Teacher):
        
        if not isinstance(teacher, Teacher):
            raise ValueError("Debe proporcionar un docente válido")
        
        self._teacher = teacher
        self._calculation_history: List[Dict[str, Any]] = []
    
    @property
    def teacher(self) -> Teacher:
        
        return self._teacher
    
    def register_evaluations(
        self,
        student: Student,
        evaluations: List[Evaluation]
    ) -> Dict[str, Any]:
        
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
        
        start_time = time.time()
        
        try:
            if not isinstance(student, Student):
                raise ValueError("Debe proporcionar un estudiante válido")
            
            if not isinstance(extra_points, (int, float)):
                raise ValueError("Los puntos extra deben ser un número")
            
            if extra_points < 0:
                raise ValueError("Los puntos extra no pueden ser negativos")
            
            if student.get_evaluation_count() == 0:
                raise GradeCalculationError(
                    f"El estudiante {student.student_id} no tiene evaluaciones registradas"
                )
            
            total_weight = sum(eval.weight for eval in student.evaluations)
            if abs(total_weight - 100.0) > 0.01:
                raise InvalidWeightError(
                    f"Los pesos de las evaluaciones deben sumar 100%, actualmente suman {total_weight}%"
                )
            
            base_grade = sum(
                eval.calculate_weighted_score() 
                for eval in student.evaluations
            )
            
            attendance_check = AttendancePolicy.check_minimum_attendance(
                student.has_minimum_attendance
            )
            
            teachers_agree = AttendancePolicy.get_teachers_agreement()
            
            extra_points_result = ExtraPointsPolicy.calculate_extra_points(
                base_grade=base_grade,
                extra_points=extra_points if student.has_minimum_attendance else 0,
                teachers_agree=teachers_agree
            )
            
            final_grade = extra_points_result['final_grade']
            
            passes_course = student.has_minimum_attendance and final_grade >= 10.5
            
            calculation_time = time.time() - start_time
            if calculation_time > self.MAX_CALCULATION_TIME:
                raise CalculationTimeoutError(
                    f"El cálculo excedió el tiempo máximo de {self.MAX_CALCULATION_TIME * 1000}ms "
                    f"(tomó {calculation_time * 1000:.2f}ms) - RNF04"
                )
            
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
        
        if not isinstance(student, Student):
            raise ValueError("Debe proporcionar un estudiante válido")
        
        calculation_result = self.calculate_final_grade(student, extra_points)
        
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
        
        attendance_detail = AttendancePolicy.check_minimum_attendance(
            student.has_minimum_attendance
        )
        
        teachers_agree = AttendancePolicy.get_teachers_agreement()
        extra_points_detail = ExtraPointsPolicy.calculate_extra_points(
            base_grade=calculation_result['base_grade'],
            extra_points=extra_points if student.has_minimum_attendance else 0,
            teachers_agree=teachers_agree
        )
        
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
        
        return self._calculation_history.copy()
    
    def clear_history(self) -> None:
        
        self._calculation_history.clear()
