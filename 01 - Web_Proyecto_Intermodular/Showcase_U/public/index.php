<?php
require_once __DIR__ . '/../config/db.php';

/**
 * Escapa valores antes de imprimirlos en HTML.
 */
function e($valor) {
    return htmlspecialchars((string) $valor, ENT_QUOTES, 'UTF-8');
}

/**
 * Divide un texto separado por " · " en elementos individuales.
 */
function separarListado($texto) {
    if (empty($texto)) {
        return [];
    }

    return array_filter(array_map('trim', explode(' · ', $texto)));
}

/**
 * Agrupa los proyectos por estado para poder imprimirlos por bloques.
 */
function agruparProyectosPorEstado($proyectos) {
    $grupos = [
        'GANADOR' => [],
        'FINALISTA' => [],
        'SELECCIONADO' => [],
        'PRESENTADO' => []
    ];

    foreach ($proyectos as $proyecto) {
        $estado = $proyecto['estado'] ?? '';

        if (isset($grupos[$estado])) {
            $grupos[$estado][] = $proyecto;
        }
    }

    return $grupos;
}

/**
 * Obtiene los proyectos con su área y tecnologías asociadas.
 */
function obtenerProyectos($pdo) {
    $sql = "
        SELECT
            p.id,
            p.titulo,
            p.lema,
            p.autor,
            p.curso,
            p.descripcion,
            p.impacto,
            p.enlace_demo,
            p.color_acento,
            p.anio,
            p.estado,
            p.destacado,
            p.imagen_principal,
            a.nombre AS area,
            a.imagen_fondo AS imagen_area,
            GROUP_CONCAT(t.nombre ORDER BY t.nombre SEPARATOR ' · ') AS tecnologias
        FROM proyectos p
        INNER JOIN areas a ON a.id = p.area_id
        LEFT JOIN proyecto_tecnologias pt ON pt.proyecto_id = p.id
        LEFT JOIN tecnologias t ON t.id = pt.tecnologia_id
        GROUP BY
            p.id,
            p.titulo,
            p.lema,
            p.autor,
            p.curso,
            p.descripcion,
            p.impacto,
            p.enlace_demo,
            p.color_acento,
            p.anio,
            p.estado,
            p.destacado,
            p.imagen_principal,
            a.nombre,
            a.imagen_fondo
        ORDER BY FIELD(p.estado, 'GANADOR', 'FINALISTA', 'SELECCIONADO', 'PRESENTADO'), p.id ASC
    ";

    return $pdo->query($sql)->fetchAll();
}

/**
 * Obtiene las áreas formativas que se muestran en la sección final.
 */
function obtenerAreas($pdo) {
    $sql = "
        SELECT
            id,
            nombre,
            lema,
            descripcion,
            aprendizaje,
            salidas,
            competencias,
            color_acento,
            imagen_fondo
        FROM areas
        ORDER BY id ASC
    ";

    return $pdo->query($sql)->fetchAll();
}

/**
 * Imprime una tarjeta de proyecto.
 */
function renderProyecto($proyecto) {
    $estado = $proyecto['estado'] ?? '';
    $estadoClase = strtolower($estado);
    $destacada = !empty($proyecto['destacado']) ? 'work-destacada' : '';
    $clases = trim("work-card work-$estadoClase $destacada");
    $colorAcento = !empty($proyecto['color_acento']) ? $proyecto['color_acento'] : '#38bdf8';
    ?>

<article class="<?= e($clases) ?>" style="--project-accent: <?= e($colorAcento) ?>;">

    <div class="work-media">
        <img class="work-img" src="../assets/img/<?= e($proyecto['imagen_principal']) ?>"
            alt="<?= e($proyecto['titulo']) ?>">
    </div>

    <div class="work-info">

        <div class="work-top">
            <span class="badge <?= e($estadoClase) ?>">
                <?= e($estado) ?>
            </span>

            <span class="work-area">
                <?= e($proyecto['area']) ?>
            </span>
        </div>

        <h4><?= e($proyecto['titulo']) ?></h4>

        <?php if (!empty($proyecto['lema'])): ?>
        <p class="work-lema">
            <?= e($proyecto['lema']) ?>
        </p>
        <?php endif; ?>

        <p class="work-meta">
            <?= e($proyecto['autor']) ?> · <?= e($proyecto['curso']) ?> · <?= e($proyecto['anio']) ?>
        </p>

        <?php if (!empty($proyecto['impacto'])): ?>
        <div class="work-impacto">
            <span>Impacto</span>
            <p><?= e($proyecto['impacto']) ?></p>
        </div>
        <?php else: ?>
        <p class="work-description">
            <?= e($proyecto['descripcion']) ?>
        </p>
        <?php endif; ?>

        <?php if (!empty($proyecto['tecnologias'])): ?>
        <div class="work-tech">
            <?php foreach (separarListado($proyecto['tecnologias']) as $tecnologia): ?>
            <span><?= e($tecnologia) ?></span>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>

    </div>

</article>

<?php
}

