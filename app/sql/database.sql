-- ==============================================================================
-- 1. LIMPIEZA Y FUNCIONES BASE
-- ==============================================================================
DROP TABLE IF EXISTS auditoria_accesos CASCADE;
DROP TABLE IF EXISTS inscripciones CASCADE;
DROP TABLE IF EXISTS horarios CASCADE;
DROP TABLE IF EXISTS entrenadores CASCADE;
DROP TABLE IF EXISTS deportes CASCADE;
DROP TABLE IF EXISTS permisos_rol CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS modulos CASCADE;
DROP TABLE IF EXISTS roles CASCADE;

-- Actualización automática del campo updated_
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ==============================================================================
-- 2. DEFINICIÓN DE TABLAS
-- ==============================================================================

-- Tabla: roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: modulos
CREATE TABLE modulos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES roles(id),
    tipo_documento_id INTEGER NOT NULL,
    numero_documento VARCHAR(50) NOT NULL,
    facultad_id INTEGER NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: permisos_rol
CREATE TABLE permisos_rol (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    modulo_id INTEGER REFERENCES modulos(id) ON DELETE CASCADE,
    acceso BOOLEAN DEFAULT TRUE,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rol_id, modulo_id)
);

-- Tabla: deportes
CREATE TABLE deportes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: entrenadores
CREATE TABLE entrenadores (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    deporte_id INTEGER REFERENCES deportes(id),
    biografia TEXT,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);          

-- Tabla: horarios
CREATE TABLE horarios (
    id SERIAL PRIMARY KEY,
    deporte_id INTEGER REFERENCES deportes(id),
    entrenador_id INTEGER REFERENCES entrenadores(id),
    dia_semana VARCHAR(20),
    hora_inicio TIME,
    hora_fin TIME,
    lugar VARCHAR(150),
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: inscripciones
CREATE TABLE inscripciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    horario_id INTEGER REFERENCES horarios(id),
    programa_id INTEGER NOT NULL,
    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado BOOLEAN DEFAULT TRUE,
    created_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_ TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: auditoria_accesos
CREATE TABLE auditoria_accesos (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER REFERENCES usuarios(id),
    tabla_afectada VARCHAR(100),
    accion TEXT,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==============================================================================
-- 3. ACTIVACIÓN DE TRIGGERS
-- ==============================================================================

CREATE TRIGGER trg_roles_update BEFORE UPDATE ON roles FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_modulos_update BEFORE UPDATE ON modulos FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_usuarios_update BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_permisos_update BEFORE UPDATE ON permisos_rol FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_deportes_update BEFORE UPDATE ON deportes FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();
CREATE TRIGGER trg_horarios_update BEFORE UPDATE ON horarios FOR EACH ROW EXECUTE FUNCTION update_timestamp_column();

-- ==============================================================================
-- 4. INSERCIÓN DE DATOS INICIALES
-- ==============================================================================

-- Roles base
INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso total'),
('Estudiante', 'Consulta e inscripciones'),
('Entrenador', 'Gestiona sus grupos'),
('Planeación', 'Audita recursos');

-- Módulos
INSERT INTO modulos (nombre, descripcion) VALUES
('Panel Control', 'Dashboard general'),
('Deportes', 'CRUD de disciplinas'),
('Inscripciones', 'Registro de estudiantes'),
('Horarios', 'Agenda deportiva');

-- Usuario Admin de prueba
INSERT INTO usuarios (nombre, apellido, tipo_documento_id, numero_documento, facultad_id, usuario, contrasena, rol_id) 
VALUES ('Juan', 'Torres', 1, '123456', 1, 'admin', 'admin123', 1);

-- Permisos 
INSERT INTO permisos_rol (rol_id, modulo_id) VALUES (1,1), (1,2), (1,3), (1,4);