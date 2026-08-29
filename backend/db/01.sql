CREATE TABLE `biblioteca` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text,
  `direccion` varchar(500),
  `horario` varchar(300),
  `telefono` varchar(30),
  `correo` varchar(254),
  `sitio_web` varchar(500),
  `activa` boolean NOT NULL DEFAULT true,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `editorial` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(200) UNIQUE NOT NULL,
  `pais` varchar(100)
);

CREATE TABLE `libro` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `editorial_id` int,
  `isbn` varchar(20) UNIQUE,
  `titulo` varchar(500) NOT NULL,
  `subtitulo` varchar(500),
  `descripcion` text,
  `numero_edicion` int,
  `anio_publicacion` int NOT NULL,
  `idioma` varchar(50) NOT NULL DEFAULT 'Español',
  `numero_paginas` int,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `autor` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombres` varchar(150) NOT NULL,
  `apellidos` varchar(150) NOT NULL
);

CREATE TABLE `libro_autor` (
  `libro_id` int NOT NULL,
  `autor_id` int NOT NULL,
  `orden_autoria` int NOT NULL,
  PRIMARY KEY (`libro_id`, `autor_id`)
);

CREATE TABLE `tema` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(150) UNIQUE NOT NULL,
  `descripcion` text
);

CREATE TABLE `libro_tema` (
  `libro_id` int NOT NULL,
  `tema_id` int NOT NULL,
  PRIMARY KEY (`libro_id`, `tema_id`)
);

CREATE TABLE `ejemplar` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `libro_id` int NOT NULL,
  `codigo_inventario` varchar(100) UNIQUE NOT NULL,
  `ubicacion` varchar(200),
  `estado` ENUM ('DISPONIBLE', 'PRESTADO', 'RESERVADO', 'MANTENIMIENTO') NOT NULL DEFAULT 'DISPONIBLE',
  `fecha_adquisicion` date,
  `observaciones` text,
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `usuario` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `codigo` varchar(100) UNIQUE NOT NULL,
  `nombres` varchar(150) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `correo` varchar(254) UNIQUE NOT NULL,
  `estado` ENUM ('ACTIVO', 'SUSPENDIDO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  `created_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `reserva` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `libro_id` int NOT NULL,
  `ejemplar_id` int,
  `estado` ENUM ('PENDIENTE', 'CONFIRMADA', 'COMPLETADA', 'CANCELADA', 'EXPIRADA') NOT NULL DEFAULT 'PENDIENTE',
  `fecha_solicitud` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  `fecha_expiracion` datetime,
  `fecha_finalizacion` datetime,
  `observaciones` text,
  `updated_at` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE INDEX `libro_index_0` ON `libro` (`titulo`);

CREATE INDEX `libro_index_1` ON `libro` (`isbn`);

CREATE INDEX `libro_index_2` ON `libro` (`anio_publicacion`);

CREATE INDEX `autor_index_3` ON `autor` (`apellidos`, `nombres`);

CREATE UNIQUE INDEX `libro_autor_index_4` ON `libro_autor` (`libro_id`, `orden_autoria`);

CREATE INDEX `libro_autor_index_5` ON `libro_autor` (`autor_id`);

CREATE INDEX `libro_tema_index_6` ON `libro_tema` (`tema_id`);

CREATE INDEX `ejemplar_index_7` ON `ejemplar` (`libro_id`);

CREATE INDEX `ejemplar_index_8` ON `ejemplar` (`estado`);

CREATE INDEX `ejemplar_index_9` ON `ejemplar` (`libro_id`, `estado`);

CREATE INDEX `reserva_index_10` ON `reserva` (`usuario_id`);

CREATE INDEX `reserva_index_11` ON `reserva` (`libro_id`);

CREATE INDEX `reserva_index_12` ON `reserva` (`ejemplar_id`);

CREATE INDEX `reserva_index_13` ON `reserva` (`libro_id`, `estado`);

CREATE INDEX `reserva_index_14` ON `reserva` (`usuario_id`, `estado`);

ALTER TABLE `biblioteca` COMMENT = 'Se espera que el sistema administre una sola biblioteca.
El horario puede guardarse como un texto descriptivo.
';

ALTER TABLE `libro` COMMENT = 'Cada registro representa una edición específica de un libro.
Contiene la información necesaria para generar una referencia APA 7.
';

ALTER TABLE `libro_autor` COMMENT = 'Un libro puede tener varios autores y un autor puede escribir
varios libros. orden_autoria permite generar correctamente
las referencias APA 7.
';

ALTER TABLE `libro_tema` COMMENT = 'Los temas permiten encontrar y recomendar libros relacionados.
Ejemplos: redes, programación, bases de datos y seguridad.
';

ALTER TABLE `ejemplar` COMMENT = 'Un libro puede tener varios ejemplares físicos.
La disponibilidad se obtiene contando los ejemplares cuyo estado
sea DISPONIBLE.
';

ALTER TABLE `reserva` COMMENT = 'La reserva inicialmente se realiza sobre un libro.
Cuando exista una copia disponible, se asigna en ejemplar_id.
';

ALTER TABLE `libro` ADD FOREIGN KEY (`editorial_id`) REFERENCES `editorial` (`id`);

ALTER TABLE `libro_autor` ADD FOREIGN KEY (`libro_id`) REFERENCES `libro` (`id`);

ALTER TABLE `libro_autor` ADD FOREIGN KEY (`autor_id`) REFERENCES `autor` (`id`);

ALTER TABLE `libro_tema` ADD FOREIGN KEY (`libro_id`) REFERENCES `libro` (`id`);

ALTER TABLE `libro_tema` ADD FOREIGN KEY (`tema_id`) REFERENCES `tema` (`id`);

ALTER TABLE `ejemplar` ADD FOREIGN KEY (`libro_id`) REFERENCES `libro` (`id`);

ALTER TABLE `reserva` ADD FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

ALTER TABLE `reserva` ADD FOREIGN KEY (`libro_id`) REFERENCES `libro` (`id`);

ALTER TABLE `reserva` ADD FOREIGN KEY (`ejemplar_id`) REFERENCES `ejemplar` (`id`);
