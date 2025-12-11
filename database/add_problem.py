#!/usr/bin/env python3
"""
Problem Database Manager for CS37 Practice Problems

Usage:
    python add_problem.py --add-category <id> <title> <order>
    python add_problem.py --add-section <id> <category_id> <title>
    python add_problem.py --add-problem <json_string>
    python add_problem.py --list-categories
    python add_problem.py --list-problems [category_id]
    python add_problem.py --export <output_file>
"""

import json
import argparse
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "problems.json"


def load_db():
    """Load the database from JSON file."""
    if not DB_PATH.exists():
        return {
            "version": "1.0",
            "course": "CS37",
            "categories": [],
            "sections": [],
            "problems": []
        }
    with open(DB_PATH, 'r') as f:
        return json.load(f)


def save_db(db):
    """Save the database to JSON file."""
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)


def add_category(db, cat_id, title, order):
    """Add a new category to the database."""
    # Check if category already exists
    for cat in db["categories"]:
        if cat["id"] == cat_id:
            print(f"Category '{cat_id}' already exists, skipping.")
            return False

    db["categories"].append({
        "id": cat_id,
        "title": title,
        "order": order
    })
    print(f"Added category: {title}")
    return True


def add_section(db, section_id, category_id, title):
    """Add a new section to the database."""
    # Check if section already exists
    for sec in db["sections"]:
        if sec["id"] == section_id:
            print(f"Section '{section_id}' already exists, skipping.")
            return False

    db["sections"].append({
        "id": section_id,
        "categoryId": category_id,
        "title": title
    })
    print(f"Added section: {title}")
    return True


def add_problem(db, problem):
    """Add a new problem to the database."""
    # Check if problem already exists
    for p in db["problems"]:
        if p["id"] == problem["id"]:
            print(f"Problem '{problem['id']}' already exists, skipping.")
            return False

    db["problems"].append(problem)
    print(f"Added problem: {problem['id']} - {problem['concept']}")
    return True


def list_categories(db):
    """List all categories."""
    print("\nCategories:")
    print("-" * 50)
    for cat in sorted(db["categories"], key=lambda x: x["order"]):
        print(f"  [{cat['order']}] {cat['id']}: {cat['title']}")


def list_problems(db, category_id=None):
    """List all problems, optionally filtered by category."""
    problems = db["problems"]
    if category_id:
        problems = [p for p in problems if p.get("categoryId") == category_id]

    print(f"\nProblems ({len(problems)} total):")
    print("-" * 50)
    for p in problems:
        print(f"  {p['id']}: {p['concept']}")


def export_db(db, output_file):
    """Export database to a file."""
    with open(output_file, 'w') as f:
        json.dump(db, f, indent=2)
    print(f"Exported to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="CS37 Problem Database Manager")
    parser.add_argument("--add-category", nargs=3, metavar=("ID", "TITLE", "ORDER"),
                        help="Add a category")
    parser.add_argument("--add-section", nargs=3, metavar=("ID", "CAT_ID", "TITLE"),
                        help="Add a section")
    parser.add_argument("--add-problem", type=str,
                        help="Add a problem (JSON string)")
    parser.add_argument("--list-categories", action="store_true",
                        help="List all categories")
    parser.add_argument("--list-problems", nargs="?", const="", metavar="CAT_ID",
                        help="List problems (optionally filter by category)")
    parser.add_argument("--export", type=str, metavar="FILE",
                        help="Export database to file")
    parser.add_argument("--stats", action="store_true",
                        help="Show database statistics")

    args = parser.parse_args()

    db = load_db()

    if args.add_category:
        cat_id, title, order = args.add_category
        add_category(db, cat_id, title, int(order))
        save_db(db)

    elif args.add_section:
        section_id, cat_id, title = args.add_section
        add_section(db, section_id, cat_id, title)
        save_db(db)

    elif args.add_problem:
        problem = json.loads(args.add_problem)
        add_problem(db, problem)
        save_db(db)

    elif args.list_categories:
        list_categories(db)

    elif args.list_problems is not None:
        cat_filter = args.list_problems if args.list_problems else None
        list_problems(db, cat_filter)

    elif args.export:
        export_db(db, args.export)

    elif args.stats:
        print(f"\nDatabase Statistics:")
        print(f"  Categories: {len(db['categories'])}")
        print(f"  Sections: {len(db['sections'])}")
        print(f"  Problems: {len(db['problems'])}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
