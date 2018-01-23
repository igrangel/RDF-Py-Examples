@ECHO OFF
ECHO.-----Starting the server-----
cd back
CALL activate websto
ECHO.-----Starting app on localhost:5555/-----
python run.py

ECHO ON