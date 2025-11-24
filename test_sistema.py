import sys
import time
from models import Student, Teacher, Evaluation
from services import GradeCalculator
from policies import AttendancePolicy, ExtraPointsPolicy
from utils.exceptions import (
    GradeCalculationError,
    MaxEvaluationsExceededError,
    InvalidWeightError
)
class TestRunner:
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
    def run_test(self, test_name, test_func):
        
        self.tests_total += 1
        print(f"\n{'=' * 70}")
        print(f"PRUEBA {self.tests_total}: {test_name}")
        print('=' * 70)
        try:
            test_func()
            self.tests_passed += 1
            print(f" PRUEBA PASADA")
        except AssertionError as e:
            self.tests_failed += 1
            print(f" PRUEBA FALLIDA: {e}")
        except Exception as e:
            self.tests_failed += 1
            print(f" ERROR INESPERADO: {e}")
            import traceback
            traceback.print_exc()
    def print_summary(self):
        
        print("\n" + "=" * 70)
        print("RESUMEN DE PRUEBAS")
        print("=" * 70)
        print(f"Total de pruebas: {self.tests_total}")
        print(f" Pasadas: {self.tests_passed}")
        print(f" Fallidas: {self.tests_failed}")
        print(f"Porcentaje de éxito: {(self.tests_passed/self.tests_total)*100:.1f}%")
        print("=" * 70)
        if self.tests_failed == 0:
            print("\n ¡TODAS LAS PRUEBAS PASARON!")
        else:
            print(f"\n {self.tests_failed} prueba(s) fallaron")
def test_crear_modelos():
    
    teacher = Teacher("T001", "Dr. Juan Pérez")
    assert teacher.teacher_id == "T001"
    assert teacher.name == "Dr. Juan Pérez"
    print(" Docente creado correctamente")
    student = Student("202110001", "María González")
    assert student.student_id == "202110001"
    assert student.name == "María González"
    assert student.get_evaluation_count() == 0
    print(" Estudiante creado correctamente")
    evaluation = Evaluation("Parcial 1", 15.5, 30.0)
    assert evaluation.name == "Parcial 1"
    assert evaluation.score == 15.5
    assert evaluation.weight == 30.0
    print(" Evaluación creada correctamente")
def test_validaciones_basicas():
    
    try:
        eval_invalida = Evaluation("Test", 25.0, 30.0)
        assert False, "Debería lanzar ValueError"
    except ValueError:
        print(" Validación de nota máxima funciona")
    try:
        eval_invalida = Evaluation("Test", 15.0, 150.0)
        assert False, "Debería lanzar ValueError"
    except ValueError:
        print(" Validación de peso máximo funciona")
    try:
        student_invalido = Student("", "Nombre")
        assert False, "Debería lanzar ValueError"
    except ValueError:
        print(" Validación de ID vacío funciona")
def test_rf01_registrar_evaluaciones():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial 1", 15.0, 50.0),
        Evaluation("Parcial 2", 16.0, 50.0)
    ]
    result = calculator.register_evaluations(student, evaluations)
    assert result['success'] == True
    assert result['evaluations_added'] == 2
    assert student.get_evaluation_count() == 2
    print(" RF01: Evaluaciones registradas correctamente")
def test_rf02_registrar_asistencia():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    result = calculator.register_attendance(student, True)
    assert result['success'] == True
    assert student.has_minimum_attendance == True
    print(" RF02: Asistencia cumplida registrada")
    result = calculator.register_attendance(student, False)
    assert result['success'] == True
    assert student.has_minimum_attendance == False
    print(" RF02: Asistencia no cumplida registrada")
def test_rf03_politica_puntos_extra():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    result = calculator.register_extra_points_policy(True, ["T001", "T002"])
    assert result['success'] == True
    assert result['teachers_agree'] == True
    print(" RF03: Política aprobada configurada")
    result = calculator.register_extra_points_policy(False)
    assert result['success'] == True
    assert result['teachers_agree'] == False
    print(" RF03: Política rechazada configurada")
