# This file "db_connector.py" contains methods to read and write a MySQL database, that is used to store the results

# All needed imports for this script file
import mysql.connector
import matplotlib.pyplot as plt

def createConnection(dbUser, dbPassword, dbHost, dbDatabase, dbAutoCommit):
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
  
# Method for writing the stemming results to DB
def storeTextStemmingResultToDB(connection, emailPath, emailFrom, emailTo, emailSubject, emailBody, stemmingWords):
  cursor = connection.cursor()
  add_email = ("insert ignore into email_list (email_path, email_from, email_to, email_subject, email_body) values (%s, %s, %s, %s, %s)")
  data_email = (emailPath, emailFrom, emailTo, emailSubject, emailBody)
  cursor.execute(add_email, data_email)
  resultId = cursor.lastrowid
  connection.commit()
  print(resultId, " | ", emailPath, " | ", emailFrom, " | ", emailTo, " | ", emailSubject, "|", emailBody)
  
  if(resultId != 0):
    for stemmingWord in stemmingWords:
      add_stemming = ("insert ignore into email_stemming (emailID, stemming_word) values (%s, %s)")
      data_stemming = (int(resultId), stemmingWord)
      cursor.execute(add_stemming, data_stemming)
      resultId2 = cursor.lastrowid
      connection.commit()
      print(resultId2, " | ", stemmingWord)
  
  cursor.close()

# Query the database for a specific search word
def querySearchWordAndPrintResults(connection, searchWord, function_prepareImagesForClassification):
  cursor = connection.cursor()
  query = ("select distinct local_path, prediction_class from results where prediction_class = %s")
  cursor.execute(query, (searchWord,))
  
  for (local_path, prediction_class) in cursor:
    foundFiles = [open(local_path, 'rb')]
    preparedImage224x224 = function_prepareImagesForClassification(foundFiles, 224, 224)[0]
    plt.figure()
    plt.imshow(preparedImage224x224)
    plt.title("{}".format(local_path))
    plt.axis('off')
    plt.show()
    plt.clf()

  cursor.close()
