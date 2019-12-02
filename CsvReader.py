import csv

with open('assets/frame0.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
  for row in spamreader:
     print(row)