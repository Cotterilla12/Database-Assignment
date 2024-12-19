# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:21:52 2024

@author: archie.cotterill
"""
#%% Modules

import mariadb
import sys
import os
import shutil
from TableExtractionFunctions import *
import pydicom as dicom
import numpy as np

#%% MariaDB Connector

username = input("Please enter your username: ")
password = input("Please enter your password: ")

try:
    conn_OLTP = mariadb.connect(
        user=username,
        password=password,
        host="127.0.0.1",
        port=3306,
        database="irradiationevents")

    cur_OLTP = conn_OLTP.cursor()

    conn_OLAP = mariadb.connect(
        user=username,
        password=password,
        host="127.0.0.1",
        port=3306,
        database="irradiationfacts")

    cur_OLAP = conn_OLAP.cursor()
    
    print("Connected to DB")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

#%% Extraction Statements

extractStudies = """SELECT StudyUID FROM studydetails WHERE PatientID = '{}';"""
extractStudiesDetails = """SELECT * FROM studydetails WHERE StudyUID = '{}'"""
extractSeries = """SELECT SeriesUID FROM seriesdetails WHERE StudyUID = '{}';"""
extractSeriesDetails = """SELECT * FROM seriesdetails WHERE SeriesUID = '{}'"""
extractEvents = """SELECT IrradiationEventUID FROM irradiationevent WHERE SeriesUID = '{}';"""
extractEventsDetails = """SELECT * FROM irradiationevent WHERE IrradiationEventUID = '{}'"""

#%% Insertion Statements

insertDeviceDetails = """INSERT INTO devicedetailsdimtable (DeviceSerialNumber,
                                                            StationName,
                                                            InstitutionName,
                                                            InstitutionAddress,
                                                            Model,
                                                            Manufacturer)
                        VALUES (?, ?, ?, ?, ?, ?)"""

insertIrradFact = """INSERT INTO irradiationfacttable (StudyUID,
                                                       TotalMeanCTDIvol,
                                                       TotalDLP,
                                                       TotalSizeSpecificDoseEstimation,
                                                       IrradiationStart,
                                                       IrradiationEnd,
                                                       AmountOfIrradiationEvents,
                                                       PatientID)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

#%% Assisting Functions

def UpdateOrPopulateFact(studyUID, cursor, conn):
    extractEvents = """SELECT MeanCTDIvol, DLP, SizeSpecificDoseEstimation, StartOfExposure, EndOfExposure FROM irradiationeventdimtable WHERE StudyUID = %s;"""
    
    cursor.execute(extractEvents, [studyUID])
    
    events = cursor.fetchall()
    
    cursor.execute("SELECT AmountOfIrradiationEvents FROM irradiationfacttable WHERE StudyUID = %s", [studyUID])
    initialAmountOfEvents = cursor.fetchone()[0]
    if len(events) == initialAmountOfEvents:
        return
    
    TotalMeanCTDIvol = 0
    TotalDLP = 0
    TotalSizeSpecificDoseEstimation = 0
    IrradiationStart = None
    IrradiationEnd = None
    AmountOfIrradiationEvents = len(events)
    
    for event in events:
        if event[0] is not None:
            TotalMeanCTDIvol += event[0]
        if event[1] is not None:
            TotalDLP += event[1]
        if event[2] is not None:
            TotalSizeSpecificDoseEstimation += event[2]
        
        if IrradiationStart is None or event[3] < IrradiationStart:
            IrradiationStart = event[3]
        if IrradiationEnd is None or event[3] > IrradiationEnd:
            IrradiationEnd = event[3]
    
    updateStatement = "UPDATE irradiationfacttable SET TotalMeanCTDIvol = %s, TotalDLP = %s, TotalSizeSpecificDoseEstimation = %s, IrradiationStart = %s, IrradiationEnd = %s, AmountOfIrradiationEvents = %s, Completed = %s WHERE StudyUID = %s"
    
    inputTuple = (TotalMeanCTDIvol, TotalDLP, TotalSizeSpecificDoseEstimation, IrradiationStart, IrradiationEnd, AmountOfIrradiationEvents, 0, studyUID)
    
    cursor.execute(updateStatement, inputTuple)
    conn.commit()
    
    cursor.execute("SELECT PatientID FROM irradiationfacttable WHERE StudyUID = %s", [studyUID])
    PatientID = cursor.fetchone()[0]
    
    print("Updated fact for patient: " + PatientID)

