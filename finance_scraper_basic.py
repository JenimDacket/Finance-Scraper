#!/usr/bin/env python

def google_sector_report():
    import json
    from bs4 import BeautifulSoup as BS
    import requests as re
    response = re.get('https://www.google.com/finance')
    soup = BS(response.content, ('lxml'))
    jsond = {'result':{}}
    sectors = soup.find('div', class_='id-secperf').find_all('tr')
   
    for x in sectors:
        if x.has_attr('class') or x.find('a') == None:
            continue
        sector = x.find('a').get_text()
        jsond['result'][sector] = {}
        index = jsond['result'][sector]
        index['change'] = x.find('span').get_text()
                
        response = re.get('https://www.google.com' + x.find('a').get('href'))
        soup = BS(response.content, 'lxml').find('table', class_='topmovers')

        table = soup.find_all('tr')
        hold = get_gainers_losers(table)
        index['biggest_gainer'] = {}
        index['biggest_gainer']['equity'] = hold[0][0]
        index['biggest_gainer']['change'] = hold[0][1]
        
        index['biggest_loser'] = {}
        index['biggest_loser']['equity'] = hold[1][0]
        index['biggest_loser']['change'] = hold[1][1]

    json_string = json.dumps(jsond)
    return(json_string)


def get_gainers_losers(table):
    name = ''
    val = 0
    hold = []
    i = 0
    for row in table:
        if row.find('b') and val == 0:
            continue
        elif row.find('b'):
            hold.append([name, val])
            name = ''
            val = 0
            continue
        for chng in row.find_all('span'):
            if clean(chng) == None:
                continue
            temp = clean(chng)
        if temp > val:
            val = temp
            name = row.find('a').get_text()
    return(hold)
    
    
def clean(row):
    text = row.get_text()
    if not '%' in text:
        return (None)
    for i in text:
        if not i.isdigit(): 
            text = text.strip(i)
        text = text.strip('%')
    return(float(text))

print(google_sector_report())
