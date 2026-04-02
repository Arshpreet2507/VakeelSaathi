from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError

# -----------------------------
# MongoDB connection
# -----------------------------
MONGO_URI = "mongodb+srv://kaurashi2507_db_user:03e9r37ivCgt8AYg@vakeelsaathi-cluster.priaxef.mongodb.net/"
DB_NAME = "vakeelSathi"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# -----------------------------
# Ensure collections exist
# -----------------------------
required_collections = ["laws", "rights", "checklists"]

existing = db.list_collection_names()

for col in required_collections:
    if col not in existing:
        db.create_collection(col)
        print(f"Created collection: {col}")
    else:
        print(f"Collection already exists: {col}")

laws_collection = db["laws"]
rights_collection = db["rights"]
checklists_collection = db["checklists"]

# -----------------------------
# Sample data
# -----------------------------
laws_data = [
    {
        "offence_key": "theft",
        "offence_name": "Theft",
        "section": "IPC 379",
        "plain_explanation": "Taking someone else's movable property dishonestly without consent.",
        "bailable": True,
        "cognizable": True,
        "compoundable": False,
        "arrest_possible": True,
        "max_punishment": "Up to 3 years, or fine, or both",
        "rights": [
            "The accused must be produced before a magistrate within 24 hours.",
            "The accused has the right to contact a lawyer.",
            "Family or a friend should be informed of the arrest."
        ],
        "police_can_do": [
            "Register FIR",
            "Question the accused",
            "Arrest in appropriate circumstances"
        ],
        "police_cannot_do": [
            "Keep the accused in custody for more than 24 hours without producing them before a magistrate",
            "Force a confession",
            "Deny access to legal counsel"
        ],
        "next_2_hours": [
            "Contact a criminal lawyer immediately",
            "Ask for FIR number or copy if available",
            "Note exact time and place of arrest",
            "Keep ID proof ready"
        ],
        "documents_needed": [
            "ID proof of accused",
            "Address proof",
            "FIR details if available",
            "Any notice received from police"
        ],
        "what_happens_next": [
            "Police questioning may take place",
            "The accused must be presented before a magistrate within 24 hours",
            "Bail may be considered depending on facts of the case"
        ]
    },
    {
        "offence_key": "assault",
        "offence_name": "Assault",
        "section": "IPC 351",
        "plain_explanation": "Threat or use of criminal force against another person.",
        "bailable": True,
        "cognizable": False,
        "compoundable": True,
        "arrest_possible": True,
        "max_punishment": "Depends on related section and gravity",
        "rights": [
            "The accused has the right to contact a lawyer.",
            "The accused has the right to know the grounds of arrest.",
            "The accused must be produced before a magistrate within 24 hours if arrested."
        ],
        "police_can_do": [
            "Question the persons involved",
            "Register complaint or FIR where applicable"
        ],
        "police_cannot_do": [
            "Use unlawful force",
            "Detain illegally",
            "Force a confession"
        ],
        "next_2_hours": [
            "Understand the exact section applied",
            "Call a lawyer",
            "Collect complaint details"
        ],
        "documents_needed": [
            "ID proof",
            "Complaint/FIR details",
            "Medical papers if injury is involved"
        ],
        "what_happens_next": [
            "Police inquiry",
            "Possible notice or arrest depending on section and facts"
        ]
    },
    {
        "offence_key": "cyber_fraud",
        "offence_name": "Cyber Fraud",
        "section": "IT Act / related IPC sections",
        "plain_explanation": "Online cheating, scam, phishing, or fraudulent digital transactions.",
        "bailable": "Depends on exact section",
        "cognizable": True,
        "compoundable": False,
        "arrest_possible": True,
        "max_punishment": "Depends on section invoked",
        "rights": [
            "The accused has the right to contact a lawyer.",
            "The accused has the right to know the allegations.",
            "If arrested, the accused must be produced before a magistrate within 24 hours."
        ],
        "police_can_do": [
            "Seize relevant digital devices as per procedure",
            "Question the accused",
            "Investigate digital evidence"
        ],
        "police_cannot_do": [
            "Detain without legal basis",
            "Force passwords or confession unlawfully",
            "Keep the accused beyond legal custody limits"
        ],
        "next_2_hours": [
            "Ask which exact section is applied",
            "Contact a lawyer with cybercrime experience",
            "Do not hand over devices without proper record/memo",
            "Note names of officers and police station"
        ],
        "documents_needed": [
            "ID proof",
            "Notice/FIR copy if available",
            "Seizure memo if devices are taken"
        ],
        "what_happens_next": [
            "Police may examine devices and accounts",
            "Statements may be recorded",
            "Further action depends on digital evidence"
        ]
    },
    {
        "offence_key": "cheating_fraud",
        "offence_name": "Cheating / Fraud",
        "section": "IPC 420",
        "plain_explanation": "Dishonestly inducing a person to deliver property or money by deception.",
        "bailable": False,
        "cognizable": True,
        "compoundable": False,
        "arrest_possible": True,
        "max_punishment": "Up to 7 years and fine",
        "rights": [
            "Right to contact a lawyer",
            "Right to know grounds of arrest",
            "Production before magistrate within 24 hours if arrested"
        ],
        "police_can_do": [
            "Register FIR",
            "Investigate documents and money trail",
            "Question accused and witnesses"
        ],
        "police_cannot_do": [
            "Force confession",
            "Detain beyond legal limit without magistrate",
            "Ignore arrest memo requirements"
        ],
        "next_2_hours": [
            "Contact a lawyer immediately",
            "Understand exact allegations and amount involved",
            "Keep all transaction records ready"
        ],
        "documents_needed": [
            "ID proof",
            "Transaction records",
            "Complaint/FIR details",
            "Business agreements if any"
        ],
        "what_happens_next": [
            "Financial and document investigation",
            "Possible recovery-related investigation",
            "Bail strategy may become important quickly"
        ]
    },
    {
        "offence_key": "drug_possession",
        "offence_name": "Drug Possession",
        "section": "NDPS Act (varies by substance and quantity)",
        "plain_explanation": "Possession of prohibited narcotic or psychotropic substances.",
        "bailable": "Depends heavily on quantity and section",
        "cognizable": True,
        "compoundable": False,
        "arrest_possible": True,
        "max_punishment": "Varies significantly by substance and quantity",
        "rights": [
            "Right to contact a lawyer",
            "Right to know the grounds of arrest",
            "Production before magistrate within 24 hours"
        ],
        "police_can_do": [
            "Search and seizure as per legal procedure",
            "Question the accused",
            "Send seized substance for analysis"
        ],
        "police_cannot_do": [
            "Ignore mandatory procedure during search and seizure",
            "Force confession",
            "Detain beyond legal custody limits"
        ],
        "next_2_hours": [
            "Contact a lawyer immediately",
            "Ask what quantity and substance is alleged",
            "Check whether seizure memo was prepared properly"
        ],
        "documents_needed": [
            "ID proof",
            "Arrest memo",
            "Seizure memo",
            "Notice/FIR details"
        ],
        "what_happens_next": [
            "Seized material may be sent for forensic testing",
            "Magistrate production is required",
            "Bail depends greatly on the section and quantity involved"
        ]
    }
]

