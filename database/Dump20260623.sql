CREATE DATABASE  IF NOT EXISTS `grandmas_recipes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `grandmas_recipes`;
-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: grandmas_recipes
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'mohansai','mohan');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  KEY `variant_id` (`variant_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cart_ibfk_3` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,1,1,1,2,'2026-06-15 05:38:11'),(2,1,2,4,1,'2026-06-15 05:38:11'),(35,2,2,5,1,'2026-06-22 15:55:21');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `variant_id` int DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  KEY `variant_id` (`variant_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `order_items_ibfk_3` FOREIGN KEY (`variant_id`) REFERENCES `product_variants` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Placed',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `address` text,
  `phone` varchar(20) DEFAULT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_status` varchar(50) DEFAULT NULL,
  `order_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `product_name` varchar(255) DEFAULT NULL,
  `product_image` varchar(255) DEFAULT NULL,
  `product_price` int DEFAULT NULL,
  `delivery_charge` int DEFAULT '0',
  `quantity` int DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (55,2,500.00,'Placed','2026-06-21 15:12:34','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-21 15:12:34','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',500,30,1),(56,2,260.00,'Placed','2026-06-22 08:27:07','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan',NULL,'Paid','2026-06-22 08:27:07','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',260,50,1),(57,2,140.00,'Placed','2026-06-22 08:28:53','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','Card','Paid','2026-06-22 08:28:53','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',140,50,1),(58,2,260.00,'Placed','2026-06-22 08:37:17','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 08:37:17','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',260,50,1),(59,2,140.00,'Placed','2026-06-22 08:57:45','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 08:57:45','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',140,0,1),(60,2,140.00,'Placed','2026-06-22 09:22:47','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','Google Pay','Paid','2026-06-22 09:22:47','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',140,0,1),(61,2,140.00,'Placed','2026-06-22 13:11:09','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 13:11:09','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',140,0,1),(62,2,260.00,'Delivered','2026-06-22 13:13:43','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 13:13:43','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',260,0,1),(63,2,520.00,'Placed','2026-06-22 15:35:29','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 15:35:29','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',260,0,2),(64,2,260.00,'Placed','2026-06-22 17:22:04','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-22 17:22:04','Grandma Special Kaju Karam Boondi','kaju_karam_boondi.jpeg',260,0,1),(65,2,260.00,'Delivered','2026-06-23 14:13:41','PEDDIREDDY VARI STREET,SALIPETA,  JANGAREDDYGUDEM ., Andhra Pradesh, 534447','9676346594','mohan','PhonePe','Paid','2026-06-23 14:13:41','Rava Laddu','rava_laddu.jpeg',260,0,1);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_method` varchar(50) DEFAULT NULL,
  `payment_status` varchar(50) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `payment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_variants`
--

DROP TABLE IF EXISTS `product_variants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_variants` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `weight` varchar(20) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `product_variants_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_variants`
--

LOCK TABLES `product_variants` WRITE;
/*!40000 ALTER TABLE `product_variants` DISABLE KEYS */;
INSERT INTO `product_variants` VALUES (1,1,'250g',150.00),(2,1,'500g',200.00),(3,1,'1kg',500.00),(4,2,'250g',140.00),(5,2,'500g',260.00),(6,2,'1kg',500.00),(7,3,'250g',130.00),(8,3,'500g',240.00),(9,3,'1kg',460.00),(10,4,'250g',130.00),(11,4,'500g',250.00),(12,4,'1kg',480.00),(13,5,'250g',120.00),(14,5,'500g',230.00),(15,5,'1kg',440.00),(16,6,'250g',180.00),(17,6,'500g',350.00),(18,6,'1kg',680.00),(19,7,'250g',150.00),(20,7,'500g',280.00),(21,7,'1kg',540.00),(22,8,'250g',140.00),(23,8,'500g',260.00),(24,8,'1kg',500.00),(25,9,'250g',130.00),(26,9,'500g',250.00),(27,9,'1kg',480.00),(28,10,'250g',150.00),(29,10,'500g',250.00),(30,10,'1kg',500.00),(31,11,'250g',130.00),(32,11,'500g',250.00),(33,11,'1kg',480.00),(34,12,'250g',140.00),(35,12,'500g',270.00),(36,12,'1kg',520.00),(37,13,'250g',150.00),(38,13,'500g',300.00),(39,13,'1kg',580.00);
/*!40000 ALTER TABLE `product_variants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `description` text,
  `image` varchar(255) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Jantikulu','Crunchy traditional snack','jantikulu.jpeg','Hot Items'),(2,'Grandma Special Kaju Karam Boondi','Spicy sweet boondi mix','kaju_karam_boondi.jpeg','Hot Items'),(3,'Chekkalu','Rice flour crispy snack','chekkalu.jpeg','Hot Items'),(4,'Hot Gulabi Puvvulu','Spicy sweet snack','hot_gulabi_puvvulu.jpeg','Hot Items'),(5,'Karapusa','Crispy spicy snack','karapusa.jpeg','Hot Items'),(6,'Dry Fruit Ariselu','Premium dry fruit sweet','dry_fruit_ariselu.jpeg','Signature Items'),(7,'Sunnundalu','Healthy traditional sweet','sunnundalu.jpeg','Sweets'),(8,'Rava Laddu','Soft and delicious sweet','rava_laddu.jpeg','Sweets'),(9,'Ribbon Pakoda','Crunchy ribbon shaped snack','ribbon_pakoda.jpeg','Hot Items'),(10,'Grandma Ghee Bobbatlu','Pure ghee stuffed sweet','ghee_bobbatlu.jpeg','Sweets'),(11,'Gavvalu','Traditional shell shaped sweet','gavvalu.jpeg','Sweets'),(12,'Sweet Gulabi Puvvulu','Flower shaped sweet snack','sweet_gulabi_puvvulu.jpeg','Sweets'),(13,' Dry Frit Kajjikayalu','Coconut stuffed sweet','kajjikayalu.jpeg','Signature Items');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `address` text,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(10) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `profile_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Nikhitha','[nikhitha485@gmail.com]','9676346594','967634',NULL,NULL,NULL,NULL,'2026-06-15 05:37:24',NULL),(2,'mohan','mohan@gmail.com','9676346594','mohan123','PEDDIREDDY VARI STREET,SALIPETA',' JANGAREDDYGUDEM .','Andhra Pradesh','534447','2026-06-15 06:17:22',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
INSERT INTO `wishlist` VALUES (19,2,2),(22,2,7);
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-23 20:44:48
