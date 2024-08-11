# Greentown RP Project Manager Bot

Ce bot Discord est conçu pour gérer efficacement les projets et les activités sur le serveur Greentown RP. Il permet de gérer les stocks d'outils comme les clée d'ATM, crochetage etc et de synchroniser les informations entre Discord et la base de données, et d'afficher des tableaux mis à jour pour différentes catégories telles que les armes, les munitions, les drogues, les outils, et les zone de ventes.

## Fonctionnalités

- **Affichage des tableaux** : Le bot peut afficher des tableaux d'informations sur les armes, munitions, drogues, outils, et ventes dans des canaux spécifiques.
- **Gestion du stock** : Les commandes permettent de gérer le stock en temps réel, incluant la diminution des quantités disponibles lors du lancement d'activités.
- **Minuteurs d'activités** : Le bot peut démarrer des minuteurs pour différentes activités, avec des notifications automatiques lorsqu'une activité est terminée.
- **Mise à jour via commandes Slash** : Le bot supporte des commandes slash pour mettre à jour les informations sur les armes, munitions, drogues, outils, et ventes directement depuis Discord.
- **Interactions avec les utilisateurs** : Le bot peut réagir aux interactions des utilisateurs avec des messages spécifiques et gérer les réponses éphémères.

## Prérequis

- Python 3.8+
- Une base de données MySQL
- Un serveur Discord avec les permissions nécessaires pour gérer les messages et les canaux

## Installation

1. Clonez ce dépôt :
    ```bash
    git clone https://github.com/Niwagame/Bot_Gestion_GreentownRP
    cd Bot_Gestion_GreentownRP
    ```

2. Installez les dépendances nécessaires :
    ```bash
    pip install -r requirements.txt
    ```

3. Configurez votre base de données MySQL avec la structure fournie dans le fichier `database.sql`. Vous pouvez importer ce fichier dans votre base de données.

4. Mettez à jour le fichier de configuration pour inclure votre propre token Discord et vos informations de base de données.

    ```python
    TOKEN = 'VOTRE_TOKEN_DISCORD'

    DB_HOST = 'VOTRE_HOTE'
    DB_PORT = 3306
    DB_USER = 'VOTRE_UTILISATEUR'
    DB_PASSWORD = 'VOTRE_MOT_DE_PASSE'
    DB_NAME = 'VOTRE_NOM_DE_BASE_DE_DONNEES'
    ```

## Utilisation

Lancez le bot en exécutant le script principal :

```bash
python bot.py
```

## Commandes Disponibles

- **!atm** : Démarre un minuteur pour l'activité ATM. Et enleve 1 **clée ATM** dans la BDD
- **!cam** : Démarre un minuteur pour un cambriolage. Et enleve 1 **clée ATM** dans la BDD
- **!fle** : Démarre un minuteur pour un braquage de banque Fleeca. Et enleve 1 **clée de banque** dans la BDD
- **!ent** : Démarre un minuteur pour un entrepôt. Et enleve 1 **thermite** dans la BDD
- **!sup** : Démarre un minuteur pour une supérette.
- **!cf** : Démarre un minuteur pour un coffre-fort.
- **!bij** : Démarre un minuteur pour une bijouterie.
- **!tra** : Démarre un minuteur pour un train.
- **/stock** : Affiche le stock actuel.
- **/armes**, **/munitions**, **/drogues**, **/outils**, **/ventes** : Commandes pour mettre à jour les différentes catégories.

## Synchronisation des Commandes Slash

Le bot synchronise automatiquement les commandes slash lors de son démarrage. Assurez-vous que les commandes sont bien configurées dans votre serveur Discord.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une pull request ou à signaler des problèmes.

## Sécurité

Ne partagez jamais votre token Discord en ligne. Assurez-vous que vos informations de base de données sont sécurisées.

## License

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus d'informations.


Ce `README.md` donne un aperçu complet du bot, de ses fonctionnalités, de son installation, et de son utilisation. Assurez-vous de remplacer les informations placeholders comme le token Discord, les informations de base de données, et le lien du dépôt git par vos propres données.
