import re
def process_img(ocr_output:dict) -> str:
    timestamp_pattern =re.compile(r"([0-1]?[0-9]|2[0-3]):([0-5][0-9])")
    twinby_pattern = re.compile(r"(Полная информация|Совместимость)|(, \w+, \d{2})|((\w+), (\d{2})(.*?)(\d+) км)")
    leo_pattern = re.compile(r"(Leo – match and meet)|(Дайвинчик)|(, (\d{2}), )")
    features = {'timestamp_count':0, 'text':False, 'twinby_info':False}

    text = ocr_output['result']['textAnnotation']['fullText']
    print(ocr_output['result']['textAnnotation']['fullText'])
    text = text.replace('\n',' ')
    print(text)
    if not text:
        return features
    features['text'] = bool(text) 
    features['timestamp_count'] = len(timestamp_pattern.findall(text))
    print(text)
    print(features['timestamp_count'])
    features['dating'] = twinby_pattern.findall(text) or leo_pattern.findall(text)  
    
    return features