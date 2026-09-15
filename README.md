# DISC1 Psychiatric Interactome & Hub Discovery Pipeline

An automated bioinformatics and graph analysis pipeline that models protein-protein interaction (PPI) networks for **DISC1** (*Disrupted in Schizophrenia 1*), a critical scaffold protein implicated in major psychiatric disorders.

This project translates computational neuroscience research conducted during the **AUC PFx Research Program** into an automated Python data pipeline and interactive visualizer.

---

## Live Demo
Explore the interactive network graph directly in your browser:  
👉 **[View Interactive Interactome](https://Joesiyuh.github.io/disc1-interactome-pipeline/disc1_interactome.html)**

---

## Overview & Scientific Context
DISC1 functions biologically as a molecular "scaffold," physically anchoring multiple signaling pathways essential for neural development, neurite outgrowth, and synaptic plasticity. 

This project programmatically queries verified human biological data to:
1. Reconstruct the first-degree interaction network surrounding DISC1.
2. Quantitatively identify critical "bottleneck" proteins and regulatory hubs using network centrality metrics.
3. Render physics-based, draggable network visualizations for exploratory analysis.

---

## Pipeline Architecture
- **Data Ingestion (`requests`):** Queries the public STRING-db REST API for high-confidence human interactors (Taxonomy ID: `9606`, Confidence Score ≥ `0.700`).
- **Data Processing (`pandas`):** Normalizes tab-separated tabular output and scales interaction confidence scores.
- **Graph Modeling & Centrality (`networkx`):** Constructs an undirected weighted network and computes:
  - **Degree Centrality:** Measures the density of direct protein interactions.
  - **Betweenness Centrality:** Identifies bottleneck proteins that control information flow across sub-networks (e.g., *PDE4B*, *NDEL1*, *GSK3B*).
- **Interactive Visualization (`pyvis`):** Renders a browser-based graph with physics simulation where node size and line thickness reflect biological centrality and interaction confidence.

---

## Key Findings (Example Output)
| Protein | Degree Centrality | Betweenness Centrality | Biological Role |
| :--- | :--- | :--- | :--- |
| **DISC1** | High | High | Primary scaffold hub |
| **PDE4B** | High | High | Critical cAMP signaling regulator |
| **NDEL1** | Moderate | High | Neurite outgrowth & centrosome positioning |
| **GSK3B** | Moderate | Moderate | Neurodevelopmental kinase (Wnt pathway) |

---

## Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/disc1-interactome-pipeline.git](https://github.com/YOUR_GITHUB_USERNAME/disc1-interactome-pipeline.git)
   cd disc1-interactome-pipeline
