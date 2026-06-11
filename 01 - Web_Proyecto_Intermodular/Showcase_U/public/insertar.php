<?php
require_once __DIR__ . '/../config/db.php';

/* =========================================================
   CONFIGURACIÓN
   ========================================================= */

const ESTADOS_PERMITIDOS = [
    'GANADOR',
    'FINALISTA',
    'SELECCIONADO',
    'PRESENTADO'
];

const ANIO_MINIMO = 2020;
const ANIO_MAXIMO = 2035;

$error = '';

/* =========================================================
   FUNCIONES AUXILIARES
   ========================================================= */

/**
 * Escapa valores antes de imprimirlos en HTML.
 */
function e($valor) {
    return htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8');
}

/**
 * Comprueba que el nombre de imagen tenga un formato seguro.
 * Solo permite letras, números, guiones, guiones bajos y formatos web habituales.
 */
function nombreImagenValido($nombre) {
    return preg_match('/^[a-zA-Z0-9_-]+\.(jpg|jpeg|png|webp)$/', $nombre) === 1;
}

/**
 * Comprueba que un texto no supere la longitud indicada.
 */
function longitudValida($texto, $maximo) {
    return mb_strlen($texto, 'UTF-8') <= $maximo;
}

/**
 * Recupera y limpia los datos enviados por el formulario.
 */
function obtenerDatosFormulario() {
    return [
        'titulo' => trim($_POST['titulo'] ?? ''),
        'autor' => trim($_POST['autor'] ?? ''),
        'curso' => trim($_POST['curso'] ?? ''),
        'descripcion' => trim($_POST['descripcion'] ?? ''),
        'imagen_principal' => trim($_POST['imagen_principal'] ?? ''),
        'anio' => (int)($_POST['anio'] ?? 0),
        'estado' => $_POST['estado'] ?? '',
        'area_id' => (int)($_POST['area_id'] ?? 0),
        'destacado' => isset($_POST['destacado']) ? 1 : 0
    ];
}

/**
 * Valida los campos obligatorios y las reglas básicas del formulario.
 */
function validarProyecto($datos) {
    if (
        empty($datos['titulo']) ||
        empty($datos['autor']) ||
        empty($datos['curso']) ||
        empty($datos['descripcion']) ||
        empty($datos['imagen_principal']) ||
        empty($datos['anio']) ||
        empty($datos['estado']) ||
        empty($datos['area_id'])
    ) {
        return 'Todos los campos son obligatorios.';
    }

    if (!longitudValida($datos['titulo'], 120)) {
        return 'El título es demasiado largo.';
    }

    if (!longitudValida($datos['autor'], 120)) {
        return 'El autor o equipo es demasiado largo.';
    }

    if (!longitudValida($datos['curso'], 80)) {
        return 'El curso es demasiado largo.';
    }

    if (!longitudValida($datos['descripcion'], 600)) {
        return 'La descripción es demasiado larga.';
    }

    if ($datos['anio'] < ANIO_MINIMO || $datos['anio'] > ANIO_MAXIMO) {
        return 'El año no es válido.';
    }

    if (!in_array($datos['estado'], ESTADOS_PERMITIDOS, true)) {
        return 'El estado seleccionado no es válido.';
    }

    if (!nombreImagenValido($datos['imagen_principal'])) {
        return 'El nombre de la imagen no es válido. Usa solo letras, números, guiones y formato jpg, jpeg, png o webp.';
    }

    return '';
}

/**
 * Comprueba si el área existe en la base de datos.
 */
function areaExiste($pdo, $areaId) {
    $sql = 'SELECT COUNT(*) FROM areas WHERE id = :id';
    $stmt = $pdo->prepare($sql);
    $stmt->execute([':id' => $areaId]);

    return (int)$stmt->fetchColumn() > 0;
}

/**
 * Inserta el proyecto en la base de datos usando consulta preparada.
 */
function insertarProyecto($pdo, $datos) {
    $sql = '
        INSERT INTO proyectos
            (area_id, titulo, autor, curso, descripcion, estado, destacado, imagen_principal, anio)
        VALUES
            (:area_id, :titulo, :autor, :curso, :descripcion, :estado, :destacado, :imagen_principal, :anio)
    ';

    $stmt = $pdo->prepare($sql);

    $stmt->execute([
        ':area_id' => $datos['area_id'],
        ':titulo' => $datos['titulo'],
        ':autor' => $datos['autor'],
        ':curso' => $datos['curso'],
        ':descripcion' => $datos['descripcion'],
        ':estado' => $datos['estado'],
        ':destacado' => $datos['destacado'],
        ':imagen_principal' => $datos['imagen_principal'],
        ':anio' => $datos['anio']
    ]);
}

/**
 * Carga las áreas disponibles para el desplegable.
 */
function obtenerAreas($pdo) {
    $sql = 'SELECT id, nombre FROM areas ORDER BY nombre';
    return $pdo->query($sql)->fetchAll();
}

/* =========================================================
   PROCESAMIENTO DEL FORMULARIO
   ========================================================= */

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $datos = obtenerDatosFormulario();
    $error = validarProyecto($datos);

    if ($error === '') {
        if (!areaExiste($pdo, $datos['area_id'])) {
            $error = 'El área seleccionada no existe.';
        } else {
            insertarProyecto($pdo, $datos);
            header('Location: index.php');
            exit;
        }
    }
}

$areas = obtenerAreas($pdo);
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insertar Proyecto | SHOWCASE U</title>
    <link rel="stylesheet" href="../assets/css/estilos.css">
</head>

<body style="padding: 40px;">

    <h2>Insertar nuevo proyecto</h2>

    <?php if (!empty($error)): ?>
        <p style="color: red; font-weight: bold;">
            <?= e($error) ?>
        </p>
    <?php endif; ?>

    <form method="POST" style="max-width: 500px; display: grid; gap: 12px;">

        <label for="titulo">Título:</label>
        <input id="titulo" type="text" name="titulo" maxlength="120" required>

        <label for="autor">Autor o equipo:</label>
        <input id="autor" type="text" name="autor" maxlength="120" required>

        <label for="curso">Curso:</label>
        <input id="curso" type="text" name="curso" maxlength="80" placeholder="Ej: 1º DAM" required>

        <label for="descripcion">Descripción:</label>
        <textarea id="descripcion" name="descripcion" rows="4" maxlength="600" required></textarea>

        <label for="imagen_principal">Nombre del archivo de imagen:</label>
        <input id="imagen_principal" type="text" name="imagen_principal" placeholder="Ej: proyecto_dam_1.jpg" required>

        <label for="anio">Año:</label>
        <input id="anio" type="number" name="anio" min="<?= ANIO_MINIMO ?>" max="<?= ANIO_MAXIMO ?>" value="2026" required>

        <label for="estado">Estado:</label>
        <select id="estado" name="estado" required>
            <option value="">-- Seleccionar --</option>
            <?php foreach (ESTADOS_PERMITIDOS as $estado): ?>
                <option value="<?= e($estado) ?>">
                    <?= e($estado) ?>
                </option>
            <?php endforeach; ?>
        </select>

        <label>
            <input type="checkbox" name="destacado" value="1">
            Marcar como destacado
        </label>

        <label for="area_id">Área:</label>
        <select id="area_id" name="area_id" required>
            <option value="">-- Seleccionar área --</option>
            <?php foreach ($areas as $area): ?>
                <option value="<?= (int)$area['id'] ?>">
                    <?= e($area['nombre']) ?>
                </option>
            <?php endforeach; ?>
        </select>

        <button type="submit">Guardar proyecto</button>

    </form>

</body>

</html>
