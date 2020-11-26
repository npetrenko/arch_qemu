set -e

BRC_PATH=/home/npetric/.bashrc
BAL_PATH=/home/npetric/.bash_aliases

touch $BRC_PATH
chown npetric:npetric $BRC_PATH
chmod 700 $BRC_PATH

echo source $BAL_PATH >> $BRC_PATH

touch $BAL_PATH
chown npetric:npetric $BAL_PATH
chmod 700 $BAL_PATH
