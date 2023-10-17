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
def florence(input: str) -> str:
    
    data =  {
        "url": input
    }

    body = str.encode(json.dumps(data))

    ['tags', 'objects', 'caption', 'read', 'smartCrops', 'denseCaptions', 'people']


    ##### IMPORTANT: Replace this with the URL for your endpoint #####
    url = 'https://endpoint.cognitiveservices.azure.com/computervision/imageanalysis:analyze?features=tags,objects,denseCaptions,people,smartCrops,caption,read&model-version=latest&language=en&api-version=2023-02-01-preview'


    ##### IMPORTANT: Replace this with the primary/secondary key or AMLToken for the endpoint #####
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = '111111111111111111111111111111111'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key': api_key}

    req = urllib.request.Request(url, body, headers)
    res = {}


    try:
        response = urllib.request.urlopen(req)

        # result = response.read()
        response = json.loads(response.read().decode("utf8", 'ignore'))

        
        res['main_caption'] = response['captionResult']['text']
        res['tags'] = [tag['name'] for tag in response['tagsResult']['values']]
        res['ocr'] = response['readResult']['content']
        res['captions'] = [caption['text'] for caption in response['denseCaptionsResult']['values']]

        res['text'] = f"This is an image. Main Caption: {res['main_caption']}\nOCR: {res['ocr']}\nDense Captions: {', '.join(res['captions'])}\nTags: {', '.join(res['tags'])}"


        # print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))
        res['text'] = error.read().decode("utf8", 'ignore')

    return res['text']
