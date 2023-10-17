from promptflow import tool
import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

# In Python tool you can do things like calling external services or
# pre/post processing of data, pretty much anything you want


@tool
def echo(input: str) -> str:
    data =  {
    "input_data": {
        "columns": [
        "image"
        ],
        "index": [0],
        "data": [input]
    },
    "params": {}
    }

    body = str.encode(json.dumps(data))

    ##### IMPORTANT: Replace this with the URL for your endpoint #####
    url = 'https://endpoint.westeurope.inference.ml.azure.com/score'

    ##### IMPORTANT: Replace this with the primary/secondary key or AMLToken for the endpoint #####
    api_key = '1111111111111111111111111111'


    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    ### IMPORTANT: Replace 'yolof-r50-c5-8x8-1x-coco-6' with the name of your model deployment ###
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'yolof-r50-c5-8x8-1x-coco-6' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        # result = response.read()
        result = json.loads(response.read().decode("utf8", 'ignore'))

        objs = {}

        for b in result[0]['boxes']: 
            if b['score'] > 0.3:
                if objs.get(b['label'], -1) == -1:
                    objs[b['label']] = 1
                else:
                    objs[b['label']] = 1 + objs[b['label']]

                print(b['label'], b['score'])


        counts = ''

        for k in objs.keys():
            if objs[k] == 1:
                counts = counts + f"There is {objs[k]} {k} in this image. "
            else:
                counts = counts + f"There are {objs[k]} {k} in this image. "

        # print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        counts = error.read().decode("utf8", 'ignore')

    return counts
