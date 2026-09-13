import json

with open("data/synthetic/playbook.json", "r") as f:
    playbook = json.load(f)

for clause in playbook:
    if clause["clause_type"] == "Governing Law":
        clause["query_text"] = "Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the applicable jurisdiction."

with open("data/synthetic/playbook.json", "w") as f:
    json.dump(playbook, f, indent=2)

print("Updated Governing Law query_text")
