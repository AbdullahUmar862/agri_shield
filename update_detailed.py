import os
import re

app_path = r"C:\Users\User\OneDrive\semester four computer science\Ai theory\aiagri\app.py"

with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Define the highly detailed definitions
DETAILED_FRUITS = """    "Apple_Healthy": {
        "plant_type": "Apple Fruit",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Clean skin without spots, lesions, or rotting",
            "Firm texture and appropriate coloration",
            "No signs of pest entry holes or fungal growth"
        ],
        "medicine": [
            "No chemical treatment needed for healthy fruit",
            "Maintain preventive organic fungicide schedule (e.g., neem oil) if pressure is high"
        ],
        "management": [
            "Continue regular harvesting at optimal ripeness",
            "Store in a cool, dark place (32-35°F) with high humidity (90%)",
            "Prune canopy aggressively during dormant season to ensure good airflow",
            "Rake and destroy any fallen leaves to prevent future scab"
        ]
    },
    "Apple_Diseased": {
        "plant_type": "Apple Fruit",
        "health_status": "Diseased",
        "diagnosis": "Apple Scab / Black Rot",
        "symptoms": [
            "Olive-green to black velvety spots on fruit surface",
            "Dark, sunken rotting areas spreading across the skin",
            "Fruit may become cracked, deformed, or drop prematurely",
            "Corky, brown, or hardened tissue underneath the skin"
        ],
        "medicine": [
            "Captan 50WP (2.5g/L) - Apply during early petal fall",
            "Myclobutanil (0.5ml/L) - Effective against cedar apple rust and scab",
            "Copper hydroxide spray for organic management (apply before bud break)",
            "Thiophanate-methyl (1g/L) for severe black rot cases"
        ],
        "management": [
            "Immediately remove and destroy all infected fruits (do NOT compost)",
            "Aggressively prune the tree canopy to allow sunlight and wind penetration",
            "Ensure strict orchard sanitation by burning all mummified fruits and fallen leaves",
            "Avoid overhead irrigation which promotes fungal spore spread"
        ]
    },
    "Tomato_Diseased": {
        "plant_type": "Tomato Fruit",
        "health_status": "Diseased",
        "diagnosis": "Blossom End Rot / Fruit Cracking / Anthracnose",
        "symptoms": [
            "Large, black, leathery sunken rotting at the bottom of the fruit",
            "Deep concentric cracks or radial splitting around the stem",
            "Small, circular, depressed spots on ripe fruit that expand rapidly"
        ],
        "medicine": [
            "Foliar calcium spray (Calcium chloride) for immediate blossom end rot relief",
            "Copper fungicides (2g/L) for anthracnose and bacterial spot",
            "Chlorothalonil (Bravo) applied every 7-14 days as a preventative",
            "Azoxystrobin for severe fungal infections"
        ],
        "management": [
            "Maintain deeply consistent watering to prevent calcium deficiency (Blossom End Rot)",
            "Apply a thick 3-4 inch layer of organic straw mulch to retain soil moisture",
            "Add agricultural lime or crushed eggshells to soil prior to planting",
            "Pick tomatoes slightly early and ripen indoors if heavy rain is expected (prevents cracking)"
        ]
    },
    "Blueberry_Healthy": {
        "plant_type": "Blueberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Plump, firm berries with a powdery natural white bloom",
            "Deep blue/purple uniform coloration",
            "No shriveling, softness, or fungal fuzz"
        ],
        "medicine": [
            "No treatment needed - plant is healthy",
            "Optional: Preventative compost tea foliar spray"
        ],
        "management": [
            "Maintain strict soil pH between 4.5 and 5.5",
            "Use pine needle or peat moss mulch",
            "Net bushes before fruits turn blue to prevent bird damage"
        ]
    },
    "Blueberry_Diseased": {
        "plant_type": "Blueberry",
        "health_status": "Diseased",
        "diagnosis": "Mummy Berry / Anthracnose",
        "symptoms": [
            "Berries turn pale, shrivel, and harden into 'mummies'",
            "Soft, sunken rotting spots leaking orange/pink spore masses",
            "Premature fruit drop and rapid post-harvest decay"
        ],
        "medicine": [
            "Propiconazole or Indar applied at green tip stage",
            "Captan (2.5g/L) applied during bloom to prevent Anthracnose",
            "Organic biofungicides (Bacillus subtilis) applied weekly"
        ],
        "management": [
            "Crucial: Rake, bury, or burn all dropped mummified berries before spring",
            "Apply 2 inches of fresh mulch in early spring to bury overwintering spores",
            "Cool harvested berries immediately to 32°F to stop rot progression"
        ]
    },
    "Cherry_Healthy": {
        "plant_type": "Cherry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Firm, glossy skin with deep, bright coloration",
            "No splitting, cracking, or soft spots",
            "Stems are green and firmly attached"
        ],
        "medicine": [
            "No treatment needed",
            "Dormant oil spray in late winter to prevent early pests"
        ],
        "management": [
            "Harvest with stems attached to prolong shelf life",
            "Protect from rain near harvest time to prevent cracking"
        ]
    },
    "Cherry_Diseased": {
        "plant_type": "Cherry",
        "health_status": "Diseased",
        "diagnosis": "Brown Rot / Cherry Leaf Spot (Fruit impact)",
        "symptoms": [
            "Small brown spots that rapidly expand to rot the entire fruit",
            "Fuzzy, gray or tan powdery mold appearing on the surface",
            "Fruits shrivel into hard mummies clinging to the branch"
        ],
        "medicine": [
            "Myclobutanil (Immunox) applied at popcorn, full bloom, and petal fall stages",
            "Captan or Sulfur sprays for organic management starting 3 weeks before harvest",
            "Fenbuconazole (Indar) for severe commercial outbreaks"
        ],
        "management": [
            "Sanitation is critical: remove all mummies from the tree and ground during winter",
            "Prune trees into an open-center shape for maximum sunlight",
            "Do not compost infected fruit"
        ]
    },
    "Corn_Healthy": {
        "plant_type": "Corn",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - ear appears healthy",
        "symptoms": [
            "Plump, fully developed kernels filled to the tip",
            "Tight, bright green husks",
            "Silks are brown and dry at maturity"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Ensure adequate nitrogen side-dressing at knee-high stage",
            "Provide 1.5 - 2 inches of water per week, especially during tasseling"
        ]
    },
    "Corn_Diseased": {
        "plant_type": "Corn",
        "health_status": "Diseased",
        "diagnosis": "Ear Rot (Fusarium/Diplodia) / Corn Smut",
        "symptoms": [
            "White, pink, or gray fungal growth between kernels",
            "Massive, swollen, fleshy gray/black galls replacing kernels (Smut)",
            "Kernels fused to the husk, rotting from the tip down"
        ],
        "medicine": [
            "Fungicides are rarely effective once ear rot or smut occurs",
            "Prothioconazole (Proline) can be used preventatively at silking stage"
        ],
        "management": [
            "Control ear-feeding insects (corn earworms) as they create entry wounds for fungi",
            "Plant resistant/tolerant corn hybrids next season",
            "Harvest early and dry grain to below 15% moisture immediately",
            "Rotate crop out of corn for 1-2 years"
        ]
    },
    "Grape_Healthy": {
        "plant_type": "Grape",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - bunch appears healthy",
        "symptoms": [
            "Intact, plump berries with uniform color",
            "No shriveling, cracking, or spots",
            "Stems are green and flexible"
        ],
        "medicine": [
            "No treatment needed",
            "Maintain preventative sulfur dusting for powdery mildew"
        ],
        "management": [
            "Continue regular canopy thinning",
            "Ensure proper trellis support"
        ]
    },
    "Grape_Diseased": {
        "plant_type": "Grape",
        "health_status": "Diseased",
        "diagnosis": "Black Rot / Botrytis Bunch Rot",
        "symptoms": [
            "Berries shrivel into hard, black, raisin-like mummies (Black Rot)",
            "Fuzzy gray mold enveloping the clusters (Botrytis)",
            "Brown circular lesions spreading rapidly across the fruit"
        ],
        "medicine": [
            "Myclobutanil (Rally) or Mancozeb (2.5g/L) for Black Rot (apply pre-bloom to 4 weeks post-bloom)",
            "Fenhexamid (Elevate) or Captan targeting Botrytis at veraison",
            "Copper/Sulfur combinations for organic vineyards"
        ],
        "management": [
            "Remove all mummified fruit during winter pruning (primary infection source)",
            "Aggressively pull leaves around the fruit zone to maximize airflow and sun exposure",
            "Harvest promptly before wet weather sets in"
        ]
    },
    "Orange_Healthy": {
        "plant_type": "Orange",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Smooth, bright orange rind without lesions or scabs",
            "Firm to the touch, heavy for its size",
            "No fungal growth on the stem end"
        ],
        "medicine": [
            "No treatment needed",
            "Preventative horticultural oil for scale and aphids"
        ],
        "management": [
            "Maintain balanced NPK fertilization with added micronutrients (Zinc, Iron)",
            "Prune water sprouts and dead wood"
        ]
    },
    "Orange_Diseased": {
        "plant_type": "Orange",
        "health_status": "Diseased",
        "diagnosis": "Citrus Canker / Black Spot / Alternaria Brown Spot",
        "symptoms": [
            "Raised, corky, crater-like lesions with yellow halos on the skin",
            "Dark, sunken, hard spots (Black Spot)",
            "Premature yellowing and fruit drop"
        ],
        "medicine": [
            "Copper-based bactericides (Liquid Copper Fungicide) - spray every 21 days during susceptible periods",
            "Strobilurin fungicides (e.g., Abound) for Black Spot control",
            "Do NOT use sulfur within 30 days of oil sprays"
        ],
        "management": [
            "Control citrus leafminers, as their tunnels expose the fruit to canker bacteria",
            "Plant windbreaks around the grove to prevent wind-driven rain spread",
            "Sanitize all pruning tools and equipment between trees"
        ]
    },
    "Peach_Healthy": {
        "plant_type": "Peach",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Smooth fuzzy skin with uniform blushing",
            "Firm flesh with no soft spots",
            "No gummy sap leaking from the fruit"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Thin fruits to 6-8 inches apart to prevent branches breaking and increase fruit size"
        ]
    },
    "Peach_Diseased": {
        "plant_type": "Peach",
        "health_status": "Diseased",
        "diagnosis": "Brown Rot / Peach Scab",
        "symptoms": [
            "Rapidly spreading brown rot covered in dusty gray/tan spores",
            "Small, dark, velvety spots clustering near the stem end (Scab)",
            "Fruit cracking and exuding clear, gummy sap"
        ],
        "medicine": [
            "Captan or Sulfur fungicide applied starting 3 weeks before harvest",
            "Propiconazole (Orbit) applied at pink bud and petal fall stages",
            "Chlorothalonil (Daconil) used early in the season (do not use after shuck split)"
        ],
        "management": [
            "Strict sanitation: clean up all dropped or mummified fruit instantly",
            "Prune heavily to an open-center vase shape for maximum airflow",
            "Avoid excessive nitrogen fertilizer which causes overly dense, humid canopies"
        ]
    },
    "Pepper_Healthy": {
        "plant_type": "Pepper",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Glossy, firm, thick skin without spots or wrinkling",
            "Strong attachment to the stem",
            "Proper coloration for its maturity stage"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Maintain consistent, deep watering",
            "Apply mulch to regulate soil temperature"
        ]
    },
    "Pepper_Diseased": {
        "plant_type": "Pepper",
        "health_status": "Diseased",
        "diagnosis": "Anthracnose / Blossom End Rot / Sunscald",
        "symptoms": [
            "Circular, sunken, water-soaked lesions that develop dark fungal spores in the center",
            "Papery, white, blistered patches on the sun-exposed side (Sunscald)",
            "Black rotting tissue at the bottom of the fruit (Blossom End Rot)"
        ],
        "medicine": [
            "Copper hydroxide (2g/L) sprayed every 7-10 days for Anthracnose and bacterial spots",
            "Foliar calcium spray for rapid Blossom End Rot correction",
            "Chlorothalonil for severe fungal pressure"
        ],
        "management": [
            "Ensure plants have a dense leaf canopy to shade the fruit and prevent Sunscald",
            "Maintain perfectly even soil moisture (fluctuating moisture causes Blossom End Rot)",
            "Use drip irrigation; never overhead water peppers"
        ]
    },
    "Potato_Healthy": {
        "plant_type": "Potato",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - tuber appears healthy",
        "symptoms": [
            "Smooth, firm skin with no soft or dark spots",
            "No greening (solanine) on the skin",
            "No corky lesions or deep pits"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Store in a completely dark, cool (45-50°F), and humid environment",
            "Cure for 1-2 weeks at 60°F before long-term storage"
        ]
    },
    "Potato_Diseased": {
        "plant_type": "Potato",
        "health_status": "Diseased",
        "diagnosis": "Common Scab / Late Blight Tuber Rot / Soft Rot",
        "symptoms": [
            "Rough, corky, raised or pitted lesions on the skin (Scab)",
            "Reddish-brown, granular dry rot spreading inward from the skin (Late Blight)",
            "Mushy, foul-smelling bacterial decay (Soft Rot)"
        ],
        "medicine": [
            "Fungicides applied to the foliage (Mancozeb, Chlorothalonil) prevent Late Blight spores from reaching tubers",
            "No chemical cure exists for Common Scab or Soft Rot once infected"
        ],
        "management": [
            "Lower soil pH to 5.0 - 5.2 using elemental sulfur (Scab cannot survive acidic soil)",
            "Never harvest wet fields; ensure tubers are perfectly dry before storage",
            "Hill the plants deeply to put a thick barrier of soil between spores and the tubers",
            "Use certified disease-free seed potatoes"
        ]
    },
    "Raspberry_Healthy": {
        "plant_type": "Raspberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Firm, deeply colored drupelets",
            "Hollow core is clean and intact",
            "No fuzzy mold or soft, leaking spots"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Harvest gently and place immediately into cold storage"
        ]
    },
    "Raspberry_Diseased": {
        "plant_type": "Raspberry",
        "health_status": "Diseased",
        "diagnosis": "Botrytis Fruit Rot (Gray Mold) / Sunburn",
        "symptoms": [
            "Dense, fuzzy gray mold covering individual drupelets",
            "Fruit becomes mushy, leaks juice, and rots rapidly",
            "White or bleached drupelets on the sun-exposed side (Sunburn/White Drupelet Disorder)"
        ],
        "medicine": [
            "Captan (2.5g/L) or Fenhexamid (Elevate) sprayed during early and full bloom",
            "Biological fungicides (Bacillus subtilis/Serenade) applied organically"
        ],
        "management": [
            "Thin raspberry canes aggressively (leave 4-5 per foot) to ensure fast drying after rain",
            "Harvest daily in the morning after dew has dried",
            "Cool berries to 32-34°F within 1 hour of picking to arrest mold growth"
        ]
    },
    "Soybean_Healthy": {
        "plant_type": "Soybean",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - pods appear healthy",
        "symptoms": [
            "Clean, smooth pods with well-developed seeds inside",
            "Normal yellowing/browning as they reach harvest maturity",
            "No black specks or mold on the pods"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Harvest promptly when moisture reaches 13-15%"
        ]
    },
    "Soybean_Diseased": {
        "plant_type": "Soybean",
        "health_status": "Diseased",
        "diagnosis": "Pod and Stem Blight / Phomopsis Seed Decay",
        "symptoms": [
            "Black fungal specks (pycnidia) arranged in linear rows on the pods",
            "Seeds inside become shriveled, moldy, and cracked",
            "White fungal growth covering the seeds"
        ],
        "medicine": [
            "Foliar fungicides (Strobilurins like Pyraclostrobin or Azoxystrobin) applied at the R3 to R5 (pod set) stage",
            "Thiophanate-methyl used for severe Phomopsis outbreaks"
        ],
        "management": [
            "Do not delay harvest; prompt harvesting prevents late-season seed decay",
            "Rotate with a non-host crop like corn or wheat for at least one year",
            "Plow under soybean residue to accelerate decomposition of overwintering pathogens"
        ]
    },
    "Squash_Healthy": {
        "plant_type": "Squash",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Firm rind with even, vibrant coloring",
            "No soft spots, mold, or rotting ends",
            "Stem is intact and healthy"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Elevate growing fruits off bare soil using straw"
        ]
    },
    "Squash_Diseased": {
        "plant_type": "Squash",
        "health_status": "Diseased",
        "diagnosis": "Choanephora Fruit Rot / Blossom End Rot",
        "symptoms": [
            "Fuzzy, wet growth resembling pincushions with black heads on the blossom end",
            "Black, dry rotting tissue at the tip (Blossom End Rot)",
            "Soft, mushy decay spreading rapidly through the fruit"
        ],
        "medicine": [
            "Copper sprays and standard fungicides are generally ineffective against Choanephora rot",
            "Foliar calcium sprays applied early to prevent Blossom End Rot"
        ],
        "management": [
            "Crucial: Avoid any overhead irrigation; use drip tapes exclusively",
            "Increase plant spacing to allow rapid drying of flowers and fruit",
            "Ensure consistent watering to prevent the calcium deficiencies that cause Blossom End Rot"
        ]
    },
    "Strawberry_Healthy": {
        "plant_type": "Strawberry",
        "health_status": "Healthy",
        "diagnosis": "No disease detected - fruit appears healthy",
        "symptoms": [
            "Bright red, firm, and fully colored berries",
            "Green, healthy calyx (cap)",
            "No soft spots or mold"
        ],
        "medicine": [
            "No treatment needed"
        ],
        "management": [
            "Harvest early in the day while temperatures are cool"
        ]
    },
    "Strawberry_Diseased": {
        "plant_type": "Strawberry",
        "health_status": "Diseased",
        "diagnosis": "Botrytis (Gray Mold) / Leather Rot / Anthracnose",
        "symptoms": [
            "Fuzzy gray mold covering the berry, spreading via contact",
            "Tough, leathery, dull, discolored areas with a foul smell (Leather Rot)",
            "Sunken, dark brown/black circular lesions (Anthracnose)"
        ],
        "medicine": [
            "Captan (2.5g/L) or Fludioxonil (Switch) sprayed aggressively during the bloom period",
            "Phosphite fungicides (e.g., Aliette) specifically targeting Leather Rot",
            "Organic options include biologicals like Serenade or Actinovate"
        ],
        "management": [
            "Apply thick plastic or clean straw mulch to keep all fruit completely off the bare soil",
            "Space plants adequately and control weeds to allow wind to dry the canopy",
            "Harvest frequently and remove every single rotted berry from the field"
        ]
    }"""


