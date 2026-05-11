import os
import matplotlib.pyplot as plt
import numpy as np

# Genetic definitions
START_CODON = "ATG"
VALID_STOPS = {"TAA", "TAG", "TGA"} # [cite: 321]

def get_orf_upstream_codons(seq, target_stop):
    """
    Finds the longest ORF ending with the target stop codon.
    Returns a list of codons occurring upstream of that stop.
    """
    valid_orfs = []
    # Search all possible start codons
    for i in range(len(seq) - 2):
        if seq[i:i+3] == START_CODON:
            current_codons = []
            # Scan in-frame
            for j in range(i, len(seq) - 2, 3):
                codon = seq[j:j+3]
                if codon in VALID_STOPS:
                    # Only collect if it matches the user's target stop
                    if codon == target_stop:
                        valid_orfs.append(current_codons.copy())
                    break # Stop at the first termination encountered
                current_codons.append(codon)
    
    # Return the longest sequence found among valid ORFs
    if valid_orfs:
        return max(valid_orfs, key=len) # [cite: 323]
    return []

def plot_usage_pie(counts, stop_codon):
    """
    Generates and saves a pie chart for the top 10 codons.
    Groups remaining codons into an 'Other' category for clarity.
    """
    # Sort codons by frequency descending
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    total_codons = sum(counts.values())
    
    # Extract top 10 and aggregate the rest
    labels = [item[0] for item in sorted_items[:10]]
    sizes = [item[1] for item in sorted_items[:10]]
    
    if len(sorted_items) > 10:
        labels.append("Other")
        sizes.append(sum(item[1] for item in sorted_items[10:]))
    
    # Create the visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
    ax.set_title(f"Top 10 Codon Frequency Upstream of {stop_codon}\n(Total Codons: {total_codons})")
    
    # Save the plot to a file as required by the guide
    save_name = f"codon_freq_{stop_codon}.png" # [cite: 326]
    plt.tight_layout()
    plt.savefig(save_name, dpi=150) # [cite: 336]
    print(f"Chart saved as {save_name}")
    plt.close()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Prompt user for input
    user_stop = input("Enter target stop codon (TAA/TAG/TGA): ").strip().upper() # [cite: 321]
    
    if user_stop in VALID_STOPS:
        # Note: read_fasta function should be imported or defined here
        from stop_codons import read_fasta
        genes = read_fasta("Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa")
        
        agg_counts = {}
        for sequence in genes.values():
            codons = get_orf_upstream_codons(sequence, user_stop)
            for c in codons:
                agg_counts[c] = agg_counts.get(c, 0) + 1
        
        if agg_counts:
            print(f"\nAnalysis complete. Total valid codons: {sum(agg_counts.values())}")
            plot_usage_pie(agg_counts, user_stop)
        else:
            print(f"No in-frame sequences found for stop codon {user_stop}.")
    else:
        print("Invalid input. Please use TAA, TAG, or TGA.")