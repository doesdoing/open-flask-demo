def json(**a):
    e=len(a['data']) if len(a['data'])>10 else len(a['data'])
    data_arr=[]
    for x in range(e):
        tmp = {}
        for i in range(len(a['key'])): 
            tmp[a['key'][i]] = a['data'][x][i]
        data_arr.append(tmp)
    return data_arr