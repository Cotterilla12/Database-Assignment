SELECT 
    StationName,
    DAYOFWEEK(StartOfExposure) AS EventDay,
    COUNT(*) AS EventCount
FROM irradiationeventdimtable
GROUP BY StationName, DAYOFWEEK(StartOfExposure)
ORDER BY StationName