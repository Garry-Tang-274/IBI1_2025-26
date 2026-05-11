# largest_orf.py

# The target RNA sequence defined in the manual
seq = 'AAGAUACAUGCAAGUGGUGUGUCUGUUCUGAGAGGGCCUAAAAG' # [cite: 259]

# Define translation boundaries
start_codon = "AUG" # [cite: 255]
stop_codons = {"UAA", "UAG", "UGA"} # [cite: 255]
all_orfs = []

# Iterate through the sequence to find all potential start positions
for start_pos in range(len(seq) - 2):
    # Check if the current 3-nt window matches the start codon
    if seq[start_pos:start_pos+3] == start_codon:
        current_orf = ""
        # Read the sequence in steps of 3 to maintain the reading frame
        for codon_pos in range(start_pos, len(seq) - 2, 3):
            codon = seq[codon_pos:codon_pos+3]
            current_orf += codon
            # If a stop codon is encountered, the ORF is complete
            if codon in stop_codons:
                all_orfs.append(current_orf)
                break

# Identify and display the longest ORF and its length
if all_orfs:
    longest_orf = max(all_orfs, key=len)
    print(f"The longest ORF is: {longest_orf}")
    print(f"Length of the longest ORF: {len(longest_orf)} nucleotides") # [cite: 329]
else:
    print("No valid ORF found in the sequence.")