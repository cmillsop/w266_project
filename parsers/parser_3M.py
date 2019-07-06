from bs4 import BeautifulSoup
import re
import os

path = os.path.dirname(os.path.realpath(__file__))
with open(rf'{path}\..\raw\3M_2019.htm') as f:
    html_doc = f.read()
soup = BeautifulSoup(html_doc, 'html.parser')
tables = soup.find_all(string="Nominees for director")[1].find_all_next('table',{'cellspacing':'0', 'border':'0', 'cellpadding':'0'})

z = [x for x in tables if len(x.findAll(text=re.compile('Director since'))) == 1]
for idx, table in enumerate(z):
    # row 1 is name, age, since
    # row 2 is professional qualifications, nominee qualifications, bullets
    with open(rf'{path}\..\parsed\3M_2019_{idx}.txt','wb+') as f:
        f.write(table.get_text().encode('utf-8'))