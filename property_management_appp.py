import streamlit as st
import pandas as pd
import os

# File to store the property data
file_path = "properties.csv"

# Function to load data from CSV
def load_data():
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        # Ensure that the necessary columns exist
        if 'Property ID' not in data.columns or 'Flat Number' not in data.columns:
            return pd.DataFrame(columns=["Property ID", "Flat Number", "Name", "Type", "Location", "Rent", "Number of Flats", "Flat Size (sq meters)", "Flat Status"])
        return data
    else:
        # Return a DataFrame with required columns if file doesn't exist
        return pd.DataFrame(columns=["Property ID", "Flat Number", "Name", "Type", "Location", "Rent", "Number of Flats", "Flat Size (sq meters)", "Flat Status"])

# Function to save data to CSV
def save_data(data):
    data.to_csv(file_path, index=False)

# Function to generate new Property and Flat IDs
def generate_ids(df):
    if df.empty:
        return 1, 1  # Starting with ID 1 for both Property and Flat
    else:
        max_property_id = df['Property ID'].max()
        max_flat_id = df['Flat Number'].max()
        return max_property_id + 1, max_flat_id + 1

# Title of the app
st.title("Property Management App")

# Load property data
properties = load_data()

# Sidebar for adding or updating properties
st.sidebar.header("Add or Update Property")

# Input fields
property_name = st.sidebar.text_input("Property Name")
property_type = st.sidebar.selectbox("Property Type", ["Apartment", "House", "Condo", "Commercial"])
property_location = st.sidebar.text_input("Location")
property_rent = st.sidebar.number_input("Monthly Rent (AED)", min_value=100, step=50)
num_flats = st.sidebar.number_input("Number of Flats", min_value=1, step=1)
flat_size = st.sidebar.number_input("Size of Each Flat (sq meters)", min_value=10, step=1)
flat_status = st.sidebar.selectbox("Flat Status", ["Vacant", "In Use"])

# Choose whether to add a new property or update an existing one
action = st.sidebar.selectbox("Action", ["Add New Property", "Update Existing Property", "Delete Property"])

if action == "Add New Property":
    if st.sidebar.button("Add Property"):
        new_property_id, new_flat_id = generate_ids(properties)
        new_data = pd.DataFrame({
            "Property ID": [new_property_id],
            "Flat Number": [new_flat_id],
            "Name": [property_name],
            "Type": [property_type],
            "Location": [property_location],
            "Rent": [property_rent],
            "Number of Flats": [num_flats],
            "Flat Size (sq meters)": [flat_size],
            "Flat Status": [flat_status]
        })
        properties = pd.concat([properties, new_data], ignore_index=True)
        save_data(properties)
        st.sidebar.success(f"Property '{property_name}' added successfully!")

elif action == "Update Existing Property":
    property_id_to_update = st.sidebar.number_input("Enter Property ID to Update", min_value=1)
    flat_id_to_update = st.sidebar.number_input("Enter Flat Number to Update", min_value=1)
    
    # Check if the property exists
    if st.sidebar.button("Update Property"):
        if not properties[(properties['Property ID'] == property_id_to_update) & (properties['Flat Number'] == flat_id_to_update)].empty:
            properties.loc[(properties['Property ID'] == property_id_to_update) & (properties['Flat Number'] == flat_id_to_update), 
                           ["Name", "Type", "Location", "Rent", "Number of Flats", "Flat Size (sq meters)", "Flat Status"]] = [
                property_name, property_type, property_location, property_rent, num_flats, flat_size, flat_status]
            save_data(properties)
            st.sidebar.success(f"Property '{property_id_to_update}' updated successfully!")
        else:
            st.sidebar.error(f"No property found with ID {property_id_to_update} and Flat Number {flat_id_to_update}")

elif action == "Delete Property":
    property_id_to_delete = st.sidebar.number_input("Enter Property ID to Delete", min_value=1)
    flat_id_to_delete = st.sidebar.number_input("Enter Flat Number to Delete", min_value=1)

    # Check if the property exists
    if st.sidebar.button("Delete Property"):
        if not properties[(properties['Property ID'] == property_id_to_delete) & (properties['Flat Number'] == flat_id_to_delete)].empty:
            properties = properties[~((properties['Property ID'] == property_id_to_delete) & (properties['Flat Number'] == flat_id_to_delete))]
            save_data(properties)
            st.sidebar.success(f"Property '{property_id_to_delete}' deleted successfully!")
        else:
            st.sidebar.error(f"No property found with ID {property_id_to_delete} and Flat Number {flat_id_to_delete}")

# Display all properties
st.subheader("All Properties")
st.dataframe(properties)

# Filter by location
filter_location = st.text_input("Filter by Location")
if filter_location:
    filtered_properties = properties[properties['Location'].str.contains(filter_location, case=False)]
    st.write("Filtered Properties:")
    st.dataframe(filtered_properties)

# Filter by flat status (Vacant/In Use)
filter_status = st.selectbox("Filter by Flat Status", ["All", "Vacant", "In Use"])
if filter_status != "All":
    filtered_properties = properties[properties['Flat Status'] == filter_status]
    st.write(f"Properties with status '{filter_status}':")
    st.dataframe(filtered_properties)
