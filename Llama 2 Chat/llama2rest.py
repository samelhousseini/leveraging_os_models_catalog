import urllib.request
import json
import os
import ssl
from promptflow import tool


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script





# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(query: str, chat_history: []) -> str:


  messages = []

  for h in chat_history:
    print(h)
    messages.append({ "role": "user",     "content": h['inputs']['question']} )
    messages.append({ "role":"assistant", "content": h['outputs']['answer']}) 

  messages.append({"role": "user", "content": query + '. Keep your answer concise and to the point, please reply in 3 sentences or less.'})

  print(messages)
    

  data =  {
    "input_data": {
        "input_string": messages
    },
    "parameters": {
      "temperature": 0.6,
      "top_p": 0.9,
      "do_sample": True,
      "max_new_tokens": 200
    }
  }


  print(data)

  body = str.encode(json.dumps(data))

  ##### IMPORTANT: Replace this with the URL for your endpoint #####
  url = 'https://endpoint.westeurope.inference.ml.azure.com/score'


  ##### IMPORTANT: Replace this with the primary/secondary key or AMLToken for the endpoint #####
  # Replace this with the primary/secondary key or AMLToken for the endpoint
  api_key = '111111111111111111111111111111111'
  if not api_key:
      raise Exception("A key should be provided to invoke the endpoint")

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  ### IMPORTANT: Replace 'yolof-r50-c5-8x8-1x-coco-6' with the name of your model deployment ###
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'llama-2-13b-chat-10' }

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)
      print(response)
      result = json.loads(response.read().decode("utf8", 'ignore'))['output']
      print(result)
      return result
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      # print(error.info())
      print(error.read().decode("utf8", 'ignore'))
      return error.read().decode("utf8", 'ignore')