def InsertEvent(IrradiationEventUID, seriesTuple, cur_OLTP, cur_OLAP, conn):
    selectIrradEvent = """SELECT * FROM irradiationevent WHERE IrradiationEventUID = %s"""
    
    cur_OLTP.execute(selectIrradEvent, [IrradiationEventUID])
    IrradEvent = cur_OLTP.fetchone()
    
    AddDeviceDetailsToOLAP(cur_OLTP, conn, cur_OLAP, seriesTuple[8])
    cur_OLAP.execute("SELECT StationName FROM devicedetailsdimtable WHERE DeviceSerialNumber = %s", [seriesTuple[8]])
    StationName = cur_OLAP.fetchone()[0]
    
    insertIrradEventDim = """INSERT INTO irradiationeventdimtable (IrradiationEventUID,
                                                                   StudyUID,
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
                                                                   DeviceSpecificAcquisitionProtocol,
                                                                   DeviceSerialNumber,
                                                                   StationName,
                                                                   Operator,
                                                                   StartOfExposure,
                                                                   EndOfExposure)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    inputList = list(IrradEvent)
    inputList[1] = seriesTuple[1]
    inputList.extend([seriesTuple[8], StationName, seriesTuple[2], seriesTuple[3], seriesTuple[4]])
    inputTuple = tuple(inputList)
    
    cur_OLAP.execute(insertIrradEventDim, inputTuple)
    conn.commit()
    
def AddDeviceDetailsToOLAP(cur_OLTP, conn_OLAP, cur_OLAP, deviceSerialNumber):
    checkIfInsertedAlreadyStatement = "SELECT * from devicedetailsdimtable WHERE DeviceSerialNumber = %s"
    
    cur_OLAP.execute(checkIfInsertedAlreadyStatement, [deviceSerialNumber])
    deviceThere = cur_OLAP.fetchone() is not None
    
    if not deviceThere:
        cur_OLTP.execute("SELECT * from devicetable WHERE DeviceSerialNumber = %s", [deviceSerialNumber])
        deviceDetails = cur_OLTP.fetchone()
        
        cur_OLTP.execute("SELECT Manufacturer from manufacturertable WHERE ModelName = %s", [deviceDetails[4]])
        manufacturer = cur_OLTP.fetchone()
        
        cur_OLAP.execute("""INSERT INTO devicedetailsdimtable (DeviceSerialNumber,
                                                               StationName,
                                                               InstitutionName,
                                                               InstitutionAddress,
                                                               Model,
                                                               Manufacturer)
        Values (%s, %s, %s, %s, %s, %s)""", (deviceDetails + tuple(manufacturer)))
        conn_OLAP.commit()

#%% Split into Irrad Events

path = r"R:\Archie's Scripts\DICOM Structured Reports\Full_Audit"

amount = len(os.listdir(path))
currentNumber = 0

studiesToUpdate = []
IrradsToAdd = []

#Go through the folder and add them to the OLTP Database
for unloadedStructuredReport in os.listdir(path):
    if unloadedStructuredReport.endswith(".dcm"):
        structuredReport = dicom.dcmread(os.path.join(path, unloadedStructuredReport))
        
        # Encase everything in a try catch
        try:            
            if not CheckBeforeEntry(StudyDetailsTable(structuredReport, True), "StudyUID", "studydetails", cur_OLTP):
                studyDetails_Insert(structuredReport, cur_OLTP)
                conn_OLTP.commit()
            
            if not CheckBeforeEntry(ModelNameTable(structuredReport, True), "ModelName", "manufacturertable", cur_OLTP):
                modelName_Insert(structuredReport, cur_OLTP)
                conn_OLTP.commit()
            
            if not CheckBeforeEntry(DeviceTable(structuredReport, True), "DeviceSerialNumber", "devicetable", cur_OLTP):
                deviceTable_Insert(structuredReport, cur_OLTP)
                conn_OLTP.commit()
            
            if not CheckBeforeEntry(SeriesDetailsTable(structuredReport, True), "SeriesUID", "seriesdetails", cur_OLTP):
                seriesTable_Insert(structuredReport, cur_OLTP)
                conn_OLTP.commit()
            
            irradEventsNumber = 0
            contentSequence = structuredReport.get(Tag(0x0040,0xA730)).value
            for event in SearchForAllCodeValues(contentSequence, "113819"):
                irradEventsNumber += 1
                
                if not CheckBeforeEntry(IrradiationEventTable(event, structuredReport, True), "IrradiationEventUID", "irradiationevent", cur_OLTP):
                    irradEvent_Insert(event, structuredReport, cur_OLTP)
                    conn_OLTP.commit()
                    studiesToUpdate.append(StudyDetailsTable(structuredReport, True))
                    IrradsToAdd.append(IrradiationEventTable(event, structuredReport, True))
            
            currentNumber += 1
            print(str(currentNumber) + "/" + str(amount) + " " + structuredReport.PatientID + ": " + str(irradEventsNumber) + " irradiation events")
        except ValueError as e:
            print(e)

#%% Ensure all of the patients whose studies were added in the last cell are in the OLAP

i=0

studies = np.unique(studiesToUpdate)

# Extract all of the studies associated with PatientID    
for study in studies:
    i += 1
    
    cur_OLTP.execute("SELECT PatientID FROM studydetails WHERE StudyUID = %s", [study])
    PatientID = cur_OLTP.fetchone()
    
    # Set the irradiation fact with zero values
    try:
        cur_OLAP.execute(insertIrradFact, (study, 0, 0, 0, None, None, 0, PatientID[0]))
        conn_OLAP.commit()
    except:
        pass

# Add all of the irradiation events
events = np.unique(IrradsToAdd)

eventNumber = 1

for event in events:
    cur_OLTP.execute(extractEventsDetails.format(event))
    IrradDetails = cur_OLTP.fetchone()
    
    # Extract information in series
    cur_OLTP.execute(extractSeriesDetails.format(IrradDetails[1]))
    seriesDetails = cur_OLTP.fetchone()
    
    InsertEvent(event, seriesDetails, cur_OLTP, cur_OLAP, conn_OLAP)
    
    print("Inserted event:", eventNumber)
    eventNumber += 1
    
# Update the facts
for study in studies:
    UpdateOrPopulateFact(study, cur_OLAP, conn_OLAP)

#%% Close the damn things so the DB can actually function without being deadlocked

conn_OLTP.close()
conn_OLAP.close()
cur_OLTP.close()
cur_OLAP.close()