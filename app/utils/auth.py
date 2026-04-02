import bcrypt
from utils.cnx_sql import func_get_cnx_sql


def init_users_table():
    """Crée la table users et les comptes par défaut si inexistants."""
    conn = func_get_cnx_sql()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'maintenance', 'production', 'logistique') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        # Comptes par défaut (INSERT IGNORE = ne rien faire s'ils existent déjà)
        default_users = [
            ('admin',       'admin123',   'admin'),
            ('maintenance', 'user123', 'maintenance'),
            ('production',  'user123',  'production'),
            ('logistique',  'user123',  'logistique'),
        ]
        for username, password, role in default_users:
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT IGNORE INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, password_hash, role)
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def authenticate_user(username: str, password: str):
    """
    Vérifie les credentials de l'utilisateur.
    Retourne le rôle si authentifié, sinon None.
    """
    conn = func_get_cnx_sql()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT password_hash, role FROM users WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()
        if result:
            stored_hash, role = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return role
        return None
    finally:
        cursor.close()
        conn.close()
