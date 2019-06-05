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

# Method for writing the image classification results to DB
def storeImageClassificationResultsToDB(fileNames, resultsList, modelList):
  cnx = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbDatabase, autocommit=dbAutoCommit)
  cursor = cnx.cursor()
  add_result = ("insert ignore into results (local_path, model, prediction_class, prediction_probability) values (%s, %s, %s, %s)")
  for k in range(len(modelList)):
    print("==== other model =====")
    for i in range(len(fileNames)):
      print("==== other file =====")
      for j in range(5):
        print("Counter:")
        print("Model", (k+1), "of", len(modelList))
        print("File", (i+1), "of", len(fileNames))
        print("Top", (j+1), "of", 5)
        
        fileName = fileNames[i]
        modelName = modelList[k]
        predictedClassSynsetId = resultsList[k][i][j][0]
        predictedClass = resultsList[k][i][j][1]
        predictedPropability = resultsList[k][i][j][2]
  
        data_result = (fileName, modelName, predictedClass, float(predictedPropability))
        cursor.execute(add_result, data_result)
        result_id = cursor.lastrowid
		cnx.commit()
        
        print(result_id, " | ", fileName, " | ", modelName, " | ", predictedClass, " | ", predictedPropability)
        #print("Now searching for similar words in ImageNet tree (parent / child search)")
        #expandResultsByImageNetTreeSearch(predictedClassSynsetId, fileName, modelName, predictedPropability)
  cursor.close()
  cnx.close()

# Query the database for a specific search word
def querySearchWord(searchWord):
  cnx = mysql.connector.connect(user=dbUser, password=dbPassword, host=dbHost, database=dbDatabase, autocommit=dbAutoCommit)
  cursor = cnx.cursor()
  query = ("select distinct local_path, prediction_class from results where prediction_class = %s")
  cursor.execute(query, (searchWord,))
  print("Found following files for your search word \"" + searchWord + "\":")
  for (local_path, prediction_class) in cursor:
    foundFiles = [open(local_path, 'rb')]
    preparedImage224x224 = prepareImagesForClassification(foundFiles, 224, 224)[0]
    plt.figure()
    plt.imshow(preparedImage224x224)
    plt.title("{}".format(local_path))
    plt.axis('off')
    plt.show()
    plt.clf()
  cursor.close()
  cnx.close() 