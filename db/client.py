# Linux MongoDB..
# sudo systemctl start mongod
# sudo systemctl status mongod
# sudo systemctl stop mongod
# sudo systemctl restart mongod


from pymongo import MongoClient

# Base de datos local
db_client = MongoClient().local
