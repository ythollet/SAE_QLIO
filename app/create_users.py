import bcrypt
import mysql.connector
import os

# Connexion DB
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "client")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "mdp")
DB_NAME = os.environ.get("DB_NAME", "mes4")
DB_PORT = int(os.environ.get("DB_PORT", "3308"))

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=DB_PORT
)
cursor = conn.cursor()

# Créer la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) UNIQUE NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` ENUM('admin', 'maintenance', 'production', 'logistique') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
""")

# Modifier la colonne role si nécessaire
cursor.execute("""
ALTER TABLE `users` MODIFY COLUMN `role` ENUM('admin', 'user', 'maintenance', 'production', 'logistique') NOT NULL;
""")

# Mettre à jour les rôles existants
cursor.execute("UPDATE users SET role = 'maintenance' WHERE role = 'user';")

# Maintenant modifier l'ENUM pour supprimer 'user'
cursor.execute("""
ALTER TABLE `users` MODIFY COLUMN `role` ENUM('admin', 'maintenance', 'production', 'logistique') NOT NULL;
""")

# Fonction pour hacher le mot de passe
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Utilisateurs à créer
users = [
    ('admin', 'admin123', 'admin'),
    ('maintenance', 'user123', 'maintenance'),
    ('production', 'user123', 'production'),
    ('logistique', 'user123', 'logistique')
]

for username, password, role in users:
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE password_hash=%s, role=%s", (username, password_hash, role, password_hash, role))

conn.commit()
cursor.close()
conn.close()

print("Utilisateurs créés avec succès.")