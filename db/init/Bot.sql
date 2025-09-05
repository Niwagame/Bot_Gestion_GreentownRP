-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : ven. 05 sep. 2025 à 18:26
-- Version du serveur : 11.8.3-MariaDB-ubu2404
-- Version de PHP : 8.2.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

START TRANSACTION;

SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!40101 SET NAMES utf8mb4 */
;

--
-- Base de données : `greentown`
--

-- --------------------------------------------------------

--
-- Structure de la table `activeactivities`
--

CREATE TABLE `activeactivities` (
    `action` varchar(32) NOT NULL,
    `group_name` varchar(64) NOT NULL,
    `started_at` datetime NOT NULL,
    `ends_at` datetime NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `armes`
--

CREATE TABLE `armes` (
    `ID` int(11) NOT NULL,
    `Nom` varchar(255) NOT NULL,
    `Groupe` varchar(255) DEFAULT NULL,
    `Propre` varchar(25) DEFAULT NULL,
    `Sale` varchar(25) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `armes`
--

INSERT INTO
    `armes` (
        `ID`,
        `Nom`,
        `Groupe`,
        `Propre`,
        `Sale`
    )
VALUES (
        1,
        'Arme blanche',
        NULL,
        NULL,
        NULL
    ),
    (
        2,
        'Beretta 96',
        NULL,
        NULL,
        NULL
    ),
    (
        3,
        'Five-Seven',
        NULL,
        NULL,
        NULL
    ),
    (
        4,
        'Walter PPK',
        NULL,
        NULL,
        NULL
    ),
    (
        6,
        'Desert-Eagle',
        NULL,
        NULL,
        NULL
    ),
    (
        7,
        'Glock18C',
        NULL,
        NULL,
        NULL
    ),
    (8, 'MAC11', NULL, NULL, NULL),
    (
        9,
        'Revolver',
        NULL,
        NULL,
        NULL
    ),
    (
        10,
        'Scorpion',
        NULL,
        NULL,
        NULL
    ),
    (11, 'Tec9', NULL, NULL, NULL),
    (12, 'UZI', NULL, NULL, NULL),
    (
        13,
        'Winchester',
        NULL,
        NULL,
        NULL
    ),
    (
        14,
        'Canon Scié',
        NULL,
        NULL,
        NULL
    ),
    (15, 'AKM', NULL, NULL, NULL),
    (16, 'AKU', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `drogues`
--

CREATE TABLE `drogues` (
    `ID` int(11) NOT NULL,
    `Nom` varchar(255) NOT NULL,
    `Groupe` varchar(255) DEFAULT NULL,
    `Propre` varchar(255) DEFAULT NULL,
    `Sale` varchar(255) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `drogues`
--

INSERT INTO
    `drogues` (
        `ID`,
        `Nom`,
        `Groupe`,
        `Propre`,
        `Sale`
    )
VALUES (
        3,
        'Cocaine',
        NULL,
        NULL,
        NULL
    ),
    (5, 'Weed', NULL, NULL, NULL),
    (9, 'Meth', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `globalcooldowns`
--

CREATE TABLE `globalcooldowns` (
    `action` varchar(32) NOT NULL,
    `available_at` datetime NOT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `groupdailycounts`
--

CREATE TABLE `groupdailycounts` (
    `action` varchar(32) NOT NULL,
    `group_name` varchar(64) NOT NULL,
    `day` date NOT NULL,
    `count` int(11) NOT NULL DEFAULT 0
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `message`
--

CREATE TABLE `message` (
    `Nom` varchar(255) NOT NULL,
    `ID_Salon` bigint(20) DEFAULT NULL,
    `ID_Message` bigint(20) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `message`
--

INSERT INTO
    `message` (
        `Nom`,
        `ID_Salon`,
        `ID_Message`
    )
VALUES (
        'Armes',
        1410270613498495046,
        1413560041314717865
    ),
    (
        'Drogues',
        1410270613498495046,
        1413560047841316944
    ),
    (
        'Munitions',
        1410270613498495046,
        1413560044880138447
    ),
    (
        'Outils',
        1410270613498495046,
        1413560050345050144
    ),
    (
        'Visa',
        1410270613498495046,
        1413560052446662776
    );

-- --------------------------------------------------------

--
-- Structure de la table `munitions`
--

CREATE TABLE `munitions` (
    `Nom` varchar(255) NOT NULL,
    `Groupe` varchar(255) DEFAULT NULL,
    `Propre` varchar(255) DEFAULT NULL,
    `Sale` varchar(25) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `munitions`
--

INSERT INTO
    `munitions` (
        `Nom`,
        `Groupe`,
        `Propre`,
        `Sale`
    )
VALUES ('12 gauge', NULL, NULL, NULL),
    (
        '22 Long\r\n',
        NULL,
        NULL,
        NULL
    ),
    ('38 LC', NULL, NULL, NULL),
    ('44 Mag', NULL, NULL, NULL),
    ('45 ACP', NULL, NULL, NULL),
    (
        '5.56x45mm\r\n',
        NULL,
        NULL,
        NULL
    ),
    ('50 AE', NULL, NULL, NULL),
    ('7.62x39mm', NULL, NULL, NULL),
    ('7.62x51mm', NULL, NULL, NULL),
    ('9mm', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `outils`
--

CREATE TABLE `outils` (
    `Nom` varchar(255) NOT NULL,
    `Groupe` varchar(255) DEFAULT NULL,
    `Propre` varchar(255) DEFAULT NULL,
    `Sale` varchar(255) DEFAULT NULL
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `outils`
--

INSERT INTO
    `outils` (
        `Nom`,
        `Groupe`,
        `Propre`,
        `Sale`
    )
VALUES (
        'Clé Fantôme',
        NULL,
        NULL,
        NULL
    ),
    ('Corde ATM', NULL, NULL, '-'),
    (
        'Crochetage',
        NULL,
        NULL,
        NULL
    );

-- --------------------------------------------------------

--
-- Structure de la table `visas`
--

CREATE TABLE `visas` (
    `id` int(11) NOT NULL,
    `Nom` varchar(255) NOT NULL,
    `Prenom` varchar(255) NOT NULL,
    `DateValidite` datetime NOT NULL,
    `Valide` tinyint(1) NOT NULL DEFAULT 1,
    `DelivrePar` varchar(255) DEFAULT NULL,
    `Type` enum(
        'travaille',
        'vacances',
        'autre'
    ) NOT NULL DEFAULT 'autre',
    `CreatedAt` datetime NOT NULL DEFAULT current_timestamp(),
    `UpdatedAt` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_general_ci;

--
-- Déchargement des données de la table `visas`
--

INSERT INTO
    `visas` (
        `id`,
        `Nom`,
        `Prenom`,
        `DateValidite`,
        `Valide`,
        `DelivrePar`,
        `Type`,
        `CreatedAt`,
        `UpdatedAt`
    )
VALUES (
        1,
        'Powell',
        'Tony',
        '2025-08-27 21:06:31',
        0,
        '05 | Tony Powell',
        'travaille',
        '2025-08-27 20:06:31',
        '2025-08-27 20:09:55'
    );

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `activeactivities`
--
ALTER TABLE `activeactivities`
ADD PRIMARY KEY (
    `action`,
    `group_name`,
    `started_at`
),
ADD KEY `idx_active_until` (`ends_at`);

--
-- Index pour la table `armes`
--
ALTER TABLE `armes`
ADD PRIMARY KEY (`ID`),
ADD KEY `idx_armes_nom` (`Nom`);

--
-- Index pour la table `drogues`
--
ALTER TABLE `drogues`
ADD PRIMARY KEY (`ID`),
ADD KEY `idx_drogues_nom` (`Nom`);

--
-- Index pour la table `globalcooldowns`
--
ALTER TABLE `globalcooldowns`
ADD PRIMARY KEY (`action`),
ADD KEY `idx_available_at` (`available_at`);

--
-- Index pour la table `groupdailycounts`
--
ALTER TABLE `groupdailycounts`
ADD PRIMARY KEY (`action`, `group_name`, `day`),
ADD KEY `idx_day` (`day`);

--
-- Index pour la table `message`
--
ALTER TABLE `message` ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `munitions`
--
ALTER TABLE `munitions` ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `outils`
--
ALTER TABLE `outils` ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `visas`
--
ALTER TABLE `visas`
ADD PRIMARY KEY (`id`),
ADD KEY `idx_nom_prenom` (`Nom`, `Prenom`),
ADD KEY `idx_date_validite` (`DateValidite`),
ADD KEY `idx_valide` (`Valide`),
ADD KEY `idx_nom_prenom_date` (
    `Nom`,
    `Prenom`,
    `DateValidite`
);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `armes`
--
ALTER TABLE `armes`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 20;

--
-- AUTO_INCREMENT pour la table `drogues`
--
ALTER TABLE `drogues`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 17;

--
-- AUTO_INCREMENT pour la table `visas`
--
ALTER TABLE `visas`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,
AUTO_INCREMENT = 2;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;