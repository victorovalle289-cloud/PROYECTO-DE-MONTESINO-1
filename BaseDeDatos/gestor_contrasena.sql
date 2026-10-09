-- Script de la base de datos del gestor de contraseñas
CREATE DATABASE IF NOT EXISTS gestor_contrasena;
USE gestor_contrasena;

-- Tabla baul: guarda la plataforma, el usuario y la clave (encriptada con bcrypt)
CREATE TABLE IF NOT EXISTS `baul` (
  `id_baul` int NOT NULL AUTO_INCREMENT,
  `Plataforma` varchar(80) NOT NULL,
  `usuario` varchar(80) NOT NULL,
  `clave` varchar(80) NOT NULL,
  PRIMARY KEY (`id_baul`),
  UNIQUE KEY `Plataforma` (`Plataforma`,`usuario`)
);
