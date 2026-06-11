<?php

/**
 * Archivo de conexión a la base de datos.
 * Centraliza la configuración para que index.php e insertar.php
 * utilicen la misma conexión mediante PDO.
 */

$host = 'localhost';
$dbname = 'showcase_u';
$username = 'root';
$password = '';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$dbname;charset=$charset";

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

try {
    $pdo = new PDO($dsn, $username, $password, $options);
} catch (PDOException $e) {
    die('Error en la conexión con la base de datos.');
}