# 1. Define constants
# DNA codons (cDNA sequence)
START_CODON = "ATG"
STOP_CODONS = {"TAA", "TAG", "TGA"}

# 2. Define functions
def read_fasta(file_path):
    """Read FASTA file, return {gene_name: sequence} dict"""
    fasta_data = {}
    current_name = ""
    seq_lines = []
    
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Header line
            if line.startswith(">"):
                if current_name:
                    fasta_data[current_name] = "".join(seq_lines)
                # Get gene name (first part of header)
                current_name = line.split()[0][1:]
                seq_lines = []
            # Sequence line
            else:
                seq_lines.append(line)
    # Save last gene
    if current_name:
        fasta_data[current_name] = "".join(seq_lines)
    return fasta_data

def find_in_frame_stops(sequence):
    """Find all in-frame stop codons in the sequence"""
    found_stops = set()
    seq_len = len(sequence)
    # Find all ATG start positions
    for i in range(seq_len - 2):
        if sequence[i:i+3] == START_CODON:
            # Read codons step 3 (in-frame)
            for j in range(i, seq_len - 2, 3):
                codon = sequence[j:j+3]
                if codon in STOP_CODONS:
                    found_stops.add(codon)
                    break  # Stop at first termination
    return found_stops

def write_filtered_fasta(output_path, gene_dict):
    """Write genes with stop codons to new FASTA file"""
    with open(output_path, "w") as f:
        for gene, seq in gene_dict.items():
            stops = find_in_frame_stops(seq)
            if stops:
                # Write header: >gene stop1,stop2
                f.write(f">{gene} {','.join(stops)}\n")
                # Write sequence (80 chars per line)
                for k in range(0, len(seq), 80):
                    f.write(seq[k:k+80] + "\n")

# 3. Core program execution
if __name__ == "__main__":
    # Set input and output file paths
    INPUT_FILE = r"Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa"
    OUTPUT_FILE = "stop_genes.fa"

    # Step 1: Read FASTA file
    print("Reading FASTA file...")
    genes = read_fasta(INPUT_FILE)

    # Step 2: Process genes and write results
    print("Processing genes and writing results...")
    write_filtered_fasta(OUTPUT_FILE, genes)

    print("Done! Output file: stop_genes.fa")