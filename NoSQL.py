# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 16:08:27 2024

@author: archie.cotterill
"""

from pymongo import MongoClient
from copy import deepcopy as deep
import mariadb, sys
from TableExtractionFunctions import IsValidRnumber
import json
from fpdf import FPDF
import numpy as np

#%% MongoDB Connector

client = MongoClient("mongodb://localhost:27017/")

db = client["PathwayRecord"]
collection = db["Patients"]

#%% OLAP Connector

username = input("Please enter your database username: ")
password = input("Please enter your database password: ")

try:
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

#%% Dictionary functions

def CreateEvent(eventTuple):
    irradiationEventDict = {
        'IrradiationEventUID' : eventTuple[0],
        'ScanningLength' : eventTuple[2],
        'MeanCTDIvol' : float(eventTuple[3]),
        'DLP' : float(eventTuple[4]),
        'SizeSpecificDoseEstimation' : eventTuple[5],
        'CTDIwPhantomType' : eventTuple[6],
        'MaximumXRayTubeCurrent' : float(eventTuple[7]),
        'XRayTubeCurrent' : float(eventTuple[8]),
        'PitchFactor' : eventTuple[9],
        'ExposureTime' : float(eventTuple[10]),
        'NominalSingleCollimationWidth' : eventTuple[11],
        'NominalTotalCollimationWidth' : eventTuple[12],
        'kVPeak' : eventTuple[13],
        'TargetRegion' : eventTuple[14],
        'AcquisitionType' : eventTuple[15],
        'ProcedureContext' : eventTuple[16],
        'DeviceSpecificAcquisitionProtocol' : eventTuple[17],
        'DeviceSerialNumber' : eventTuple[18],
        'StationName' : eventTuple[19],
        'Operator' : eventTuple[20],
        'StartOfExposure' : str(eventTuple[21]),
        'EndOfExposure' : str(eventTuple[22])
        }
    
    return irradiationEventDict

def CreateFact(factTuple):
    fact_Dict = {
        'PatientID' : factTuple[7],
        '_id' : factTuple[0],
        'TotalMeanCTDIvol' : float(factTuple[1]),
        'TotalDLP' : float(factTuple[2]),
        'TotalSizeSpecificDoseEstimation' : float(factTuple[3]),
        'IrradiationStart' : str(factTuple[4]),
        'IrradiationEnd' : str(factTuple[5]),
        'AmountOfIrradiationEvents' : factTuple[6],
        'IrradiationEvents' : []
        }
    
    return fact_Dict

def formatStringNicely(line):
    line = line[3:].replace("_id", "StudyUID").replace("\"", "")
    
    return line

def CreatePDF(jsonData, PatientID):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", "BU", size=20)
    pdf.cell(200, 10, txt="Imaging Irradiation Record for " + PatientID, ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    for line in jsonData.split('\n'):
        if "PatientID" in line:
            continue
        if line in ['{', '}']:
            continue
        pdf.cell(200, 6, txt=formatStringNicely(line), ln=True)
    
    output_file = r"\\MTWHome\Users_a\archie.cotterill\Data\DataBases\\" + PatientID + " Irradiation Record.pdf"
    
    pdf.output(output_file)
    print("PDF saved:", output_file)

#%% Statements

retrieveStudyDates = "SELECT StudyUID, IrradiationStart, IrradiationEnd FROM irradiationfacttable WHERE PatientID = %s AND Completed = 0"

retrieveOpenPatientTreatments = "SELECT PatientID, IrradiationStart, IrradiationEnd FROM irradiationfacttable WHERE Completed = 0"

retrieveStudyFact = "SELECT * FROM irradiationfacttable WHERE StudyUID = %s"

retrieveEvents = "SELECT * FROM irradiationeventdimtable WHERE StudyUID = %s"

completionStatement = "UPDATE irradiationfacttable SET Completed = 1 WHERE StudyUID = %s"

def TreatmentDatesString(treatment):
    return "Treatment start: " + str(treatment[1]) + "\tTreatment end: " + str(treatment[2])

#%% Reading options:

option = ""

while option.isnumeric() == False:
    option = input("""Please enter 1 if you would like to finalise a patient's treatment,
             2 if you would like to view open patients,
             3 if you would like to retrieve a previously finalised patient: """)
    
    if option.isnumeric():
        if int(option) not in [1, 2, 3]:
            option = ""

option = int(option)

# Finalise a patient treatment
if option == 1:
    RNumber = input("Please enter the RNumber of the patient you wish to retrieve: ")
    
    while IsValidRnumber(RNumber) == False:
        RNumber = input("Invalid RNumber, please try again: ")
    
    cur_OLAP.execute(retrieveStudyDates, (RNumber,))
    
    treatments = cur_OLAP.fetchall()
    
    if len(treatments) == 0:
        print("No treatments have been found for this patient")
        sys.exit(1)
    elif len(treatments) == 1:
        treatments = treatments[0]
        print(TreatmentDatesString(treatments))
    elif len(treatments) > 1:
        for i, treatment in enumerate(treatments):
            print(i+1, "\t", TreatmentDatesString(treatments[i]))
        
        treatmentSelected = int(input("Please select the treatment you wish to finalise, if not displayed, enter 0: "))
        
        if treatmentSelected == 0:
            sys.exit(1)
        
        treatments = treatments[treatmentSelected - 1]
    
    cur_OLAP.execute(retrieveEvents, [treatments[0]])
    
    events = cur_OLAP.fetchall()
    
    cur_OLAP.execute(retrieveStudyFact, [treatments[0]])
    
    fullStudy = cur_OLAP.fetchone()
    
    mainFact = CreateFact(fullStudy)
    
    for event in events:
        mainFact['IrradiationEvents'].append(CreateEvent(event))
    
    collection.replace_one({"_id": mainFact["_id"]}, mainFact, upsert = True)
    print("Added " + mainFact['PatientID'] + " to document database")
    
    document = collection.find_one({"_id": treatments[0]})
    
    jsonData = json.dumps(document, indent=4)
    
    CreatePDF(jsonData, mainFact['PatientID'])
    
    cur_OLAP.execute(completionStatement, [mainFact['_id']])
    conn_OLAP.commit()

# View all open patients
elif option == 2:
    cur_OLAP.execute(retrieveOpenPatientTreatments)
    
    openTreatments = cur_OLAP.fetchall()
    
    textString = ""
    
    for treatment in openTreatments:
        treatmentString = treatment[0] + "," + str(treatment[1]) + "," + str(treatment[2]) + "\n"
        print(treatmentString[:-12])
        textString += treatmentString
    
    with open(r"\\MTWHome\Users_a\archie.cotterill\Data\DataBases\OpenPatients.csv", "w") as output:
        output.write(textString)
    
# Retrieve previously submitted documnent
elif option == 3:
    RNumber = input("Please enter the RNumber of the patient you wish to retrieve: ")
    
    while IsValidRnumber(RNumber) == False:
        RNumber = input("Invalid RNumber, please try again: ")
    
    documents = list(collection.find({"PatientID": RNumber}))
    
    if not documents:
        print("No documents were found matchine patient identifier")
    elif len(documents) == 1:
        selectedDocument = list(documents)[0]
    else:
        print("There are multiple records for that patient, please select from the below:")
        
        for i, doc in enumerate(documents):
            print(f"{i+1}. {doc.get('IrradiationStart', 'N/A')} - {doc.get('IrradiationEnd', 'N/A')}")
        
        selectedIndex = input("Please enter the number of the treatment, enter 0 if desired record not there: ")
        
        while int(selectedIndex) not in list(range(len(documents) + 1)):
            selectedIndex = input("Invalid entry, please try again: ")
        
        selectedDocument = list(documents)[int(selectedIndex) - 1]
    
    jsonData = json.dumps(selectedDocument, indent=4)
    
    CreatePDF(jsonData, selectedDocument["PatientID"])

#%% Close connections

conn_OLAP.close()
cur_OLAP.close()
