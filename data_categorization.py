import csv
import pandas as pd
import numpy as np


input_file_path = 'output.csv' # Replace with the path to your csv file
output_file_path = 'Processed.CSV'

#with open(input_file_path, 'r', encoding='utf-8', errors='replace') as text_file, open(output_file_path, 'w', newline='') as csv_file:
#    writer = csv.writer(csv_file)

    # Read each line in the text file
#    for line in text_file:
#        # Split the line by pipe and write to the CSV file
#        writer.writerow(line.strip().split('|'))

#print('SUCCESSFULLY CONVERTED TO .CSV FILE FROM .TXT FILE')
#print('___________________________________________________')



# checking for duplicate values


print('\n\n')
data = pd.read_csv(input_file_path)
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
print("THE DATA HAS FOLLOWING NULL VALUES")
print('___________________________________________________')
print(data.isnull().sum())


data['Owner_Address'] = data['Owner_Address'].fillna('NAN')
data['Owner_CityState'] = data['Owner_CityState'].fillna('NAN')
data['TAD_Map'] = data['TAD_Map'].fillna('NAN')
data['MAPSCO'] = data['MAPSCO'].fillna('NAN')
data['LegalDescription'] = data['LegalDescription'].fillna('NAN')
data['County'] = data['County'].fillna(220)
data['City'] = data['City'].fillna(data['City'].min);
data['School'] = data['School'].fillna(data['School'].min);
data['Notice_Date'] = data['Notice_Date'].fillna(0)
data['Deed_Date'] = data['Deed_Date'].fillna('12-31-1900')
data['Deed_Book'] = data['Deed_Book'].fillna(0)
data['Deed_Page'] = data['Deed_Page'].fillna(0)
data['Instrument_No'] = data['Instrument_No'].fillna('0')
data['Overlap_Flag'] = data['Overlap_Flag'].fillna('0')
print('\n\n')
print('AFTER ELIMINATING NULL VALUES')
print('___________________________________________________')
print(data.isna().sum())
print('___________________________________________________')

#check which columns have multiple data types
df = pd.read_csv(input_file_path)

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



#   categorizing by Zip Codes and Displaying the total number of unique zipcodes generated
categorizeByZip = dict()
csvreader = csv.reader(open(input_file_path))
header = next(csvreader)
for row in csvreader:
        if(row[9]!= None):
            categorizeByZip[row[9]] = categorizeByZip.get(row[9],[])
print('\n\n')
print('THE DATA HAS '+str(len(categorizeByZip))+" UNIQUE ZIP CODES")
print('___________________________________________________')

# categorizing by Zip Codes and Displaying the Number of records per unique zipcode
csvreader = csv.reader(open(input_file_path))
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





#  dictionary mapping for indiviudal property_class
use_code_mapping = {
    "A": "Residential Single Family",
    "AC": "Single Family Interim Use",
    "A1": "Residential Single Family",
    "A2": "Residential Mobile Home",
    "A3": "Residential Condominium",
    "A4": "Residential Townhouse",
    "A5": "Residential Planned Unit",
    "B": "Multi-Family Residential",
    "BC": "Multi-Family Commercial",
    "B2": "Residential Duplex",
    "B3": "Residential Triplex",
    "B4": "Residential Quadplex",
    "C1": "Vacant Land Residential",
    "C1C": "Vacant Land Commercial",
    "C2": "Commercial Land With Improvement Value",
    "D1": "Qualified Open Space Land",
    "D2": "Farm and Ranch Improvements on Qualified Open Space Land",
    "E": "Rural Land (No Ag) and Improvements Residential",
    "EC": "Rural Land (No Ag) and Improvements Commercial",
    "F1": "Commercial",
    "F1C": "VarX Billboards",
    "F1P": "Billboards Personal Property",
    "F2": "Industrial",
    "G1": "Oil, Gas and Mineral Reserve",
    "J1": "Commercial Utility Water Systems",
    "J1C": "VarX Utility Water Systems",
    "J1P": "Personal Property Utility Water Systems",
    "J2": "Commercial Utility Gas Companies",
    "J2C": "VarX Utility Gas Companies",
    "J3": "Commercial Utility Electric Companies",
    "J3C": "VarX Utility Electric Companies",
    "J4": "Commercial Utility Telephone Companies",
    "J4C": "VarX Utility Telephone Companies",
    "J4P": "Personal Property Utility Telephone Companies",
    "J5": "Commercial Utility Railroads",
    "J5C": "VarX Utility Railroads",
    "J5P": "Personal Property Utility Railroads",
    "J6": "Commercial Utility Pipelines",
    "J6C": "VarX Utility Pipelines",
    "J7": "Commercial Utility Cable Companies",
    "J7C": "VarX Utility Cable Companies",
    "J7P": "Personal Property Utility Cable Companies",
    "J8": "Commercial Utility Other",
    "J8C": "VarX Utility Other",
    "L1": "Personal Property Tangible Commercial",
    "L1C": "VarX Commercial",
    "L1X": "VarX Parent Commercial",
    "L2": "Personal Property Tangible Industrial",
    "L2C": "VarX Industrial",
    "M1": "Mobile Home",
    "M2": "Personal Property Aircraft",
    "O": "Residential Inventory",
    "O1": "Residential Vacant Inventory",
    "O2": "Residential Improved Inventory",
    "RO": "Real Property Reference Only",
    "ROC": "Real Property Reference Only Commercial",
    "S": "Personal Property Special Inventory",
    "X": "Vacant Right of Way",
    "999": "Conversion Error Real Property"
}

