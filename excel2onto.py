import openpyxl
import nltk

nltk.download('punkt')

wb = openpyxl.load_workbook('spx_gov_2019.xlsx')
sheet = wb['Sheet1']

all_bios = []
max_length = 0
bio_count = 0

for i, row in enumerate(sheet.values):
    for j,value in enumerate(row):
        if i > 0 and j  > 13 and j < 30:
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
                company= sheet['A' + str(i+1)].value
                bio_count +=1                
                for sentence in nltk.sent_tokenize(bio):
                    words = nltk.word_tokenize(sentence)
                    all_bios.append([words, company, bio_count])
                    if len(words) > max_length:
                        max_length = len(words)

with open('bios.csv', 'w', newline='') as csvfile:
    csvfile.write("token\tcompany\tdirector\tlabel\n")
    for director in all_bios:
        for line in director[0]:
            csvfile.write(f"{line}\t{director[1]}\t{director[2]}\n")
        csvfile.write("\n")
print("exported: bios.csv")
print(f"maximum sentence length: {max_length} tokens")
