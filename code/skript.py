import subprocess

#subprocess.run(["./StatRepeats", "preprocessed.fasta", "2", "-loa", "direct2.fasta", "-dn", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed1.fasta", "3", "-loa", "direct31.fasta", "-dn", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed2.fasta", "3", "-loa", "direct32.fasta", "-dn", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed3.fasta", "3", "-loa", "direct33.fasta", "-dn", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed4.fasta", "3", "-loa", "direct34.fasta", "-dn", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed5.fasta", "3", "-loa", "direct35.fasta", "-dn", "-protein"])

#subprocess.run(["./StatRepeats", "preprocessed.fasta", "2", "-loa", "direct2.fasta", "-in", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed1.fasta", "3", "-loa", "indirect31.fasta", "-in", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed2.fasta", "3", "-loa", "indirect32.fasta", "-in", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed3.fasta", "3", "-loa", "indirect33.fasta", "-in", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed4.fasta", "3", "-loa", "indirect34.fasta", "-in", "-protein"])
subprocess.run(["./StatRepeats", "preprocessed5.fasta", "3", "-loa", "indirect35.fasta", "-in", "-protein"])

