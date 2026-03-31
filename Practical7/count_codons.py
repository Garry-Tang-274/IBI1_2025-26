# count_codons.py
# 1. Define constants
import os
import matplotlib.pyplot as plt

# DNA codons (cDNA sequence)
START_CODON = "ATG"
VALID_STOP_CODONS = {"TAA", "TAG", "TGA"}
# Plot style configuration
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['figure.figsize'] = (12, 8)

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

def get_longest_orf_codons(seq, target_stop):
    """Find longest ORF with target stop, return upstream codons"""
    orf_codons_list = []
    seq_len = len(seq)
    # Find all ATG start positions
    for start_pos in range(seq_len - 2):
        if seq[start_pos:start_pos+3] == START_CODON:
            current_codons = []
            # Read codons step 3 (in-frame)
            for codon_pos in range(start_pos, seq_len - 2, 3):
                codon = seq[codon_pos:codon_pos+3]
                if codon == START_CODON:
                    current_codons.append(codon)
                    continue
                if codon == target_stop:
                    orf_length = (codon_pos - start_pos) + 3
                    upstream_codons = current_codons[1:]
                    orf_codons_list.append((orf_length, upstream_codons))
                    break
                current_codons.append(codon)
    # Select longest ORF
    if orf_codons_list:
        orf_codons_list.sort(reverse=True, key=lambda x: x[0])
        return orf_codons_list[0][1]
    return []

def count_all_codons(fasta_dict, target_stop):
    """Count total upstream codons for target stop codon"""
    total_codon_counts = {}
    valid_genes = 0
    for gene, seq in fasta_dict.items():
        upstream_codons = get_longest_orf_codons(seq, target_stop)
        if upstream_codons:
            valid_genes += 1
            for codon in upstream_codons:
                total_codon_counts[codon] = total_codon_counts.get(codon, 0) + 1
    print(f"Total genes with {target_stop} as stop codon: {valid_genes}")
    return total_codon_counts

def plot_codon_pie(codon_counts, target_stop):
    """Plot codon frequency pie chart, save to file"""
    codons = list(codon_counts.keys())
    counts = list(codon_counts.values())
    # Draw pie chart
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        counts, labels=codons, autopct='%1.1f%%',
        startangle=90, labeldistance=1.05, rotatelabels=True
    )
    # Set text style
    for text in texts:
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(7)
    # Add title
    ax.set_title(f"Codon Frequency Upstream of {target_stop} (Longest ORF)", fontsize=16, pad=20)
    # Save pie chart
    save_path = f"codon_frequency_{target_stop}.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Pie chart saved to: {save_path}")
    plt.close()

def validate_user_input():
    """Validate user input, only accept TAA/TAG/TGA"""
    while True:
        user_input = input("Please enter one stop codon (TAA/TAG/TGA): ").strip().upper()
        if user_input in VALID_STOP_CODONS:
            return user_input
        else:
            print(f"Invalid input! Only accept: {', '.join(VALID_STOP_CODONS)}. Try again.")

# 3. Core program execution
if __name__ == "__main__":
    # Auto switch working directory to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory set to: {script_dir}\n")

    # Set input file path
    FASTA_FILE = r"Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa"

    # Step 1: Read FASTA file
    print("Reading yeast cDNA FASTA file...")
    try:
        gene_dict = read_fasta(FASTA_FILE)
        print(f"Successfully read {len(gene_dict)} genes.\n")
    except FileNotFoundError:
        print(f"Error: File {FASTA_FILE} not found! Put it in the same folder as this script.")
        exit()

    # Step 2: Get valid user input
    target_stop = validate_user_input()
    print(f"\nAnalyzing codon frequency upstream of {target_stop}...")

    # Step 3: Count upstream codons
    codon_counts = count_all_codons(gene_dict, target_stop)

    # Step 4: Report codon counts (sorted)
    print(f"\nCodon counts upstream of {target_stop} (sorted by frequency):")
    sorted_codons = sorted(codon_counts.items(), key=lambda x: x[1], reverse=True)
    for codon, count in sorted_codons:
        print(f"{codon}: {count}")

    # Step 5: Plot and save pie chart
    if codon_counts:
        plot_codon_pie(codon_counts, target_stop)
    else:
        print(f"\nNo codons found upstream of {target_stop}!")

    print("\nAnalysis completed!")