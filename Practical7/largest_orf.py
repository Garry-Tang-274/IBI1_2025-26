# Find the longest ORF with AUG start & UAA/UAG/UGA stop codons
seq = 'AAGAUACAUGCAAGUGGUGUGUCUGUUCUGAGAGGGCCUAAAAG'

# Define start and stop codons
start_codon = "AUG"
stop_codons = {"UAA", "UAG", "UGA"}
all_orfs = []  # Store all valid ORF sequences

# Traverse all possible start positions for AUG
for start_pos in range(len(seq) - 2):
    # Check if current position is start codon
    if seq[start_pos:start_pos+3] == start_codon:
        current_orf = ""
        # Extract codons 3 by 3 from start position
        for codon_pos in range(start_pos, len(seq) - 2, 3):
            codon = seq[codon_pos:codon_pos+3]
            current_orf += codon
            # Terminate when stop codon is found
            if codon in stop_codons:
                all_orfs.append(current_orf)
                break

# Get longest ORF and print result
if all_orfs:
    longest_orf = max(all_orfs, key=len)
    print(f"The longest ORF is: {longest_orf}")
    print(f"Length of the longest ORF: {len(longest_orf)} nucleotides")
else:
    print("No valid ORF found in the sequence.")