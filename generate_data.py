import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize Faker for generating names and dates
fake = Faker()
np.random.seed(254) # Seed for reproducibility (254 is Kenya's code)

print("🚀 STARTING PHASE 1: Hospital Data Simulation...")

# ======================================================
# 1. LOAD YOUR RAW SOURCES (The Ingredients)
# ======================================================
try:
    print("   -> Loading raw source files...")
    df_locs = pd.read_csv('raw_sources/nairobi_locations.csv')
    df_insu = pd.read_csv('raw_sources/insurance_providers.csv')
    df_diseases = pd.read_csv('raw_sources/icd10_diseases.csv')
    df_drugs = pd.read_csv('raw_sources/kemsa_drugs.csv')
    print("   ✅ Raw files loaded successfully.")
except FileNotFoundError as e:
    print(f"   ❌ ERROR: Could not find file: {e}")
    print("      Make sure your CSVs are inside a folder named 'raw_sources'")
    exit()

# ======================================================
# 2. GENERATE INVENTORY TABLE
# ======================================================
print("   -> Generating Hospital Inventory...")

# We take your drug list and add Stock Management columns
df_inventory = df_drugs.copy()
df_inventory['Drug_ID'] = range(5001, 5001 + len(df_inventory)) # IDs start at 5001
df_inventory['Current_Stock'] = [random.randint(10, 500) for _ in range(len(df_inventory))]
df_inventory['Reorder_Level'] = 50 # Fixed reorder level for simplicity

# Business Logic: Force a "Stock Out" scenario for Analysis later
# Let's make 'Amoxicillin' critically low
df_inventory.loc[df_inventory['Drug_Name'].str.contains('Amoxicillin', case=False, na=False), 'Current_Stock'] = 8

# ======================================================
# 3. GENERATE PATIENTS TABLE
# ======================================================
print("   -> Generating Patient Records...")

num_patients = 15000 # Simulating 1200 registered patients
patients_data = []

for i in range(1, num_patients + 1):
    # Weighted Insurance: 40% Cash, 60% Insurance
    if random.random() < 0.4:
        insurance = 'Cash'
    else:
        # Pick a random insurer excluding 'Cash' from your list if it exists there
        insurers_only = df_insu[df_insu['Insurance_Provider'] != 'Cash']['Insurance_Provider'].values
        insurance = np.random.choice(insurers_only)

    patients_data.append({
        'Patient_ID': i,
        'Full_Name': fake.name(),
        'DOB': fake.date_of_birth(minimum_age=1, maximum_age=85),
        'Gender': np.random.choice(['Male', 'Female']),
        'Location': np.random.choice(df_locs['Location'].values),
        'Insurance_Provider': insurance
    })

df_patients = pd.DataFrame(patients_data)

# ======================================================
# 4. CLINICAL LOGIC ENGINE (The "Brain")
# ======================================================
# This dictionary maps Disease Keywords to appropriate Drug Keywords
# It ensures the data makes medical sense.

clinical_map = {
    'Malaria': ['AL', 'Artemether', 'Paracetamol'],
    'Typhoid': ['Ciprofloxacin', 'Paracetamol'],
    'Pneumonia': ['Amoxicillin', 'Azithromycin', 'Cough Syrup'],
    'Respiratory': ['Cetirizine', 'Cough Syrup', 'Salbutamol', 'Amoxicillin'],
    'Diabetes': ['Metformin', 'Glibenclamide'],
    'Hypertension': ['Losartan', 'Amlodipine'],
    'Gastritis': ['Omeprazole'],
    'Gastroenteritis': ['Metronidazole', 'ORS', 'Zinc'],
    'Urinary': ['Ciprofloxacin', 'Amoxicillin'],
    'Dermatitis': ['Cetirizine'],
    'Eczema': ['Cetirizine'],
    'Anemia': ['Multivitamins'],
    'Pain': ['Paracetamol', 'Ibuprofen', 'Diclofenac']
}

