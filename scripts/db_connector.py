# This file "db_connector.py" contains methods to read and write a MySQL database, that is used to store the results

# All needed imports for this script file
import mysql.connector
import matplotlib.pyplot as plt

# Connection parameters
dbUser = "ml2"
dbPassword = "ml2@hsOg#2019!"
dbHost = "192.52.33.218"
dbDatabase = "ml2"
dbAutoCommit = True

def createConnection():
  connection = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbDatabase, autocommit=dbAutoCommit)
  return connection

# Method for writing the image classification results to DB
def storeImageClassificationResultToDB(connection, localPath, model, predictedClass, predictionProbability):
  cursor = connection.cursor()
  add_result = ("insert ignore into results (local_path, model, prediction_class, prediction_probability) values (%s, %s, %s, %s)")
  data_result = (localPath, model, predictedClass, float(predictionProbability))
  cursor.execute(add_result, data_result)
  resultId = cursor.lastrowid
  connection.commit()
  print(resultId, " | ", localPath, " | ", model, " | ", predictedClass, " | ", predictionProbability)
  cursor.close()

# Query the database for a specific search word
def querySearchWord(connection, searchWord):
  cursor = connection.cursor(buffered=True)
  query = ("select distinct local_path, prediction_class from results where prediction_class = %s")
  cursor.execute(query, (searchWord,))
  return cursor
