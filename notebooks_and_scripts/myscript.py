#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

df = pd.read_csv("customer_raw.csv")

# 1. Deduplicate & Initialize
df = df.drop_duplicates().reset_index(drop=True)
df = df.replace("", np.nan)

# 2. Fix the CamelCase bug BEFORE title casing
# This converts 'LateDelivery' -> 'Late Delivery' and 'WebsiteIssue' -> 'Website Issue'
df["escalation_reason"] = df["escalation_reason"].str.replace(r'(?<=[a-z])(?=[A-Z])', ' ', regex=True)

# 3. Strip structural spaces & apply casing rules
df["region"] = df["region"].str.strip()
df["home_store"] = df["home_store"].str.strip()
df["loyalty_member"] = df["loyalty_member"].str.strip()
df["has_escalation"] = df["has_escalation"].str.strip()
df["escalation_reason"] = df["escalation_reason"].str.strip()

# Standardize regional text strings before title case
df["region"] = df["region"].replace({"Calg Downtown": "Calgary Downtown", "Calg SE": "Calgary SE", "Calg NW": "Calgary NW"})
df[["region", "escalation_reason"]] = df[["region", "escalation_reason"]].apply(lambda x: x.str.title())
df["home_store"] = df["home_store"].str.upper().str.replace(" ", "-")

# 4. Fill numeric fields
df["total_purchases"] = df["total_purchases"].fillna(0)
df["total_spent"] = df["total_spent"].fillna(0)
df["avg_purchase_value"] = df["avg_purchase_value"].fillna(0)

# 5. Convert and handle dates cleanly
df["signup_date"] = pd.to_datetime(df["signup_date"], errors='coerce', format='mixed')
df["first_purchase_date"] = pd.to_datetime(df["first_purchase_date"], errors='coerce', format='mixed')
df["last_purchase_date"] = pd.to_datetime(df["last_purchase_date"], errors='coerce', format='mixed')

df["signup_date"] = df["signup_date"].fillna(pd.Timestamp("2026-01-01"))
df["first_purchase_date"] = df["first_purchase_date"].fillna(pd.Timestamp("2026-01-01"))
df["last_purchase_date"] = df["last_purchase_date"].fillna(pd.Timestamp("2026-01-01"))

# 6. Boolean Mappings using string flags
df["loyalty_member"] = np.where((df["loyalty_member"] == "N") | (df["loyalty_member"] == "No") | (df["loyalty_member"] == "False") | (df["loyalty_member"].isna()), "False", df["loyalty_member"])
df["loyalty_member"] = np.where((df["loyalty_member"] == "0"), "False", df["loyalty_member"])
df["loyalty_member"] = np.where((df["loyalty_member"] == "1") | (df["loyalty_member"] == "True"), "True", df["loyalty_member"])
df["loyalty_member"] = np.where((df["loyalty_member"] == "Y") | (df["loyalty_member"] == "Yes"), "True", df["loyalty_member"])

df["has_escalation"] = np.where((df["has_escalation"] == "N") | (df["has_escalation"] == "No") | (df["has_escalation"] == "False") | (df["has_escalation"].isna()), "False", df["has_escalation"])
df["has_escalation"] = np.where((df["has_escalation"] == "0"), "False", df["has_escalation"])
df["has_escalation"] = np.where((df["has_escalation"] == "1") | (df["has_escalation"] == "True"), "True", df["has_escalation"])
df["has_escalation"] = np.where((df["has_escalation"] == "Y") | (df["has_escalation"] == "Yes"), "True", df["has_escalation"])

# 7. Cleaning up None types inside text columns
df["escalation_reason"] = df["escalation_reason"].replace(["None", ""], np.nan)

# 8. Set structural indicators and clear out all remaining NaNs
df[["annual_visits", "visits_2023"]] = df[["annual_visits", "visits_2023"]].fillna("-")
df["customer_rating"] = df["customer_rating"].fillna(np.nan) # Keeping real nulls as blank fields for SQL database safety
df = df.fillna("Unknown")

# Exporting fresh file
df.to_csv("customer_clean.csv", index=False)
print("CSV compiled successfully.")


# In[ ]:




