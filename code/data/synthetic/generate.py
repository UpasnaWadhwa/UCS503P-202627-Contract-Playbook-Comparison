import json
import os

PLAYBOOK = [
    {
        "clause_type": "Termination Notice",
        "query_text": "Either party may terminate this agreement upon prior written notice.",
        "standard_position": "Either party may terminate this agreement upon 30 days prior written notice."
    },
    {
        "clause_type": "Liability Cap",
        "query_text": "Total liability shall not exceed the total fees paid.",
        "standard_position": "Total liability shall not exceed the total fees paid in the 12 months preceding the claim."
    },
    {
        "clause_type": "Auto-Renewal",
        "query_text": "This agreement shall automatically renew for successive terms unless either party provides written notice of intent not to renew.",
        "standard_position": "This agreement shall automatically renew for successive one-year terms unless either party provides 60 days written notice of intent not to renew."
    },
    {
        "clause_type": "Governing Law",
        "query_text": "This agreement shall be governed by the laws of the jurisdiction.",
        "standard_position": "This agreement shall be governed by the laws of the State of Delaware."
    }
]

CONTRACTS = [
    {
        "id": "contract_01",
        "text": "This Services Agreement is made between the parties. \n\nEither party may terminate this agreement upon 30 days prior written notice. \n\nTotal liability shall not exceed the total fees paid in the 12 months preceding the claim. \n\nThis agreement shall automatically renew for successive one-year terms unless either party provides 60 days written notice of intent not to renew. \n\nThis agreement shall be governed by the laws of the State of Delaware.",
        "ground_truth": {
            "Termination Notice": {"verdict": "MATCH", "text_span": "Either party may terminate this agreement upon 30 days prior written notice."},
            "Liability Cap": {"verdict": "MATCH", "text_span": "Total liability shall not exceed the total fees paid in the 12 months preceding the claim."},
            "Auto-Renewal": {"verdict": "MATCH", "text_span": "This agreement shall automatically renew for successive one-year terms unless either party provides 60 days written notice of intent not to renew."},
            "Governing Law": {"verdict": "MATCH", "text_span": "This agreement shall be governed by the laws of the State of Delaware."}
        }
    },
    {
        "id": "contract_02",
        "text": "Services Agreement.\n\nEither party may terminate this agreement upon 60 days prior written notice.\n\nTotal liability shall be limited to $10,000.\n\nThis agreement shall be governed by the laws of New York.",
        "ground_truth": {
            "Termination Notice": {"verdict": "DEVIATION", "text_span": "Either party may terminate this agreement upon 60 days prior written notice."},
            "Liability Cap": {"verdict": "DEVIATION", "text_span": "Total liability shall be limited to $10,000."},
            "Auto-Renewal": {"verdict": "MISSING", "text_span": None},
            "Governing Law": {"verdict": "DEVIATION", "text_span": "This agreement shall be governed by the laws of New York."}
        }
    },
    {
        "id": "contract_03",
        "text": "Vendor Agreement.\n\nThe contract will automatically renew for one year terms unless canceled with 30 days notice.\n\nThis agreement shall be governed by the laws of the State of Delaware.",
        "ground_truth": {
            "Termination Notice": {"verdict": "MISSING", "text_span": None},
            "Liability Cap": {"verdict": "MISSING", "text_span": None},
            "Auto-Renewal": {"verdict": "DEVIATION", "text_span": "The contract will automatically renew for one year terms unless canceled with 30 days notice."},
            "Governing Law": {"verdict": "MATCH", "text_span": "This agreement shall be governed by the laws of the State of Delaware."}
        }
    }
]

# Generate more contracts by mixing and matching or leaving things out
import random

