class Conyuge:
    def __init__(self, 
                 nombres: str = "", 
                 ap_paterno: str = "", 
                 ap_materno: str = "", 
                 sit_laboral: str = "", 
                 dni: str = "", 
                 nacimiento: str = "", 
                 estado_civil: str = "", 
                 condicion_eco: str = "", 
                 grado_instruccion: str = "", 
                 ocupacion: str = "", 
                 discapacidad: str = "", 
                 ingreso_mensual: str = ""):
        self.nombres = nombres
        self.ap_paterno = ap_paterno
        self.ap_materno = ap_materno
        self.sit_laboral = sit_laboral
        self.dni = dni
        self.nacimiento = nacimiento
        self.estado_civil = estado_civil
        self.condicion_eco = condicion_eco
        self.grado_instruccion = grado_instruccion
        self.ocupacion = ocupacion
        self.discapacidad = discapacidad
        self.ingreso_mensual = ingreso_mensual
