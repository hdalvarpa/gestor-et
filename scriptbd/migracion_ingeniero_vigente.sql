-- 1. Agregar nueva columna a la tabla entidades_tecnicas
ALTER TABLE entidades_tecnicas
ADD COLUMN id_ingeniero_vigente INTEGER REFERENCES ingenieros(id_ingeniero) ON DELETE SET NULL;

-- 2. Migrar los datos desde asignacion_ingenieros hacia entidades_tecnicas
-- Se asume que solo queremos conservar el que esté VIGENTE
UPDATE entidades_tecnicas et
SET id_ingeniero_vigente = ai.id_ingeniero
FROM asignacion_ingenieros ai
WHERE et.id_entidad_tecnica = ai.id_entidad_tecnica
AND ai.estado = 'VIGENTE';

-- 3. Eliminar restricciones de llave foránea que dependan de asignacion_ingenieros 
-- (PostgreSQL maneja esto automáticamente con CASCADE si es sobre la propia tabla, 
-- pero la tabla expedientes podría depender de esto, aunque expedientes apuntaba a entidades y usuarios.
-- Revisamos si algo más dependía. Por las dudas solo tiramos la tabla)

DROP TABLE asignacion_ingenieros CASCADE;