base_clauses = {
    "Termination Notice": [
        ("Either party may terminate this agreement upon 30 days prior written notice.", "MATCH"),
        ("Either party may terminate this agreement upon 90 days prior written notice.", "DEVIATION"),
        ("This agreement can be terminated immediately by either party.", "DEVIATION"),
        (None, "MISSING")
    ],
    "Liability Cap": [
        ("Total liability shall not exceed the total fees paid in the 12 months preceding the claim.", "MATCH"),
        ("Total liability is capped at 50% of the total fees paid.", "DEVIATION"),
        ("Neither party shall be liable for indirect damages, and total liability shall not exceed $1,000,000.", "DEVIATION"),
        (None, "MISSING")
    ],
    "Auto-Renewal": [
        ("This agreement shall automatically renew for successive one-year terms unless either party provides 60 days written notice of intent not to renew.", "MATCH"),
        ("This agreement shall automatically renew for a period of two years.", "DEVIATION"),
        ("This agreement will not automatically renew.", "DEVIATION"),
        (None, "MISSING")
    ],
    "Governing Law": [
        ("This agreement shall be governed by the laws of the State of Delaware.", "MATCH"),
        ("This agreement shall be governed by the laws of California.", "DEVIATION"),
        ("Governing law shall be the laws of England and Wales.", "DEVIATION"),
        (None, "MISSING")
    ]
}

for i in range(4, 16):
    contract_text_parts = [
        f"Synthetic Agreement {i}.\n\n",
        "This Agreement is entered into by and between the undersigned parties (hereinafter referred to as 'the Parties'). ",
        "WHEREAS, the Parties desire to enter into a business relationship for the provision of certain services as described herein; ",
        "NOW, THEREFORE, in consideration of the mutual covenants and promises contained herein, the Parties agree as follows: \n\n",
        "1. DEFINITIONS: Various terms used throughout this Agreement shall have the meanings ascribed to them in this section. ",
        "The term 'Services' shall mean the specific duties, tasks, and deliverables as outlined in Exhibit A. ",
        "The term 'Confidential Information' refers to any non-public data shared between the Parties during the term of this Agreement.\n\n",
        "2. SCOPE OF SERVICES: The Provider agrees to deliver the Services in a professional and workmanlike manner, in accordance with industry standards. ",
        "The Client agrees to cooperate fully, providing necessary access to information and personnel to facilitate the timely completion of the Services.\n\n"
    ]
    gt = {}
    for clause_type, options in base_clauses.items():
        choice, verdict = random.choice(options)
        if choice:
            contract_text_parts.append(choice + "\n\n")
            # add some filler after the clause sometimes
            if random.random() > 0.5:
                contract_text_parts.append("This provision shall be interpreted in accordance with standard industry practices. The Parties acknowledge that they have read and understood this section.\n\n")
        gt[clause_type] = {"verdict": verdict, "text_span": choice}
    
    contract_text_parts.append(
        "10. ENTIRE AGREEMENT: This Agreement constitutes the entire understanding between the Parties and supersedes all prior discussions, representations, and agreements, whether written or oral. "
        "No modification of this Agreement shall be binding unless executed in writing by both Parties.\n\n"
        "11. SEVERABILITY: If any provision of this Agreement is held to be invalid or unenforceable, the remaining provisions shall continue in full force and effect."
    )
    
    CONTRACTS.append({
        "id": f"contract_{i:02d}",
        "text": "".join(contract_text_parts),
        "ground_truth": gt
    })

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    contracts_dir = os.path.join(base_dir, "contracts")
    os.makedirs(contracts_dir, exist_ok=True)
    
    with open(os.path.join(base_dir, "playbook.json"), "w") as f:
        json.dump(PLAYBOOK, f, indent=2)
        
    ground_truth_out = {}
    for c in CONTRACTS:
        cid = c["id"]
        with open(os.path.join(contracts_dir, f"{cid}.txt"), "w") as f:
            f.write(c["text"])
        ground_truth_out[cid] = c["ground_truth"]
        
    with open(os.path.join(base_dir, "ground_truth.json"), "w") as f:
        json.dump(ground_truth_out, f, indent=2)
        
    print(f"Generated {len(CONTRACTS)} contracts and ground truth mapping.")

if __name__ == "__main__":
    main()
