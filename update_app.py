import os

app_path = r"C:\Users\User\OneDrive\semester four computer science\Ai theory\aiagri\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

NEW_KNOWLEDGE = """    "Blueberry_Healthy": {
        "plant_type": "Blueberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Plump, firm berries with natural bloom"],
        "medicine": ["No treatment needed"],
        "management": ["Maintain acidic soil (pH 4.5-5.5)"]
    },
    "Blueberry_Diseased": {
        "plant_type": "Blueberry",
        "health_status": "Diseased",
        "diagnosis": "Mummy Berry / Anthracnose",
        "symptoms": ["Shriveled, pale berries", "Soft, sunken rot spots"],
        "medicine": ["Apply Captan or organic copper fungicide"],
        "management": ["Rake and destroy mummified berries from ground"]
    },
    "Cherry_Healthy": {
        "plant_type": "Cherry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Firm, shiny skin with bright color"],
        "medicine": ["No treatment needed"],
        "management": ["Protect from birds as they ripen"]
    },
    "Cherry_Diseased": {
        "plant_type": "Cherry",
        "health_status": "Diseased",
        "diagnosis": "Brown Rot",
        "symptoms": ["Brown, soft spots rapidly spreading", "Gray powdery mold"],
        "medicine": ["Myclobutanil or sulfur spray"],
        "management": ["Prune for good air circulation, remove mummies"]
    },
    "Corn_Diseased": {
        "plant_type": "Corn",
        "health_status": "Diseased",
        "diagnosis": "Ear Rot / Smut",
        "symptoms": ["White/gray fungal growth on kernels", "Large fleshy galls"],
        "medicine": ["Fungicides are rarely effective for ear rot"],
        "management": ["Plant resistant hybrids, control ear-feeding insects"]
    },
    "Corn_Healthy": {
        "plant_type": "Corn",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - ear appears healthy",
        "symptoms": ["Plump kernels, tight green husks"],
        "medicine": ["No treatment needed"],
        "management": ["Ensure adequate nitrogen and water"]
    },
    "Grape_Diseased": {
        "plant_type": "Grape",
        "health_status": "Diseased",
        "diagnosis": "Black Rot / Botrytis Bunch Rot",
        "symptoms": ["Shriveled, hard black berries", "Gray mold on clusters"],
        "medicine": ["Myclobutanil or Captan spray"],
        "management": ["Ensure open canopy, remove mummified fruit"]
    },
    "Grape_Healthy": {
        "plant_type": "Grape",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - bunch appears healthy",
        "symptoms": ["Intact berries, uniform color"],
        "medicine": ["No treatment needed"],
        "management": ["Continue regular canopy management"]
    },
    "Orange_Diseased": {
        "plant_type": "Orange",
        "health_status": "Diseased",
        "diagnosis": "Citrus Canker / Black Spot",
        "symptoms": ["Raised corky lesions on skin", "Dark sunken spots"],
        "medicine": ["Copper-based bactericides/fungicides"],
        "management": ["Control leafminers, use windbreaks"]
    },
    "Orange_Healthy": {
        "plant_type": "Orange",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Smooth, bright rind without lesions"],
        "medicine": ["No treatment needed"],
        "management": ["Maintain balanced fertilization"]
    },
    "Peach_Diseased": {
        "plant_type": "Peach",
        "health_status": "Diseased",
        "diagnosis": "Brown Rot / Scab",
        "symptoms": ["Brown fuzzy mold", "Dark velvety spots on skin"],
        "medicine": ["Captan or sulfur fungicide"],
        "management": ["Clean up dropped fruit, prune for airflow"]
    },
    "Peach_Healthy": {
        "plant_type": "Peach",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Smooth fuzzy skin, firm flesh"],
        "medicine": ["No treatment needed"],
        "management": ["Thin fruit to prevent branch breakage"]
    },
    "Pepper_Diseased": {
        "plant_type": "Pepper",
        "health_status": "Diseased",
        "diagnosis": "Anthracnose / Sunscald",
        "symptoms": ["Sunken water-soaked lesions", "Papery white patches"],
        "medicine": ["Copper fungicide for anthracnose"],
        "management": ["Ensure good leaf cover to prevent sunscald"]
    },
    "Pepper_Healthy": {
        "plant_type": "Pepper",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Glossy, firm skin without spots"],
        "medicine": ["No treatment needed"],
        "management": ["Maintain consistent watering"]
    },
    "Potato_Diseased": {
        "plant_type": "Potato",
        "health_status": "Diseased",
        "diagnosis": "Common Scab / Late Blight Tuber Rot",
        "symptoms": ["Corky lesions on skin", "Reddish-brown dry rot inside"],
        "medicine": ["Use disease-free seed potatoes"],
        "management": ["Lower soil pH to 5.2 to prevent scab"]
    },
    "Potato_Healthy": {
        "plant_type": "Potato",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - tuber appears healthy",
        "symptoms": ["Smooth skin, no soft spots"],
        "medicine": ["No treatment needed"],
        "management": ["Store in dark, cool, humid environment"]
    },
    "Raspberry_Diseased": {
        "plant_type": "Raspberry",
        "health_status": "Diseased",
        "diagnosis": "Botrytis Fruit Rot (Gray Mold)",
        "symptoms": ["Fuzzy gray mold on berries", "Soft rotting fruit"],
        "medicine": ["Captan or organic biofungicides"],
        "management": ["Harvest frequently, ensure quick cooling"]
    },
    "Raspberry_Healthy": {
        "plant_type": "Raspberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Firm, deeply colored drupelets"],
        "medicine": ["No treatment needed"],
        "management": ["Keep canes thinned for airflow"]
    },
    "Soybean_Diseased": {
        "plant_type": "Soybean",
        "health_status": "Diseased",
        "diagnosis": "Pod and Stem Blight",
        "symptoms": ["Black specks arranged linearly on pods", "Shriveled seeds"],
        "medicine": ["Foliar fungicides applied at pod set"],
        "management": ["Harvest promptly when mature"]
    },
    "Soybean_Healthy": {
        "plant_type": "Soybean",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - pods appear healthy",
        "symptoms": ["Clean pods with well-developed seeds"],
        "medicine": ["No treatment needed"],
        "management": ["Monitor for late-season pests"]
    },
    "Squash_Diseased": {
        "plant_type": "Squash",
        "health_status": "Diseased",
        "diagnosis": "Choanephora Fruit Rot / Blossom End Rot",
        "symptoms": ["Fuzzy growth with black heads", "Black rotting end"],
        "medicine": ["Copper sprays are ineffective against Choanephora"],
        "management": ["Avoid overhead watering, add calcium for blossom end rot"]
    },
    "Squash_Healthy": {
        "plant_type": "Squash",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Firm rind, even coloring"],
        "medicine": ["No treatment needed"],
        "management": ["Harvest summer squash frequently"]
    },
    "Strawberry_Diseased": {
        "plant_type": "Strawberry",
        "health_status": "Diseased",
        "diagnosis": "Gray Mold / Leather Rot",
        "symptoms": ["Gray fuzzy mold", "Tough, leathery discolored areas"],
        "medicine": ["Captan or biological fungicides"],
        "management": ["Use straw mulch to keep fruit off soil"]
    },
    "Strawberry_Healthy": {
        "plant_type": "Strawberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": ["Bright red, firm berries"],
        "medicine": ["No treatment needed"],
        "management": ["Harvest early in the day"]
    },"""

