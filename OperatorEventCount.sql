SELECT Operator, COUNT(*) AS EventCount
FROM irradiationeventdimtable
GROUP BY Operator
ORDER BY EventCount DESC;