# count_codons.py
# Count in-frame codon frequency upstream of specified stop codon & plot pie chart
import os
import matplotlib.pyplot as plt

# -------------------------- 1. Define constants -------------------------
# DNA codons (cDNA sequence)
START_CODON = "ATG"
VALID_STOP_CODONS = {"TAA", "TAG", "TGA"}  # Only accept these 3 inputs
# Set plot style to make pie chart neat
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # Avoid font error
plt.rcParams['figure.figsize'] = (12, 8)  # Pie chart size

# -------------------------- 2. Define core functions -------------------------
def read_fasta(file_path):
    """Read FASTA file, return {gene_name: complete_sequence} dict"""
    fasta_data = {}
    current_name = ""
    seq_lines = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_name:
                    fasta_data[current_name] = "".join(seq_lines)
                current_name = line.split()[0][1:]  # Extract gene name
                seq_lines = []
            else:
                seq_lines.append(line)
    # Save the last gene
    if current_name:
        fasta_data[current_name] = "".join(seq_lines)
    return fasta_data

def get_longest_orf_codons(seq, target_stop):
    """
    Find all ORFs with target stop codon, select the longest one,
    return its upstream codons (start: ATG, end: target_stop, exclude both)
    """
    orf_codons_list = []  # Store (orf_length, upstream_codons) for valid ORFs
    seq_len = len(seq)
    # Traverse all ATG start positions
    for start_pos in range(seq_len - 2):
        if seq[start_pos:start_pos+3] == START_CODON:
            current_codons = []
            # Extract codons in frame (step 3)
            for codon_pos in range(start_pos, seq_len - 2, 3):
                codon = seq[codon_pos:codon_pos+3]
                if codon == START_CODON:
                    current_codons.append(codon)
                    continue
                if codon == target_stop:
                    # Calculate ORF length, save upstream codons (exclude start/stop)
                    orf_length = (codon_pos - start_pos) + 3
                    upstream_codons = current_codons[1:]  # Remove ATG
                    orf_codons_list.append((orf_length, upstream_codons))
                    break
                # Normal codon, add to list
                current_codons.append(codon)
    # Select the longest ORF's upstream codons
    if orf_codons_list:
        orf_codons_list.sort(reverse=True, key=lambda x: x[0])  # Sort by length (desc)
        return orf_codons_list[0][1]
    # No valid ORF with target stop codon
    return []

def count_all_codons(fasta_dict, target_stop):
    """Traverse all genes, count total upstream codons for target stop codon"""
    total_codon_counts = {}
    valid_genes = 0  # Count genes with target stop codon
    for gene, seq in fasta_dict.items():
        upstream_codons = get_longest_orf_codons(seq, target_stop)
        if upstream_codons:
            valid_genes += 1
            for codon in upstream_codons:
                total_codon_counts[codon] = total_codon_counts.get(codon, 0) + 1
    print(f"Total genes with {target_stop} as stop codon: {valid_genes}")
    return total_codon_counts

def plot_codon_pie(codon_counts, target_stop):
    """Plot well-labelled pie chart, save to file (not just display)"""
    # Prepare data: codon as labels, count as values
    codons = list(codon_counts.keys())
    counts = list(codon_counts.values())
    # Set pie chart properties
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        counts, labels=codons, autopct='%1.1f%%',  # Show percentage
        startangle=90, labeldistance=1.05, rotatelabels=True
    )
    # Set text styles for readability
    for text in texts:
        text.set_fontsize(8)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(7)
    # Add title (well-labelled)
    ax.set_title(
        f"Codon Frequency Upstream of {target_stop} (Longest ORF)",
        fontsize=16, pad=20
    )
    # Save pie chart to file, high resolution
    save_path = f"codon_frequency_{target_stop}.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print(f"Pie chart saved to: {save_path}")
    plt.close()  # Close plot to avoid memory leak

def validate_user_input():
    """Ask user for stop codon, only accept VALID_STOP_CODONS, loop until valid"""
    while True:
        user_input = input("Please enter one stop codon (TAA/TAG/TGA): ").strip().upper()
        if user_input in VALID_STOP_CODONS:
            return user_input
        else:
            print(f"Invalid input! Only accept: {', '.join(VALID_STOP_CODONS)}. Try again.")

# -------------------------- 3. Main program -------------------------
if __name__ == "__main__":
    # Auto switch working directory to script location (solve FileNotFoundError)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"Working directory set to: {script_dir}\n")

    # Define file path (same as stop_codons.py)
    FASTA_FILE = r"Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa"

    # Step 1: Read FASTA file first
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

    # Step 3: Count all upstream codons (longest ORF only)
    codon_counts = count_all_codons(gene_dict, target_stop)

    # Step 4: Report codon counts (sorted by count desc)
    print(f"\nCodon counts upstream of {target_stop} (sorted by frequency):")
    sorted_codons = sorted(codon_counts.items(), key=lambda x: x[1], reverse=True)
    for codon, count in sorted_codons:
        print(f"{codon}: {count}")

    # Step 5: Plot and save pie chart (core requirement)
    if codon_counts:
        plot_codon_pie(codon_counts, target_stop)
    else:
        print(f"\nNo codons found upstream of {target_stop}!")

    print("\nAnalysis completed!")