if "Blueberry_Diseased" not in content:
    # Insert before the closing brace of DISEASE_KNOWLEDGE
    split_target = "}\n\n# Generic fallback for classes not explicitly in the knowledge base"
    parts = content.split(split_target)
    
    new_content = parts[0] + "\n" + NEW_KNOWLEDGE + "\n" + split_target + parts[1]
    
    # Also fix the fallback logic just in case
    old_fallback = """    # Parse the class name to extract plant and disease info
    parts = class_name.replace("___", "|").replace("_", " ").split("|")
    plant_type = parts[0].strip() if len(parts) > 0 else "Unknown"
    disease_name = parts[1].strip() if len(parts) > 1 else "Unknown Condition\""""
    
    new_fallback = """    # Parse the class name to extract plant and disease info
    if "_" in class_name and "___" not in class_name:
        parts = class_name.split("_")
        plant_type = parts[0]
        disease_name = parts[1] if len(parts) > 1 else "Unknown Condition"
    else:
        parts = class_name.replace("___", "|").replace("_", " ").split("|")
        plant_type = parts[0].strip() if len(parts) > 0 else "Unknown"
        disease_name = parts[1].strip() if len(parts) > 1 else "Unknown Condition\""""
    
    new_content = new_content.replace(old_fallback, new_fallback)
    
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("app.py updated successfully!")
else:
    print("Already updated.")
