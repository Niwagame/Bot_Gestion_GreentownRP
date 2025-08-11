# Greentown RP Project Manager Bot

Bot Discord pour **gérer les activités et ressources** du serveur Greentown RP : tableaux (Armes, Munitions, Drogues, Outils, Ventes), **minuteurs**, et **gestion de stock** connectés à **MariaDB**.
Déploiement simple via **Docker + Docker Compose** sur un **VPS**.

---

## 🧰 Ce que le bot sait faire

* Afficher des **tableaux** par catégorie dans des salons dédiés (avec mise à jour automatique).
* Lancer des **minuteurs** d’activités (préfixe `!`) qui peuvent décrémenter le stock.
* **Commandes slash** pour mettre à jour les données (avec autocomplétion).
* Lecture/écriture en base **MariaDB** ; interface web **phpMyAdmin** incluse.

---

## ✅ Prérequis (VPS)

* Un **VPS** (Debian 12 ou Ubuntu 22.04+ recommandé) – 1 vCPU, 1 Go RAM suffisent.
* **Docker** et **Docker Compose** (installés plus bas).
* Un **token Discord** (Application > Bot), avec **Message Content Intent** activé.
* (Optionnel) Un nom de domaine / **SSH** pour sécuriser l’accès à phpMyAdmin.

---

## 🗂 Structure du dépôt

```
.
├── bot.py
├── requirements.txt
├── Dockerfile
├── compose.yml
├── .env.example
├── .dockerignore
└── db/
    └── init/            # (optionnel) scripts SQL exécutés au 1er démarrage
```

---

## ⚙️ Configuration (sans secret en dur)

1. Sur votre VPS, **cloner** le dépôt :

```bash
git clone https://github.com/Niwagame/Bot_Gestion_GreentownRP.git
cd Bot_Gestion_GreentownRP
```

2. **Créer le fichier `.env`** à partir du modèle et le remplir :

```bash
cp .env.example .env
nano .env
```

Exemple de `.env` :

```env
# Discord
DISCORD_TOKEN=VOTRE_TOKEN_DISCORD

# Base de données
DB_HOST=db
DB_PORT=3306
DB_NAME=greentown
DB_USER=botuser
DB_PASSWORD=botpass
DB_ROOT_PASSWORD=changeme-root
```

> ⚠️ Ne **committez jamais** `.env`. Gardez **.env.example** public et sans secrets.

---

## 🚀 Installation de Docker (VPS Debian/Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl gnupg lsb-release

# Clé Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo $ID)/gpg \
 | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Dépôt Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/$(. /etc/os-release; echo $ID) \
$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Paquets
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Test
sudo docker run hello-world
```

(Optionnel pour éviter `sudo` à chaque commande)

```bash
sudo usermod -aG docker $USER
newgrp docker
docker ps
```

---

## ▶️ Démarrer le bot (VPS)

Depuis le dossier du projet :

```bash
docker compose up -d --build
```

* Le bot se connecte à Discord et **synchronise** les commandes slash.
* La base **MariaDB** est créée au **premier** démarrage (avec l’utilisateur du `.env`).
* **phpMyAdmin** démarre sur le port **8080**.

### Accéder à phpMyAdmin

* URL : `http://ADRESSE_IP_DU_VPS:8080`
* Serveur : `db`
* Identifiant / Mot de passe : `DB_USER` / `DB_PASSWORD` (du `.env`)
* Compte root si besoin : `root` / `DB_ROOT_PASSWORD`

🔒 **Recommandé (VPS public)** : limiter phpMyAdmin à localhost et y accéder via **tunnel SSH** :

```yaml
# compose.yml → service: phpmyadmin
ports:
  - "127.0.0.1:8080:80"
```

Puis depuis votre machine locale :

```bash
ssh -L 8080:localhost:8080 user@ADRESSE_IP_DU_VPS
# ensuite : http://localhost:8080
```

---

## 🕹 Commandes

### Préfixe `!` (minuteurs)

* `!atm` – retire 1 *clé ATM*
* `!cam` – retire 1 *crochetage*
* `!fle` – retire 1 *clée de banque*
* `!ent` – retire 1 *thermite*
* `!sup`, `!cf`, `!bij`, `!tra` – autres minuteurs

### Slash `/`

* `/stock` – affiche le stock actuel (éphémère)
* `/armes`, `/munitions`, `/drogues`, `/outils`, `/ventes` – mises à jour des données
  *(autocomplétion des noms existants)*

> Les tableaux sont publiés dans les salons définis par la table **Message** (`Nom`, `ID_Salon`, `ID_Message`).
> À chaque mise à jour, l’ancien message est supprimé et remplacé.

---

## 🔄 Mettre à jour le bot (VPS)

```bash
cd /chemin/vers/Bot_Gestion_GreentownRP
git pull
docker compose up -d --build
```

Si vous avez changé les variables du `.env` **après** un premier démarrage de la base et que la création initiale ne correspond plus, il peut être nécessaire de **réinitialiser** la base (⚠️ supprime les données) :

```bash
docker compose down -v
docker compose up -d --build
```

---

## 💾 Sauvegarder / Restaurer la base

**Dump :**

```bash
docker compose exec db sh -c 'exec mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' > backup.sql
```

**Restauration :**

```bash
docker compose exec -T db sh -c 'exec mariadb -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"' < backup.sql
```

---

## 🧯 Dépannage rapide

* **Le bot n’arrive pas à se connecter à la DB**

  * Vérifiez `.env` (utilisateur/mot de passe/nom de DB).
  * Voyez les logs :

    ```bash
    docker compose logs -f bot
    docker compose logs -f db
    ```
  * Si le volume DB a été créé avant la bonne config :
    `docker compose down -v && docker compose up -d --build`

* **phpMyAdmin inaccessible**

  * Vérifiez les ports :

    ```bash
    docker ps | grep phpmyadmin
    ```
  * Sur VPS public, préférez le **tunnel SSH** (voir plus haut).

* **Afficher les logs / Arrêter**

  ```bash
  docker compose logs -f
  docker compose down
  ```

---

## 🔐 Sécurité

* **Ne divulguez jamais** votre `DISCORD_TOKEN`. En cas de fuite : **régénérez** le token dans le portail Discord.
* Limitez l’exposition réseau (bind `127.0.0.1` + tunnel SSH pour phpMyAdmin).
* Gardez votre VPS et Docker **à jour**.

---

## 🤝 Contribution

Issues et PR bienvenues. Merci de ne pas pousser de secrets dans le dépôt.

---

## 📄 Licence

MIT — voir `LICENSE`.