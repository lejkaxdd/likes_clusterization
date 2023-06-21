import requests
import json
import re
import time
from auth_data import token
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By



group_name = '197542079'

full_dict_of_users = {}
full_dict_of_likes = {}

offset = [int(x) for x in range(0, 61000, 1000)]
posts = ['https://vk.com/kero_kero20?w=wall-197542079_36883', 'https://vk.com/kero_kero20?w=wall-197542079_37019',
        'https://vk.com/kero_kero20?w=wall-197542079_32478', 'https://vk.com/kero_kero20?w=wall-197542079_37304']
post_name = ['Я тиран в оборонительной игре', 'Элис: наложница императора',  'СМЕРТЬ', 'Святая, удочеренная эрцгерцогом']

for x in offset:
    print('offset = ', x )
    get_members = f'https://api.vk.com/method/groups.getMembers?group_id={group_name}&fields=sex,country,city,bdate&offset={x}&access_token={token}&v=5.131'
    req = requests.get(get_members)
    members = json.loads(req.text)
    print(members)
    response = members["response"]
    items = response["items"]

    for i in range(len(items)):
        # try:
        tmp_list = []
        # print(items[i])
        id = items[i]['id']
        
        if 'bdate' in items[i]:
            bd_str = items[i]['bdate']
            bd  = int(bd_str.split('.')[-1])
            if bd > 1900:
                bd = 2023 - bd
                tmp_list.append(bd)
        
        if 'country' in items[i]:
            contry = items[i]['country']['title']
            tmp_list.append(contry)
        
        if 'city' in items[i]: 
            city = items[i]['city']['title']
            tmp_list.append(city)
            
        sex = items[i]['sex']
        
        if sex == 1:
            sex = 'Ж'
        else:
            sex = 'М'
            
        name = items[i]['first_name']
        surname = items[i]['last_name']
        
        tmp_list.append(sex)
        tmp_list.append(name)
        tmp_list.append(surname)
        full_dict_of_users[id] = tmp_list
            
# print(full_dict_of_users)
with open('users.txt', 'w', encoding="utf-8") as f:
    f.write(json.dumps(full_dict_of_users, ensure_ascii=False))
    f.close()

driver = webdriver.Edge()
driver.get('https://vk.com/login')


# Login 
number = driver.find_element('xpath' , '//*[@id="index_email"]') 
number.click()
number.send_keys(phone)
voiti_1 = driver.find_element('xpath' , '//*[@id="content"]/div[1]/form/button/span')
voiti_1.click()
time.sleep(5)
input_pass = driver.find_element('xpath' , '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[1]/div[3]/div[1]/div/input')
input_pass.click()
input_pass.send_keys(password)
vk_button_in = driver.find_element('xpath', '//*[@id="root"]/div/div/div/div/div[1]/div/div/div/div/form/div[2]/button/span[1]')
vk_button_in.click()
time.sleep(5)

# Parsing
try: 
    for i in range(len(posts)):
        element = driver.get(posts[i])
        time.sleep(15)
        likes = driver.find_element('xpath', '//*[@id="wk_likes_rows"]').text
        full_dict_of_likes[post_name[i]] = re.split("\n+", likes)
            
    print(full_dict_of_likes)

    with open('likes.txt', 'w', encoding="utf-8") as f_l:
        f_l.write(json.dumps(full_dict_of_likes,ensure_ascii=False))
        f_l.close()
except IOError as e:
        print(e)
