import email
from email import policy
from email.parser import BytesParser

# This opens an Email and extracts relevant information from it (from, to, subject, body). It writes these attributes and their values into a Dictionary object and returns it.

def examineEmail(pathToEmail):
  get_list = ['from','to','subject']
  info_dict = {}
  
  with open(pathToEmail, 'rb') as fp:  # select a specific email file from the list
    msg = BytesParser(policy=policy.default).parse(fp)
    text = msg.get_body(preferencelist=('plain')).get_content()
    
    for get_item in get_list:
      info_dict[get_item] = msg[get_item]
      
    info_dict["body"] = text
    
    return info_dict