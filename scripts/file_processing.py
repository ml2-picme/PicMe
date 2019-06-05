# This file "file_processing.py" contains methods for downloading and working with files

# All needed imports for this script file
import urllib.request
import os
import shutil

# This method uses the urllib library and downloads a file from a URL to a local path
def downloadFileFromUrl(URL, localPath):
  print("Download", URL, "to", localPath)
  with urllib.request.urlopen(URL) as url:
    with open(localPath, 'wb') as f:
      f.write(url.read())
  #load_img(localPath)
  
# Extracts the absolution file path to find the file name in it (the part after the last "/" that is found)
def getFileNameFromPath(path):
  filename = path.split("/")[len(path.split("/")) - 1]
  return filename

# Creates a directory
def createLocalDirectory(dir):
  print("Create local directory:", dir, end='\t')
  try:  
    os.makedirs(dir)
  except OSError:  
    print (" - Failed")
  else:
    print(" - OK")
	
# Deletes a directory (recursive!)
def deleteLocalDirectory(dir):
  try:
    print("Delete local directory:", dir, end='')  
    shutil.rmtree(dir) 
    print(" - OK")
  except OSError:
    print(" - Failed")
	
# Walk through a directory (recursive) and find files with corresponding file extensions
def findFilesInPathByFileExtension(dir, extensionList):
  foundFiles = []
  # r=root, d=directories, f = files
  for r, d, f in os.walk(dir):
    for file in f:
      for extension in extensionList:
        if file.lower().endswith(extension.lower()):
            foundFiles.append(os.path.join(r, file))
            break
  return foundFiles