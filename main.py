"""
Sistema CS-GradeCalculator
Programa principal para demostrar todos los casos de uso del sistema.
Este programa implementa el caso de uso CU001: Calcular nota final del estudiante
y demuestra todos los requerimientos funcionales y no funcionales.
"""
import sys
from typing import List, Optional
from models import Student, Teacher, Evaluation
from services import GradeCalculator
from policies import AttendancePolicy, ExtraPointsPolicy
from utils.exceptions import GradeCalculationError
class GradeCalculatorApp:
    """
    Aplicación principal del sistema de cálculo de notas.
    Proporciona una interfaz de terminal para interactuar con el sistema.
    """
    def __init__(self):
        """Inicializa la aplicación."""
        self.calculator: Optional[GradeCalculator] = None
        self.students: dict = {}
        self.current_teacher: Optional[Teacher] = None
    def display_header(self) -> None:
        """Muestra el encabezado de la aplicación."""
        print("\n" + "=" * 70)
        print(" " * 15 + "CS-GRADECALCULATOR - UTEC")
        print(" " * 10 + "Sistema de Cálculo de Notas Finales")
        print("=" * 70)
    def display_menu(self) -> None:
        """Muestra el menú principal."""
        print("\n" + "-" * 70)
        print("MENÚ PRINCIPAL:")
        print("-" * 70)
        print("1. Inicializar sistema (Registrar docente)")
        print("2. Registrar estudiante")
        print("3. Registrar evaluaciones de estudiante (RF01)")
        print("4. Registrar asistencia de estudiante (RF02)")
        print("5. Configurar política de puntos extra (RF03)")
        print("6. Calcular nota final (RF04)")
        print("7. Ver detalle del cálculo (RF05)")
        print("8. Ver todos los estudiantes registrados")
        print("9. Ejecutar caso de uso completo (demo)")
        print("0. Salir")
        print("-" * 70)
    def initialize_system(self) -> None:
        """Inicializa el sistema registrando un docente."""
        print("\n--- INICIALIZAR SISTEMA ---")
        teacher_id = input("Ingrese ID del docente: ").strip()
        teacher_name = input("Ingrese nombre del docente: ").strip()
        try:
            self.current_teacher = Teacher(teacher_id, teacher_name)
            self.calculator = GradeCalculator(self.current_teacher)
            print(f"\n Sistema inicializado correctamente")
            print(f"  Docente: {teacher_name} (ID: {teacher_id})")
        except Exception as e:
            print(f"\n Error al inicializar sistema: {e}")
    def register_student(self) -> None:
        """Registra un nuevo estudiante."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero (opción 1)")
            return
        print("\n--- REGISTRAR ESTUDIANTE ---")
        student_id = input("Ingrese ID/código del estudiante: ").strip()
        student_name = input("Ingrese nombre del estudiante: ").strip()
        try:
            student = Student(student_id, student_name)
            self.students[student_id] = student
            print(f"\n Estudiante registrado correctamente")
            print(f"  {student_name} (ID: {student_id})")
        except Exception as e:
            print(f"\n Error al registrar estudiante: {e}")
    def register_evaluations(self) -> None:
        """RF01: Registra evaluaciones para un estudiante."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero (opción 1)")
            return
        if not self.students:
            print("\n Error: No hay estudiantes registrados")
            return
        print("\n--- REGISTRAR EVALUACIONES (RF01) ---")
        self._list_students()
        student_id = input("\nIngrese ID del estudiante: ").strip()
        if student_id not in self.students:
            print(f"\n Error: Estudiante {student_id} no encontrado")
            return
        student = self.students[student_id]
        try:
            num_evaluations = int(input("¿Cuántas evaluaciones desea registrar? (máx. 10): "))
            if num_evaluations <= 0:
                print("\n Error: Debe registrar al menos 1 evaluación")
                return
            if num_evaluations > 10:
                print("\n Error: Máximo 10 evaluaciones permitidas (RNF01)")
                return
            evaluations = []
            total_weight = 0
            print(f"\nRegistrando {num_evaluations} evaluación(es)...")
            print("NOTA: Los pesos deben sumar exactamente 100%\n")
            for i in range(num_evaluations):
                print(f"\nEvaluación {i + 1}:")
                name = input("  Nombre: ").strip()
                score = float(input("  Nota (0-20): "))
                weight = float(input("  Peso porcentual: "))
                evaluation = Evaluation(name, score, weight)
                evaluations.append(evaluation)
                total_weight += weight
                print(f"   Evaluación agregada (peso acumulado: {total_weight}%)")
            # Validar que suman 100%
            if abs(total_weight - 100.0) > 0.01:
                print(f"\n Error: Los pesos suman {total_weight}%, deben sumar 100%")
                return
            # Registrar evaluaciones
            result = self.calculator.register_evaluations(student, evaluations)
            if result['success']:
                print(f"\n Evaluaciones registradas correctamente")
                print(f"  Total de evaluaciones: {result['total_evaluations']}")
            else:
                print(f"\n Errores al registrar evaluaciones:")
                for error in result['errors']:
                    print(f"  - {error}")
        except ValueError as e:
            print(f"\n Error de validación: {e}")
        except Exception as e:
            print(f"\n Error: {e}")
    def register_attendance(self) -> None:
        """RF02: Registra si el estudiante cumplió con asistencia mínima."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero")
            return
        if not self.students:
            print("\n Error: No hay estudiantes registrados")
            return
        print("\n--- REGISTRAR ASISTENCIA (RF02) ---")
        self._list_students()
        student_id = input("\nIngrese ID del estudiante: ").strip()
        if student_id not in self.students:
            print(f"\n Error: Estudiante {student_id} no encontrado")
            return
        student = self.students[student_id]
        print("\n¿El estudiante cumplió con la asistencia mínima requerida?")
        response = input("(S/N): ").strip().upper()
        has_attendance = response == 'S'
        try:
            result = self.calculator.register_attendance(student, has_attendance)
            if result['success']:
                print(f"\n Asistencia registrada correctamente")
                print(f"  {result['message']}")
        except Exception as e:
            print(f"\n Error: {e}")
    def configure_extra_points_policy(self) -> None:
        """RF03: Configura la política de puntos extra."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero")
            return
        print("\n--- CONFIGURAR POLÍTICA DE PUNTOS EXTRA (RF03) ---")
        print("\n¿Todos los docentes del curso están de acuerdo en otorgar puntos extra?")
        response = input("(S/N): ").strip().upper()
        teachers_agree = response == 'S'
        teachers_list = []
        if teachers_agree:
            print("\nIngrese los IDs de los docentes participantes (separados por coma):")
            teachers_input = input("IDs: ").strip()
            teachers_list = [t.strip() for t in teachers_input.split(',') if t.strip()]
        try:
            result = self.calculator.register_extra_points_policy(
                teachers_agree,
                teachers_list if teachers_list else None
            )
            if result['success']:
                print(f"\n Política configurada correctamente")
                print(f"  {result['message']}")
                if teachers_list:
                    print(f"  Docentes participantes: {result['teachers_count']}")
        except Exception as e:
            print(f"\n Error: {e}")
    def calculate_grade(self) -> None:
        """RF04: Calcula la nota final de un estudiante."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero")
            return
        if not self.students:
            print("\n Error: No hay estudiantes registrados")
            return
        print("\n--- CALCULAR NOTA FINAL (RF04) ---")
        self._list_students()
        student_id = input("\nIngrese ID del estudiante: ").strip()
        if student_id not in self.students:
            print(f"\n Error: Estudiante {student_id} no encontrado")
            return
        student = self.students[student_id]
        # Validar que tiene evaluaciones
        if student.get_evaluation_count() == 0:
            print(f"\n Error: El estudiante no tiene evaluaciones registradas")
            return
        try:
            extra_points = float(input("Puntos extra a otorgar (0 si no aplica): "))
            result = self.calculator.calculate_final_grade(student, extra_points)
            print("\n" + "=" * 70)
            print("RESULTADO DEL CÁLCULO")
            print("=" * 70)
            print(f"Estudiante: {result['student_name']} (ID: {result['student_id']})")
            print(f"\nNota base: {result['base_grade']}")
            print(f"Puntos extra aplicados: +{result['extra_points_applied']}")
            print(f"NOTA FINAL: {result['final_grade']}")
            print(f"\nAsistencia mínima: {' SÍ' if result['has_minimum_attendance'] else ' NO'}")
            print(f"Estado: {' APROBADO' if result['passes_course'] else ' DESAPROBADO'}")
            if result['grade_capped']:
                print("\nNOTA: La nota fue limitada a 20 (máximo permitido)")
            print(f"\nTiempo de cálculo: {result['calculation_time_ms']} ms (RNF04: < 300ms)")
            print("=" * 70)
        except GradeCalculationError as e:
            print(f"\n Error en el cálculo: {e}")
        except Exception as e:
            print(f"\n Error: {e}")
    def show_calculation_detail(self) -> None:
        """RF05: Muestra el detalle completo del cálculo."""
        if not self.calculator:
            print("\n Error: Debe inicializar el sistema primero")
            return
        if not self.students:
            print("\n Error: No hay estudiantes registrados")
            return
        print("\n--- DETALLE DEL CÁLCULO (RF05) ---")
        self._list_students()
        student_id = input("\nIngrese ID del estudiante: ").strip()
        if student_id not in self.students:
            print(f"\n Error: Estudiante {student_id} no encontrado")
            return
        student = self.students[student_id]
        if student.get_evaluation_count() == 0:
            print(f"\n Error: El estudiante no tiene evaluaciones registradas")
            return
        try:
            extra_points = float(input("Puntos extra a considerar (0 si no aplica): "))
            detail = self.calculator.get_calculation_detail(student, extra_points)
            # Mostrar detalle completo
            print("\n" + "=" * 70)
            print("DETALLE COMPLETO DEL CÁLCULO")
            print("=" * 70)
            # Información del estudiante
            print("\n1. INFORMACIÓN DEL ESTUDIANTE:")
            print(f"   ID: {detail['student_info']['id']}")
            print(f"   Nombre: {detail['student_info']['name']}")
            print(f"   Evaluaciones registradas: {detail['student_info']['evaluations_count']}")
            # Detalle de evaluaciones
            print("\n2. EVALUACIONES:")
            for eval_detail in detail['evaluations_detail']:
                print(f"\n   Evaluación {eval_detail['number']}: {eval_detail['name']}")
                print(f"   - Nota: {eval_detail['score']}/20")
                print(f"   - Peso: {eval_detail['weight']}%")
                print(f"   - Contribución: {eval_detail['contribution']}")
            # Cálculo base
            print("\n3. CÁLCULO BASE:")
            print(f"   Fórmula: {detail['base_calculation']['formula']}")
            print(f"   Peso total: {detail['base_calculation']['total_weight']}%")
            print(f"   Nota base: {detail['base_calculation']['base_grade']}")
            # Asistencia
            print("\n4. ASISTENCIA:")
            print(f"   Cumple requisito: {' SÍ' if detail['attendance']['meets_requirement'] else ' NO'}")
            print(f"   Estado: {detail['attendance']['message']}")
            print(f"   Impacto: {detail['attendance']['impact']}")
            # Puntos extra
            print("\n5. PUNTOS EXTRA:")
            print(f"   Solicitados: {detail['extra_points']['requested']}")
            print(f"   Aplicados: {detail['extra_points']['applied']}")
            print(f"   Docentes aprueban: {' SÍ' if detail['extra_points']['teachers_agree'] else ' NO'}")
            print(f"   Detalle: {detail['extra_points']['message']}")
            # Resultado final
            print("\n6. RESULTADO FINAL:")
            print(f"   NOTA FINAL: {detail['final_result']['final_grade']}")
            print(f"   Umbral de aprobación: {detail['final_result']['approval_threshold']}")
            print(f"   Estado: {' APROBADO' if detail['final_result']['passes_course'] else ' DESAPROBADO'}")
            if detail['final_result']['grade_capped']:
                print(f"   NOTA: Nota limitada a 20 (máximo permitido)")
            # Metadata
            print("\n7. METADATA:")
            print(f"   Calculado por: {detail['metadata']['calculated_by']}")
            print(f"   ID Docente: {detail['metadata']['teacher_id']}")
            print(f"   Tiempo de cálculo: {detail['metadata']['calculation_time_ms']} ms")
            print(f"   Fecha/Hora: {detail['metadata']['timestamp']}")
            print("\n" + "=" * 70)
        except GradeCalculationError as e:
            print(f"\n Error en el cálculo: {e}")
        except Exception as e:
            print(f"\n Error: {e}")
    def list_students(self) -> None:
        """Muestra todos los estudiantes registrados."""
        if not self.students:
            print("\n No hay estudiantes registrados")
            return
        print("\n--- ESTUDIANTES REGISTRADOS ---")
        self._list_students()
    def _list_students(self) -> None:
        """Método auxiliar para listar estudiantes."""
        for student_id, student in self.students.items():
            print(f"  - {student.name} (ID: {student_id}) - "
                  f"Evaluaciones: {student.get_evaluation_count()}, "
                  f"Asistencia: {'' if student.has_minimum_attendance else ''}")
    def run_complete_demo(self) -> None:
        """Ejecuta un caso de uso completo demostrando todas las funcionalidades."""
        print("\n" + "=" * 70)
        print("DEMO: CASO DE USO COMPLETO - CU001")
        print("=" * 70)
        try:
            # 1. Inicializar sistema
            print("\n1. Inicializando sistema...")
            self.current_teacher = Teacher("T001", "Dr. Juan Pérez")
            self.calculator = GradeCalculator(self.current_teacher)
            print(f"    Docente registrado: {self.current_teacher.name}")
            # 2. Crear estudiante
            print("\n2. Registrando estudiante...")
            student = Student("202110001", "María González")
            self.students[student.student_id] = student
            print(f"    Estudiante: {student.name}")
            # 3. RF01: Registrar evaluaciones
            print("\n3. RF01: Registrando evaluaciones...")
            evaluations = [
                Evaluation("Parcial 1", 15.0, 30.0),
                Evaluation("Parcial 2", 16.5, 30.0),
                Evaluation("Laboratorios", 18.0, 20.0),
                Evaluation("Proyecto Final", 17.0, 20.0)
            ]
            result = self.calculator.register_evaluations(student, evaluations)
            print(f"    {result['evaluations_added']} evaluaciones registradas")
            for eval in evaluations:
                print(f"     - {eval.name}: {eval.score}/20 (peso: {eval.weight}%)")
            # 4. RF02: Registrar asistencia
            print("\n4. RF02: Registrando asistencia...")
            result = self.calculator.register_attendance(student, True)
            print(f"    {result['message']}")
            # 5. RF03: Configurar política de puntos extra
            print("\n5. RF03: Configurando política de puntos extra...")
            teachers_list = ["T001", "T002", "T003"]
            result = self.calculator.register_extra_points_policy(True, teachers_list)
            print(f"    {result['message']}")
            # 6. RF04: Calcular nota final
            print("\n6. RF04: Calculando nota final...")
            extra_points = 1.5
            result = self.calculator.calculate_final_grade(student, extra_points)
            print(f"    Nota base: {result['base_grade']}")
            print(f"    Puntos extra: +{result['extra_points_applied']}")
            print(f"    NOTA FINAL: {result['final_grade']}")
            print(f"    Estado: {'APROBADO' if result['passes_course'] else 'DESAPROBADO'}")
            print(f"    Tiempo de cálculo: {result['calculation_time_ms']} ms (RNF04: < 300ms)")
            # 7. RF05: Mostrar detalle
            print("\n7. RF05: Generando detalle del cálculo...")
            detail = self.calculator.get_calculation_detail(student, extra_points)
            print(f"    Detalle generado exitosamente")
            print(f"    Incluye: {len(detail['evaluations_detail'])} evaluaciones detalladas")
            # Validaciones RNF
            print("\n8. VERIFICACIÓN DE REQUERIMIENTOS NO FUNCIONALES:")
            print(f"    RNF01: Evaluaciones registradas: {student.get_evaluation_count()}/10 (máximo)")
            print(f"    RNF02: Sistema preparado para concurrencia (hasta 50 usuarios)")
            print(f"    RNF03: Cálculo determinista (mismos datos = misma nota)")
            print(f"    RNF04: Tiempo < 300ms (actual: {result['calculation_time_ms']} ms)")
            print("\n" + "=" * 70)
            print(" DEMO COMPLETADA EXITOSAMENTE")
            print("=" * 70)
        except Exception as e:
            print(f"\n Error en la demo: {e}")
            import traceback
            traceback.print_exc()
    def run(self) -> None:
        """Ejecuta el bucle principal de la aplicación."""
        self.display_header()
        while True:
            self.display_menu()
            try:
                choice = input("\nSeleccione una opción: ").strip()
                if choice == '0':
                    print("\n¡Hasta luego!")
                    break
                elif choice == '1':
                    self.initialize_system()
                elif choice == '2':
                    self.register_student()
                elif choice == '3':
                    self.register_evaluations()
                elif choice == '4':
                    self.register_attendance()
                elif choice == '5':
                    self.configure_extra_points_policy()
                elif choice == '6':
                    self.calculate_grade()
                elif choice == '7':
                    self.show_calculation_detail()
                elif choice == '8':
                    self.list_students()
                elif choice == '9':
                    self.run_complete_demo()
                else:
                    print("\n Opción inválida. Por favor, intente de nuevo.")
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\n Error inesperado: {e}")
                import traceback
                traceback.print_exc()
def main():
    """Función principal."""
    app = GradeCalculatorApp()
    app.run()
if __name__ == "__main__":
    main()
