# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:02:39 2024

@author: archie.cotterill
"""

from pydicom.tag import Tag
from datetime import datetime
import mariadb
import sys

def IrradiationEventTable(dicomObject, parentDicomObject, primary = False, seriesUID = None):
    """
    Order of Information:
        Irradiation Event UID - 113769
        Series UID - (0020,000E)
        Acquisition Protocol - 125203
        Scanning Length - 113825
        Pitch Factor - 113828
        Maximum X-Ray Tube Current (mA) - 113833
        X-Ray Tube Current (mA) - 113734
        Mean CTDIvol (mGy) - 113830
        CTDIw Phantom Type - 113835
        DLP - 113838
        Size Specific Dose Estimation - 113930
        Exposure Time - 113824
        
        irradiationEventUID,
        seriesUID,
        scanningLength,
        meanCTDIvol,
        DLP,
        sizeSpecificDoseEstimation,
        CTDIwPhantomType,
        maximumXRayTubeCurrent,
        xRayTubeCurrent,
        pitchFactor,
        exposureTime,
        nominalSingleCollimationWidth,
        nominalTotalCollimationWidth,
        kVP,
        targetRegion,
        CTAcquisitionType, 
        procedureContext)
        
    """
    irradiationEventUIDDataset = SearchForCodeValue(dicomObject, "113769")
    irradiationEventUID = irradiationEventUIDDataset.get(Tag(0x0040,0xA124)).value
    
    if irradiationEventUID is None or irradiationEventUID == "":
        raise ValueError("Irradiation Event UID invalid, moving to next")
    
    if primary:
        return irradiationEventUID
    
    if seriesUID is None:
        seriesUID = parentDicomObject.get(Tag(0x0020,0x000E)).value
    
    scanningLengthDataset = SearchForCodeValue(dicomObject, "113825")
    scanningLength = float(scanningLengthDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    pitchFactorDataset = SearchForCodeValue(dicomObject, "113828")
    if pitchFactorDataset is not None:
        pitchFactor = float(pitchFactorDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    else:
        pitchFactor = None
    
    maximumXRayTubeCurrentDataset = SearchForCodeValue(dicomObject, "113833")
    maximumXRayTubeCurrent = float(maximumXRayTubeCurrentDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    xRayTubeCurrentDataset = SearchForCodeValue(dicomObject, "113734")
    xRayTubeCurrent = float(xRayTubeCurrentDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    meanCTDIvolDataset = SearchForCodeValue(dicomObject, "113830")
    meanCTDIvol = float(meanCTDIvolDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    CTDIwPhantomTypeDataset = SearchForCodeValue(dicomObject, "113835")
    CTDIwPhantomType = CTDIwPhantomTypeDataset.get(Tag(0x0040,0xA168)).value._list[0].get(Tag(0x0008,0x0104)).value
    
    DLPDataset = SearchForCodeValue(dicomObject, "113838")
    DLP = float(DLPDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    sizeSpecificDoseEstimationDataset = SearchForCodeValue(dicomObject, "113930")
    if sizeSpecificDoseEstimationDataset is not None:
        sizeSpecificDoseEstimation = float(sizeSpecificDoseEstimationDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    else:
        sizeSpecificDoseEstimation = None
    
    exposureTimeDataset = SearchForCodeValue(dicomObject, "113824")
    exposureTime = float(exposureTimeDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
        
    nominalSingleCollimationWidthDataset = SearchForCodeValue(dicomObject, "113826")
    nominalSingleCollimationWidth = float(nominalSingleCollimationWidthDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    nominalTotalCollimationWidthDataset = SearchForCodeValue(dicomObject, "113827")
    nominalTotalCollimationWidth = float(nominalTotalCollimationWidthDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    kVPDataset = SearchForCodeValue(dicomObject, "113733")
    kVP = float(kVPDataset.get(Tag(0x0040,0xA300)).value._list[0].get(Tag(0x0040,0xA30A)).value)
    
    targetRegionDataset = SearchForCodeValue(dicomObject, "123014")
    targetRegion = targetRegionDataset.get(Tag(0x0040,0xA168)).value._list[0].get(Tag(0x0008,0x0104)).value
     
    CTAcquisitionTypeDataset = SearchForCodeValue(dicomObject, "113820")
    CTAcquisitionType = CTAcquisitionTypeDataset.get(Tag(0x0040,0xA168)).value._list[0].get(Tag(0x0008,0x0104)).value
    
    procedureContextDataset = SearchForCodeValue(dicomObject, "G-C32C")
    if procedureContextDataset is not None:
        procedureContext = procedureContextDataset.get(Tag(0x0040,0xA168)).value._list[0].get(Tag(0x0008,0x0104)).value
    else:
        procedureContext = None
    
    AquisitionProtocolDataset = SearchForCodeValue(dicomObject, "125203")
    AquisitionProtocol = AquisitionProtocolDataset.get(Tag(0x0040,0xA160)).value
    
    return (irradiationEventUID,
            seriesUID,
            scanningLength,
            meanCTDIvol,
            DLP,
            sizeSpecificDoseEstimation,
            CTDIwPhantomType,
            maximumXRayTubeCurrent,
            xRayTubeCurrent,
            pitchFactor,
            exposureTime,
            nominalSingleCollimationWidth,
            nominalTotalCollimationWidth,
            kVP,
            targetRegion,
            CTAcquisitionType, 
            procedureContext,
            AquisitionProtocol)
    
def SeriesDetailsTable(dicomObject, primary = False):
    """
    Order of Information:
        Series UID - (0020,000E)
        Study UID - (0020,000D)
        Device Serial Number - (0018,1000)
        Software Version - (0018,1020)
        Procedure Reported - 121058
        Has Intent - G-C0E8
        Person Name/Operator - (0008,1070) - or - 121008
        Start of X-Ray Irradiation - 113809
        End of X-Ray Irradiation - 113810
        Source of Dose Information - 113854
    """
    
    seriesUIDTag = Tag(0x0020,0x000E)
    studyUIDTag = Tag(0x0020,0x000D)
    deviceSerialNumberTag = Tag(0x0018,0x1000)
    softwareVersionTag = Tag(0x0018,0x1020)
    operatorTag = Tag(0x0008,0x1070)
    
    dicomSequenceObject = dicomObject.get(Tag(0x0040,0xA730))
    
    seriesUID = dicomObject.get(seriesUIDTag).value
    if seriesUID == "":
        raise ValueError("SeriesUID not valid, continuing to next patient")
    
    if primary:
        return seriesUID
    
    studyUID = dicomObject.get(studyUIDTag).value
    if studyUID == "":
        raise ValueError("StudyUID not valid, continuing to next patient")
    
    deviceSerialNumber = dicomObject.get(deviceSerialNumberTag).value
    if deviceSerialNumber == "":
        raise ValueError("Device Serial Number not valid, continuing to next patient")
    
    softwareVersion = dicomObject.get(softwareVersionTag).value
    if softwareVersion == "":
        softwareVersion = None
    
    operator = dicomObject.get(operatorTag)
    if operator is None:
        operatorDataset = SearchForCodeValue(dicomObject, "121008")
        
        operator = str(operatorDataset.get(Tag(0x0040,0xA123)).value)
    else:
        operator = str(operator.value)
    
    startOfXRayIrradiationDataset = SearchForCodeValue(dicomObject, "113809")
    startOfXRayIrradiationString = startOfXRayIrradiationDataset.get(Tag(0x0040,0xA120)).value
    startOfXRayIrradiation = MakeDateTimeFromString(startOfXRayIrradiationString)
    
    endOfXRayIrradiationDataset = SearchForCodeValue(dicomObject, "113810")
    endOfXRayIrradiationString = endOfXRayIrradiationDataset.get(Tag(0x0040,0xA120)).value
    endOfXRayIrradiation = MakeDateTimeFromString(endOfXRayIrradiationString)
    
    hasIntentDataset = SearchForCodeValue(dicomObject, "G-C0E8")
    hasIntent = hasIntentDataset.get(Tag(0x0040,0xA168)).value._list[0].get(Tag(0x0008,0x0104)).value
    
    sourceOfDoseInformationDataset = SearchForCodeValue(dicomObject, "113854")
    sourceOfDoseInformationChunk = sourceOfDoseInformationDataset.get(Tag(0x0040,0xA168)).value._list[0]
    sourceOfDoseInformation = sourceOfDoseInformationChunk.get(Tag(0x0008,0x0104)).value
    
    procedureReportedDataset = SearchForCodeValue(dicomObject, "121058")
    procedureReportedChunk = procedureReportedDataset.get(Tag(0x0040,0xA168)).value._list[0]
    procedureReported = procedureReportedChunk.get(Tag(0x0008,0x0104)).value
    
    return (seriesUID,
            studyUID,
            operator,
            startOfXRayIrradiation,
            endOfXRayIrradiation,
            hasIntent,
            sourceOfDoseInformation,
            procedureReported,
            deviceSerialNumber,
            softwareVersion)

def DeviceTable(dicomObject, primary = False):
    """
    Order of Information:
        Institution Name - (0008,0080)
        Institution Address - (0008,0081)
        Station Name - (0008,1010)
        Manufacturer's Model Name - (0008,1090)
        Device Serial Number - (0018,1000)
    """
    
    deviceSerialNumberTag = Tag(0x0018,0x1000)
    manufacturersModelNameTag = Tag(0x0008,0x1090)
    stationNameTag = Tag(0x0008,0x1010)
    institutionNameTag = Tag(0x0008,0x0080)
    institutionAddressTag = Tag(0x0008,0x0081)
    
    deviceSerialNumber = dicomObject.get(deviceSerialNumberTag).value
    if deviceSerialNumber == '':
        raise ValueError("No device serial number detected, continuing to next patient")
    
    if primary:
        return deviceSerialNumber
    
    stationName = dicomObject.get(stationNameTag)
    if stationName is not None:
        if stationName == "":
            stationName = None
        else:
            stationName = stationName.value

    institutionName = dicomObject.get(institutionNameTag)
    if institutionName is not None:
        if institutionName == "":
            institutionName = None
        else:
            institutionName = institutionName.value
    
    institutionAddress = dicomObject.get(institutionAddressTag)
    if institutionAddress is not None:
        if institutionAddress == "":
            institutionAddress = None
        else:
            institutionAddress = institutionAddress.value
    
    manufacturersModelName = dicomObject.get(manufacturersModelNameTag)
    if manufacturersModelName is not None:
        if manufacturersModelName == "":
            manufacturersModelName = None
        else:
            manufacturersModelName = manufacturersModelName.value
    
    # Return the extracted values
    return (deviceSerialNumber, stationName, institutionName, institutionAddress, manufacturersModelName)

def ModelNameTable(dicomObject, primary = False):
    """
    Order of Information:
        Manufacturer's Model Name - (0008,1090)
        Manufacturer - (0008,0070)
    """
    
    manufacturerTag = Tag(0x0008,0x0070)
    manufacturersModelNameTag = Tag(0x0008,0x1090)
    
    manufacturersModelName = dicomObject.get(manufacturersModelNameTag).value
    
    if primary:
        return manufacturersModelName
    
    manufacturer = dicomObject.get(manufacturerTag).value
    
    return (manufacturersModelName, manufacturer)
    
def StudyDetailsTable(dicomObject, primary = False):
    """
    Order of information:
        Study UID (0020,000D)
        Referring Physician's Name (0008,0090)
        Study Description (0008,1030)
        Patient ID (0010,0020)
    """
    studyUIDTag = Tag(0x0020, 0x000D)
    referringPhysiciansNameTag = Tag(0x0008, 0x0090)
    studyDescriptionTag = Tag(0x0008, 0x1030)
    patientIDTag = Tag(0x0010, 0x0020)
    
    studyUID = dicomObject.get(studyUIDTag)
    if studyUID is None:
        raise ValueError("Unable to enter study due to invalid study UID")
    studyUID = studyUID.value
    
    if primary:
        return studyUID
    
    patientID = dicomObject.get(patientIDTag).value
    if not IsValidRnumber(patientID):
        raise ValueError("Cannot add record as RNumber is invalid")
    
    referringPhysician = dicomObject.get(referringPhysiciansNameTag)
    if referringPhysician is not None:
        referringPhysician = str(referringPhysician.value)
    if referringPhysician == '':
        referringPhysician = None
    
    studyDescription = dicomObject.get(studyDescriptionTag)
    if studyDescription is not None:
        studyDescription = studyDescription.value
    
    return (studyUID, studyDescription, referringPhysician, patientID)
    
def Modulus11Check(NHSID):
    
    # Checking a none hasn't been inputted
    if NHSID is None:
        return False
    
    NHSID = NHSID.value.replace(" ","")
    
    # Checking the length of the number is 10
    if not len(NHSID) == 10:
        return False
    # Checking the values of each digit are numeric
    if not NHSID.isnumeric():
        return False
    
    # Calculation of validity using the Modulus 11 algorithm
    weights = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    
    # Instantiating check value
    check = 0
    
    for i in range(9):
        check += weights[i] * int(NHSID[i])
    
    check = check % 11
    
    check = 11 - check
    
    return str(check) == NHSID[9]

def IsValidRnumber(patientID):    
    
    # Checking a none or "" hasn't been answered
    if patientID is None or patientID == "":
        return False
    
    # Check if it is a valid R number by checking that the first value is R
    if patientID[0].lower() != "r":
        return False
    
    # Check that it is the right length to be an R number
    if len(patientID) != 7:
        if len(patientID) == 8 and (patientID[-1].lower() == "m" or patientID[-1].lower() == "c"):
            return True
        return False
    
    # It didnt hit either of the checks to invalidate, therefore must be valid
    return True

def IsValidDate(dateInQuestion):
    
    # Checking a none hasn't been answered
    if dateInQuestion is None:
        return False
    
    # Should be YYYYMMDD, therefore 8 digits
    # Or YYYYMMDDHHmmSS.SSS, therefore 18 digits
    if not len(dateInQuestion.value) == 8 or len(dateInQuestion.value) == 18:
        return False
    
    # Should be completely numeric
    if not dateInQuestion.value.isnumeric():
        return False
    
    # Get the year and see if it is valid
    # Oldest man in the world born in 1912
    # Checking to see if born in a reasonable date and not in the future
    year = int(dateInQuestion[0:4])
    if year < 1912 or year > datetime.now().year:
        return False
    
    # Check the month is between 1 and 12
    month = int(dateInQuestion[4:6])
    if month < 1 or month >= 12:
        return False
    
    # Check the days is less than 32 and greater than 0
    day = int(dateInQuestion[6:8])
    if day < 1 or day >= 31:
        return False
    
    # If value is date time as well, check validity
    if len(dateInQuestion.value) == 18:
        # Hours must be between 0 and 23
        hours = int(dateInQuestion[8:10])
        if hours < 0 or hours >= 23:
            return False
        
        # Minutes between 00 and 59
        minutes = int(dateInQuestion[10:12])
        if minutes < 0 or minutes >= 59:
            return False
        
        # Seconds must be between 0 and 59.999
        seconds = float(dateInQuestion[12:])
        if seconds < 0 or seconds > 60:
            return False
    
    # If they havent activated any of the conditions, it is safe to say that they must be valid
    return True

def SearchForCodeValue(dicomSequenceObject, codeValue):
    codeValuePart = dicomSequenceObject.get(Tag(0x0040,0xA043)).value[0]
    codeValueGrabbed = codeValuePart.get(Tag(0x0008,0x0100)).value
    if codeValueGrabbed == codeValue:
        return dicomSequenceObject
    
    #If nothing found check for a sequence object and search that
    nestedSequence = dicomSequenceObject.get(Tag(0x0040,0xA730))
    if nestedSequence is not None:
        nestedSequence = nestedSequence.value._list
        for dataset in nestedSequence:
            result = SearchForCodeValue(dataset, codeValue)
            
            #Ensure that this result is not none and return it if it is
            if result is not None:
                return result
    
    # If nothing got caught
    return None

def MakeDateTimeFromString(dateStringInput):
    # Split by '+' as the first move, then deal with the date string as normal
    if "+" in dateStringInput:
        dateStringList = dateStringInput.split('+')
        plus = True
        greenwichIncluded = True
    elif "-" in dateStringInput:
        dateStringList = dateStringInput.split('-')
        plus = False
        greenwichIncluded = True
    else:
        dateStringList = [dateStringInput]
        greenwichIncluded = False
        
    dateString = dateStringList[0]
    
    # Must be 14 or greater
    if len(dateStringList[0]) < 14:
        raise ValueError("Value before decimal point must be 14 characters or longer")
    
    # Standard, this wont change
    year = int(dateString[0:4])
    month = int(dateString[4:6])
    day = int(dateString[6:8])
    hour = int(dateString[8:10])
    minute = int(dateString[10:12])
    second = int(dateString[12:14])
    
    # Dont know how many decimal points there are
    dateStringListNoGreenwich = dateString.split('.')
    if len(dateStringListNoGreenwich) > 1:
        milliString = dateStringListNoGreenwich[1]
        microsecond = int(milliString) * 10**(6-len(milliString))
    else:
        microsecond = 0
    
    if greenwichIncluded:
        hourAdd = int(dateStringList[1][0:2])
        minAdd = int(dateStringList[1][2:4])
        
        if not plus:
            hourAdd = -hourAdd
            minAdd = -minAdd
        
        hour += hourAdd
        minute += minAdd
    
    dateList = [year, month, day, hour, minute, second, microsecond]
    return datetime(*dateList)

def SearchForAllCodeValues(dicomSequenceObject, codeValue):
    results = []
    
    for thing in dicomSequenceObject:
        codeValuePart = thing.get(Tag(0x0040,0xA043)).value[0]
        codeValueGrabbed = codeValuePart.get(Tag(0x0008,0x0100)).value
        if codeValueGrabbed == codeValue:
            results.append(thing)
        
        #If nothing found check for a sequence object and search that
        nestedSequence = thing.get(Tag(0x0040,0xA730))
        if nestedSequence is not None:
            nestedResults = SearchForAllCodeValues(nestedSequence, codeValue)
            results.extend(nestedResults) 
            
    return results

#%% Insert Commands

def patientDetails_Insert(dicomObject, cursor):
    results = PatientDetailsTable(dicomObject)
    
    insertQuery = """
    INSERT INTO patientdetails (PatientID,
                                DOB,
                                Sex,
                                NHSNumber)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(insertQuery, results)

