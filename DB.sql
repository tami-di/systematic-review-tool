SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `papers` DEFAULT CHARACTER SET utf8 ;
USE `papers` ;

DROP TABLE IF EXISTS papers.author;
CREATE TABLE papers.author (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  affiliation text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES author WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS papers.categories;
CREATE TABLE papers.categories (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  description text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES `categories` WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS papers.subcategories;
CREATE TABLE papers.subcategories (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES subcategories WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS papers.cat_subcat_interactions;
CREATE TABLE papers.cat_subcat_interactions (
  cat_id mediumint(9) DEFAULT NULL,
  interaction varchar(100) DEFAULT NULL,
  subcat_id mediumint(9) DEFAULT NULL,
  KEY cat_id (cat_id),
  KEY subcat_id (subcat_id),
  CONSTRAINT cat_subcat_interactions_ibfk_1 FOREIGN KEY (cat_id) REFERENCES categories (id),
  CONSTRAINT cat_subcat_interactions_ibfk_2 FOREIGN KEY (subcat_id) REFERENCES subcategories (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES cat_subcat_interactions WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS papers.paper;
CREATE TABLE papers.paper (
  id int(11) NOT NULL AUTO_INCREMENT,
  title varchar(200) NOT NULL,
  library varchar(20) DEFAULT NULL,
  code_name varchar(30) DEFAULT NULL,
  year year(4) DEFAULT NULL,
  abstract text,
  summary text,
  source varchar(30) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY id (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES paper WRITE;
UNLOCK TABLES;

DROP TABLE IF EXISTS papers.paper_has_authors;
CREATE TABLE papers.paper_has_authors (
  author_id mediumint(9) DEFAULT NULL,
  paper_id int(11) DEFAULT NULL,
  KEY author_id (author_id),
  KEY paper_n_id (paper_id),
  CONSTRAINT paper_has_authors_ibfk_2 FOREIGN KEY (author_id) REFERENCES author (id),
  CONSTRAINT paper_has_authors_ibfk_3 FOREIGN KEY (paper_id) REFERENCES paper (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
LOCK TABLES paper_has_authors WRITE;
UNLOCK TABLES;
