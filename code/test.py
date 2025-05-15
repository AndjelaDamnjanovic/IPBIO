from typing import List
from Bio import SeqIO
import numpy as np
import json
import sqlite3

def update_rolling_hash(current_hash: int, old_char: str, new_char: str, window_size: int, base: int = 31, mod: int = 10**9 + 9) -> int:

    current_hash = (current_hash - ord(old_char) * pow(base, window_size - 1, mod)) % mod
    current_hash = (current_hash * base + ord(new_char)) % mod
    
    return current_hash if current_hash >= 0 else current_hash + mod

def calculate_initial_hash(s: str, window_size: int, base: int = 31, mod: int = 10**9 + 9) -> int:
    current_hash = 0
    for i in range(window_size):
        current_hash = (current_hash * base + ord(s[i])) % mod
    return current_hash

def processResults(records, threshold, i, n, disorderPredictor, f, id):
    if not records:
        return
    numInstances = records[0] + records[1] + records[2]
    disorderPercentage = float(records[0]/numInstances)
    intersectPercentage = float(records[1]/numInstances)
    orderPercentage = float(records[2]/numInstances)

    # IMA DOSTA NISKI SA DISORDER % PREKO 80% 
    mostFrequent = max(disorderPercentage, intersectPercentage, orderPercentage)
    if disorderPercentage == mostFrequent and disorderPercentage >= threshold:
        f.write(id + ": " + str(i) + " - " + str(n) + "\n")
        for j in range(i, n):
            disorderPredictor[j][0] += 1
    elif orderPercentage == mostFrequent and orderPercentage >= threshold:
        for j in range(i, n):
            disorderPredictor[j][2] += 1
    elif intersectPercentage == mostFrequent and intersectPercentage >= threshold:
        for j in range(i, n):
            disorderPredictor[j][1] += 1 

def disorderToString(disorderPredictor):
    res = ""
    # BICE PROBLEMA AKO IMA VISE MAKSIMUMA, NISKA CE BITI DUZA NEGO STO TREBA
    # NADJI NEKO RESENJE DA SE ODLUCUJE, NPR AKO JE BILO DISORDERA DO NJE, VRV
    # JE I TU DISORDER...
    for l in disorderPredictor:
        maxElem = max(l[0], l[1], l[2])
        if l[0] == maxElem:
            res = res + "d"
        elif l[1] == maxElem:
            res = res + "i"
        else:
            res = res + "o"
    return res

def extractSequences(testSet, threshold, outfile):
    try:
        fasta_sequences = SeqIO.parse(open(testSet), 'fasta')
        conn = sqlite3.connect('../sequences/sequences2.db')
        cursor = conn.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        f = open(outfile, "w")
        for fasta in fasta_sequences:
            name, sequence = fasta.id, str(fasta.seq)
            if name == "DP00072":
                continue
            disorderPredictor = [[0, 0, 0] for i in range(len(sequence))]
            seq_len = len(sequence)
            print(name)
            for n in range(3, seq_len + 1):
                # Compute the initial hash for the first window of size n
                if seq_len >= n:
                    current_hash = calculate_initial_hash(sequence[:n], n)
                    cursor.execute('SELECT d, i, o FROM sequenceMap WHERE SEQUENCE = ?', (current_hash,))
                    records = cursor.fetchone()

                    processResults(records, threshold, 0, n, disorderPredictor, f, name)
                    
                    # Sliding window with rolling hash
                    for i in range(1, seq_len - n + 1):
                        current_hash = update_rolling_hash(current_hash, sequence[i - 1], sequence[i + n - 1], n)
                        cursor.execute('SELECT d, i, o FROM sequenceMap WHERE SEQUENCE = ?', (current_hash,))
                        records = cursor.fetchone()
                        
                        processResults(records, threshold, i, n + i, disorderPredictor, f, name)
            #print(disorderPredictor)
            #res = disorderToString(disorderPredictor) 
            disorderPredictor.clear() 
            #f.write(name + " " + res + "\n")
        f.close()          
            
        cursor.close()  # Close the cursor explicitly
        print("Data has been successfully stored in the SQLite database.")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed") 

#extractSequences("../testSets/testSet1.fasta")
extractSequences("../testSets/testSet2.fasta", 0.80, "../results/proba2.txt")