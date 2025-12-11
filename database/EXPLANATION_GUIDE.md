# Database Schema Reference

## Database Structure

```json
{
  "version": "1.0",
  "course": "CS 37",
  "categories": [...],
  "problems": [...]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version |
| `course` | string | Course identifier |
| `categories` | array | Problem categories |
| `problems` | array | All practice problems |

---

## Category Schema

```json
{
  "id": "control-structures",
  "title": "Control Structures & Operators",
  "order": 1
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique category identifier |
| `title` | string | Display name |
| `order` | number | Sort order for display |

---

## Problem Schema

```json
{
  "id": "ctrl-001",
  "categoryId": "control-structures",
  "concept": "`&&` operator behavior",
  "code": "int main() {\n    cout << (true && true);\n}",
  "output": "1",
  "tags": ["control-flow", "operators"],
  "explanation": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique problem identifier (e.g., `ctrl-001`, `ptr-015`) |
| `categoryId` | string | References a category `id` |
| `concept` | string | Short description of the concept tested. Use backticks for code |
| `code` | string | C++ source code to trace |
| `output` | string | Expected stdout when program runs |
| `tags` | string[] | Searchable topic tags |
| `explanation` | object | Step-by-step execution trace (see below) |

---

## Explanation Schema

```json
{
  "explanation": {
    "steps": [ ... ],
    "finalOutput": "1",
    "keyInsight": "Main takeaway for this problem"
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `steps` | array | Ordered list of execution steps |
| `finalOutput` | string | Complete stdout when program finishes |
| `keyInsight` | string | The main concept or "trick" being tested |

---

## Step Schema

```json
{
  "line": 2,
  "action": "declare",
  "description": "Declare `x` = 5",
  "state": {"x": 5},
  "output": "5",
  "concepts": ["variable-declaration"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `line` | number \| null | Yes | Source line number. Use `null` for implicit operations (e.g., destructor at scope end) |
| `action` | string | Yes | Operation type (see Action Types) |
| `description` | string | Yes | Human-readable explanation. Use backticks for code: `` `x` `` |
| `state` | object | No | Variable values after this step. Keys = variable names |
| `output` | string | No | Text printed to stdout by this step |
| `concepts` | string[] | No | 1-3 concept tags for this step |

---

## Action Types

| Action | Description |
|--------|-------------|
| `declare` | Variable or object declaration |
| `assign` | Assignment to existing variable |
| `evaluate` | Expression evaluation |
| `call` | Function or method invocation |
| `return` | Function return statement |
| `output` | Print statement (cout) |
| `construct` | Constructor execution |
| `destruct` | Destructor execution |
| `branch` | Conditional decision (if/else/switch) |
| `loop-start` | Beginning of loop iteration |
| `loop-check` | Loop condition evaluation |
| `loop-end` | Loop termination |
| `allocate` | Heap allocation (new) |
| `deallocate` | Heap deallocation (delete) |
| `dereference` | Pointer dereference |
| `copy` | Copy constructor or assignment |

---

## Guidelines

1. Steps follow **execution order**, not source line order
2. Include implicit operations (constructors, destructors)
3. Use active voice: "Declare `x` = 5" not "x is declared"
4. `state` tracks only variables relevant to understanding
5. `keyInsight` explains what makes this problem tricky
