#!/usr/bin/env python3
"""
Add step-by-step explanations to problems in the database.

Usage:
    python add_explanation.py --add <problem_id> <json_file>
    python add_explanation.py --list-pending
    python add_explanation.py --list-completed
    python add_explanation.py --show <problem_id>
    python add_explanation.py --validate <problem_id>
"""

import json
import argparse
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "problems.json"

# Valid action types for steps
VALID_ACTIONS = {
    "declare", "initialize", "assign", "evaluate", "call", "return",
    "output", "construct", "destruct", "branch", "loop-start",
    "loop-check", "loop-end", "allocate", "deallocate", "dereference", "copy"
}


def load_db():
    """Load the database from JSON file."""
    if not DB_PATH.exists():
        return {"version": "1.0", "course": "CS37", "categories": [], "sections": [], "problems": []}
    with open(DB_PATH, 'r') as f:
        return json.load(f)


def save_db(db):
    """Save the database to JSON file."""
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)


def find_problem(db, problem_id):
    """Find a problem by ID."""
    for p in db["problems"]:
        if p["id"] == problem_id:
            return p
    return None


def validate_explanation(explanation):
    """Validate an explanation structure."""
    errors = []

    if "steps" not in explanation:
        errors.append("Missing 'steps' array")
    elif not isinstance(explanation["steps"], list):
        errors.append("'steps' must be an array")
    else:
        for i, step in enumerate(explanation["steps"]):
            if "action" not in step:
                errors.append(f"Step {i}: missing 'action'")
            elif step["action"] not in VALID_ACTIONS:
                errors.append(f"Step {i}: invalid action '{step['action']}'")

            if "description" not in step:
                errors.append(f"Step {i}: missing 'description'")

    if "finalOutput" not in explanation:
        errors.append("Missing 'finalOutput'")

    if "keyInsight" not in explanation:
        errors.append("Missing 'keyInsight'")

    return errors


def add_explanation(db, problem_id, explanation):
    """Add an explanation to a problem."""
    problem = find_problem(db, problem_id)
    if not problem:
        print(f"Error: Problem '{problem_id}' not found")
        return False

    # Validate
    errors = validate_explanation(explanation)
    if errors:
        print("Validation errors:")
        for err in errors:
            print(f"  - {err}")
        return False

    problem["explanation"] = explanation
    print(f"Added explanation to {problem_id} ({len(explanation['steps'])} steps)")
    return True


def list_pending(db):
    """List problems without explanations."""
    pending = [p for p in db["problems"] if "explanation" not in p]
    print(f"\nProblems pending explanation ({len(pending)}/{len(db['problems'])}):")
    print("-" * 60)
    for p in pending:
        print(f"  {p['id']}: {p['concept']}")
    return pending


def list_completed(db):
    """List problems with explanations."""
    completed = [p for p in db["problems"] if "explanation" in p]
    print(f"\nProblems with explanations ({len(completed)}/{len(db['problems'])}):")
    print("-" * 60)
    for p in completed:
        steps = len(p["explanation"]["steps"])
        print(f"  {p['id']}: {p['concept']} ({steps} steps)")
    return completed


def show_problem(db, problem_id):
    """Show a problem with its explanation."""
    problem = find_problem(db, problem_id)
    if not problem:
        print(f"Error: Problem '{problem_id}' not found")
        return

    print(f"\n{'='*60}")
    print(f"Problem: {problem['id']}")
    print(f"Concept: {problem['concept']}")
    print(f"{'='*60}")
    print("\nCode:")
    print(problem['code'])
    print(f"\nExpected Output: {problem['output']}")

    if "explanation" in problem:
        exp = problem["explanation"]
        print(f"\n{'─'*60}")
        print("EXPLANATION:")
        print(f"{'─'*60}")
        for i, step in enumerate(exp["steps"], 1):
            line = f"L{step['line']}" if step.get('line') else "   "
            action = step['action'].upper()
            desc = step['description']
            print(f"  {i}. [{line}] {action}: {desc}")
            if step.get('state'):
                print(f"      State: {step['state']}")
            if step.get('output'):
                print(f"      Output: \"{step['output']}\"")
            if step.get('concepts'):
                print(f"      Concepts: {', '.join(step['concepts'])}")
        print(f"\nFinal Output: \"{exp['finalOutput']}\"")
        print(f"Key Insight: {exp['keyInsight']}")
    else:
        print("\n[No explanation yet]")


def generate_todo_markdown(db):
    """Generate a markdown todo list of all problems."""
    output = "# Explanation Todo List\n\n"
    output += f"Total problems: {len(db['problems'])}\n\n"

    # Group by category
    categories = {}
    for p in db["problems"]:
        cat_id = p.get("categoryId", "unknown")
        if cat_id not in categories:
            categories[cat_id] = []
        categories[cat_id].append(p)

    # Get category titles
    cat_titles = {c["id"]: c["title"] for c in db["categories"]}

    for cat_id in sorted(categories.keys()):
        problems = categories[cat_id]
        title = cat_titles.get(cat_id, cat_id)
        output += f"## {title}\n\n"

        for p in problems:
            has_exp = "explanation" in p
            checkbox = "[x]" if has_exp else "[ ]"
            output += f"- {checkbox} `{p['id']}`: {p['concept']}\n"

        output += "\n"

    return output


def main():
    parser = argparse.ArgumentParser(description="Manage problem explanations")
    parser.add_argument("--add", nargs=2, metavar=("PROBLEM_ID", "JSON_FILE"),
                        help="Add explanation from JSON file")
    parser.add_argument("--list-pending", action="store_true",
                        help="List problems without explanations")
    parser.add_argument("--list-completed", action="store_true",
                        help="List problems with explanations")
    parser.add_argument("--show", type=str, metavar="PROBLEM_ID",
                        help="Show problem with explanation")
    parser.add_argument("--validate", type=str, metavar="PROBLEM_ID",
                        help="Validate a problem's explanation")
    parser.add_argument("--generate-todo", type=str, metavar="OUTPUT_FILE",
                        help="Generate markdown todo list")
    parser.add_argument("--stats", action="store_true",
                        help="Show explanation statistics")

    args = parser.parse_args()
    db = load_db()

    if args.add:
        problem_id, json_file = args.add
        with open(json_file, 'r') as f:
            explanation = json.load(f)
        if add_explanation(db, problem_id, explanation):
            save_db(db)

    elif args.list_pending:
        list_pending(db)

    elif args.list_completed:
        list_completed(db)

    elif args.show:
        show_problem(db, args.show)

    elif args.validate:
        problem = find_problem(db, args.validate)
        if not problem:
            print(f"Error: Problem '{args.validate}' not found")
        elif "explanation" not in problem:
            print(f"Problem '{args.validate}' has no explanation")
        else:
            errors = validate_explanation(problem["explanation"])
            if errors:
                print("Validation errors:")
                for err in errors:
                    print(f"  - {err}")
            else:
                print("Explanation is valid!")

    elif args.generate_todo:
        todo_md = generate_todo_markdown(db)
        with open(args.generate_todo, 'w') as f:
            f.write(todo_md)
        print(f"Generated todo list: {args.generate_todo}")

    elif args.stats:
        completed = sum(1 for p in db["problems"] if "explanation" in p)
        total = len(db["problems"])
        print(f"\nExplanation Statistics:")
        print(f"  Completed: {completed}/{total} ({100*completed/total:.1f}%)")
        print(f"  Pending: {total - completed}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
