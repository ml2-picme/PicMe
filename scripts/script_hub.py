from urllib.request import urlopen
from keras.applications import *

import sys
import hashlib

import db_connector
import file_processing
import image_classification
import imagenet_tree_search
import text_processing
import email_processing

def createDbConnection(dbUser, dbPassword, dbHost, dbDatabase, dbAutoCommit):
  return db_connector.createConnection(dbUser, dbPassword, dbHost, dbDatabase, dbAutoCommit)

# This is the entry method for directory preparation. It downloads the files from ./input directory into local directories on colab instance
def simulateDirectoryStructure(path, hashrange):
  createDirectoryStructure(path, hashrange)
  downloadPictures(path, hashrange)
  downloadEmails(path, hashrange)

# This is the entry method for examining the local directory structure. It looks for images, emails and documents and writes results to DB
def examineDirectoryStructure(path, imageExtensions, emailExtensions, documentExtensions, dbConnection):
  examineImages(path, imageExtensions, dbConnection)
  examineEmails(path, emailExtensions, dbConnection)

# This is the entry method for finding results based on a fix search-term
def searchByTerm(searchTerm, dbConnection):
  searchTheDbBasedOnTerm(searchTerm, dbConnection)

# This is the entry method for automatically finding image-text mappings
def searchImageTextMappings(dbConnection):
  searchDbAutomaticallyForImageTextMappings(dbConnection)

"""### Method definitions"""

def createDirectoryStructure(path, hashrange):
  # Step 1: Delete local files, if existing
  file_processing.deleteLocalDirectory(path)
  
  # Step 2: Re-create local directory structure
  for i in range(hashrange):
    if(i % 10 == 0):
      parentPath = path + "/" + str((int)(i/10))
      file_processing.createLocalDirectory(parentPath)
    normalizedI = '%02d' % i  # Normalization, pad zeroes
    filePath = parentPath + "/" + normalizedI
    file_processing.createLocalDirectory(filePath)

def downloadPictures(path, hashrange):
  
  filesDict = {}

  data = urlopen("https://raw.githubusercontent.com/ml2-picme/PicMe/master/input/images_subset.txt")
  for line in data:
    if not line.startswith(b'#'):                     # Ignore Lines that begin with a comment (#)
      line = line.decode("utf-8").split("\n")[0]      # Normalization
      url = line.split(";")[0]
      label = line.split(";")[1]

      filename = file_processing.getFileNameFromPath(url)

      hashvalue = int(hashlib.sha1(filename.encode('utf-8')).hexdigest(), 16) % hashrange  # get the hash-value from filename
      parent_dir = (int)(hashvalue / 10)
      hashvalue = '%02d' % hashvalue                  # Normalization, pad zeroes

      filetype = filename.split(".")[len(filename.split(".")) - 1]
      newFilename = label + "." + filetype

      print(url, " -> ", hashvalue, " -> ", label, " -> ", parent_dir, " -> ", filename)

      localPath = path + "/" + str(parent_dir) + "/" + hashvalue + "/" + newFilename
      file_processing.downloadFileFromUrl(url, localPath)
      filesDict[localPath] = url
      
  return filesDict

def downloadEmails(path, hashrange):
  filesDict = {}

  data = urlopen("https://raw.githubusercontent.com/ml2-picme/PicMe/master/input/emails.txt")
  for line in data:
    if not line.startswith(b'#'):                     # Ignore Lines that begin with a comment (#)
      url = line.decode("utf-8").split("\n")[0]      # Normalization

      filename = file_processing.getFileNameFromPath(url)

      hashvalue = int(hashlib.sha1(filename.encode('utf-8')).hexdigest(), 16) % hashrange  # get the hash-value from filename
      parent_dir = (int)(hashvalue / 10)
      hashvalue = '%02d' % hashvalue                  # Normalization, pad zeroes

      print(url, " -> ", hashvalue, " -> ", parent_dir, " -> ", filename)

      localPath = path + "/" + str(parent_dir) + "/" + hashvalue + "/" + filename
      file_processing.downloadFileFromUrl(url, localPath)
      filesDict[localPath] = url
      
  return filesDict

