-- Création de la table utilisateurs pour l'authentification
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('admin', 'maintenance', 'production', 'logistique') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- Modifier la colonne role si elle existe avec l'ancien ENUM
ALTER TABLE `users` MODIFY COLUMN `role` ENUM('admin', 'maintenance', 'production', 'logistique') NOT NULL;

-- Insertion d'utilisateurs exemple (mots de passe hachés)
INSERT INTO `users` (`username`, `password_hash`, `role`) VALUES
('admin', '$2b$12$kQRXecRpMn1i9NdkS9O8EuX5entkkMxo9VXCN7HPCoCg77M/MMnpy', 'admin'),
('maintenance', '$2b$12$e51Uf/cswj/14UdlK09QaOuVdVGdsHYX1Nsrv2QrBIO5fLqaPhZpO', 'maintenance'),
('production', '$2b$12$e51Uf/cswj/14UdlK09QaOuVdVGdsHYX1Nsrv2QrBIO5fLqaPhZpO', 'production'),
('logistique', '$2b$12$e51Uf/cswj/14UdlK09QaOuVdVGdsHYX1Nsrv2QrBIO5fLqaPhZpO', 'logistique');