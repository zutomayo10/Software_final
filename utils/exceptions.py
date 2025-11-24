class GradeCalculationError(Exception):
    
    pass

class InvalidEvaluationError(GradeCalculationError):
    
    pass

class MaxEvaluationsExceededError(GradeCalculationError):
    
    pass

class InvalidWeightError(GradeCalculationError):
    
    pass

class AttendanceRequirementError(GradeCalculationError):
    
    pass

class CalculationTimeoutError(GradeCalculationError):
    
    pass

class InvalidStudentDataError(GradeCalculationError):
    
    pass
