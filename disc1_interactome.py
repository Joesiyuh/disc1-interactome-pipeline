import io
import requests
import pandas as pd
import networkx as nx
from pyvis.network import Network

# ==============================================================================
# 1. CONFIGURATION & API SETUP
# ==============================================================================
TARGET_PROTEIN = "DISC1"
SPECIES_ID = 9606          # 9606 is Homo sapiens (Human)
CONFIDENCE_THRESHOLD = 700 # 700/1000 = High confidence interactions
LIMIT = 25                 # Number of interactors to retrieve

print(f"[1/4] Fetching interaction data for {TARGET_PROTEIN} from STRING-db API...")

API_URL = "https://string-db.org/api/tsv/interaction_partners"
params = {
    "identifiers": TARGET_PROTEIN,
    "species": SPECIES_ID,
    "required_score": CONFIDENCE_THRESHOLD,
    "limit": LIMIT,
    "caller_identity": "auc_pfx_research_pipeline"
}

response = requests.get(API_URL, params=params)

if response.status_code != 200:
    raise RuntimeError(f"API request failed: {response.status_code} - {response.text}")

# ==============================================================================
# 2. PARSE DATA INTO A TABLE
# ==============================================================================
print("[2/4] Parsing interaction table...")

tsv_data = io.StringIO(response.text)
df = pd.read_csv(tsv_data, sep="\t")

edges_df = df[["preferredName_A", "preferredName_B", "score"]].copy()
edges_df["score"] = (edges_df["score"] * 1000).astype(int)

print(f"Loaded {len(edges_df)} verified interactions.")

# ==============================================================================
# 3. BUILD GRAPH & COMPUTE NETWORK CENTRALITY
# ==============================================================================
print("[3/4] Modeling biological network and computing centrality metrics...")

G = nx.Graph()

for _, row in edges_df.iterrows():
    protein_a = row["preferredName_A"]
    protein_b = row["preferredName_B"]
    weight = row["score"]
    G.add_edge(protein_a, protein_b, weight=weight)

degree_dict = nx.degree_centrality(G)
betweenness_dict = nx.betweenness_centrality(G)

analysis_rows = []
for node in G.nodes():
    analysis_rows.append({
        "Protein": node,
        "Connections": G.degree(node),
        "Degree_Centrality": round(degree_dict[node], 3),
        "Betweenness_Centrality": round(betweenness_dict[node], 3)
    })

results_df = pd.DataFrame(analysis_rows).sort_values(by="Betweenness_Centrality", ascending=False)

print("\n--- TOP 5 REGULATORY HUBS / BOTTLENECK PROTEINS ---")
print(results_df.head(5).to_string(index=False))
print("-" * 52)

# ==============================================================================
# 4. GENERATE INTERACTIVE HTML VISUALIZATION
# ==============================================================================
print("\n[4/4] Generating physics-based interactive graph visualization...")

net = Network(height="750px", width="100%", bgcolor="#1a1a1a", font_color="white")
net.force_atlas_2based()

for node in G.nodes():
    is_target = (node == TARGET_PROTEIN)
    centrality_score = betweenness_dict[node]
    
    color = "#FFD700" if is_target else "#00CED1"
    size = 35 if is_target else (15 + centrality_score * 40)
    
    hover_label = (
        f"Protein: {node}\n"
        f"Degree: {G.degree(node)}\n"
        f"Betweenness Centrality: {round(centrality_score, 4)}"
    )
    
    net.add_node(node, label=node, title=hover_label, color=color, size=size)

for u, v, data in G.edges(data=True):
    confidence = data["weight"]
    thickness = (confidence / 1000) * 3
    net.add_edge(u, v, value=thickness, title=f"Confidence: {confidence}/1000", color="#555555")

output_file = "disc1_interactome.html"
net.write_html(output_file)

print(f"\nSuccess! Open '{output_file}' in your web browser to explore the interactome.")
