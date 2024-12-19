SELECT 
    i.Operator,
    f.PatientID,
    i.StartOfExposure,
    COUNT(*) AS EventCount
FROM irradiationeventdimtable AS i
JOIN irradiationfacttable AS f
    ON i.StudyUID = f.StudyUID
WHERE
	 i.StationName != 'HOST-20027'
	 AND i.StartOfExposure BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY i.StartOfExposure, f.PatientID, i.Operator
HAVING COUNT(*) > 1
ORDER BY i.StartOfExposure;