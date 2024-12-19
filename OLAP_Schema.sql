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

-- Dumping structure for table irradiationfacts.devicedetailsdimtable
CREATE TABLE IF NOT EXISTS `devicedetailsdimtable` (
  `DeviceSerialNumber` varchar(20) NOT NULL DEFAULT '',
  `StationName` varchar(20) DEFAULT '',
  `InstitutionName` varchar(20) DEFAULT '',
  `InstitutionAddress` varchar(45) DEFAULT '',
  `Model` varchar(30) NOT NULL DEFAULT '',
  `Manufacturer` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`DeviceSerialNumber`),
  UNIQUE KEY `DeviceSerialNumber` (`DeviceSerialNumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationfacts.irradiationeventdimtable
CREATE TABLE IF NOT EXISTS `irradiationeventdimtable` (
  `IrradiationEventUID` varchar(70) NOT NULL,
  `StudyUID` varchar(70) NOT NULL,
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
  `DeviceSerialNumber` varchar(20) NOT NULL,
  `StationName` varchar(20) NOT NULL,
  `Operator` varchar(50) DEFAULT NULL,
  `StartOfExposure` datetime NOT NULL,
  `EndOfExposure` datetime DEFAULT NULL,
  PRIMARY KEY (`IrradiationEventUID`),
  UNIQUE KEY `IrradiationEventUID` (`IrradiationEventUID`),
  KEY `FK_irradiationeventdimtable_irradiationfacttable` (`StudyUID`),
  KEY `FK_irradiationeventdimtable_devicedetailsdimtable` (`DeviceSerialNumber`),
  CONSTRAINT `FK_irradiationeventdimtable_devicedetailsdimtable` FOREIGN KEY (`DeviceSerialNumber`) REFERENCES `devicedetailsdimtable` (`DeviceSerialNumber`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_irradiationeventdimtable_irradiationfacttable` FOREIGN KEY (`StudyUID`) REFERENCES `irradiationfacttable` (`StudyUID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

-- Dumping structure for table irradiationfacts.irradiationfacttable
CREATE TABLE IF NOT EXISTS `irradiationfacttable` (
  `StudyUID` varchar(70) NOT NULL,
  `TotalMeanCTDIvol` decimal(9,3) NOT NULL DEFAULT 0.000,
  `TotalDLP` decimal(9,3) NOT NULL DEFAULT 0.000,
  `TotalSizeSpecificDoseEstimation` decimal(9,3) NOT NULL DEFAULT 0.000,
  `IrradiationStart` date DEFAULT NULL,
  `IrradiationEnd` date DEFAULT NULL,
  `AmountOfIrradiationEvents` int(11) NOT NULL DEFAULT 0,
  `PatientID` varchar(8) NOT NULL,
  `Completed` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`StudyUID`),
  UNIQUE KEY `StudyUID` (`StudyUID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Data exporting was unselected.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