/**
 * Imprime un grupo de proyectos si contiene resultados.
 */
function renderGrupoProyectos($proyectos, $claseGrupo, $numero, $etiqueta, $titulo, $descripcion = '') {
    if (empty($proyectos)) {
        return;
    }
    ?>

<section class="works-section <?= e($claseGrupo) ?>">

    <header class="works-heading">

        <div class="works-index">
            <span><?= e($numero) ?></span>
            <small><?= e($etiqueta) ?></small>
        </div>

        <div class="works-title">
            <h3><?= e($titulo) ?></h3>

            <?php if (!empty($descripcion)): ?>
            <p><?= e($descripcion) ?></p>
            <?php endif; ?>
        </div>

    </header>

    <div class="works-grid">
        <?php foreach ($proyectos as $proyecto): ?>
        <?php renderProyecto($proyecto); ?>
        <?php endforeach; ?>
    </div>

</section>

<?php
}

/**
 * Imprime una tarjeta de área formativa.
 */
function renderArea($area) {
    $colorArea = !empty($area['color_acento']) ? $area['color_acento'] : '#38bdf8';
    $labelArea = ($area['nombre'] === 'Videojuegos') ? 'Taller aplicado' : 'Área formativa';
    ?>

<article class="area-card" style="--area-accent: <?= e($colorArea) ?>;">

    <img class="area-img" src="../assets/img/<?= e($area['imagen_fondo']) ?>" alt="<?= e($area['nombre']) ?>">

    <div class="area-body">

        <span class="area-label">
            <?= e($labelArea) ?>
        </span>

        <h3><?= e($area['nombre']) ?></h3>

        <?php if (!empty($area['lema'])): ?>
        <p class="area-lema">
            <?= e($area['lema']) ?>
        </p>
        <?php endif; ?>

        <?php if (!empty($area['aprendizaje'])): ?>
        <div class="area-info">
            <strong>Qué se trabaja</strong>
            <p><?= e($area['aprendizaje']) ?></p>
        </div>
        <?php endif; ?>

        <?php if (!empty($area['salidas'])): ?>
        <div class="area-info">
            <strong>Salidas</strong>
            <p><?= e($area['salidas']) ?></p>
        </div>
        <?php endif; ?>

        <?php if (!empty($area['competencias'])): ?>
        <div class="area-competencias">
            <?php foreach (separarListado($area['competencias']) as $competencia): ?>
            <span><?= e($competencia) ?></span>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>

    </div>

</article>

<?php
}

$proyectos = obtenerProyectos($pdo);
$areas = obtenerAreas($pdo);
$proyectosPorEstado = agruparProyectosPorEstado($proyectos);

$totalProyectos = count($proyectos);
$totalAreas = count($areas);
$totalGanadores = count($proyectosPorEstado['GANADOR']);
$totalFinalistas = count($proyectosPorEstado['FINALISTA']);
$totalSeleccionados = count($proyectosPorEstado['SELECCIONADO']);
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SHOWCASE U</title>
    <link rel="stylesheet" href="../assets/css/estilos.css?v=205">
</head>

