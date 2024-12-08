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
# 49 GRESAKA -- 28.82 GRESAKA
"""
from xgboost import XGBClassifier

clf = XGBClassifier(
    n_estimators=500,
    max_depth=15,
    scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]),
    random_state=42
)

"""
# 37.99 POSTO GRESAKA, 68 PROMASENIH KARAKTERA

"""
from lightgbm import LGBMClassifier

clf = LGBMClassifier(
    n_estimators=500,
    max_depth=15,
    class_weight='balanced',
    random_state=42
)
"""
#clf.fit(X_train, y_train)

from mlxtend.frequent_patterns import fpgrowth, association_rules

# Transform data to one-hot encoding for FP-Growth
import pandas as pd
X_train_bin = pd.DataFrame((X_train > 0).astype(int))  # Simplify for association rule mining
frequent_itemsets = fpgrowth(X_train_bin, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)
print(rules.head())
"""
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
"""