# First, remove all old definitions of these fruits from app.py to avoid duplicates.
fruits_to_replace = [
    "Apple_Healthy", "Apple_Diseased", "Tomato_Diseased", 
    "Blueberry_Healthy", "Blueberry_Diseased", "Cherry_Healthy", "Cherry_Diseased",
    "Corn_Diseased", "Corn_Healthy", "Grape_Diseased", "Grape_Healthy",
    "Orange_Diseased", "Orange_Healthy", "Peach_Diseased", "Peach_Healthy",
    "Pepper_Diseased", "Pepper_Healthy", "Potato_Diseased", "Potato_Healthy",
    "Raspberry_Diseased", "Raspberry_Healthy", "Soybean_Diseased", "Soybean_Healthy",
    "Squash_Diseased", "Squash_Healthy", "Strawberry_Diseased", "Strawberry_Healthy"
]

# We will use regex to find and remove the blocks for these keys.
for fruit in fruits_to_replace:
    # Match `"Fruit_Name": { ... },`
    # We use a non-greedy match until the next top-level key or the end of DISEASE_KNOWLEDGE
    pattern = r'[ \t]*"' + fruit + r'":\s*\{.*?\}(?:,)?\n'
    content = re.sub(pattern, '', content, flags=re.DOTALL)


# Now insert DETAILED_FRUITS right after `DISEASE_KNOWLEDGE = {\n`
pattern_insert = r'(DISEASE_KNOWLEDGE\s*=\s*\{\n)'
content = re.sub(pattern_insert, r'\1' + DETAILED_FRUITS + ',\n', content, count=1)

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated app.py with fully detailed fruit knowledge base!")
