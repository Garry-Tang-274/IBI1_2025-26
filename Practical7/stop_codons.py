import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# 2. Define genetic constants
START_CODON = "ATG"
VALID_STOPS = {"TAA", "TAG", "TGA"}

# 3. Define standalone functions
def read_fasta(file_path):
    """
    Standalone function to parse FASTA files.
    Extracts only the gene ID to comply with formatting requirements.
    """
    fasta_data = {}
    current_name = ""
    seq_lines = []
    
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Handle the header line
            if line.startswith(">"):
                if current_name:
                    fasta_data[current_name] = "".join(seq_lines)
                # split()[0] removes metadata; [1:] removes '>'
                current_name = line.split()[0][1:] 
                seq_lines = []
            else:
                seq_lines.append(line)
    
    if current_name:
        fasta_data[current_name] = "".join(seq_lines)
    return fasta_data

def get_longest_orf_codons(seq, target_stop):
    """
    Finds the longest ORF that ends specifically with the user-defined target stop codon.
    Returns the list of codons located upstream of that stop codon.
    """
    valid_orfs = []
    seq_len = len(seq)
    
    # Scan every position for the start codon 'ATG'
    for i in range(seq_len - 2):
        if seq[i:i+3] == START_CODON:
            current_codons = []
            # Read in steps of 3 (in-frame)
            for j in range(i, seq_len - 2, 3):
                codon = seq[j:j+3]
                
                # Check for any stop codon in the current frame
                if codon in VALID_STOPS:
                    # If it matches the target stop, save this potential ORF
                    if codon == target_stop:
                        valid_orfs.append(current_codons.copy())
                    break  # Stop translation at the first stop codon encountered
                
                current_codons.append(codon)
                
    # Return the longest sequence from the valid ORFs found
    if valid_orfs:
        return max(valid_orfs, key=len)
    return []

def plot_usage_pie(counts, stop_type):
    """
    Generates and saves a pie chart showing the frequency of the Top 10 codons.
    The remaining codons are grouped into 'Other' for visual clarity.
    """
    # Sort codons by frequency in descending order
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    total_count = sum(counts.values())
    
    # Logic to separate Top 10 from the rest
    labels = [item[0] for item in sorted_items[:10]]
    sizes = [item[1] for item in sorted_items[:10]]
    
    if len(sorted_items) > 10:
        labels.append("Other")
        sizes.append(sum(item[1] for item in sorted_items[10:]))
    
    # Plot configuration
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
    
    # Include the total codon count in the chart title
    ax.set_title(f"Top 10 Codon Frequency Upstream of {stop_type}\n(Total Codons: {total_count})", fontsize=14)
    ax.axis('equal')
    
    # Save the figure to a file as required by the portfolio
    save_path = f"codon_freq_{stop_type}_top10.png"
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"Pie chart saved successfully: {save_path}")
    plt.close()

# 4. Main execution logic
if __name__ == "__main__":
    # Ensure the script operates in its own directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # User interaction for stop codon selection
    target = input("Please enter a stop codon for analysis (TAA/TAG/TGA): ").strip().upper()
    
    if target in VALID_STOPS:
        INPUT_FILE = "Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa"
        
        print(f"Reading {INPUT_FILE}...")
        try:
            genes = read_fasta(INPUT_FILE)
            
            # Aggregate codon counts across all valid genes
            global_counts = {}
            for sequence in genes.values():
                upstream_codons = get_longest_orf_codons(sequence, target)
                for codon in upstream_codons:
                    global_counts[codon] = global_counts.get(codon, 0) + 1
            
            # Output report and generate plot
            if global_counts:
                print(f"\n--- Results for {target} ---")
                print(f"Total upstream codons analyzed: {sum(global_counts.values())}")
                plot_usage_pie(global_counts, target)
            else:
                print(f"No in-frame sequences were found ending with {target}.")
                
        except FileNotFoundError:
            print(f"Error: The file '{INPUT_FILE}' was not found in this folder.")
    else:
        print("Invalid entry. Please use TAA, TAG, or TGA.")

    print("\nProcess finished.")