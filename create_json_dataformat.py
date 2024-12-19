import pandas as pd
import json

# Load the CSV file into a DataFrame
df = pd.read_csv('/content/drive/MyDrive/Data/BuildPermit.csv')

# Group the data by zip code and building type, summing the values
grouped = df.groupby(['Zip Code', 'Permit Type Description'])['Construction Cost'].sum().reset_index()

# Create the hierarchical JSON structure
city_data = {
    "city": {
        "parent": "city",
        "children": []
    }
}

# Build the structure
for zip_code, group in grouped.groupby('Zip Code'):
    zip_code_node = {
        "zip_code": zip_code,
        "parent": zip_code,
        "children": []
    }
    
    for _, row in group.iterrows():
        building_type_node = {
            "building_type": row['Permit Type Description'],
            "value": row['Construction Cost']
        }
        zip_code_node["children"].append(building_type_node)
    
    city_data["city"]["children"].append(zip_code_node)

# Convert to JSON string (if needed)
json_data = json.dumps(city_data, indent=4)

# Save the JSON to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_data)

# Print the JSON structure
print(json_data)
