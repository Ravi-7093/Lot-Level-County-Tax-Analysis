import csv
import pandas as pd
import numpy as np

# Path to your text file
input_file_path = '/Users/rav_1797/Desktop/Raw_Data_Set/PropertyData.txt'  # Replace with the path to your text file
output_file_path = '/Users/rav_1797/Desktop/output.csv'

with open(input_file_path, 'r', encoding='utf-8', errors='replace') as text_file, open(output_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Read each line in the text file
    for line in text_file:
        # Split the line by pipe and write to the CSV file
        writer.writerow(line.strip().split('|'))

print('SUCCESSFULLY CONVERTED TO .CSV FILE FROM .TXT FILE')
print('___________________________________________________')



# checking for duplicate values
print('\n\n')
data = pd.read_csv(output_file_path)
value = data.duplicated().sum()
if value>0:
    print("THE DATA HAS "+str(value)+" DUPLICATE VALUES")
    data.drop_duplicates()
    print("AFTER DELETING DUPLICATE VALUES THE RESULT IS "+str(data.duplicated().sum()))
else:
    print("THE DATA HAS NO DUPLICATE VALUES")
    print('___________________________________________________')
print('\n\n')




#checking for Null Values
print("DATA HAS FOLLOWING NULL VALUES")
print('___________________________________________________')
print(data.isnull().sum())
print('___________________________________________________')
data['Owner_Address'] = data['Owner_Address'].fillna('NAN')
data['Owner_CityState'] = data['Owner_CityState'].fillna('NAN')
data['Notice_Date'] = data['Notice_Date'].fillna(0)
data['Deed_Date'] = data['Deed_Date'].fillna('12-31-1900')
data['Instrument_No'] = data['Instrument_No'].fillna('0')
data['Overlap_Flag'] = data['Overlap_Flag'].fillna('0')
print('\n\n')
print('AFTER ELIMINATING NULL VALUES')
print('___________________________________________________')
print(data.isna().sum())
print('___________________________________________________')



#   categorizing by Zip Codes and Displaying the total number of unique zipcodes generated
categorizeByZip = dict()
csvreader = csv.reader(open(output_file_path))
header = next(csvreader)
for row in csvreader:
        if(row[9]!= None):
            categorizeByZip[row[9]] = categorizeByZip.get(row[9],[])
print('\n\n')
print('THE DATA HAS '+str(len(categorizeByZip))+" UNIQUE ZIP CODES")
print('___________________________________________________')

# categorizing by Zip Codes and Displaying the Number of records per unique zipcode
csvreader = csv.reader(open(output_file_path))
header = next(csvreader)
for row in csvreader:
    datavalue = categorizeByZip[row[9]]
    if(datavalue!= None):
        datavalue.append(row)
        categorizeByZip[row[9]] = datavalue
print('\n\n')  
for i in categorizeByZip.keys():
    if(categorizeByZip[i] != None) and (i != None):
        if(i == '     '):
            print("ZIP CODE NOT MENTIONED "+" has "+str(len(categorizeByZip[i]))+" LOCATIONS")
        else:
            print(i+" has "+str(len(categorizeByZip[i]))+" LOCATION")

#check which columns have multiple data types
df = pd.read_csv(output_file_path)

# Function to get unique data types in a column
def get_unique_data_types(column):
    return column.apply(lambda x: type(x)).unique()


data_types_per_column = {}

for column in df.columns:
    data_types_per_column[column] = get_unique_data_types(df[column])

for column, types in data_types_per_column.items():
    print(f"Column '{column}' contains types: {types}")

def convert_and_handle_nans(df):
    for column in df.columns:
        # Determine if the column has more than one unique data type
        unique_types = df[column].apply(lambda x: type(x)).unique()

        # If there's more than one unique type, perform conversion and handle NaNs
        if len(unique_types) > 1:
            # If the column is mostly numeric, convert non-numeric to NaN, then handle NaNs
            if np.issubdtype(df[column].dtype, np.number):
                df[column] = pd.to_numeric(df[column], errors='coerce')
                # Here you can decide how to handle NaNs, for example:
                # Fill NaNs with 0, mean, or median
                
                df[column].fillna(df[column].median(), inplace=True)
            else:
                # For columns that are not primarily numeric, convert everything to strings
                df[column] = df[column].astype(str)
                # Replace 'nan' string (resulting from conversion) with a placeholder
                df[column].replace('nan', 'Unknown', inplace=True)
        else:
            # If the column has a single type but still could contain NaNs, handle accordingly
            if df[column].isnull().any():
                if df[column].dtype == np.float64 or df[column].dtype == np.int64:
                    # Handle NaNs for numeric columns
                    df[column].fillna(df[column].median(), inplace=True)
                else:
                    # Handle NaNs for non-numeric columns
                    df[column].fillna('Unknown', inplace=True)

# Apply the function to your DataFrame
convert_and_handle_nans(df)

# Verify the conversions and NaN handling
for column in df.columns:
    print(f"{column}: {df[column].dtype}, NaNs: {df[column].isnull().any()}")


