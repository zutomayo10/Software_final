class Teacher:
    
    def __init__(self, teacher_id: str, name: str):
        
        if not teacher_id or not isinstance(teacher_id, str):
            raise ValueError("El ID del docente debe ser un string no vacío")
        if not name or not isinstance(name, str):
            raise ValueError("El nombre del docente debe ser un string no vacío")
            
        self._teacher_id = teacher_id.strip()
        self._name = name.strip()
        
    @property
    def teacher_id(self) -> str:
        
        return self._teacher_id
    
    @property
    def name(self) -> str:
        
        return self._name
    
    def __str__(self) -> str:
        return f"Teacher(ID: {self._teacher_id}, Name: {self._name})"
    
    def __repr__(self) -> str:
        return self.__str__()
