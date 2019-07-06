from bs4 import BeautifulSoup
import re
import os

path = os.path.dirname(os.path.realpath(__file__))
raw = os.listdir(rf'{path}\..\raw')

for raw_file in raw:
    with open(rf'{path}\..\raw\{raw_file}') as f:
        html_doc = f.read()

    soup = BeautifulSoup(html_doc, 'html.parser')

    if '2019' in raw_file:
        tables = soup.find_all(string="Nominees for director")[1].find_all_next('table',{'cellspacing':'0', 'border':'0', 'cellpadding':'0'})

        z = [x for x in tables if len(x.findAll(text=re.compile('Director since'))) == 1]
        for idx, table in enumerate(z):
            # row 1 is name, age, since
            # row 2 is professional qualifications, nominee qualifications, bullets
            out_name = f'{raw_file[:raw_file.find(".htm")]}_{idx}.txt'
            with open(rf'{path}\..\parsed\{out_name}','wb+') as f:
                f.write(table.get_text().encode('utf-8'))
    else:
        print(raw_file)
        current = soup.find(string=re.compile("Nominees\s+for\s+Director:")).find_next('img').parent
        idx = 0
        while not current.find(string=re.compile('RECOMMENDATION OF THE BOARD')):
            out_name = f'{raw_file[:raw_file.find(".htm")]}_{idx}.txt'
            with open(rf'{path}\..\parsed\out_name','wb+') as f:
                flag = True
                while flag:
                    current = current.find_next_sibling()
                    if current.find('img'):
                        flag = False
                    else:
                        print(current.get_text())
                        f.write(current.get_text().encode('utf-8'))
            idx += 1