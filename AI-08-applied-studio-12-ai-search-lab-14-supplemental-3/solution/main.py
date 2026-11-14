from studio import GRAPH, iterative_deepening


def solve_extension():
    result = iterative_deepening(GRAPH, "S", "G", 4)
    visits = [visit for attempt in result["attempts"] for visit in attempt["visits"]]
    return {"attempts": len(result["attempts"]), "visits": len(visits),
            "start_visits": sum(visit["node"] == "S" for visit in visits)}

if __name__ == "__main__":
    import json
    print(json.dumps(solve_extension(), sort_keys=True))
