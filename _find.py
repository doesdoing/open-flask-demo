def find(**json):
    tmp_data=[]
    tmp_json={}
    for x in json['data']:
        if str(x[json['target']]).lower().find(json['value']) >= 0:
            tmp_data.append(x)
            tmp_json['data']=tmp_data[int(json['start']):int(json['end'])]
            tmp_json['len'] =len(tmp_data)
    return tmp_json