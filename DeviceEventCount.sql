SELECT StationName, COUNT(*) AS EventCount
FROM irradiationeventdimtable
GROUP BY StationName
ORDER BY EventCount DESC;