# Check for null values in the 'Use Code' column
null_data = data[data['Property_Class'].isnull()]

if not null_data.empty:
    print("Warning: There are rows with null values in the Property_Class column")
#check for any unique values 
unique_values = set(data['Property_Class'].str.strip()) - set(use_code_mapping.keys()) 

if unique_values:
    print("Warning: There are unique_values values in the 'Property_Class' column:")
    print(unique_values)

# Mapping the Use_Description to Property Class 
data['Property_Description'] = data['Property_Class'].str.strip().map(use_code_mapping)


# Print the DataFrame to see the mapped descriptions
list_property_codes=(data[['Property_Class','Property_Description','Owner_Zip']])
print(list_property_codes)


# Initialize an empty dictionary to store grouped data
grouped_data = {}

# Iterate over each row in the DataFrame
for index, row in data.iterrows():
    # Get the zip code, property class, and use description from the current row
    zip_code = row['Owner_Zip']
    property_class = row['Property_Class']
    property_description = row['Property_Description']
    
    # Create a dictionary for the property class and use description
    property_dict = {'Property_Class': property_class, 'Property_Description': property_description}
    
    # Check if the zip code is already in the grouped data dictionary
    if zip_code in grouped_data:
        # If yes, append the property dictionary to the existing list
        grouped_data[zip_code].append(property_dict)
    else:
        # If no, create a new list with the property dictionary and add it to the dictionary
        grouped_data[zip_code] = [property_dict]

# Print the grouped data
for zip_code, properties in grouped_data.items():
    print(f"Zip Code: {zip_code}")
    for prop in properties:
        print(f"Property Class: {prop['Property_Class']}, Property_Description: {prop['Property_Description']}")



#Calculating Property Value by using apprisal_value
#if Apprisal value is zero we use Total Value and if that is zero we add 100$ and segregate by Zip Code
propertyValueByZip = {}

for i in categorizeByZip.keys():
    propertyValueByZip[i] = []
    
for row in categorizeByZip.keys():
    propertyValueByZip[i] = []
    for j in categorizeByZip[row]:
        propertyvalueData = propertyValueByZip[row]
        insertData = []
        propertyvalueData = propertyValueByZip[row]
        insertData.append(j[6])
        #property value
        if(int(j[52])>0):
            insertData.append(int(j[52]))
                
        else:
            insertData.append(100 if(int(j[34])==0) else j[34])
            
        #accerage
        insertData.append(j[43] if(float(j[43])>0) else str(0.0001))
        
        #property Type:
        insertData.append(use_code_mapping[j[17].strip()])
        
        # Property Tax Collected
        if(int(j[52])>0):
            insertData.append(j[52])
        else:
            insertData.append(100 if(int(j[34])==0) else j[34])
            
        #standard Metrics
        insertData.append(int(insertData[-1])/float(insertData[-3]))
        
        propertyvalueData.append(insertData)
        propertyValueByZip[row] = propertyvalueData

#Inserting the calculated value to CSV File
with open(output_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ZipCode','Owner Address','Property Value', 'Acerage', 'Property Description', 'Property Tax','Standardized Metric'])
    
    for i in propertyValueByZip.keys():
        for j in propertyValueByZip[i]:
           writer.writerow([i,j[0],j[1],j[2],j[3],j[4],j[5]])

print('SUCCESSFULLY CONVERTED THE PROCESSED DATA TO .CSV FILE')
        
    

