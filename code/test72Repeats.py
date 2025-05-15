from typing import List
from Bio import SeqIO
import numpy as np
import json
import sqlite3


def processResults(records, threshold, i, n, disorderPredictor, f, id):
    if not records:
        return
    numInstances = records[0] + records[1] + records[2]
    if numInstances == 0:
        return
    disorderPercentage = float(records[0]/numInstances)
    intersectPercentage = float(records[1]/numInstances)
    orderPercentage = float(records[2]/numInstances)

    # IMA DOSTA NISKI SA DISORDER % PREKO 80% 
    mostFrequent = max(disorderPercentage, orderPercentage)
    if disorderPercentage == mostFrequent and disorderPercentage >= threshold:
        #f.write(id + ": " + str(i) + " - " + str(n) + "\n")
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
        conn = sqlite3.connect('../repeats/repeats31.db')
        cursor = conn.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        f = open(outfile, "w")
        for fasta in fasta_sequences:
            name, sequence = fasta.id, str(fasta.seq)
            disorderPredictor = [[0, 0, 0] for i in range(len(sequence))]
            seq_len = len(sequence)
            if name != "DP00072":
                continue
            print(name)
            for n in range(3, seq_len + 1):
                for i in range(seq_len - n + 1):     
                    cursor.execute('SELECT d, i, o FROM repeatMap3 WHERE SEQUENCE = ?', (sequence[i:i + n],))
                    records = cursor.fetchone()    
                    processResults(records, threshold, i, n + i, disorderPredictor, f, name)
            
            #print(disorderPredictor)
            res = disorderToString(disorderPredictor) 
            disorderPredictor.clear() 
            f.write(name + " " + res + "\n")
        f.close()          
            
        cursor.close()  # Close the cursor explicitly
        print("Data has been successfully stored in the SQLite database.")
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if conn:
            conn.close()
        print("The SQLite connection is closed") 

#extractSequences("../testSets/testSet2.fasta")
extractSequences("../testSets/testSet3.fasta", 0.30, "../results/resultRepeats723.txt")