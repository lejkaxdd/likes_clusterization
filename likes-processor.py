import json
import re
from collections import Counter

with open('users.txt', encoding='utf-8') as f:
    users = f.read()
    
with open('likes.txt', encoding='utf-8') as f_l:
    likes = f_l.read()
    
dict_users = json.loads(users)
dict_likes = json.loads(likes)

analitic_dict = {}

for key in dict_likes:
    tmp_sex = []
    tmp_city = []
    tmp_age = []
    tmp_full = []
    count = 0
    for element in dict_likes[key]:
        for id in dict_users:
            fio = dict_users[id][-2] + ' ' + dict_users[id][-1]
            if element == fio:
                count += 1
                for k in range(len(dict_users[id])):
                    if isinstance(dict_users[id][k], int):
                        tmp_age.append(dict_users[id][k])
                    if dict_users[id][k] == 'Ж' or dict_users[id][k] =='М':
                        tmp_sex.append(dict_users[id][k])
                    if isinstance(dict_users[id][k], str) and dict_users[id][k] != 'Ж' and dict_users[id][k] != 'М' and (len(dict_users[id][-2]+dict_users[id][-2])) > 9:
                            tmp_city.append(dict_users[id][k])  

    tmp_full.append(Counter(tmp_age))
    tmp_full.append(Counter(tmp_sex))   
    tmp_full.append(count)    
    analitic_dict[key] = tmp_full
        
                
print(analitic_dict)
                
                
                
                    
                