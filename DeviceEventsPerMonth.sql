SELECT 
    StationName,
    YEAR(StartOfExposure) AS EventYear,
    MONTH(StartOfExposure) AS EventMonth,
    COUNT(*) AS EventCount
FROM irradiationeventdimtable
GROUP BY StationName, YEAR(StartOfExposure), MONTH(StartOfExposure)
ORDER BY StationName, EventYear, EventMonth;