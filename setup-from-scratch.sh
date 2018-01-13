echo "-----Pulling last changes from repository-----"
git pull

echo "-----Updating node_modules-----"
cd front
npm i

echo "-----Starting the server-----"
cd ../back
conda env create -f dev_environment.yml
source activate SpaceAtlas
python run.py