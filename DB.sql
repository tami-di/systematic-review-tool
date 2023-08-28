SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `papers` DEFAULT CHARACTER SET utf8 ;
USE `papers` ;

DROP TABLE IF EXISTS papers.int_cat;
DROP TABLE IF EXISTS papers.cat_cont;
DROP TABLE IF EXISTS papers.paper_has_cont;
DROP TABLE IF EXISTS papers.paper_has_authors;
DROP TABLE IF EXISTS papers.interaction;
DROP TABLE IF EXISTS papers.content;
DROP TABLE IF EXISTS papers.categories;
DROP TABLE IF EXISTS papers.author;
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

CREATE TABLE papers.author (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(50) DEFAULT NULL,
  affiliation text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.categories (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  description text,
  extra text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.content (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  description text,
  extra text,
  extra_int text,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.interaction (
  id mediumint(9) NOT NULL AUTO_INCREMENT,
  name varchar(100) DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.paper_has_authors (
  author_id mediumint(9) NOT NULL,
  paper_id int(11) NOT NULL,
  KEY author_id (author_id),
  KEY paper_n_id (paper_id),
  FOREIGN KEY (author_id) REFERENCES author (id),
  FOREIGN KEY (paper_id) REFERENCES paper (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.paper_has_cont (
  paper_id int(11) NOT NULL,
  cat_id mediumint(9) NOT NULL,
  cont_id mediumint(9) NOT NULL,
  KEY paper_id (paper_id),
  KEY cat_id (cat_id),
  KEY cont_id (cont_id),
  FOREIGN KEY (paper_id) REFERENCES paper (id),
  FOREIGN KEY (cat_id) REFERENCES categories (id),
  FOREIGN KEY (cont_id) REFERENCES content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.cat_cont (
  cat_id mediumint(9) NOT NULL,
  cont_id mediumint(9) NOT NULL,
  KEY cat_id (cat_id),
  KEY cont_id (cont_id),
  FOREIGN KEY (cat_id) REFERENCES categories (id),
  FOREIGN KEY (cont_id) REFERENCES content (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE papers.int_cat (
  cat_id mediumint(9) NOT NULL,
  int_id mediumint(9) NOT NULL,
  name varchar(200) NOT NULL,
  KEY cat_id (cat_id),
  KEY int_id (int_id),
  FOREIGN KEY (cat_id) REFERENCES categories (id),
  FOREIGN KEY (int_id) REFERENCES interaction (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
