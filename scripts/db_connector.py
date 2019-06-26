# This file "db_connector.py" contains methods to read and write a MySQL database, that is used to store the results

# All needed imports for this script file
import mysql.connector
import matplotlib.pyplot as plt

def createConnection(dbUser, dbPassword, dbHost, dbDatabase, dbAutoCommit):
  connection = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbDatabase, autocommit=dbAutoCommit)
  return connection

# Method for writing the image classification results to DB
def storeImageClassificationResultToDB(connection, localPath, model, predictedClass, predictionProbability, stemmingWords):
  cursor = connection.cursor()
  add_result = ("insert ignore into image_list (local_path, model, prediction_class, prediction_probability) values (%s, %s, %s, %s)")
  data_result = (localPath, model, predictedClass, float(predictionProbability))
  cursor.execute(add_result, data_result)
  resultId = cursor.lastrowid
  connection.commit()
  print(resultId, " | ", localPath, " | ", model, " | ", predictedClass, " | ", predictionProbability)
  
  if(resultId != 0):
    for stemmingWord in stemmingWords:
      add_stemming = ("insert ignore into image_stemming (imageID, stemming_word) values (%s, %s)")
      data_stemming = (int(resultId), stemmingWord)
      cursor.execute(add_stemming, data_stemming)
      resultId2 = cursor.lastrowid
      connection.commit()
      print(resultId2, " | ", stemmingWord)
  
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

# Query the image table for a specific search word
def queryImagesByTermAndPrintResults(connection, searchWord, function_prepareImagesForClassification):
  searchWord = "%" + searchWord + "%"
  cursor = connection.cursor()
  query = ("select distinct local_path from image_list where prediction_class like %s")
  cursor.execute(query, (searchWord,))
  
  print("Found following images for search term \"" + searchWord + "\"")
  
  for local_path in cursor:
    foundFiles = [open(local_path, 'rb')]
    preparedImage224x224 = function_prepareImagesForClassification(foundFiles, 224, 224)[0]
    plt.figure()
    plt.imshow(preparedImage224x224)
    plt.title("{}".format(local_path))
    plt.axis('off')
    plt.show()
    plt.clf()

  cursor.close()

# Query the stemming table for a specific search word
def queryStemmingsByTermAndPrintResults(connection, searchWord):
  cursor = connection.cursor()
  query = ("select email_path, email_from, email_to, email_subject, email_body from email_list, email_stemming where email_list.ID = email_stemming.emailID and email_stemming.stemming_word = %s")
  cursor.execute(query, (searchWord,))
  
  print("Found following emails for search term \"" + searchWord + "\"")
  
  for (emailPath, emailFrom, emailTo, emailSubject, emailBody) in cursor:
    print("File:   ", emailPath)
    print("From:   ", emailFrom)
    print("To:     ", emailTo)
    print("Subject:", emailSubject)
    print("Body:   ", emailBody)
    print("====================")
    
  cursor.close()
  
# Query to find image-text matchings automatically
def queryImagesAndMailsForSameStemmingWords(connection, function_prepareImagesForClassification):
  cursor = connection.cursor()
  query = ("select distinct image_list.
           , image_stemming.stemming_word, image_list.local_path, email_list.email_from, email_list.email_to, email_list.email_subject, email_list.email_body from image_list, image_stemming, email_list, email_stemming where email_stemming.emailID = email_list.ID and image_stemming.imageID = image_list.ID and email_stemming.stemming_word = image_stemming.stemming_word")
  cursor.execute(query)
  print("Found following matches")
  
  for (imagePredictionClass, stemmedClass, imagePath, emailFrom, emailTo, emailSubject, emailBody) in cursor:
    # Show mail info
    print("Das Stemming-Wort", stemmedClass, "(abgeleitet vom Wort", imagePredictionClass, ") matcht für folgende Image / Mail Kombination:")
    print("* From:     ", emailFrom)
    print("* To:       ", emailTo)
    print("* Subject:  ", emailSubject)
    print("* Body:     ", emailBody)
    
    # Show image
    localFile = [open(imagePath, 'rb')]
    preparedImage224x224 = function_prepareImagesForClassification(localFile, 224, 224)[0]
    plt.figure()
    plt.imshow(preparedImage224x224)
    plt.title("{}".format(imagePath))
    plt.axis('off')
    plt.show()
    plt.clf()
    
    print("====================")
  
  cursor.close()
