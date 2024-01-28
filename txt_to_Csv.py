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
