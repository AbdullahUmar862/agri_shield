import os
import re

app_path = r"C:\Users\User\OneDrive\semester four computer science\Ai theory\aiagri\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

DETAILED_MANGO = """    "Mango_Healthy": {
        "plant_type": "Mango Fruit",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Smooth, unblemished skin with proper coloring",
            "Firm to the touch with a sweet aroma at the stem",
            "No dark sunken lesions or oozing sap"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Harvest with a 1-inch stem attached to prevent sap burn",
            "Wash fruit immediately after harvest to remove any sap",
            "Store at 55°F (13°C) to delay ripening if needed"
        ]
    },
    "Mango_Diseased": {
        "plant_type": "Mango Fruit",
        "health_status": "Diseased",
        "diagnosis": "Anthracnose / Stem-End Rot",
        "symptoms": [
            "Black, sunken, irregular lesions on the skin that merge together",
            "Tear-stain patterns of rot running down the side of the fruit",
            "Dark brown/black decay starting precisely at the stem attachment",
            "Pinkish spore masses visible in wet conditions"
        ],
        "medicine": [
            "Copper fungicides (e.g., Kocide) sprayed before and during flowering",
            "Azoxystrobin (Abound) applied during fruit development",
            "Post-harvest hot water treatment (125°F for 5 minutes) mixed with Prochloraz"
        ],
        "management": [
            "Prune the tree canopy extensively to ensure rapid drying after rain",
            "Do NOT pack diseased fruit with healthy ones as the fungus spreads via contact",
            "Harvest carefully to avoid bruising or scratching the waxy cuticle"
        ]
    },"""

# Remove old Mango keys
for fruit in ["Mango_Healthy", "Mango_Diseased"]:
    pattern = r'[ \t]*"' + fruit + r'":\s*\{.*?\}(?:,)?\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

# Insert detailed Mango keys
pattern_insert = r'(DISEASE_KNOWLEDGE\s*=\s*\{\n)'
content = re.sub(pattern_insert, r'\1' + DETAILED_MANGO + '\n', content, count=1)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Mango detailed knowledge added successfully!")
