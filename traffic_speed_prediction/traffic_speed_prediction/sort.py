import csv
with open('qgisdata.csv', 'r') as inp, open('databig.csv', 'w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
        if row[0] != "0" :
            writer.writerow(row)