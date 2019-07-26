import openpyxl
import re
import csv

wb = openpyxl.load_workbook('spx_gov_2019.xlsx')
sheet = wb['Sheet1']

rules = ['(?!I?n?c\.)(?!Y?a?h?o?o!)([aA-zZ\d!]+)([!\.,\-:\?\(\)\#\&])','([!\.,\-:\?\(\)\#\&])([aA-zZ\d]+)',"(\w+)(n't)","(\w+)('s)","(\w+)('.*)"]

all_bios = []
max_length = 0

for i, row in enumerate(sheet.values):
    for j,value in enumerate(row):
        if i > 0 and j  > 13:
            if value is not None:
                # replace non-breaking spaces
                bio = value.replace(u'\xa0',' ')
                # replace right single quote
                bio = bio.replace(chr(8217),"'")
                # replace hair space
                bio = bio.replace(u'\u200A',' ')
                # replace macron
                bio = bio.replace(u'\u0113', 'e')
                # replce non-breaking hyphen
                bio = bio.replace(u'\u2011', '-')
                # replace thin space
                bio = bio.replace(u'\u2009', ' ')
                # replace en space
                bio = bio.replace(u'\u2002', ' ')
                for rule in rules:
                    bio = re.sub(rule, "\g<1> \g<2>", bio)
                all_bios += ["\n"] + bio.split(" ")
                if len(bio.split(" ")) > max_length:
                    max_length = len(bio.split(" "))

with open('bios.csv', 'w', newline='') as csvfile:
    #spamwriter = csv.writer(csvfile,quoting=csv.QUOTE_MINIMAL, escapechar='\\')
    for line in all_bios:
        csvfile.write(line + "\n")

print("exported bios.csv")
print(f"maximum bio length: {max_length} words/tokens")
