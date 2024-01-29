import csv

# Path to your text file
input_file_path = '/Users/rav_1797/Desktop/Raw_Data_Set/PropertyData.txt'  # Replace with the path to your text file
output_file_path = '/Users/rav_1797/Desktop/output.csv'

# Open the text file and a new CSV file
with open(input_file_path, 'r', encoding='utf-8', errors='replace') as text_file, open(output_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Read each line in the text file
    for line in text_file:
        # Split the line by pipe and write to the CSV file
        writer.writerow(line.strip().split('|'))

#   categorizing by Zip Codes and Displaying the total number of unique zipcodes generated
categorizeByZip = dict()
csvreader = csv.reader(open(output_file_path))
header = next(csvreader)
for row in csvreader:
        if(row[9]!= None):
            categorizeByZip[row[9]] = categorizeByZip.get(row[9],[])
print(len(categorizeByZip))

# categorizing by Zip Codes and Displaying the Number of records per unique zipcode
csvreader = csv.reader(open(output_file_path))
header = next(csvreader)
for row in csvreader:
    datavalue = categorizeByZip[row[9]]
    if(datavalue!= None):
        datavalue.append(row)
        categorizeByZip[row[9]] = datavalue
    
for i in categorizeByZip.keys():
    if(categorizeByZip[i] != None) and (i != None):
        if(i == '     '):
            print("ZIP Code Not Mentioned "+" has "+str(len(categorizeByZip[i]))+" locations")
        else:
            print(i+" has "+str(len(categorizeByZip[i]))+" locations")
