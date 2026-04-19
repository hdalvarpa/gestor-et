class Predio:
    def __init__(self, direccion: str, departamento: str, provincia: str, 
                 distrito: str, manzana: str, lote: str, sublote: str, 
                 centro_poblado: str, referencia: str):
        self.direccion = direccion
        self.departamento = departamento
        self.provincia = provincia
        self.distrito = distrito
        self.manzana = manzana
        self.lote = lote
        self.sublote = sublote
        self.centro_poblado = centro_poblado
        self.referencia = referencia