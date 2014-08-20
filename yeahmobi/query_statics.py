
import json

group_map = {}
data_map = {}
filter_map = {}
sort_map = {}



with open('F://query.list', 'r') as f:
    lines = f.readlines()
    total = len(lines)
    for line in lines:
        start_index = line.find('{"settings"')
        querystr = line[start_index:].strip()
        queryjson = json.loads(querystr)
        group = str(queryjson.get('group'))
        data = str(queryjson.get('data'))
        try:
            sort = str(queryjson.get('sort'))
        except Exception:
            sort = None
        try:
            filters = str(queryjson.get('filters').get('$and'))
        except Exception:
            filters = None
        
        if group not in group_map:
            group_map[group] = 1
        else:
            group_map[group] += 1

        if data not in data_map:
            data_map[data] = 1
        else:
            data_map[data] += 1

        if filters not in filter_map:
            filter_map[filters] = 1
        else:
            filter_map[filters] += 1

        if sort not in sort_map:
            sort_map[sort] = 1
        else:
            sort_map[sort] += 1


fobj = open('F://query_result.txt', 'w')

    
fobj.writelines('*' * 500) 
for key in group_map:
    fobj.writelines('%5d\t%4.2f\t%s\n' % (group_map[key], round(group_map[key]/total,2), key))
fobj.writelines('*' * 500)  
for key in data_map:
    fobj.writelines('%5d\t%4.2f\t%s\n' % (data_map[key], round(data_map[key]/total,2), key))
fobj.writelines('*' * 500)   
for key in filter_map:
    fobj.writelines('%5d\t%4.2f\t%s\n' % (filter_map[key], round(filter_map[key]/total,2), key))
fobj.writelines('*' * 500)  
for key in sort_map:
    fobj.writelines('%5d\t%4.2f\t%s\n' % (sort_map[key], round(sort_map[key]/total,2), key)) 

fobj.close()
        
