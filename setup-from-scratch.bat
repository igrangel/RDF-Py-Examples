@ECHO OFF

ECHO.-----Pulling last changes from repository-----
CALL git pull

ECHO.-----Updating node_modules-----
cd front
CALL npm i

ECHO.-----Starting the server-----
cd ..\back
CALL conda env create -f dev_environment.yml
CALL activate websto
ECHO.-----Starting app on localhost:5555/-----
python run.py

ECHO ON