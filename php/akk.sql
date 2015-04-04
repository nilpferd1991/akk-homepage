-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Erstellungszeit: 04. Apr 2015 um 12:58
-- Server Version: 5.5.41-0ubuntu0.14.04.1
-- PHP-Version: 5.5.9-1ubuntu4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Datenbank: `akk`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `artists`
--

CREATE TABLE IF NOT EXISTS `artists` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`artist_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `dances`
--

CREATE TABLE IF NOT EXISTS `dances` (
  `dance_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`dance_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `notes`
--

CREATE TABLE IF NOT EXISTS `notes` (
  `note_id` int(11) NOT NULL AUTO_INCREMENT,
  `song_id` int(11) NOT NULL,
  `note` text NOT NULL,
  `date_created` date NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` tinyint(4) NOT NULL,
  PRIMARY KEY (`note_id`),
  KEY `song_id` (`song_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `playlists`
--

CREATE TABLE IF NOT EXISTS `playlists` (
  `playlist_id` int(11) NOT NULL AUTO_INCREMENT,
  `date_created` date NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `songlists`
--

CREATE TABLE IF NOT EXISTS `songlists` (
  `songlist_id` int(11) NOT NULL AUTO_INCREMENT,
  `playlist_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `song_number` int(11) NOT NULL,
  PRIMARY KEY (`songlist_id`),
  KEY `playlist_id` (`playlist_id`),
  KEY `song_id` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `songs`
--

CREATE TABLE IF NOT EXISTS `songs` (
  `song_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `dance_id` int(11) NOT NULL,
  PRIMARY KEY (`song_id`),
  UNIQUE KEY `title` (`title`),
  KEY `dance_id` (`dance_id`),
  KEY `artist_id` (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `password_hash` binary(123) NOT NULL,
  `password_salt` binary(123) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`),
  ADD CONSTRAINT `notes_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints der Tabelle `playlists`
--
ALTER TABLE `playlists`
  ADD CONSTRAINT `playlists_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints der Tabelle `songlists`
--
ALTER TABLE `songlists`
  ADD CONSTRAINT `songlists_ibfk_1` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`),
  ADD CONSTRAINT `songlists_ibfk_2` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);

--
-- Constraints der Tabelle `songs`
--
ALTER TABLE `songs`
  ADD CONSTRAINT `songs_ibfk_1` FOREIGN KEY (`dance_id`) REFERENCES `dances` (`dance_id`),
  ADD CONSTRAINT `songs_ibfk_2` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
