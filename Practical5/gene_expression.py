import matplotlib.pyplot as plt

# 1. Create initial gene expression dict
gene_exp = {"TP53": 12.4, "EGFR": 15.1, "BRCA1": 8.2, "PTEN": 5.3, "ESR1": 10.7}
print("="*50)
print("🔍 Initial Gene Expression Dictionary")
print("="*50)
for gene, exp in gene_exp.items():
    print(f"{gene:<8} : {exp:>5.1f}")

# 2. Add MYC gene (11.6)
gene_exp["MYC"] = 11.6
print("\n" + "="*50)
print("🔍 Dictionary After Adding MYC")
print("="*50)
for gene, exp in gene_exp.items():
    print(f"{gene:<8} : {exp:>5.1f}")

# 3. Plot labeled bar chart
genes = list(gene_exp.keys())
expressions = list(gene_exp.values())
plt.bar(genes, expressions, color="#1f77b4", alpha=0.8)
plt.title("Gene Expression Levels", fontsize=12, pad=10)
plt.xlabel("Gene Name", fontsize=10)
plt.ylabel("Expression Level", fontsize=10)
plt.xticks(fontsize=9)
plt.yticks(fontsize=9)
plt.tight_layout()
plt.show()

# 4. Query target gene (with error handling)
target_gene = "EGFR"  # Modify to test different genes
print("\n" + "="*50)
print("🔍 Target Gene Query Result")
print("="*50)
if target_gene in gene_exp:
    print(f"✅ Gene '{target_gene}' found!")
    print(f"   Expression Level: {gene_exp[target_gene]:.1f}")
else:
    print(f"❌ Error: Gene '{target_gene}' not found in the dictionary!")
    print(f"   Available genes: {', '.join(gene_exp.keys())}")

# 5. Calculate average expression
avg_exp = sum(expressions) / len(expressions)
print("\n" + "="*50)
print("📊 Summary Statistics")
print("="*50)
print(f"Total Genes:       {len(gene_exp):>3}")
print(f"Average Expression: {avg_exp:>8.2f}")
print("="*50)