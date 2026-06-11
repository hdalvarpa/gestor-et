-- 1. Crear Tabla Roles
CREATE TABLE roles (
    id_rol SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Crear Tabla Permisos
CREATE TABLE permisos (
    id_permiso SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(200)
);

-- 3. Crear Tabla Intermedia Roles_Permisos
CREATE TABLE roles_permisos (
    id_rol INTEGER REFERENCES roles(id_rol) ON DELETE CASCADE,
    id_permiso INTEGER REFERENCES permisos(id_permiso) ON DELETE CASCADE,
    PRIMARY KEY (id_rol, id_permiso)
);

-- 4. Insertar Permisos del Sistema
INSERT INTO permisos (nombre, descripcion) VALUES
('GESTIONAR_SEGURIDAD', 'Crear, editar usuarios y gestionar roles/permisos.'),
('ASIGNAR_ENTIDADES', 'Asignar entidades técnicas a los usuarios del sistema.'),
('CREAR_ENTIDADES', 'Crear nuevas entidades técnicas (RUC, Empresa).'),
('VER_ENTIDADES', 'Ver la lista de entidades técnicas asignadas y acceder a ellas.'),
('GESTIONAR_INGENIEROS', 'Listar, crear y editar el padrón global de ingenieros.'),
('ASIGNAR_INGENIEROS', 'Vincular ingenieros del padrón a las entidades técnicas asignadas.'),
('GESTIONAR_REGISTROS', 'Crear y administrar códigos de registro anuales.'),
('ASIGNAR_REGISTROS', 'Asignar códigos de registro a las entidades técnicas asignadas.');

-- 5. Insertar Roles por Defecto
INSERT INTO roles (nombre) VALUES
('SuperAdmin'),
('Usuario Básico');

-- 6. Asignar todos los permisos al SuperAdmin
INSERT INTO roles_permisos (id_rol, id_permiso)
SELECT (SELECT id_rol FROM roles WHERE nombre = 'SuperAdmin'), id_permiso 
FROM permisos;

-- 7. Asignar permisos limitados al Usuario Básico
INSERT INTO roles_permisos (id_rol, id_permiso)
SELECT (SELECT id_rol FROM roles WHERE nombre = 'Usuario Básico'), id_permiso 
FROM permisos 
WHERE nombre IN ('VER_ENTIDADES', 'GESTIONAR_INGENIEROS', 'ASIGNAR_INGENIEROS', 'GESTIONAR_REGISTROS', 'ASIGNAR_REGISTROS');

-- 8. Actualizar la tabla Usuarios
-- Agregamos la columna permitiendo nulos momentáneamente
ALTER TABLE usuarios ADD COLUMN id_rol INTEGER REFERENCES roles(id_rol);

-- Migramos los datos basándonos en la columna vieja
UPDATE usuarios 
SET id_rol = (SELECT id_rol FROM roles WHERE nombre = 'SuperAdmin') 
WHERE rol = 'ADMIN';

UPDATE usuarios 
SET id_rol = (SELECT id_rol FROM roles WHERE nombre = 'Usuario Básico') 
WHERE rol = 'USER';

-- Aseguramos que nadie se quede sin rol (por si hay basura en la DB)
UPDATE usuarios 
SET id_rol = (SELECT id_rol FROM roles WHERE nombre = 'Usuario Básico') 
WHERE id_rol IS NULL;

-- Hacemos la nueva columna requerida
ALTER TABLE usuarios ALTER COLUMN id_rol SET NOT NULL;

-- Eliminamos la columna vieja de texto
ALTER TABLE usuarios DROP COLUMN rol;
