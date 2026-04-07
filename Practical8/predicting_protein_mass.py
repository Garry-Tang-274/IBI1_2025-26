# Amino acid mass table
AA_MASS = {
    'G': 57.02, 'A': 71.04, 'S': 87.03, 'P': 97.05, 'V': 99.07,
    'T': 101.05, 'C': 103.01, 'I': 113.08, 'L': 113.08, 'N': 114.04,
    'D': 115.03, 'Q': 128.06, 'K': 128.09, 'E': 129.04, 'M': 131.04,
    'H': 137.06, 'F': 147.07, 'R': 156.10, 'Y': 163.06, 'W': 186.08
}

def calculate_protein_mass(sequence):
    total = 0.0
    invalid_aa = []
    # Traverse all amino acids
    for aa in sequence:
        if aa not in AA_MASS:
            invalid_aa.append(aa)
        else:
            total += AA_MASS[aa]
    # Remove duplicate invalid amino acids
    unique_invalid = list(set(invalid_aa))
    # Check invalid amino acids
    if unique_invalid:
        raise ValueError(f"Invalid amino acids: {', '.join(unique_invalid)}")
    return total

# Run example and user input
if __name__ == "__main__":
    # Label and show example
    print("This is an example:")
    example_seq = "GAV"
    print(f"Sequence {example_seq} mass: {calculate_protein_mass(example_seq):.2f} amu\n")
    
    # User input
    user_seq = input("Enter amino acid sequence: ")
    try:
        print(f"Sequence {user_seq} mass: {calculate_protein_mass(user_seq):.2f} amu")
    except ValueError as e:
        print(f"Error: {e}")