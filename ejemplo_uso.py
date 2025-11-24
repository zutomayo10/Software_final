from models import Student, Teacher, Evaluation
from services import GradeCalculator
from utils.exceptions import GradeCalculationError
def ejemplo_uso_basico():
    
    print("=" * 70)
    print("CS-GRADECALCULATOR")
    print("=" * 70)
    print("\n1. Creando docente...")
    docente = Teacher("T001", "Dr. Carlos Ruiz")
    calculadora = GradeCalculator(docente)
    print(f"    Docente: {docente.name}")
    print("\n2. Creando estudiante...")
    estudiante = Student("202110123", "Ana Torres")
    print(f"    Estudiante: {estudiante.name}")
    print("\n3. Registrando evaluaciones...")
    evaluaciones = [
        Evaluation("Examen Parcial 1", 14.5, 25.0),
        Evaluation("Examen Parcial 2", 15.0, 25.0),
        Evaluation("Laboratorios", 17.5, 30.0),
        Evaluation("Proyecto Final", 16.0, 20.0)
    ]
    resultado = calculadora.register_evaluations(estudiante, evaluaciones)
    print(f"    Evaluaciones registradas: {resultado['evaluations_added']}")
    print("\n4. Registrando asistencia...")
    resultado = calculadora.register_attendance(estudiante, True)
    print(f"    {resultado['message']}")
    print("\n5. Configurando política de puntos extra...")
    resultado = calculadora.register_extra_points_policy(
        teachers_agree=True,
        teachers_list=["T001", "T002", "T003"]
    )
    print(f"    {resultado['message']}")
    print("\n6. Calculando nota final...")
    resultado = calculadora.calculate_final_grade(estudiante, extra_points=1.0)
    print(f"\n   RESULTADO:")
    print(f"   - Nota base: {resultado['base_grade']}")
    print(f"   - Puntos extra: +{resultado['extra_points_applied']}")
    print(f"   - NOTA FINAL: {resultado['final_grade']}")
    print(f"   - Estado: {' APROBADO' if resultado['passes_course'] else ' DESAPROBADO'}")
    print(f"   - Tiempo: {resultado['calculation_time_ms']} ms")
    print("\n7. Obteniendo detalle del cálculo...")
    detalle = calculadora.get_calculation_detail(estudiante, extra_points=1.0)
    print(f"    Detalle generado")
    print(f"   - Evaluaciones: {len(detalle['evaluations_detail'])}")
    print(f"   - Cumple asistencia: {detalle['attendance']['meets_requirement']}")
    print(f"   - Docentes aprueban puntos extra: {detalle['extra_points']['teachers_agree']}")
    print("\n" + "=" * 70)
    print(" EJEMPLO COMPLETADO EXITOSAMENTE")
    print("=" * 70)
def ejemplo_sin_asistencia():
    
    print("\n" + "=" * 70)
    print("EJEMPLO: ESTUDIANTE SIN ASISTENCIA MÍNIMA")
    print("=" * 70)
    docente = Teacher("T002", "Dra. María López")
    calculadora = GradeCalculator(docente)
    estudiante = Student("202110456", "Pedro Sánchez")
    evaluaciones = [
        Evaluation("Parcial 1", 16.0, 40.0),
        Evaluation("Parcial 2", 15.5, 40.0),
        Evaluation("Trabajos", 18.0, 20.0)
    ]
    calculadora.register_evaluations(estudiante, evaluaciones)
    calculadora.register_attendance(estudiante, False)
    calculadora.register_extra_points_policy(True)
    resultado = calculadora.calculate_final_grade(estudiante, extra_points=1.5)
    print(f"\nEstudiante: {estudiante.name}")
    print(f"Nota base: {resultado['base_grade']}")
    print(f"Asistencia: {' Cumple' if resultado['has_minimum_attendance'] else ' NO cumple'}")
    print(f"Puntos extra aplicados: {resultado['extra_points_applied']} (solicitados: 1.5)")
    print(f"Nota final: {resultado['final_grade']}")
    print(f"Estado: {' APROBADO' if resultado['passes_course'] else ' DESAPROBADO'}")
    print("\nNOTA: Sin asistencia mínima, no se aprueban puntos extra y no se aprueba el curso.")
    print("=" * 70)
def ejemplo_manejo_errores():
    
    print("\n" + "=" * 70)
    print("EJEMPLO: MANEJO DE ERRORES")
    print("=" * 70)
    docente = Teacher("T003", "Dr. Luis Vargas")
    calculadora = GradeCalculator(docente)
    estudiante = Student("202110789", "Laura Ramírez")
    print("\n1. Intentando calcular nota sin evaluaciones...")
    try:
        resultado = calculadora.calculate_final_grade(estudiante)
        print("    No debería llegar aquí")
    except GradeCalculationError as e:
        print(f"    Error capturado correctamente: {e}")
    print("\n2. Intentando agregar evaluaciones con pesos que no suman 100%...")
    try:
        evaluaciones_invalidas = [
            Evaluation("Parcial", 15.0, 40.0),
            Evaluation("Labs", 18.0, 30.0)
        ]
        calculadora.register_evaluations(estudiante, evaluaciones_invalidas)
        calculadora.register_attendance(estudiante, True)
        resultado = calculadora.calculate_final_grade(estudiante)
        print("    No debería llegar aquí")
    except Exception as e:
        print(f"    Error capturado correctamente: {e}")
    print("\n3. Intentando agregar más de 10 evaluaciones...")
    try:
        estudiante2 = Student("202110999", "Test Student")
        evaluaciones = [
            Evaluation(f"Eval {i}", 15.0, 100/11) for i in range(11)
        ]
        resultado = calculadora.register_evaluations(estudiante2, evaluaciones)
        if not resultado['success']:
            print(f"    Límite respetado: {resultado['errors']}")
    except Exception as e:
        print(f"    Error capturado: {e}")
    print("\n" + "=" * 70)
    print(" MANEJO DE ERRORES VERIFICADO")
    print("=" * 70)
if __name__ == "__main__":
    ejemplo_uso_basico()
    ejemplo_sin_asistencia()
    ejemplo_manejo_errores()
    print("\n" + "=" * 70)
    print("TODOS LOS EJEMPLOS COMPLETADOS")
    print("=" * 70)
