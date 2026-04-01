# count_codons.py
# 1. Define constants
import os
import matplotlib.pyplot as plt
import numpy as np

# DNA codons (cDNA sequence)
START_CODON = "ATG"
VALID_STOP_CODONS = {"TAA", "TAG", "TGA"}
# Plot style configuration (EXTREMELY LARGE for all 64 codons)
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['figure.figsize'] = (24, 20)  # Super large figure
plt.rcParams['axes.unicode_minus'] = False

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

def plot_codon_pie_all_codons(codon_counts, target_stop):
    """
    Plot PIE CHART WITH ALL 64 CODONS (NO 'Other'), SORTED DESCENDING, NO OVERLAP.
    Uses extremely large figure, external multi-column legend, and smart labeling.
    """
    # 1. Sort ALL codons STRICTLY by frequency (DESCENDING) - REQUIREMENT 2
    sorted_items = sorted(codon_counts.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    sizes = [item[1] for item in sorted_items]
    total_count = sum(sizes)
    
    # 2. Create figure with EXTREMELY LARGE size to fit everything
    fig, ax = plt.subplots()
    
    # 3. Use a high-contrast color map with 64 distinct colors
    colors = plt.cm.gist_ncar(np.linspace(0, 1, len(labels)))
    
    # 4. Draw pie chart: NO LABELS ON PIE, ONLY PERCENTAGE (smart display)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,  # CRITICAL: NO CODON NAMES ON PIE TO AVOID OVERLAP
        autopct=lambda pct: f'{pct:.1f}%' if pct > 0.5 else '',  # Show % only if > 0.5%
        startangle=90,
        colors=colors,
        wedgeprops=dict(edgecolor='white', linewidth=0.5, alpha=0.95),
        pctdistance=0.82,  # Position percentage text inside
        counterclock=False  # Sort CLOCKWISE (largest first at top right)
    )
    
    # 5. Style percentage text
    for autotext in autotexts:
        autotext.set_color("black")
        autotext.set_fontsize(7)
        autotext.set_weight('bold')
    
    # 6. Add EXTERNAL MULTI-COLUMN LEGEND (SOLVES OVERLAP) - REQUIREMENT 3
    # Legend is placed on the right, split into 4 columns for all 64 codons
    ax.legend(wedges, labels,
              title=f"Codon (Total: {len(labels)})",
              loc="center left",
              bbox_to_anchor=(1.02, 0, 0.5, 1),
              ncol=4,  # Split into 4 columns to fit all 64 codons
              fontsize=9,
              title_fontsize=12)
    
    # 7. Add title (explicitly states sorted descending)
    ax.set_title(f"Codon Frequency Upstream of {target_stop}\n(All {len(labels)} Codons, Sorted by Frequency Descending)",
                 fontsize=20, pad=30)
    
    # 8. Equal aspect ratio ensures pie is drawn as a circle
    ax.axis('equal')
    
    # 9. Save pie chart (EXTREMELY HIGH DPI to capture all details)
    save_path = f"codon_frequency_{target_stop}_all_codons.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=400, bbox_inches="tight")
    print(f"Full codon pie chart saved to: {save_path}")
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

    # Step 5: Plot and save FULL PIE CHART (ALL CODONS, NO OVERLAP)
    if codon_counts:
        plot_codon_pie_all_codons(codon_counts, target_stop)
    else:
        print(f"\nNo codons found upstream of {target_stop}!")

    print("\nAnalysis completed!")