rights_data = [
    {
        "right_key": "produce_before_magistrate_24h",
        "title": "Production before magistrate",
        "plain_text": "Police cannot keep an arrested person in custody for more than 24 hours without producing them before a magistrate.",
        "applies_when": ["arrested"]
    },
    {
        "right_key": "lawyer_access",
        "title": "Right to lawyer",
        "plain_text": "An arrested person has the right to consult a lawyer.",
        "applies_when": ["arrested", "questioning"]
    },
    {
        "right_key": "inform_family",
        "title": "Right to inform family or friend",
        "plain_text": "A family member, friend, or known person should be informed about the arrest.",
        "applies_when": ["arrested"]
    },
    {
        "right_key": "grounds_of_arrest",
        "title": "Right to know grounds of arrest",
        "plain_text": "The accused has the right to know why they are being arrested or questioned.",
        "applies_when": ["arrested", "questioning"]
    },
    {
        "right_key": "silence_protection",
        "title": "Protection against forced confession",
        "plain_text": "Police cannot lawfully force a confession.",
        "applies_when": ["arrested", "questioning"]
    },
    {
        "right_key": "women_arrest_safeguard",
        "title": "Women arrest safeguard",
        "plain_text": "Women generally have added procedural safeguards, especially regarding arrest timing and treatment.",
        "applies_when": ["arrested"]
    }
]

checklists_data = [
    {
        "situation_key": "arrested_at_night",
        "title": "Arrest happened at night",
        "immediate_steps": [
            "Note the exact time of arrest",
            "Ask where the person is being taken",
            "Call a lawyer immediately",
            "Keep ID and case details ready"
        ],
        "documents_needed": [
            "ID proof",
            "Any memo or paper given by police"
        ]
    },
    {
        "situation_key": "called_for_questioning",
        "title": "Called for questioning",
        "immediate_steps": [
            "Ask whether a written notice was issued",
            "Do not panic",
            "Take ID proof",
            "Consult a lawyer before giving detailed statement"
        ],
        "documents_needed": [
            "ID proof",
            "Any written notice from police"
        ]
    },
    {
        "situation_key": "police_took_from_home",
        "title": "Police took person from home",
        "immediate_steps": [
            "Ask officers where the person is being taken",
            "Note names if possible",
            "Ask whether FIR has been filed",
            "Contact a lawyer immediately"
        ],
        "documents_needed": [
            "ID proof",
            "Address proof",
            "Any arrest memo or notice"
        ]
    },
    {
        "situation_key": "fir_registered",
        "title": "FIR already registered",
        "immediate_steps": [
            "Get FIR number if available",
            "Understand which sections are applied",
            "Call a lawyer with FIR details",
            "Preserve relevant papers and evidence"
        ],
        "documents_needed": [
            "FIR copy or number",
            "ID proof",
            "Related transaction or incident records"
        ]
    }
]

# -----------------------------
# Upsert helper
# -----------------------------
def upsert_many(collection, docs, unique_key):
    operations = []
    for doc in docs:
        operations.append(
            UpdateOne(
                {unique_key: doc[unique_key]},
                {"$set": doc},
                upsert=True
            )
        )

    if operations:
        result = collection.bulk_write(operations)
        print(
            f"{collection.name}: "
            f"matched={result.matched_count}, "
            f"modified={result.modified_count}, "
            f"upserted={len(result.upserted_ids)}"
        )

# -----------------------------
# Seed data
# -----------------------------
try:
    upsert_many(laws_collection, laws_data, "offence_key")
    upsert_many(rights_collection, rights_data, "right_key")
    upsert_many(checklists_collection, checklists_data, "situation_key")

    # Optional indexes for faster lookups
    laws_collection.create_index("offence_key", unique=True)
    rights_collection.create_index("right_key", unique=True)
    checklists_collection.create_index("situation_key", unique=True)

    print("\nSeeding completed successfully.")
    print("Database:", DB_NAME)
    print("Collections:", db.list_collection_names())

except PyMongoError as e:
    print("MongoDB error:", e)

finally:
    client.close()