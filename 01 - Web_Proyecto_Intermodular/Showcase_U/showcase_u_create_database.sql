-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-06-2026 a las 17:08:12
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


--
-- Crear y seleccionar la base de datos automáticamente
--
CREATE DATABASE IF NOT EXISTS `showcase_u` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `showcase_u`;

--
-- Base de datos: `showcase_u`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `lema` varchar(180) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `aprendizaje` text DEFAULT NULL,
  `salidas` text DEFAULT NULL,
  `competencias` varchar(255) DEFAULT NULL,
  `color_acento` varchar(20) DEFAULT NULL,
  `imagen_fondo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id`, `nombre`, `lema`, `descripcion`, `aprendizaje`, `salidas`, `competencias`, `color_acento`, `imagen_fondo`) VALUES
(1, 'DAM', 'Aplicaciones útiles para resolver problemas reales.', 'Desarrollo de aplicaciones móviles y de escritorio orientadas a resolver problemas reales mediante soluciones útiles, accesibles y multiplataforma.', 'En DAM se trabaja el desarrollo de aplicaciones móviles y de escritorio, la lógica de programación, la gestión de datos, el diseño de interfaces y la creación de soluciones multiplataforma orientadas a necesidades reales.', 'Desarrollador/a de aplicaciones multiplataforma, programador/a junior, técnico/a de software, desarrollador/a de aplicaciones móviles o soporte en equipos de desarrollo.', 'Apps móviles · Escritorio · Multiplataforma · Bases de datos · Interfaces', '#38bdf8', 'area_dam_robot_movil.jpg'),
(2, 'DAW', 'Experiencias web pensadas para comunicar, conectar y funcionar.', 'Creación de sitios web, interfaces digitales y plataformas online con diseño responsive, experiencia de usuario y contenido interactivo.', 'En DAW se trabaja la creación de sitios web, interfaces digitales, diseño responsive, programación cliente-servidor, gestión de contenidos y desarrollo de plataformas online con enfoque visual y funcional.', 'Desarrollador/a web, programador/a frontend junior, programador/a backend junior, maquetador/a web, técnico/a en plataformas digitales o soporte en proyectos online.', 'HTML5 · CSS3 · UX/UI · Responsive · Desarrollo web', '#8b5cf6', 'area_daw_diseno_web.jpg'),
(3, 'ASIR', 'Infraestructura, redes y servicios preparados para funcionar.', 'Administración de servidores, redes, servicios cloud y sistemas seguros, con especial atención a la monitorización y la continuidad del servicio.', 'En ASIR se trabaja la administración de sistemas, redes, servidores, servicios cloud, seguridad, monitorización e infraestructuras necesarias para mantener entornos tecnológicos estables y protegidos.', 'Administrador/a de sistemas, técnico/a de redes, técnico/a de soporte, operador/a de sistemas, técnico/a cloud junior o especialista junior en ciberseguridad.', 'Redes · Servidores · Cloud · Seguridad · Monitorización', '#06b6d4', 'area_asir_laboratorio_redes.jpg'),
(4, 'Videojuegos', 'Taller aplicado de diseño interactivo y creación de experiencias jugables.', 'Diseño de videojuegos, mundos interactivos y experiencias narrativas donde se combinan creatividad, mecánicas jugables y tecnología.', 'En el taller de Videojuegos se aplican conocimientos de programación, narrativa, diseño visual, mecánicas, niveles e interacción para crear prototipos y experiencias jugables vinculadas a la creatividad digital.', 'Introducción a perfiles como diseñador/a de niveles, creador/a de prototipos, tester de videojuegos, diseñador/a narrativo junior o apoyo en proyectos interactivos y multimedia.', 'Taller aplicado · Narrativa · Mecánicas · Prototipado · Experiencia jugable', '#f97316', 'area_videojuegos_criatura_aula.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `concursos`
--

CREATE TABLE `concursos` (
  `id` int(11) NOT NULL,
  `titulo` varchar(120) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_limite` date NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `concursos`
--

INSERT INTO `concursos` (`id`, `titulo`, `descripcion`, `fecha_limite`, `imagen`) VALUES
(1, 'Hackathon Universitario', 'Reto por equipos orientado a iniciación. Se valora claridad, organización y presentación del proyecto.', '2026-03-15', 'concurso_1.jpg'),
(2, 'Reto de Videojuegos', 'Game Jam de nivel inicial con entrega de prototipo funcional. Se valora originalidad y jugabilidad.', '2026-04-10', 'concurso_2.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id` int(11) NOT NULL,
  `tipo` enum('TALLER','CHARLA') NOT NULL,
  `titulo` varchar(120) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha` date NOT NULL,
  `imagen` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id`, `tipo`, `titulo`, `descripcion`, `fecha`, `imagen`) VALUES
(1, 'TALLER', 'SEMINARIO DE WORDPRESS', 'Seminario de iniciación a WordPress: instalación en local, temas, plugins y publicación de una web básica.', '2026-02-10', 'wordpress.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagenes_proyectos`
--

CREATE TABLE `imagenes_proyectos` (
  `id` int(11) NOT NULL,
  `proyecto_id` int(11) NOT NULL,
  `imagen` varchar(255) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `imagenes_proyectos`
--

INSERT INTO `imagenes_proyectos` (`id`, `proyecto_id`, `imagen`, `descripcion`) VALUES
(1, 1, 'proyecto_dam_1.jpg', NULL),
(2, 1, 'proyecto_dam_1.jpg', NULL),
(3, 2, 'proyecto_daw_1.jpg', NULL),
(4, 1, 'proyecto_dam_1.jpg', 'Pantalla principal de la aplicación AulaGo'),
(5, 1, 'area_dam.jpg', 'Concepto visual de desarrollo multiplataforma'),
(6, 2, 'proyecto_daw_1.jpg', 'Vista principal de la galería web Aurelia Gallery'),
(7, 2, 'area_daw.jpg', 'Concepto visual de desarrollo web'),
(8, 3, 'area_asir.jpg', 'Infraestructura y red del proyecto CloudLab ASIR'),
(9, 4, 'area_videojuegos.jpg', 'Portada visual del videojuego Campus Z'),
(10, 1, 'proyecto_dam_1.jpg', 'Pantalla principal de la aplicación AulaGo'),
(11, 1, 'area_dam.jpg', 'Concepto visual de desarrollo multiplataforma'),
(12, 2, 'proyecto_daw_1.jpg', 'Vista principal de la galería web Aurelia Gallery'),
(13, 2, 'area_daw.jpg', 'Concepto visual de desarrollo web'),
(14, 3, 'area_asir.jpg', 'Infraestructura y red del proyecto CloudLab ASIR'),
(15, 4, 'area_videojuegos.jpg', 'Portada visual del videojuego Campus Z');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyectos`
--

CREATE TABLE `proyectos` (
  `id` int(11) NOT NULL,
  `area_id` int(11) NOT NULL,
  `titulo` varchar(120) NOT NULL,
  `lema` varchar(160) DEFAULT NULL,
  `autor` varchar(120) DEFAULT NULL,
  `curso` varchar(80) DEFAULT NULL,
  `descripcion` text NOT NULL,
  `impacto` varchar(220) DEFAULT NULL,
  `enlace_demo` varchar(255) DEFAULT NULL,
  `color_acento` varchar(20) DEFAULT NULL,
  `estado` enum('GANADOR','SELECCIONADO','FINALISTA','PRESENTADO') NOT NULL DEFAULT 'PRESENTADO',
  `destacado` tinyint(1) NOT NULL DEFAULT 0,
  `imagen_principal` varchar(255) NOT NULL,
  `anio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proyectos`
--

INSERT INTO `proyectos` (`id`, `area_id`, `titulo`, `lema`, `autor`, `curso`, `descripcion`, `impacto`, `enlace_demo`, `color_acento`, `estado`, `destacado`, `imagen_principal`, `anio`) VALUES
(1, 1, 'AulaGo', 'Tecnología para cuidar cuando nadie está cerca.', 'Lucía Romero y Mario Vidal', '1º DAM', 'Aplicación móvil ganadora orientada al cuidado de personas mayores que viven solas, capaz de monitorizar ritmos vitales y enviar alertas por voz a familiares y servicios sanitarios en caso de emergencia.', 'Mejora la seguridad y autonomía de personas mayores que viven solas mediante alertas por voz y comunicación con familiares.', NULL, '#10b981', 'GANADOR', 1, 'proyecto_dam_ganador_salud.png', 2026),
(2, 2, 'Starlink Lunar Frontier', 'Una ventana digital hacia la exploración lunar.', 'Nora Castillo y Diego Martín', '1º DAW', 'Página web informativa seleccionada como finalista que recopila misiones, sondas, telemetría y comunicaciones lunares relacionadas con proyectos Starlink orientados a la exploración de la cara oculta de la Luna.', 'Convierte información técnica sobre misiones, sondas y comunicaciones espaciales en una experiencia web clara y visual.', NULL, '#3b82f6', 'FINALISTA', 1, 'proyecto_daw_1.png', 2026),
(3, 3, 'CloudLab Secure Network', 'Infraestructura segura para aprender, probar y escalar.', 'Hugo Serrano y Carla Méndez', '1º ASIR', 'Proyecto de administración de sistemas y redes basado en el diseño de una infraestructura cloud segura, con servidores virtualizados, control de accesos, monitorización del estado de la red y gestión de incidencias.', 'Diseña un entorno cloud controlado con servidores, redes y monitorización para simular una infraestructura profesional.', NULL, '#06b6d4', 'FINALISTA', 1, 'proyecto_asir_finalista_1.png', 2026),
(4, 4, 'Campus Z', 'Sobrevivir al campus nunca fue tan difícil.', 'Iker Molina y Alba Torres', '1º Videojuegos', 'Videojuego de supervivencia ambientado en el campus de la UAX durante una invasión zombie, donde estudiantes y profesores colaboran para defender las instalaciones, construir recursos y salvar la universidad.', 'Transforma el entorno universitario en una experiencia interactiva de supervivencia, cooperación y toma de decisiones.', NULL, '#ef4444', 'FINALISTA', 1, 'proyecto_videojuegos_campus_z.png', 2026),
(6, 1, 'NeuroAgenda', 'Organizar el día también puede ser una experiencia inteligente.', 'Paula Ibáñez y Marcos León', '1º DAM', 'Aplicación móvil seleccionada que ayuda a organizar rutinas, medicación, tareas y recordatorios personales mediante una interfaz clara, accesible y orientada al seguimiento diario.', 'Ayuda al alumnado a planificar tareas, horarios y recordatorios desde una herramienta sencilla y orientada a la productividad.', NULL, '#8b5cf6', 'SELECCIONADO', 1, 'agenda_estudiantil_dam.png', 2026),
(7, 2, 'EcoWeb Market', 'Comprar, vender y reutilizar con conciencia digital.', 'Claudia Ramos y Daniel Ortega', '1º DAW', 'Página web seleccionada de comercio sostenible que presenta productos ecológicos, categorías responsables y una experiencia responsive orientada al consumo consciente.', 'Plantea un mercado web orientado a productos sostenibles, reutilización y consumo responsable dentro de una experiencia digital.', NULL, '#22c55e', 'SELECCIONADO', 1, 'proyecto_daw_seleccionado_1.png', 2026),
(8, 3, 'NetCloud Monitor', 'Ver el estado de la red antes de que aparezca el problema.', 'Álvaro Ruiz y Marta Sánchez', '1º ASIR', 'Proyecto seleccionado de ASIR basado en una infraestructura de red con servidor, conectividad cloud, monitorización de servicios y seguridad básica para garantizar el correcto funcionamiento del sistema.', 'Centraliza información de servidores, servicios y red para facilitar la supervisión técnica y la detección de incidencias.', NULL, '#0ea5e9', 'SELECCIONADO', 1, 'proyecto_asir_seleccionado_1.png', 2026),
(9, 4, 'Susurro del Vendaval', 'Un mundo interactivo donde cada decisión deja huella.', NULL, NULL, 'Videojuego narrativo de fantasía inspirado en un mundo de música, magia y leyendas, donde el jugador explora un universo medieval y descubre secretos ocultos a través de la aventura y la narrativa interactiva.', 'Explora narrativa, ambientación y mecánicas jugables en una experiencia centrada en exploración, atmósfera y emoción.', NULL, '#f97316', 'SELECCIONADO', 0, 'proyecto_vj_seleccionado_1.png', 2026);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto_tecnologias`
--

CREATE TABLE `proyecto_tecnologias` (
  `proyecto_id` int(11) NOT NULL,
  `tecnologia_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proyecto_tecnologias`
--

INSERT INTO `proyecto_tecnologias` (`proyecto_id`, `tecnologia_id`) VALUES
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(2, 3),
(2, 4),
(2, 11),
(2, 12),
(2, 13),
(2, 14),
(3, 15),
(3, 16),
(3, 17),
(3, 18),
(3, 19),
(3, 20),
(4, 21),
(4, 22),
(4, 23),
(4, 24),
(4, 25),
(6, 5),
(6, 6),
(6, 10),
(6, 26),
(6, 27),
(7, 3),
(7, 4),
(7, 10),
(7, 11),
(7, 28),
(7, 29),
(8, 16),
(8, 18),
(8, 19),
(8, 30),
(8, 31),
(9, 14),
(9, 21),
(9, 22),
(9, 23),
(9, 25);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tecnologias`
--

CREATE TABLE `tecnologias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tecnologias`
--

INSERT INTO `tecnologias` (`id`, `nombre`) VALUES
(9, 'Accesibilidad'),
(26, 'Agenda digital'),
(7, 'Alertas por voz'),
(6, 'Aplicación móvil'),
(8, 'Asistencia sanitaria'),
(17, 'Ciberseguridad'),
(15, 'Cloud'),
(12, 'Comunicación espacial'),
(14, 'Contenido interactivo'),
(4, 'CSS3'),
(22, 'Diseño de niveles'),
(10, 'Diseño responsive'),
(25, 'Gamificación'),
(20, 'Gestión de incidencias'),
(3, 'HTML5'),
(31, 'Infraestructura cloud'),
(11, 'Interfaz web'),
(28, 'Marketplace'),
(18, 'Monitorización'),
(2, 'MySQL'),
(23, 'Narrativa interactiva'),
(30, 'Panel de control'),
(1, 'PHP'),
(27, 'Productividad'),
(19, 'Redes'),
(16, 'Servidores virtualizados'),
(29, 'Sostenibilidad'),
(24, 'Supervivencia'),
(13, 'Telemetría'),
(5, 'UX/UI'),
(21, 'Videojuegos');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `concursos`
--
ALTER TABLE `concursos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `imagenes_proyectos`
--
ALTER TABLE `imagenes_proyectos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `proyecto_id` (`proyecto_id`);

--
-- Indices de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `area_id` (`area_id`);

--
-- Indices de la tabla `proyecto_tecnologias`
--
ALTER TABLE `proyecto_tecnologias`
  ADD PRIMARY KEY (`proyecto_id`,`tecnologia_id`),
  ADD KEY `tecnologia_id` (`tecnologia_id`);

--
-- Indices de la tabla `tecnologias`
--
ALTER TABLE `tecnologias`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `concursos`
--
ALTER TABLE `concursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `imagenes_proyectos`
--
ALTER TABLE `imagenes_proyectos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `proyectos`
--
ALTER TABLE `proyectos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tecnologias`
--
ALTER TABLE `tecnologias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `imagenes_proyectos`
--
ALTER TABLE `imagenes_proyectos`
  ADD CONSTRAINT `imagenes_proyectos_ibfk_1` FOREIGN KEY (`proyecto_id`) REFERENCES `proyectos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `proyectos`
--
ALTER TABLE `proyectos`
  ADD CONSTRAINT `proyectos_ibfk_1` FOREIGN KEY (`area_id`) REFERENCES `areas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `proyecto_tecnologias`
--
ALTER TABLE `proyecto_tecnologias`
  ADD CONSTRAINT `proyecto_tecnologias_ibfk_1` FOREIGN KEY (`proyecto_id`) REFERENCES `proyectos` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `proyecto_tecnologias_ibfk_2` FOREIGN KEY (`tecnologia_id`) REFERENCES `tecnologias` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