def examineImages(path, imageExtensions, dbConnection):
  
  # Step 1: Search the directory based on file extensions
  foundFiles = file_processing.findFilesInPathByFileExtension(path, imageExtensions)

  for foundFile in foundFiles:
    print(foundFile)

  # Step 2: Prepare the found images for classification
  preparedImages224x224 = image_classification.prepareImagesForClassification(foundFiles, 224, 224)
  preparedImages299x299 = image_classification.prepareImagesForClassification(foundFiles, 299, 299)
  
  # Step 3: CLASSIFY THE IMAGES
  # Important: We give functions here: 
  # 1) preprocess_input function
  # 2) decode_predictions function
  # => These functions are model-dependent!
  predictedClassesVGG16 = image_classification.classifyImages(preparedImages224x224, vgg16.preprocess_input, vgg16.decode_predictions, vgg16.VGG16(input_shape=(224, 224, 3)))
  predictedClassesVGG19 = image_classification.classifyImages(preparedImages224x224, vgg19.preprocess_input, vgg19.decode_predictions, vgg19.VGG19(input_shape=(224, 224, 3)))
  #predictedClassesMobileNetV2 = classifyImages(preparedImages224x224, mobilenet_v2.preprocess_input, mobilenet_v2.decode_predictions, mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3)))
  #predictedClassesResNet50 = classifyImages(preparedImages224x224, resnet50.preprocess_input, resnet50.decode_predictions, resnet50.ResNet50(input_shape=(224, 224, 3)))
  #predictedClassesDenseNet201 = classifyImages(preparedImages224x224, densenet.preprocess_input, densenet.decode_predictions, densenet.DenseNet201(input_shape=(224, 224, 3)))
  #predictedClassesInceptionV3 = classifyImages(preparedImages299x299, inception_v3.preprocess_input, inception_v3.decode_predictions, inception_v3.InceptionV3(input_shape=(299, 299, 3)))
  #predictedClassesXception = classifyImages(preparedImages299x299, xception.preprocess_input, xception.decode_predictions, xception.Xception(input_shape=(299, 299, 3)))
  #predictedClassesInceptionResNet = classifyImages(preparedImages299x299, inception_resnet_v2.preprocess_input, inception_resnet_v2.decode_predictions,inception_resnet_v2.InceptionResNetV2(input_shape=(299, 299, 3)))
  
  resultsList = [predictedClassesVGG16, predictedClassesVGG19]#, predictedClassesMobileNetV2, predictedClassesResNet50, predictedClassesDenseNet201, predictedClassesInceptionV3, predictedClassesXception, predictedClassesInceptionResNet]
  modelList = ['VGG16', 'VGG19']#, 'MobileNetV2', 'ResNet50', 'DenseNet201', 'InceptionV3', 'Xception', 'InceptionResNet']
  
  # Step 4: Iterate the results
  # a) save the result to DB
  # b) search the ImageNet tree to expand the list of matching class names
  # c) save also these results to DB
  
  parentToChildrenDictionary = imagenet_tree_search.getParentToChildrenDictionary()
  childToParentsDictionary = imagenet_tree_search.getChildToParentsDictionary()
  
  # Iterating the classification results:
  for k in range(len(modelList)):
      print("==== other model =====")
      for i in range(len(foundFiles)):
        print("==== other file =====")
        for j in range(5):
          print("Counter:")
          print("Model", (k+1), "of", len(modelList))
          print("File", (i+1), "of", len(foundFiles))
          print("Top", (j+1), "of", 5)

          fileName = foundFiles[i]
          modelName = modelList[k]
          predictedClassSynsetId = resultsList[k][i][j][0]
          predictedClass = resultsList[k][i][j][1]
          predictedProbability = resultsList[k][i][j][2]

          # a) Store the original class to DB
          db_connector.storeImageClassificationResultToDB(dbConnection, fileName, modelName, predictedClass, predictedProbability)

          # b) Expand ImageNet classes by ImageNet tree search
          newWords = imagenet_tree_search.getWords(predictedClassSynsetId, parentToChildrenDictionary, childToParentsDictionary)

          # c) Also save these new results to DB
          for newWord in newWords:
            db_connector.storeImageClassificationResultToDB(dbConnection, fileName, modelName, newWord, predictedProbability)

def examineEmails(path, emailExtensions, dbConnection):
  
  emailsDict = {}
  stemmingStopWords = text_processing.prepare()
  
  # Step 1: Search the directory based on file extensions
  emailList = file_processing.findFilesInPath(localEmailPath, extensionsToCheck)
  
  # Step 2: Iterate the Emails and examine their content
  for email in emailList:
    
    # a) Examine email content
    emailDict = examineEmail(email)
    
    emailPath = email
    emailFrom = emailDict["from"]
    emailTo = emailDict["to"]
    emailSubject = emailDict["subject"]
    emailBody = emailDict["body"]
    
    # b) Prepare for stemming
    normalizedSubject = text_processing.normalizeWords(emailSubject, stemmingStopWords)
    normalizedBody = text_processing.normalizeWords(emailBody, stemmingStopWords)
    
    stemmingWords = []
    
    stemmedBody = text_processing.stem(normalizedSubject)
    stemmedSubject = text_processing.stem(normalizedBody)
    
    stemmingWords.extend(stemmedSubject)
    stemmingWords.extend(stemmedBody)
    
    # c) Store the results into DB
    storeTextStemmingResultToDB(dbConnection, emailPath, emailFrom, emailTo, emailSubject, emailBody, stemmingWords)

def searchTheDbBasedOnTerm(searchTerm, dbConnection):
  resultCursor = db_connector.querySearchWordAndPrintResults(dbConnection, searchTerm, image_classification.prepareImagesForClassification)

def searchDbAutomaticallyForImageTextMappings(dbConnection):
  print("todo")