ROWS = [
    ("A", 1, 0), ("A", 1, 0), ("A", 0, 1), ("A", 0, 0),
    ("B", 1, 1), ("B", 1, 1), ("B", 0, 0), ("B", 0, 1),
]


def metrics(rows):
    if any(expected not in (0, 1) or predicted not in (0, 1) for _, expected, predicted in rows):
        raise ValueError("Use binary expected and predicted labels.")
    groups = {}
    for group, expected, predicted in rows:
        correct, total = groups.get(group, (0, 0))
        groups[group] = (correct + (expected == predicted), total + 1)
    positives = sum(expected == 1 for _, expected, _ in rows)
    true_positives = sum(expected == predicted == 1 for _, expected, predicted in rows)
    return {
        "overall": sum(expected == predicted for _, expected, predicted in rows) / len(rows) if rows else None,
        "groups": {group: correct / total for group, (correct, total) in groups.items()},
        "positive_recall": true_positives / positives if positives else None,
    }


def solve_extension():
    return metrics(ROWS)

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
