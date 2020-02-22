-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: anime_db
-- ------------------------------------------------------
-- Server version	5.7.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anime_genre`
--

DROP TABLE IF EXISTS `anime_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anime_genre` (
  `id_anime` varchar(20) NOT NULL,
  `id_genre` varchar(20) NOT NULL,
  PRIMARY KEY (`id_anime`,`id_genre`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `animes`
--

DROP TABLE IF EXISTS `animes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animes` (
  `id` varchar(20) CHARACTER SET latin1 NOT NULL,
  `id_api` varchar(45) DEFAULT NULL,
  `name` varchar(200) CHARACTER SET latin1 DEFAULT NULL,
  `description` longtext CHARACTER SET latin1,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `averageScore` float DEFAULT NULL,
  `popularity` int(11) DEFAULT NULL,
  `format` varchar(45) DEFAULT NULL,
  `bannerImage` varchar(200) DEFAULT NULL,
  `coverImage` varchar(200) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `slug` varchar(200) NOT NULL,
  `t` varchar(45) NOT NULL DEFAULT 't',
  PRIMARY KEY (`id`),
  UNIQUE KEY `slog_UNIQUE` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `banners`
--

DROP TABLE IF EXISTS `banners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `banners` (
  `id_api` varchar(45) NOT NULL,
  `name` varchar(200) NOT NULL,
  `slug` varchar(200) NOT NULL,
  `bannerImage` varchar(200) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `episodes`
--

DROP TABLE IF EXISTS `episodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `episodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_anime` varchar(45) NOT NULL,
  `episode` varchar(45) NOT NULL,
  `index_ep` int(11) NOT NULL,
  `links` longtext,
  `posted_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=115671 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `get_latest_episodes`
--

DROP TABLE IF EXISTS `get_latest_episodes`;
/*!50001 DROP VIEW IF EXISTS `get_latest_episodes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `get_latest_episodes` AS SELECT 
 1 AS `id`,
 1 AS `id_api`,
 1 AS `name`,
 1 AS `slug`,
 1 AS `episode`,
 1 AS `id_episode`,
 1 AS `coverImage`,
 1 AS `index_ep`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'anime_db'
--

--
-- Final view structure for view `get_latest_episodes`
--

/*!50001 DROP VIEW IF EXISTS `get_latest_episodes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `get_latest_episodes` AS select `an`.`id` AS `id`,`an`.`id_api` AS `id_api`,`an`.`name` AS `name`,`an`.`slug` AS `slug`,`eps`.`episode` AS `episode`,`eps`.`id` AS `id_episode`,`an`.`coverImage` AS `coverImage`,`temp`.`index_ep` AS `index_ep` from ((`anime_db`.`animes` `an` join (select `anime_db`.`episodes`.`id_anime` AS `id_anime`,max(`anime_db`.`episodes`.`index_ep`) AS `index_ep` from `anime_db`.`episodes` group by `anime_db`.`episodes`.`id_anime`) `temp`) join `anime_db`.`episodes` `eps`) where ((`an`.`id` = `temp`.`id_anime`) and (`an`.`id` = `eps`.`id_anime`) and (`temp`.`index_ep` = `eps`.`index_ep`)) order by `eps`.`posted_time` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-23  0:16:40
