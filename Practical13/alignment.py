import os

def get_file_path(filename):
    """
    Constructs an absolute path to a file in the same directory as this script.
    """
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, filename)

def read_fasta(file_name):
    """
    Reads a protein sequence from a FASTA file in the local directory.
    """
    path = get_file_path(file_name)
    sequence = ""
    if not os.path.exists(path):
        print(f"Error: {file_name} not found at {path}")
        return None
    
    with open(path, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                sequence += line.strip()
    return sequence

def read_blosum62(file_name):
    """
    Parses a BLOSUM62 matrix file from the local directory.
    """
    path = get_file_path(file_name)
    matrix = {}
    if not os.path.exists(path):
        print(f"Error: {file_name} not found at {path}")
        return None

    with open(path, 'r') as f:
        # Skip comment lines starting with # [cite: 145]
        lines = [line for line in f if not line.startswith('#') and line.strip()]
        header = lines[0].split()
        for line in lines[1:]:
            parts = line.split()
            row_aa = parts[0]
            scores = parts[1:]
            for col_aa, score in zip(header, scores):
                matrix[(row_aa, col_aa)] = int(score)
    return matrix

def perform_alignment(seq1, seq2, matrix, label):
    """
    Implements a non-gapped global alignment algorithm [cite: 136-138].
    """
    if seq1 is None or seq2 is None:
        return

    score = 0
    identical_count = 0
    length = min(len(seq1), len(seq2))

    # Compare each amino acid position [cite: 171]
    for i in range(length):
        aa1 = seq1[i].upper()
        aa2 = seq2[i].upper()
        
        if aa1 == aa2:
            identical_count += 1
            
        # Retrieve score from substitution matrix [cite: 153]
        score += matrix.get((aa1, aa2), -4)

    identity_pct = (identical_count / length) * 100

    print(f"--- Alignment: {label} ---")
    print(f"BLOSUM62 Total Score: {score}")
    print(f"Identity: {identity_pct:.2f}% ({identical_count}/{length})\n")

def main():
    # Step 1: Read input files from the same folder 
    matrix_data = read_blosum62("blosum62.txt")
    h_seq = read_fasta("human.fasta")
    m_seq = read_fasta("mouse.fasta")
    r_seq = read_fasta("random.fasta")

    if not matrix_data:
        return

    # Step 2 & 3: Comparison and Output [cite: 178]
    perform_alignment(h_seq, m_seq, matrix_data, "Human vs Mouse")
    perform_alignment(h_seq, r_seq, matrix_data, "Human vs Random")
    perform_alignment(m_seq, r_seq, matrix_data, "Mouse vs Random")

if __name__ == "__main__":
    main()