-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le : dim. 11 août 2024 à 18:16
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
  `ID` int(11) NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `AvecP` varchar(25) DEFAULT NULL,
  `SansP` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Armes`
--

INSERT INTO `Armes` (`ID`, `Nom`, `Groupe`, `AvecP`, `SansP`) VALUES
(1, 'Arme blanche', 'OBlock', NULL, NULL),
(2, 'Beretta 96', 'Aztécas', NULL, NULL),
(3, 'Five-Seven', 'Vagos', '300K', '400K'),
(4, 'Walter PPK', 'OBlock', NULL, NULL),
(5, 'Fn Model 1970', NULL, NULL, NULL),
(6, 'Desert-Eagle', 'HB', '550K', '650K'),
(7, 'Glock18C', 'Hoover', NULL, NULL),
(8, 'MAC11', NULL, NULL, NULL),
(9, 'Revolver', 'MI', NULL, NULL),
(10, 'Scorpion', NULL, NULL, NULL),
(11, 'Tec9', 'BMF', NULL, NULL),
(12, 'UZI', NULL, NULL, NULL),
(13, 'Winchester', NULL, NULL, NULL),
(14, 'Canon Scié', NULL, NULL, NULL),
(15, 'AKM', NULL, NULL, NULL),
(16, 'AKU', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `Drogues`
--

CREATE TABLE `Drogues` (
  `ID` int(11) NOT NULL,
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Prix_Unité` varchar(255) DEFAULT NULL,
  `Prix_100` varchar(255) DEFAULT NULL,
  `Prix_1000` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Drogues`
--

INSERT INTO `Drogues` (`ID`, `Nom`, `Groupe`, `Prix_Unité`, `Prix_100`, `Prix_1000`) VALUES
(1, 'Champignon', NULL, NULL, NULL, NULL),
(2, 'Graine Champignon', NULL, NULL, NULL, NULL),
(3, 'Coke', 'Cayo - NY', NULL, NULL, NULL),
(4, 'Graine Coke', NULL, NULL, NULL, NULL),
(5, 'OG Kush', 'H-Block', NULL, NULL, NULL),
(6, 'Graine OG Kush', NULL, NULL, NULL, NULL),
(7, 'White Widow', 'Harlem Boyz', NULL, NULL, NULL),
(8, 'Graine White Widow', NULL, NULL, NULL, NULL),
(9, 'Opium', NULL, NULL, NULL, NULL),
(16, 'Graine Opium', NULL, NULL, NULL, NULL);

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
('Armes', 1254931410754600961, 1271262066291900487),
('Drogues', 1270781340865790023, 1271128679874953342),
('Munitions', 1254931410754600961, 1271128677379473450),
('Outils', 1270780742414106684, 1271259926257209480),
('Ventes', 1270781184997326949, 1271128689647685693);

-- --------------------------------------------------------

--
-- Structure de la table `Munitions`
--

CREATE TABLE `Munitions` (
  `Nom` varchar(255) NOT NULL,
  `Groupe` varchar(255) DEFAULT NULL,
  `Prix` varchar(255) DEFAULT NULL,
  `Prix500` varchar(25) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `Munitions`
--

INSERT INTO `Munitions` (`Nom`, `Groupe`, `Prix`, `Prix500`) VALUES
('44 magnum', 'BMF', NULL, NULL),
('45 ACP', NULL, NULL, NULL),
('7.62', NULL, NULL, NULL),
('9mm', 'BMF', NULL, NULL),
('Cal 12.', NULL, NULL, NULL);

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

--
-- Déchargement des données de la table `Outils`
--

INSERT INTO `Outils` (`Nom`, `Groupe`, `Prix_Unité`, `Prix_100`, `Prix_500`) VALUES
('Clé ATM', 'Vagos', NULL, '-', NULL),
('Clé Fleeca', 'SOA', NULL, NULL, NULL),
('Crochetage', 'Hoover', '6000', NULL, NULL),
('Thermites', 'SOA', NULL, NULL, NULL);

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
(1, 'clé ATM', 76),
(2, 'crochetage', 212),
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
-- Déchargement des données de la table `Ventes`
--

INSERT INTO `Ventes` (`Nom`, `Groupe`, `Drogue`) VALUES
('Fête-Foraine', 'Vagos', 'OG Kush'),
('Grapeseed ', NULL, 'Champignons'),
('Mirror Park', 'OBlock', 'White Widow'),
('Paleto', 'HB', 'Champignons'),
('Plage', 'SouthSide', 'Opium'),
('Université ', 'OBlock', 'Champignons'),
('Vinewood', 'BMF', 'Coke');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Armes`
--
ALTER TABLE `Armes`
  ADD PRIMARY KEY (`ID`);

--
-- Index pour la table `Drogues`
--
ALTER TABLE `Drogues`
  ADD PRIMARY KEY (`ID`);

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
-- AUTO_INCREMENT pour la table `Armes`
--
ALTER TABLE `Armes`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT pour la table `Drogues`
--
ALTER TABLE `Drogues`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `Stock`
--
ALTER TABLE `Stock`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
