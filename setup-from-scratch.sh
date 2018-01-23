echo "-----Pulling last changes from repository-----"
git pull

echo "-----Updating node_modules-----"
cd front
npm i

echo "-----Starting the server-----"
cd ../back
conda env create -f dev_environment.yml
source activate websto
echo "Starting app on localhost:5555/"
python run.py