import numpy as np
import pandas as pd
import json

def map_to_disorder_vector(sequence, disordered_regions):
    # Create a vector of zeros with the same length as the sequence
    vector = [0] * len(sequence)
    
    # Iterate over the disordered regions
    for start, end in disordered_regions:
        # Convert to 0-based indexing
        start = start - 1
        end = end - 1
        
        # Mark the disordered regions in the vector as 1
        for i in range(start, end + 1):
            vector[i] = 1
    
    return vector

# Example usage
protein_sequence = "MKTQRDGHSLGRWSLVLLLLGLVMPLAIIAQVLSYKEAVLRAIDGINQRSSDANLYRLLDLDPRPTMDGDPDTPKPVSFTVKETVCPRTTQQSPEDCDFKKDGLVKRCMGTVTLNQARGSFDISCDDNKRFALLGDFFRKSKEKIGKEFKRIVQRIKDFLRNLVPRTES"
disordered_regions = [(4, 8), (12, 14)]

disorder_vector = map_to_disorder_vector(protein_sequence, disordered_regions)

print(disorder_vector)
