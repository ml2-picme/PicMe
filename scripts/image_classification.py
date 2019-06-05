# This file "image_classification.py" contains methods for working with image classification.
# We use multiple, pretrained models for image classification: VGG16, VGG19, MobileNetV2, ResNet50, DenseNet201, InceptionV3, Xception, InceptionResNet
# All used models are trained on the ImageNet dataset. Information about the classification models can be found here: https://github.com/tensorflow/models/tree/master/research/slim

# All needed imports for this script file
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# This method takes a list of files, then creates numpy arrays of a pre-defined size (x, y) for these files and return the numpy arrays
def prepareImagesForClassification(files, sizeX, sizeY):
  images = []
  for file in files:
    try:
      image = Image.open(file)
      image = image.resize((sizeX, sizeY), Image.LANCZOS)
      image = image.convert("RGB")
      image = np.asarray(image)
      images.append(image)
    except OSError:
      pass
  images = np.asarray(images)
  return images
  
# This function takes the previously prepared images and predicts the classes based on the model
# The method takes the model depending preprocessInput and decodePrediction methods!
def classifyImages(preparedImages, function_preprocessInput, function_decodePredictions, model):
  # preprocess the images to fit to the model
  images_preprocessed = function_preprocessInput(preparedImages)
  # use the model to classifi the images
  images_pred = model.predict(images_preprocessed, verbose=1)
  # Decode the predictions using the function belonging to the model
  pred_results = function_decodePredictions(images_pred)
  return pred_results
  
# ======================== Methods for printing the classification results ========================

# Show the classification results in a good, readable format (prints the predications based on their model and accuracy
def compareResults(fileNames, resultsList, modelList, threshold, images):
  for i in range(len(fileNames)):
    print("Comparing the Results for File: " + fileNames[i])
    plt.figure()
    plt.imshow(images[i])
    plt.axis('off')
    plt.show()
    plt.clf()
    # For position 1 to 5 (top-5 accuracy)
    for j in range(5):
      for k in range(len(modelList)):
        resultToPrint = resultsList[k][i][j]
        # Using threshold to filter results
        if(resultToPrint is not None and resultToPrint[2] > threshold):
          print(" > Top", (j+1), "@", modelList[k], ":", resultsList[k][i][j])
        else:
          print(" > Top", (j+1), "@", modelList[k], ":", "--- Threshold-Filter ---")
      print("=================================================================")
    print("")
	
# Generates a CSV-like output for the results of the predictions -> these are used for the model_comparison Excel sheet
# It has the following structure:
# URL;Hyperlink(picture1);Hyperlink(picture2);...
# ModelName;picture1;picture2;...
# Top1;prediction1picture1;prediction1picture2;...
# Top2;prediction2picture1;prediction2picture2;...
# Top3;prediction3picture1;prediction3picture2;...
# Top4;prediction4picture1;prediction4picture2;...
# Top5;prediction5picture1;prediction5picture2;...
def generateCsvForModelComparison(fileNames, resultsList, modelList, filesDict):
  allModelCSVs = []
  # ===== Generate the Header rows =====
  # Walk through the different models
  for k in range(len(modelList)):
    # First row: The image URLs as Hyperlinks
    modelCSV = "URL"
    for i in range(len(fileNames)):
      modelCSV += ";" + "=HYPERLINK(\"" + filesDict[fileNames[i]] + "\")"
    modelCSV += "\n"
	# Second row: Model name + File names
    modelCSV += modelList[k]
    for i in range(len(fileNames)):
      modelCSV += ";" + getFileNameFromPath(fileNames[i])  
    modelCSV += "\n"
    # ===== Generate the content rows containing the results ======
    for j in range(5):
      modelCSV += "Top" + str(j+1)
	  # For each file print the x-th prediction position
      for i in range(len(fileNames)):
        modelCSV += ";" + str(resultsList[k][i][j][1])
      modelCSV += "\n"
    # Append the output for one model to the list of all model outputs
    allModelCSVs.append(modelCSV)
  return allModelCSVs
