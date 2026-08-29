-- 1. Insertar Biblioteca
INSERT INTO biblioteca (nombre, descripcion, direccion, horario, telefono, correo, sitio_web)
VALUES ('Biblioteca Central UVG', 'Biblioteca principal campus central', 'Vista Hermosa III, Zona 15', 'Lun-Vie 07:00-20:00', '+502 2368-8000', 'biblioteca@uvg.edu.gt', 'https://biblioteca.uvg.edu.gt');

-- 2. Insertar Editoriales
INSERT INTO editorial (id, nombre, pais) VALUES 
(1, 'Pearson Educación', 'España'),
(2, 'McGraw-Hill', 'Estados Unidos'),
(3, 'Addison-Wesley', 'Estados Unidos'),
(4, 'Alfaomega', 'México');

-- 3. Insertar Libros
INSERT INTO libro (id, editorial_id, isbn, titulo, subtitulo, descripcion, numero_edicion, anio_publicacion, idioma, numero_paginas) VALUES
(1, 1, '978-0132126953', 'Redes de Computadoras', 'Un enfoque ascendente', 'Libro fundamental de redes y protocolos TCP/IP', 5, 2013, 'Español', 800),
(2, 2, '978-6071506153', 'Organización de Computadoras', 'Diseño de sistemas', 'Conceptos de arquitectura de computadoras', 4, 2011, 'Español', 750),
(3, 3, '978-0132856201', 'Redes de Computadoras: Un Enfoque Descendente', 'Internet y Protocolos', 'Enfoque práctico centrado en la capa de aplicación hacia abajo', 6, 2017, 'Español', 860),
(4, 1, '978-0131392052', 'Comunicaciones y Redes de Computadores', 'Fundamentos de Redes', 'Principios de transmisión de datos y protocolos de red', 7, 2004, 'Español', 896),
(5, 4, '978-6077072102', 'Sistemas de Bases de Datos', 'Diseño e Implementación', 'Conceptos de modelos relacionales, SQL y transacciones', 5, 2018, 'Español', 950);

-- 4. Insertar Autores
INSERT INTO autor (id, nombres, apellidos) VALUES
(1, 'Andrew S.', 'Tanenbaum'),
(2, 'David J.', 'Wetherall'),
(3, 'David A.', 'Patterson'),
(4, 'James F.', 'Kurose'),
(5, 'Keith W.', 'Ross'),
(6, 'William', 'Stallings'),
(7, 'Carlos', 'Coronel');

-- 5. Relacionar Libros y Autores (orden_autoria para APA 7)
INSERT INTO libro_autor (libro_id, autor_id, orden_autoria) VALUES
(1, 1, 1), -- Tanenbaum (Primer autor)
(1, 2, 2), -- Wetherall (Segundo autor)
(2, 3, 1), -- Patterson
(3, 4, 1), -- Kurose
(3, 5, 2), -- Ross
(4, 6, 1), -- Stallings
(5, 7, 1); -- Coronel

-- 6. Temas
INSERT INTO tema (id, nombre, descripcion) VALUES
(1, 'Redes', 'Redes de computadoras, protocolos y telecomunicaciones'),
(2, 'Arquitectura de Computadoras', 'Hardware y diseño de procesadores'),
(3, 'Bases de Datos', 'Sistemas de almacenamiento, modelado relacional y SQL');

-- 7. Relacionar Libros y Temas
INSERT INTO libro_tema (libro_id, tema_id) VALUES
(1, 1), -- Redes de Computadoras -> Redes
(2, 2), -- Organización -> Arquitectura
(3, 1), -- Kurose -> Redes
(4, 1), -- Stallings -> Redes
(5, 3); -- Coronel -> Bases de Datos

-- 8. Ejemplares
INSERT INTO ejemplar (libro_id, codigo_inventario, ubicacion, estado) VALUES
(1, 'RED-001', 'Estante R1-A', 'DISPONIBLE'),
(1, 'RED-002', 'Estante R1-A', 'PRESTADO'),
(2, 'ARQ-001', 'Estante A3-B', 'DISPONIBLE'),
(3, 'RED-003', 'Estante R1-B', 'DISPONIBLE'),
(4, 'RED-004', 'Estante R2-A', 'PRESTADO'),   -- Libro 4 completamente prestado (para probar alternativas)
(5, 'BD-001',  'Estante B1-A', 'DISPONIBLE');

-- 9. Usuario de prueba
INSERT INTO usuario (id, codigo, nombres, apellidos, correo, estado) VALUES
(1, 'UVG-2026-01', 'Estudiante', 'Prueba', 'estudiante@uvg.edu.gt', 'ACTIVO');