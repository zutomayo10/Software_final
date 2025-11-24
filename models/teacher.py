"""
Clase Teacher: Representa un docente en el sistema.
"""


class Teacher:
    """
    Representa un docente del UTEC.
    
    Attributes:
        teacher_id (str): Identificador único del docente
        name (str): Nombre completo del docente
    """
    
    def __init__(self, teacher_id: str, name: str):
        """
        Inicializa un docente.
        
        Args:
            teacher_id: Identificador único del docente
            name: Nombre completo del docente
            
        Raises:
            ValueError: Si el ID o nombre están vacíos
        """
        if not teacher_id or not isinstance(teacher_id, str):
            raise ValueError("El ID del docente debe ser un string no vacío")
        if not name or not isinstance(name, str):
            raise ValueError("El nombre del docente debe ser un string no vacío")
            
        self._teacher_id = teacher_id.strip()
        self._name = name.strip()
        
    @property
    def teacher_id(self) -> str:
        """Obtiene el ID del docente."""
        return self._teacher_id
    
    @property
    def name(self) -> str:
        """Obtiene el nombre del docente."""
        return self._name
    
    def __str__(self) -> str:
        return f"Teacher(ID: {self._teacher_id}, Name: {self._name})"
    
    def __repr__(self) -> str:
        return self.__str__()
