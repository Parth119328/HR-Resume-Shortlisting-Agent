import json 

def readLinkedinJSON(uploaded_file):
    raw_data = uploaded_file.read()
    json_text = raw_data.decode("utf-8")
    data = json.loads(json_text)
    return data