def get_prescribed_drug(disease_name):
    """Returns a drug that matches the disease."""
    for key, drugs in clinical_map.items():
        if key.lower() in str(disease_name).lower():
            return np.random.choice(drugs)
    # Fallback: If no specific match, prescribe a general painkiller or supplement
    return np.random.choice(['Paracetamol', 'Multivitamins', 'Ibuprofen'])

# ======================================================
# 5. GENERATE VISITS & TRANSACTIONS
# ======================================================
print("   -> Generating Visits and Pharmacy Orders...")

num_visits = 65000 # Simulating 20000 visits over the year
visits_data = []
orders_data = []
order_id_counter = 90001

start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
days_range = (end_date - start_date).days

for i in range(1, num_visits + 1):
    # 1. Create the Visit
    visit_id = 20000 + i
    patient_id = random.randint(1, num_patients)
    
    # Random Date
    visit_date = start_date + timedelta(days=random.randint(0, days_range))
    
    # Pick a Disease
    disease_row = df_diseases.sample(1).iloc[0]
    disease_name = disease_row['Disease_Name']
    icd_code = disease_row['ICD10_Code'] # Using your specific header
    
    visits_data.append({
        'Visit_ID': visit_id,
        'Patient_ID': patient_id,
        'Visit_Date': visit_date.strftime('%Y-%m-%d'),
        'Diagnosis': disease_name,
        'ICD10_Code': icd_code,
        'Department': np.random.choice(['Outpatient', 'Inpatient', 'Pediatrics'])
    })

    # 2. Create the Pharmacy Order (Clinical Logic applied here)
    # 80% of visits result in a pharmacy purchase
    if random.random() < 0.8:
        # Determine which drug to buy based on the disease
        prescribed_drug_keyword = get_prescribed_drug(disease_name)
        
        # Find the actual drug in inventory that matches the keyword
        # We look for the keyword inside the full 'Drug_Name' (e.g., find 'Amoxicillin' in 'Amoxicillin 500mg')
        matching_drugs = df_inventory[df_inventory['Drug_Name'].str.contains(prescribed_drug_keyword, case=False, na=False)]
        
        if not matching_drugs.empty:
            selected_drug = matching_drugs.sample(1).iloc[0]
            
            qty = random.randint(1, 3) # Bought 1 to 3 units
            total_cost = selected_drug['Unit_Price'] * qty
            
            orders_data.append({
                'Order_ID': order_id_counter,
                'Visit_ID': visit_id,
                'Drug_ID': selected_drug['Drug_ID'],
                'Quantity': qty,
                'Total_Cost': total_cost
            })
            order_id_counter += 1

# Convert to DataFrames
df_visits = pd.DataFrame(visits_data)
df_orders = pd.DataFrame(orders_data)

# ======================================================
# 6. SAVE OUTPUT FILES
# ======================================================
print("   -> Saving Generated Data to CSV...")

df_patients.to_csv('hospital_patients.csv', index=False)
df_visits.to_csv('hospital_visits.csv', index=False)
df_inventory.to_csv('hospital_inventory.csv', index=False)
df_orders.to_csv('hospital_orders.csv', index=False)

print("\n✅ SUCCESS! 4 Files Generated:")
print(f"   1. hospital_patients.csv ({len(df_patients)} rows)")
print(f"   2. hospital_visits.csv ({len(df_visits)} rows)")
print(f"   3. hospital_inventory.csv ({len(df_inventory)} rows)")
print(f"   4. hospital_orders.csv ({len(df_orders)} rows)")
print("\n👉 NEXT STEP: Open these files in Excel to inspect them.")


# Note: I have added the "Clinical Logic Engine" inside the script. 
# This ensures that if a patient gets Malaria, the script forces them to buy AL, not Metformin.
print("🚀 PHASE 1 COMPLETE.")
