-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : mer. 07 août 2024 à 18:21
-- Version du serveur : 11.3.2-MariaDB-1:11.3.2+maria~deb12
-- Version de PHP : 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `s19886_Bot`
--

-- --------------------------------------------------------

--
-- Structure de la table `Armes`
--

CREATE TABLE `Armes` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `AvecP` varchar(25) DEFAULT NULL,
  `SansP` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Armes`
--

INSERT INTO `Armes` (`Nom`, `Groupe`, `AvecP`, `SansP`) VALUES
('AKM', NULL, NULL, NULL),
('AKU', NULL, NULL, NULL),
('Beretta 96', NULL, NULL, NULL),
('Canon Scié', NULL, NULL, NULL),
('Desert-Eagle', NULL, NULL, NULL),
('Five-Seven', NULL, NULL, NULL),
('Fn Model 1970', NULL, NULL, NULL),
('Glock18C', NULL, NULL, NULL),
('MAC11', NULL, NULL, NULL),
('Revolver', NULL, NULL, NULL),
('Scorpion', NULL, NULL, NULL),
('Tec9', NULL, NULL, NULL),
('UZI', NULL, NULL, NULL),
('Walter PPK', NULL, NULL, NULL),
('Winchester', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Drogues`
--

CREATE TABLE `Drogues` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Prix_Unité` varchar(255) DEFAULT NULL,
  `Prix_100` varchar(255) DEFAULT NULL,
  `Prix_1000` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Drogues`
--

INSERT INTO `Drogues` (`Nom`, `Groupe`, `Prix_Unité`, `Prix_100`, `Prix_1000`) VALUES
('Champignon', NULL, NULL, NULL, NULL),
('Coke', NULL, NULL, NULL, NULL),
('Opium', NULL, NULL, NULL, NULL),
('Oz Kush', NULL, NULL, NULL, NULL),
('White weedo', NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Message`
--

CREATE TABLE `Message` (
  `Nom` varchar(255) NOT NULL,
  `ID_Salon` bigint(20) DEFAULT NULL,
  `ID_Message` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Message`
--

INSERT INTO `Message` (`Nom`, `ID_Salon`, `ID_Message`) VALUES
('Armes', 1270698488228876298, 1270771184929210390),
('Drogues', 1270753203687784620, 1270771190692053044),
('Munitions', 1270698488228876298, 1270771187022299136),
('Outils', 1270776614258479124, NULL),
('Ventes', 1270776598580297819, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Munitions`
--

CREATE TABLE `Munitions` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Prix` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Munitions`
--

INSERT INTO `Munitions` (`Nom`, `Groupe`, `Prix`) VALUES
('44 magnum', NULL, NULL),
('45 ACP', NULL, NULL),
('7.62', NULL, NULL),
('9mm', NULL, NULL),
('Cal 12.', NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Outils`
--

CREATE TABLE `Outils` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Prix_Unité` varchar(255) DEFAULT NULL,
  `Prix_100` varchar(255) DEFAULT NULL,
  `Prix_500` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `Stock`
--

CREATE TABLE `Stock` (
  `id` int(11) NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Stock`
--

INSERT INTO `Stock` (`id`, `item_name`, `quantity`) VALUES
(1, 'clé ATM', 81),
(2, 'crochetage', 218),
(3, 'clée de banque', 8),
(4, 'thermite', 3);

-- --------------------------------------------------------

--
-- Structure de la table `Ventes`
--

CREATE TABLE `Ventes` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Drogue` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Armes`
--
ALTER TABLE `Armes`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Drogues`
--
ALTER TABLE `Drogues`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Message`
--
ALTER TABLE `Message`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Munitions`
--
ALTER TABLE `Munitions`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Outils`
--
ALTER TABLE `Outils`
  ADD PRIMARY KEY (`Nom`);

--
-- Index pour la table `Stock`
--
ALTER TABLE `Stock`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `Ventes`
--
ALTER TABLE `Ventes`
  ADD PRIMARY KEY (`Nom`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `Stock`
--
ALTER TABLE `Stock`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
