import numpy as np
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# TREBA MI OVDE KOD KOJI CE POSTOJECE SEKVENCE MAPIRATI U VEKTOR [0/1] TAKO DA
# SU KECEVI U NEUREDJENOM, A NULE U UREDJENOM REGIONU
def transform(sequence, start, end):
    for i in range(start, end):
        sequence[i] = 1

def get_labels():
    with open("../trainSets/trainSet1.json") as f:
        podaci = json.load(f)
        n = len(podaci)

        sequences = []
        labels = []
    
        for i in range(n):
            sequence = podaci[i]['sequence']
            #print(podaci[i]['disprot_id'])
            seq_len = len(sequence)

            labels.append([0]* seq_len)
            regions = podaci[i]['disprot_consensus']['Structural state']
            for region in regions:
                if region["type"] == "D":
                    start = region["start"]
                    #print(start)
                    end = region["end"]
                    #print(end)
                    transform(labels[i], start - 1, end)
            sequences.append(sequence)
    return sequences, labels

sequences, disorder_labels = get_labels()

def extract_features(sequence, window_size=3):
    amino_acids = list("ACDEFGHIKLMNPQRSTVWY")
    aa_to_index = {aa: i for i, aa in enumerate(amino_acids)}
    
    features = []
    for i in range(len(sequence)):
        # Create a window around the residue
        start = max(0, i - window_size)
        end = min(len(sequence), i + window_size + 1)
        window = sequence[start:end]
        
        # Count amino acid occurrences in the window
        composition = [window.count(aa) / len(window) for aa in amino_acids]
        features.append(composition)
    
    return np.array(features)

# Flatten the sequences and disorder labels for residue-level predictions
flat_features = []
flat_labels = []

for seq, labels in zip(sequences, disorder_labels):
    features = extract_features(seq)
    flat_features.extend(features)
    flat_labels.extend(labels)

flat_features = np.array(flat_features)
flat_labels = np.array(flat_labels)

X_train, X_test, y_train, y_test = train_test_split(flat_features, flat_labels, test_size=0.2, random_state=42)

# ISPROBAVAJ KLASIFIKATORE, PA IH UPOREDI SVE NA KRAJU. NARAVNO AKO NEKI DA KRSTEN REZ
# 41% PROMASIO
#clf = RandomForestClassifier(n_estimators=50, max_depth = 15, random_state=42, class_weight = 'balanced')

# ISTI KAO ONAJ ISPOD
"""
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth = 15,
    class_weight={0: 1, 1: 5}  # Assign a higher weight to Disordered (class 1)
)
"""
# 37% PROMASENIH
"""
clf = RandomForestClassifier(
    n_estimators=500,  # Increase the number of trees
    random_state=42,
    max_depth = 15,
    class_weight='balanced'
)
"""
# GRESI NA 2 POZICIJE VISE NEGO GORNJI 
"""
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    min_samples_split=10,  # Require at least 10 samples to split a node
    min_samples_leaf=5, 
    max_depth = 15    # Require at least 5 samples in each leaf
)
"""
# GRESKA MANJE NEGO GORE 
"""
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth = 15,
    class_weight='balanced',
    criterion='entropy'
)

"""
# GRESKA VIDE NEGO GORE
"""
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    max_depth = 15,
    bootstrap=False  # Use the entire dataset for each tree
)

"""

# GRESKA MANJE NEGO PRETHODNI
"""
clf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    max_depth=15
)

clf.fit(X_train, y_train)

# Predict with a custom threshold
probs = clf.predict_proba(X_test)[:, 1]
threshold = 0.3
y_pred = (probs > threshold).astype(int)
"""
# SVE 
# GRESKA MANJE OD PROSLE
clf = RandomForestClassifier(
    n_estimators=500,
    random_state=42,
    class_weight='balanced',
    max_depth=15,
    min_samples_split=10,
    min_samples_leaf=5,
    criterion='entropy'
)

clf.fit(X_train, y_train)

# Predict with a custom threshold
probs = clf.predict_proba(X_test)[:, 1]
threshold = 0.3
y_pred = (probs > threshold).astype(int)

# Predictions
y_pred = clf.predict(X_test)

# Evaluation Metrics
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred, target_names=["Ordered", "Disordered"]))

# ZAMENI OVO NEW SEQUENCE!!!!!!!
new_sequence = "MKTQRDGHSLGRWSLVLLLLGLVMPLAIIAQVLSYKEAVLRAIDGINQRSSDANLYRLLDLDPRPTMDGDPDTPKPVSFTVKETVCPRTTQQSPEDCDFKKDGLVKRCMGTVTLNQARGSFDISCDKDNKRFALLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES"
print(len(new_sequence))
new_features = extract_features(new_sequence)
new_predictions = clf.predict(new_features)

# Display the results
print("Sequence:", new_sequence)
print("Predicted Disorder:", new_predictions)

