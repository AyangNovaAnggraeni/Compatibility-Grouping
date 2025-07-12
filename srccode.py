import pandas as pd
import networkx as nx
from itertools import combinations

# Load Data from CSV
file_path = "responses.csv"  # Change to your CSV file path
df = pd.read_csv(file_path)

# Fix: Ensure correct column name for student names
name_column = "Name "  # Adjust based on your CSV file
if name_column not in df.columns:
    print("Error: 'Name' column not found! Check your CSV headers.")
    exit()

# Define weights for each question
weights = [2, 2, 1.5, 2, 1, 1.5, 2, 1, 1, 0.5, 0.5, 0.5, 10]  # Adjust as needed

# Create a Graph for Matching
G = nx.Graph()

# Pairwise Comparison: Calculate Matching Scores
pair_scores = {}  # Store scores for reference

for student_A, student_B in combinations(df.index, 2):  # Compare every pair
    score = 0
    score_breakdown = []  # Track individual score calculations

    name_A = df.iloc[student_A][name_column]
    name_B = df.iloc[student_B][name_column]

    # Compare answers and calculate score
    for i, weight in enumerate(weights[:-1]):  # Exclude "Preferred Partner"
        answer_A = df.iloc[student_A, i + 1]
        answer_B = df.iloc[student_B, i + 1]

        if answer_A == answer_B:  # If answers match, add the weighted score
            score += weight
            score_breakdown.append(f"Q{i+1}: {answer_A} = {answer_B} → +{weight}")

    # Check mutual preference bonus
    preferred_partner_A = df.iloc[student_A, -1]  # Last column = Preferred Partner
    preferred_partner_B = df.iloc[student_B, -1]

    if preferred_partner_A == name_B and preferred_partner_B == name_A:
        score += weights[-1]  # Extra points for mutual choice
        score_breakdown.append(f"🎯 Mutual Choice Bonus → +{weights[-1]}")

    # Store score details for debugging
    pair_scores[(name_A, name_B)] = (score, score_breakdown)

    # Add to Graph if score > 0
    if score > 0:
        G.add_edge(name_A, name_B, weight=score)

# Compute Maximum Weight Matching
matched_pairs = nx.max_weight_matching(G, maxcardinality=True)

# Print Final Pairs with Score Breakdown
print("\nFinal Group Pairs with Score Calculation:\n")
for pair in matched_pairs:
    name_A, name_B = pair
    score, breakdown = pair_scores.get((name_A, name_B), pair_scores.get((name_B, name_A), (0, [])))

    print(f"{name_A} is paired with {name_B} (Final Score: {score})")
    print("\n".join(breakdown))  # Show detailed score calculations
    print("-" * 40)  # Separator
