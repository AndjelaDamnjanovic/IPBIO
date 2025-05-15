import subprocess

subprocess.run(["./StatRepeats", "trainSetTrimmed.fasta", "3", "-dn", "-out", "trainSetTrimmedDN.out"])
subprocess.run(["./StatRepeats", "trainSetTrimmed.fasta", "3", "-dc", "-out", "trainSetTrimmedDC.out"])
subprocess.run(["./StatRepeats", "trainSetTrimmed.fasta", "3", "-in", "-out", "trainSetTrimmedIN.out"])
subprocess.run(["./StatRepeats", "trainSetTrimmed.fasta", "3", "-ic", "-out", "trainSetTrimmedIC.out"])
