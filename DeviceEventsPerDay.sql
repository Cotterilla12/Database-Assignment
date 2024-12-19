SELECT 
    StationName,
    DAYOFWEEK(StartOfExposure) AS EventDay,
    COUNT(*) AS EventCount
FROM irradiationeventdimtable
    WHERE StartOfExposure BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY StationName, DAYOFWEEK(StartOfExposure)
ORDER BY StationName
