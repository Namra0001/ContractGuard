def compare_contracts(contract_a_analysis: dict, contract_b_analysis: dict) -> dict:
    """Compares the analysis of two contracts."""
    comparison = {
        "parties_diff": {
            "only_in_a": list(set(contract_a_analysis.get("parties", [])) - set(contract_b_analysis.get("parties", []))),
            "only_in_b": list(set(contract_b_analysis.get("parties", [])) - set(contract_a_analysis.get("parties", [])))
        },
        "risks_combined": contract_a_analysis.get("risks", []) + contract_b_analysis.get("risks", [])
    }
    return comparison
