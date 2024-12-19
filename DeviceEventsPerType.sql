SELECT 
    StationName,
    AcquisitionType,
    COUNT(*) AS EventCount
FROM irradiationeventdimtable
GROUP BY StationName, AcquisitionType
ORDER BY StationName, AcquisitionType;