def studyDetails_Insert(dicomObject, cursor):
    results = StudyDetailsTable(dicomObject)
    
    insertQuery = """
    INSERT INTO studydetails (StudyUID,
                              Description,
                              ReferringPhysician,
                              PatientID)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(insertQuery, results)

def modelName_Insert(dicomObject, cursor):
    results = ModelNameTable(dicomObject)
    
    insertQuery = """
    INSERT INTO manufacturertable (ModelName,
                                   Manufacturer)
    VALUES (?, ?)
    """
    cursor.execute(insertQuery, results)

def deviceTable_Insert(dicomObject, cursor):
    results = DeviceTable(dicomObject)
    
    insertQuery = """
    INSERT INTO devicetable (DeviceSerialNumber,
                             StationName,
                             InstitutionName,
                             InstitutionAddress,
                             ModelName)
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(insertQuery, results)

def seriesTable_Insert(dicomObject, cursor):
    results = SeriesDetailsTable(dicomObject)
    
    insertQuery = """
    INSERT INTO seriesdetails (SeriesUID,
                                StudyUID,
                                Operator,
                                IrradiationStart,
                                IrradiationEnd,
                                ExposureIntent,
                                DoseInformationSource,
                                ReportedProcedure,
                                DeviceSerialNumber,
                                SoftwareVersion)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insertQuery, results)

def irradEvent_Insert(dicomObject, parentDicomObject, cursor):
    results = IrradiationEventTable(dicomObject, parentDicomObject)
    
    insertQuery = """
    INSERT INTO irradiationevent (IrradiationEventUID,
                                  SeriesUID,
                                  ScanningLength,
                                  MeanCTDIvol,
                                  DLP,
                                  SizeSpecificDoseEstimation,
                                  CTDIwPhantomType,
                                  MaximumXRayTubeCurrent,
                                  XRayTubeCurrent,
                                  PitchFactor,
                                  ExposureTime,
                                  NominalSingleCollimationWidth,
                                  NominalTotalCollimationWidth,
                                  kVPeak,
                                  TargetRegion,
                                  AcquisitionType, 
                                  ProcedureContext,
                                  DeviceSpecificAcquisitionProtocol)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(insertQuery, results)

def CheckBeforeEntry(primaryKey, columnName, table, cursor):
    query = f"SELECT {columnName} FROM {table} WHERE {columnName} = %s"
    cursor.execute(query, (primaryKey,))
    return cursor.rowcount > 0