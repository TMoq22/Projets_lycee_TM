import sqlite3

# Connexion à la base de données SQLite (ou création si elle n'existe pas)
conn = sqlite3.connect('chat.db')
cursor = conn.cursor()


# Création de la table Utilisateur
cursor.execute('''
CREATE TABLE IF NOT EXISTS Utilisateur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(30) NOT NULL CHECK(length(password)>=10),
    id_autorisation INTEGER CHECK (id_autorisation =0 OR id_autorisation=1)
);
''')

# # Création de la table Message
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Message (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_auteur INTEGER NOT NULL,
#     date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     message TEXT NOT NULL,
#     FOREIGN KEY (id_auteur) REFERENCES Utilisateur(id)
# );
# ''')

# Validation des modifications
conn.commit()

#Insertion d'un utilisateur de base admin
## Bien entendu, dans une véritable création de base de donnée, l'utilisateur admin ne
## devrait pas avoir un mot de passe si faible et en clair

cursor.execute('''INSERT INTO Utilisateur(pseudo, email, password, id_autorisation)
               VALUES ('admin', 'admin@lechat.fr', 'admin1234!', 0)
               ''')

conn.commit()
# Fermeture de la connexion
conn.close()

print("Base de données et tables créées avec succès.")