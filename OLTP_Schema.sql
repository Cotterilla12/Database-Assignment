-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.5.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table irradiationevents.devicetable
CREATE TABLE IF NOT EXISTS `devicetable` (
  `DeviceSerialNumber` varchar(20) NOT NULL DEFAULT '',
  `StationName` varchar(20) DEFAULT '',
  `InstitutionName` varchar(20) DEFAULT '',
  `InstitutionAddress` varchar(45) DEFAULT '',
  `ModelName` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`DeviceSerialNumber`),
  UNIQUE KEY `DeviceSerialNumber` (`DeviceSerialNumber`),
  KEY `FK_devicetable_manufacturertable` (`ModelName`),
  CONSTRAINT `FK_devicetable_manufacturertable` FOREIGN KEY (`ModelName`) REFERENCES `manufacturertable` (`ModelName`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationevents.irradiationevent
CREATE TABLE IF NOT EXISTS `irradiationevent` (
  `IrradiationEventUID` varchar(70) NOT NULL,
  `SeriesUID` varchar(70) NOT NULL,
  `ScanningLength` double NOT NULL DEFAULT 0,
  `MeanCTDIvol` decimal(6,3) NOT NULL DEFAULT 0.000,
  `DLP` decimal(6,3) NOT NULL DEFAULT 0.000,
  `SizeSpecificDoseEstimation` decimal(6,3) DEFAULT 0.000,
  `CTDIwPhantomType` varchar(60) NOT NULL,
  `MaximumXRayTubeCurrent` decimal(6,3) NOT NULL DEFAULT 0.000,
  `XRayTubeCurrent` decimal(6,3) NOT NULL DEFAULT 0.000,
  `PitchFactor` decimal(6,3) DEFAULT 0.000,
  `ExposureTime` decimal(6,3) NOT NULL DEFAULT 0.000,
  `NominalSingleCollimationWidth` double NOT NULL DEFAULT 0,
  `NominalTotalCollimationWidth` double NOT NULL DEFAULT 0,
  `kVPeak` double NOT NULL DEFAULT 0,
  `TargetRegion` varchar(30) DEFAULT NULL,
  `AcquisitionType` varchar(60) DEFAULT NULL,
  `ProcedureContext` varchar(60) DEFAULT NULL,
  `DeviceSpecificAcquisitionProtocol` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`IrradiationEventUID`),
  UNIQUE KEY `IrradiationEventUID` (`IrradiationEventUID`),
  KEY `FK_irradiationevent_seriesdetails` (`SeriesUID`),
  CONSTRAINT `FK_irradiationevent_seriesdetails` FOREIGN KEY (`SeriesUID`) REFERENCES `seriesdetails` (`SeriesUID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationevents.manufacturertable
CREATE TABLE IF NOT EXISTS `manufacturertable` (
  `ModelName` varchar(45) NOT NULL DEFAULT '',
  `Manufacturer` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`ModelName`),
  UNIQUE KEY `ModelName` (`ModelName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationevents.seriesdetails
CREATE TABLE IF NOT EXISTS `seriesdetails` (
  `SeriesUID` varchar(70) NOT NULL,
  `StudyUID` varchar(70) NOT NULL,
  `Operator` varchar(30) DEFAULT NULL,
  `IrradiationStart` datetime DEFAULT NULL,
  `IrradiationEnd` datetime DEFAULT NULL,
  `ExposureIntent` varchar(30) DEFAULT NULL,
  `DoseInformationSource` varchar(30) DEFAULT NULL,
  `ReportedProcedure` varchar(40) DEFAULT NULL,
  `DeviceSerialNumber` varchar(20) NOT NULL,
  `SoftwareVersion` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`SeriesUID`),
  UNIQUE KEY `SeriesUID` (`SeriesUID`),
  KEY `FK_seriesdetails_studydetails` (`StudyUID`),
  KEY `FK_seriesdetails_devicetable` (`DeviceSerialNumber`),
  CONSTRAINT `FK_seriesdetails_devicetable` FOREIGN KEY (`DeviceSerialNumber`) REFERENCES `devicetable` (`DeviceSerialNumber`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_seriesdetails_studydetails` FOREIGN KEY (`StudyUID`) REFERENCES `studydetails` (`StudyUID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationevents.studydetails
CREATE TABLE IF NOT EXISTS `studydetails` (
  `StudyUID` varchar(70) NOT NULL,
  `Description` varchar(45) DEFAULT NULL,
  `ReferringPhysician` varchar(45) DEFAULT NULL,
  `PatientID` varchar(12) NOT NULL,
  PRIMARY KEY (`StudyUID`),
  UNIQUE KEY `StudyUID` (`StudyUID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