def test_rf04_calcular_nota_final():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial 1", 15.0, 30.0),
        Evaluation("Parcial 2", 16.0, 30.0),
        Evaluation("Labs", 18.0, 20.0),
        Evaluation("Proyecto", 17.0, 20.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    calculator.register_extra_points_policy(True)
    result = calculator.calculate_final_grade(student, extra_points=0.0)
    assert result['success'] == True
    expected_base = 15.0*0.3 + 16.0*0.3 + 18.0*0.2 + 17.0*0.2
    assert abs(result['base_grade'] - expected_base) < 0.01
    assert result['final_grade'] == result['base_grade']
    print(f" RF04: Nota calculada correctamente (base: {result['base_grade']})")
def test_rf04_con_puntos_extra():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial", 15.0, 100.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    calculator.register_extra_points_policy(True)
    result = calculator.calculate_final_grade(student, extra_points=2.0)
    assert result['base_grade'] == 15.0
    assert result['extra_points_applied'] == 2.0
    assert result['final_grade'] == 17.0
    print(" RF04: Puntos extra aplicados correctamente")
def test_rf05_detalle_calculo():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial", 15.0, 100.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    detail = calculator.get_calculation_detail(student, 1.0)
    assert 'student_info' in detail
    assert 'evaluations_detail' in detail
    assert 'base_calculation' in detail
    assert 'attendance' in detail
    assert 'extra_points' in detail
    assert 'final_result' in detail
    assert 'metadata' in detail
    print(" RF05: Detalle del cálculo generado correctamente")
def test_rnf01_maximo_evaluaciones():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation(f"Eval {i+1}", 15.0, 10.0) for i in range(10)
    ]
    calculator.register_evaluations(student, evaluations)
    assert student.get_evaluation_count() == 10
    print(" RNF01: 10 evaluaciones permitidas")
    try:
        student.add_evaluation(Evaluation("Eval 11", 15.0, 10.0))
        assert False, "Debería lanzar ValueError"
    except ValueError as e:
        assert "máximo de 10" in str(e).lower()
        print(" RNF01: Límite de 10 evaluaciones respetado")
def test_rnf03_determinismo():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    results = []
    for i in range(2):
        student = Student(f"20211000{i}", "Test Student")
        evaluations = [
            Evaluation("Parcial 1", 15.0, 40.0),
            Evaluation("Parcial 2", 16.0, 60.0)
        ]
        calculator.register_evaluations(student, evaluations)
        calculator.register_attendance(student, True)
        result = calculator.calculate_final_grade(student, 1.0)
        results.append(result['final_grade'])
    assert results[0] == results[1]
    print(f" RNF03: Cálculo determinista (ambas notas: {results[0]})")
def test_rnf04_tiempo_calculo():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation(f"Eval {i+1}", 15.0, 10.0) for i in range(10)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    result = calculator.calculate_final_grade(student)
    assert result['calculation_time_ms'] < 300
    print(f" RNF04: Tiempo de cálculo: {result['calculation_time_ms']} ms (< 300ms)")
def test_caso_sin_asistencia():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial", 18.0, 100.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, False)
    calculator.register_extra_points_policy(True)
    result = calculator.calculate_final_grade(student, extra_points=2.0)
    assert result['extra_points_applied'] == 0.0
    assert result['passes_course'] == False
    print(" Caso sin asistencia: Puntos extra no aplicados, no aprueba")
def test_validacion_pesos():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial 1", 15.0, 40.0),
        Evaluation("Parcial 2", 16.0, 40.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    try:
        result = calculator.calculate_final_grade(student)
        assert False, "Debería lanzar InvalidWeightError"
    except Exception as e:
        assert "100" in str(e)
        print(" Validación de pesos: Error detectado correctamente")
def test_nota_maxima_20():
    
    teacher = Teacher("T001", "Dr. Test")
    calculator = GradeCalculator(teacher)
    student = Student("202110001", "Test Student")
    evaluations = [
        Evaluation("Parcial", 19.0, 100.0)
    ]
    calculator.register_evaluations(student, evaluations)
    calculator.register_attendance(student, True)
    calculator.register_extra_points_policy(True)
    result = calculator.calculate_final_grade(student, extra_points=5.0)
    assert result['final_grade'] == 20.0
    assert result['grade_capped'] == True
    print(" Nota máxima: Limitada correctamente a 20")
def main():
    
    print("\n" + "=" * 70)
    print(" " * 15 + "CS-GRADECALCULATOR - PRUEBAS")
    print(" " * 10 + "Suite de Pruebas Automatizadas")
    print("=" * 70)
    runner = TestRunner()
    runner.run_test("Creación de modelos básicos", test_crear_modelos)
    runner.run_test("Validaciones básicas", test_validaciones_basicas)
    runner.run_test("RF01: Registrar evaluaciones", test_rf01_registrar_evaluaciones)
    runner.run_test("RF02: Registrar asistencia", test_rf02_registrar_asistencia)
    runner.run_test("RF03: Política de puntos extra", test_rf03_politica_puntos_extra)
    runner.run_test("RF04: Calcular nota final", test_rf04_calcular_nota_final)
    runner.run_test("RF04: Calcular con puntos extra", test_rf04_con_puntos_extra)
    runner.run_test("RF05: Detalle del cálculo", test_rf05_detalle_calculo)
    runner.run_test("RNF01: Máximo 10 evaluaciones", test_rnf01_maximo_evaluaciones)
    runner.run_test("RNF03: Cálculo determinista", test_rnf03_determinismo)
    runner.run_test("RNF04: Tiempo de cálculo < 300ms", test_rnf04_tiempo_calculo)
    runner.run_test("Caso: Sin asistencia mínima", test_caso_sin_asistencia)
    runner.run_test("Validación: Pesos suman 100%", test_validacion_pesos)
    runner.run_test("Validación: Nota máxima 20", test_nota_maxima_20)
    runner.print_summary()
    return runner.tests_failed == 0
if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