<body>

    <header class="site-hero">

        <div class="hero-content">

            <div class="hero-copy">

                <h1 class="hero-logo">
                    <span>SHOWCASE</span>
                    <strong>U</strong>
                </h1>

                <span class="hero-subtitle">
                    Talento universitario en acción
                </span>

                <div class="hero-claim">
                    <span class="claim-main">Diseña. Crea. Impacta.</span>
                    <span class="claim-sub">El futuro empieza <em>aquí</em></span>
                </div>

            </div>

            <div class="hero-highlights">

                <div>
                    <strong>DAM</strong>
                    <span>Apps multiplataforma</span>
                </div>

                <div>
                    <strong>DAW</strong>
                    <span>Web digital</span>
                </div>

                <div>
                    <strong>ASIR</strong>
                    <span>Sistemas y redes</span>
                </div>

                <div>
                    <strong>VIDEOJUEGOS</strong>
                    <span>Diseño interactivo</span>
                </div>

            </div>

        </div>

    </header>

    <nav>
        <div class="nav-inner">
            <a href="#presentacion">Presentación</a>
            <a href="#galeria">Galería</a>
            <a href="#roles">Áreas</a>
        </div>
    </nav>

    <main>

        <section id="presentacion" class="parallax-section">

            <div class="parallax-content">

                <span class="parallax-tag">
                    01 / Presentación
                </span>

                <h2>Explora el talento en acción</h2>

                <p class="parallax-texto">
                    SHOWCASE U transforma proyectos académicos en una experiencia visual:
                    una muestra donde cada idea se presenta como una solución real,
                    creativa y conectada con el futuro digital.
                </p>

                <div class="tech-stack-wrap" aria-label="Tecnologías utilizadas en el proyecto">
                    <span class="tech-stack-title">Stack técnico del proyecto</span>

                    <div class="tech-stack">
                        <span>PHP</span>
                        <span>MySQL</span>
                        <span>PDO</span>
                        <span>CSS3</span>
                        <span>Responsive</span>
                        <span>XAMPP</span>
                    </div>
                </div>

                <div class="parallax-stats">

                    <div>
                        <strong>Proyectos reales</strong>
                        <span>Trabajos creados desde el aula con enfoque práctico.</span>
                    </div>

                    <div>
                        <strong>Áreas conectadas</strong>
                        <span>DAM, DAW, ASIR y Videojuegos dentro de una misma muestra.</span>
                    </div>

                    <div>
                        <strong>Talento en evolución</strong>
                        <span>Ideas que combinan tecnología, diseño y creatividad.</span>
                    </div>

                </div>

            </div>

        </section>

        <section id="galeria">

            <div class="gallery-intro">

                <span class="section-kicker">02 / Exposición digital</span>

                <h2>Proyectos que merecen ser vistos</h2>

                <p>
                    Una muestra de trabajos creados desde distintas especialidades, organizada
                    como un recorrido visual por las ideas más destacadas de SHOWCASE U.
                </p>

            </div>

            <div class="gallery-metrics">

                <div class="metric-card metric-total">
                    <strong><?= e($totalProyectos) ?></strong>
                    <span>Proyectos</span>
                </div>

                <div class="metric-card metric-areas">
                    <strong><?= e($totalAreas) ?></strong>
                    <span>Áreas conectadas</span>
                </div>

                <div class="metric-card metric-winner">
                    <strong><?= e($totalGanadores) ?></strong>
                    <span>Ganador</span>
                </div>

                <div class="metric-card metric-finalists">
                    <strong><?= e($totalFinalistas + $totalSeleccionados) ?></strong>
                    <span>Finalistas y selección</span>
                </div>

            </div>

            <div class="gallery-criteria">

                <span>Criterios de exposición</span>

                <div>
                    <strong>Impacto real</strong>
                    <strong>Desarrollo técnico</strong>
                    <strong>Presentación visual</strong>
                    <strong>Aplicación práctica</strong>
                </div>

            </div>

            <?php
            renderGrupoProyectos(
                $proyectosPorEstado['GANADOR'],
                'grupo-ganador',
                '01',
                'Proyecto estrella',
                'Ganador de la edición',
                'La propuesta protagonista de la muestra: una solución con impacto real, desarrollo técnico y una presentación visual destacada.'
            );

            renderGrupoProyectos(
                $proyectosPorEstado['FINALISTA'],
                'grupo-finalistas',
                '02',
                'Selección destacada',
                'Finalistas',
                'Proyectos con una idea sólida, buena ejecución y capacidad para representar el nivel creativo y técnico de la exposición.'
            );

            renderGrupoProyectos(
                $proyectosPorEstado['SELECCIONADO'],
                'grupo-seleccionados',
                '03',
                'Ideas en recorrido',
                'Seleccionados',
                'Propuestas que amplían la muestra y reflejan distintas formas de aplicar tecnología, diseño y creatividad.'
            );

            renderGrupoProyectos(
                $proyectosPorEstado['PRESENTADO'],
                'grupo-presentados',
                '04',
                'Muestra completa',
                'Presentados',
                'Trabajos incorporados al recorrido general como parte de la exposición académica de SHOWCASE U.'
            );
            ?>

        </section>

        <section id="roles">

            <div class="section-heading">

                <span class="section-kicker">03 / Áreas formativas</span>

                <h2>Rutas de talento universitario</h2>

                <p>
                    Cada especialidad aporta una forma distinta de crear: aplicaciones,
                    experiencias web, infraestructuras seguras y mundos interactivos.
                </p>

            </div>

            <div class="grid-areas">
                <?php foreach ($areas as $area): ?>
                <?php renderArea($area); ?>
                <?php endforeach; ?>
            </div>

        </section>

    </main>

    <footer class="site-footer">

    <div class="footer-inner">

        <div class="footer-brand">
            <strong>SHOWCASE U</strong>
            <span>Proyecto intermodular · 1º DAM</span>
        </div>

        <div class="footer-tech">
            <span>PHP</span>
            <span>MySQL</span>
            <span>PDO</span>
            <span>CSS3</span>
            <span>Responsive</span>
            <span>XAMPP</span>
        </div>

        <p>
            Francisca Selma Catalá · 2026
        </p>

    </div>

</footer>

</body>

</html>