from studio import GRAPH, ADMISSIBLE, BAD, search


def solve_extension():
    good = search(GRAPH, "S", "G", ADMISSIBLE, "astar")
    bad = search(GRAPH, "S", "G", BAD, "astar")
    return {"admissible_cost": good["cost"], "overestimate_cost": bad["cost"]}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
