# Memory Visualization Schema Plan

## Overview

This document outlines the plan to add memory visualization support to the CS37 practice problems database. The schema enables visual representation of program state (stack, heap) at each execution step.

---

## Goals

1. **Flexible Granularity**: Support both expression-level and statement-level steps
2. **Separation of Concerns**: Keep memory traces distinct from pedagogical explanations
3. **Full Memory State**: Track stack frames, heap allocations, and variable values
4. **Object Expansion**: Allow drilling into complex types (arrays, structs, pointers)
5. **Debugger Compatibility**: Structure that can be generated from debugger/analyzer output

---

## Schema Design

### Problem Extension

Add optional `memoryTrace` field to existing Problem schema:

```json
{
  "id": "ptr-001",
  "categoryId": "pointers",
  "concept": "...",
  "code": "...",
  "output": "...",
  "tags": [...],
  "explanation": { ... },
  "memoryTrace": { ... }
}
```

The `memoryTrace` is separate from `explanation` because:
- Explanations are pedagogical (human-written, concept-focused)
- Memory traces are technical (machine-generated or precise state snapshots)
- Different granularity needs (explanation steps vs debugger steps)

---

### MemoryTrace Schema

```json
{
  "memoryTrace": {
    "granularity": "statement" | "expression",
    "steps": [ ... ],
    "expansions": { ... }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `granularity` | string | Step level: `"statement"` or `"expression"` |
| `steps` | array | Ordered execution steps with full memory state |
| `expansions` | object | Registry of expanded objects (keyed by address) |

---

### MemoryStep Schema

```json
{
  "index": 0,
  "location": {
    "line": 3,
    "column": 5,
    "function": "main"
  },
  "statement": "int x = 5;",
  "stack": [ ... ],
  "heap": [ ... ],
  "output": "Hello"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | number | Yes | Step sequence number (0-based) |
| `location` | object | Yes | Source code position |
| `location.line` | number | Yes | Line number |
| `location.column` | number | No | Column (for expression granularity) |
| `location.function` | string | Yes | Enclosing function name |
| `statement` | string | No | Code being executed |
| `stack` | array | Yes | Call stack (array of StackFrame) |
| `heap` | array | No | Heap allocations (array of HeapBlock) |
| `output` | string | No | Cumulative stdout at this step |

---

### StackFrame Schema

```json
{
  "functionName": "main",
  "address": "0x7fff5000",
  "variables": [
    {
      "name": "x",
      "type": "int",
      "value": "5",
      "address": "0x7fff4ffc",
      "initialized": true,
      "expandable": false
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `functionName` | string | Name of function |
| `address` | string | Frame base address |
| `variables` | array | Local variables in this frame |

---

### Variable Schema

```json
{
  "name": "arr",
  "type": "int[3]",
  "value": "[1, 2, 3]",
  "address": "0x7fff4ff0",
  "initialized": true,
  "expandable": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Variable name |
| `type` | string | C++ type |
| `value` | string | Display value (summary for complex types) |
| `address` | string | Memory address |
| `initialized` | boolean \| `"partial"` | Initialization state |
| `expandable` | boolean | Can be expanded to show internals |

**Initialization States**:
- `true`: Has been assigned a value
- `false`: Uninitialized (contains garbage)
- `"partial"`: Some members initialized (structs only)

**Expandable Rules**:
- Primitives: Never expandable
- Arrays: Always expandable
- Structs: Always expandable
- Pointers to complex types: Expandable when non-null

---

### HeapBlock Schema

```json
{
  "address": "0x55a00010",
  "type": "int",
  "size": 4,
  "value": "42",
  "initialized": true,
  "expandable": false,
  "freed": false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `address` | string | Heap address |
| `type` | string | Allocated type |
| `size` | number | Size in bytes |
| `value` | string | Current value |
| `initialized` | boolean | Has been assigned |
| `expandable` | boolean | Can show internals |
| `freed` | boolean | Has been deallocated |

---

### Expansions Registry

For expandable objects, the `expansions` object maps addresses to their internal structure:

```json
{
  "expansions": {
    "0x7fff4ff0": {
      "type": "array",
      "elements": [
        { "index": 0, "value": "1" },
        { "index": 1, "value": "2" },
        { "index": 2, "value": "3" }
      ]
    },
    "0x55a00010": {
      "type": "struct",
      "members": [
        { "name": "x", "type": "int", "value": "10" },
        { "name": "y", "type": "int", "value": "20" }
      ]
    }
  }
}
```

---

## Granularity Modes

### Statement-Level (`"granularity": "statement"`)

One step per statement. Simpler, matches line-by-line tracing.

```cpp
int x = 5;    // Step 0
int y = x+1;  // Step 1
cout << y;    // Step 2
```

### Expression-Level (`"granularity": "expression"`)

Multiple steps per statement. Shows intermediate evaluations.

```cpp
int y = x + 1;
// Step 0: evaluate x -> 5
// Step 1: evaluate x + 1 -> 6
// Step 2: assign y = 6
```

Expression-level requires `location.column` to pinpoint subexpressions.

---

## Implementation Phases

### Phase 1: Schema Definition
- [x] Design MemoryTrace schema
- [x] Design MemoryStep schema
- [x] Design StackFrame/Variable schemas
- [x] Design HeapBlock schema
- [x] Design Expansions registry
- [x] Design StepMapping schema
- [x] Document in this plan

### Phase 2: Database Integration
- [ ] Update EXPLANATION_GUIDE.md with new schemas
- [ ] Add `memoryTrace` field to problem JSON schema
- [ ] Add `stepMapping` field to problem JSON schema
- [ ] Create sample problems with memory traces and mappings
- [ ] Validate JSON structure

### Phase 3: Webapp Visualization
- [ ] Design memory visualization UI component
- [ ] Implement stack frame rendering
- [ ] Implement heap block rendering
- [ ] Add variable expansion (click to drill down)
- [ ] Implement step mapping lookup (explanation → memory)
- [ ] Implement reverse mapping (memory → explanation)
- [ ] Sync memory view with explanation step clicks

### Phase 4: Content Creation
- [ ] Identify problems that benefit from memory visualization
- [ ] Prioritize: pointers, dynamic memory, references
- [ ] Create memory traces for selected problems
- [ ] Create step mappings for each trace

---

## Example: Complete MemoryTrace

```json
{
  "memoryTrace": {
    "granularity": "statement",
    "steps": [
      {
        "index": 0,
        "location": { "line": 2, "function": "main" },
        "statement": "int x = 5;",
        "stack": [
          {
            "functionName": "main",
            "address": "0x7fff5000",
            "variables": [
              {
                "name": "x",
                "type": "int",
                "value": "5",
                "address": "0x7fff4ffc",
                "initialized": true,
                "expandable": false
              }
            ]
          }
        ],
        "heap": [],
        "output": ""
      },
      {
        "index": 1,
        "location": { "line": 3, "function": "main" },
        "statement": "int* p = new int(10);",
        "stack": [
          {
            "functionName": "main",
            "address": "0x7fff5000",
            "variables": [
              {
                "name": "x",
                "type": "int",
                "value": "5",
                "address": "0x7fff4ffc",
                "initialized": true,
                "expandable": false
              },
              {
                "name": "p",
                "type": "int*",
                "value": "0x55a00010",
                "address": "0x7fff4ff8",
                "initialized": true,
                "expandable": false
              }
            ]
          }
        ],
        "heap": [
          {
            "address": "0x55a00010",
            "type": "int",
            "size": 4,
            "value": "10",
            "initialized": true,
            "expandable": false,
            "freed": false
          }
        ],
        "output": ""
      }
    ],
    "expansions": {}
  }
}
```

---

## Step Mapping: Linking Explanations to Memory

A separate `stepMapping` field connects human explanations to memory steps without coupling them. This preserves separation of concerns while enabling synchronized visualization.

### Why Separate Mapping?

| Concern | Owner | Purpose |
|---------|-------|---------|
| `explanation` | Human author | Pedagogical narrative, concept focus |
| `memoryTrace` | Debugger/analyzer | Precise machine state |
| `stepMapping` | Integration layer | Links the two without coupling |

Benefits:
- Explanations can be written independently of memory traces
- Memory traces can be auto-generated without affecting explanations
- Mapping can be 1:1, 1:many, or many:1 (flexible granularity)
- Either side can be updated without breaking the other

---

### StepMapping Schema

```json
{
  "stepMapping": {
    "mappings": [
      {
        "explanationStep": 0,
        "memorySteps": [0]
      },
      {
        "explanationStep": 1,
        "memorySteps": [1, 2, 3]
      },
      {
        "explanationStep": 2,
        "memorySteps": [4]
      }
    ]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `mappings` | array | List of explanation-to-memory step links |
| `mappings[].explanationStep` | number | Index into `explanation.steps[]` |
| `mappings[].memorySteps` | number[] | Indices into `memoryTrace.steps[]` |

---

### Mapping Patterns

#### 1:1 Mapping (Statement-level memory, statement-level explanation)

```json
{
  "mappings": [
    { "explanationStep": 0, "memorySteps": [0] },
    { "explanationStep": 1, "memorySteps": [1] },
    { "explanationStep": 2, "memorySteps": [2] }
  ]
}
```

Both have the same granularity. Each explanation step corresponds to exactly one memory state.

#### 1:Many Mapping (Expression-level memory, statement-level explanation)

```json
{
  "mappings": [
    { "explanationStep": 0, "memorySteps": [0, 1, 2] },
    { "explanationStep": 1, "memorySteps": [3, 4] }
  ]
}
```

One explanation step spans multiple expression-level memory steps. UI can animate through sub-steps or show final state.

#### Many:1 Mapping (Statement-level memory, concept-level explanation)

```json
{
  "mappings": [
    { "explanationStep": 0, "memorySteps": [0] },
    { "explanationStep": 1, "memorySteps": [0] },
    { "explanationStep": 2, "memorySteps": [1] }
  ]
}
```

Multiple explanation steps (e.g., "evaluate left side", "evaluate right side") reference the same memory snapshot.

#### Sparse Mapping (Not all steps mapped)

```json
{
  "mappings": [
    { "explanationStep": 0, "memorySteps": [0] },
    { "explanationStep": 2, "memorySteps": [3] }
  ]
}
```

Some explanation steps have no memory visualization (conceptual steps), or some memory steps have no explanation (implicit operations).

---

### Full Problem Example with Mapping

```json
{
  "id": "ptr-001",
  "categoryId": "pointers",
  "concept": "Pointer declaration and dereferencing",
  "code": "int main() {\n    int x = 5;\n    int* p = &x;\n    cout << *p;\n}",
  "output": "5",
  "tags": ["pointers", "dereference"],

  "explanation": {
    "steps": [
      { "line": 2, "action": "declare", "description": "Declare `x` = 5" },
      { "line": 3, "action": "declare", "description": "Declare pointer `p` pointing to `x`" },
      { "line": 4, "action": "output", "description": "Dereference `p` to get value of `x`, print `5`" }
    ],
    "finalOutput": "5",
    "keyInsight": "The * operator follows the pointer to access the value it points to"
  },

  "memoryTrace": {
    "granularity": "statement",
    "steps": [
      {
        "index": 0,
        "location": { "line": 2, "function": "main" },
        "stack": [{
          "functionName": "main",
          "address": "0x7fff5000",
          "variables": [
            { "name": "x", "type": "int", "value": "5", "address": "0x7fff4ffc", "initialized": true, "expandable": false }
          ]
        }],
        "heap": [],
        "output": ""
      },
      {
        "index": 1,
        "location": { "line": 3, "function": "main" },
        "stack": [{
          "functionName": "main",
          "address": "0x7fff5000",
          "variables": [
            { "name": "x", "type": "int", "value": "5", "address": "0x7fff4ffc", "initialized": true, "expandable": false },
            { "name": "p", "type": "int*", "value": "0x7fff4ffc", "address": "0x7fff4ff8", "initialized": true, "expandable": false }
          ]
        }],
        "heap": [],
        "output": ""
      },
      {
        "index": 2,
        "location": { "line": 4, "function": "main" },
        "stack": [{
          "functionName": "main",
          "address": "0x7fff5000",
          "variables": [
            { "name": "x", "type": "int", "value": "5", "address": "0x7fff4ffc", "initialized": true, "expandable": false },
            { "name": "p", "type": "int*", "value": "0x7fff4ffc", "address": "0x7fff4ff8", "initialized": true, "expandable": false }
          ]
        }],
        "heap": [],
        "output": "5"
      }
    ],
    "expansions": {}
  },

  "stepMapping": {
    "mappings": [
      { "explanationStep": 0, "memorySteps": [0] },
      { "explanationStep": 1, "memorySteps": [1] },
      { "explanationStep": 2, "memorySteps": [2] }
    ]
  }
}
```

---

### UI Behavior with Mapping

When user clicks an explanation step:
1. Look up `stepMapping.mappings` for that `explanationStep` index
2. Get the corresponding `memorySteps` array
3. Display the memory state from the last memory step in the range
4. Optionally: animate through all memory steps in sequence

When user steps through memory visualization:
1. Reverse-lookup which `explanationStep` corresponds to current `memoryStep`
2. Highlight that explanation step
3. Handle unmapped steps gracefully (no explanation highlight)

---

## Relationship to Existing Schema

| Existing | New | Relationship |
|----------|-----|--------------|
| `explanation.steps` | `memoryTrace.steps` | Parallel, independent |
| `explanation.steps[].state` | `memoryTrace.steps[].stack` | Simple vs full state |
| `explanation.steps[].line` | `memoryTrace.steps[].location` | Line vs full location |
| `explanation.keyInsight` | (none) | Pedagogical only |
| (none) | `stepMapping` | Bridges explanation ↔ memory |

The existing `explanation` remains for human-readable walkthroughs. The new `memoryTrace` provides machine-precise memory state for visualization. The `stepMapping` connects them without coupling.

---

## Next Steps

1. Review this plan and confirm approach
2. Proceed to Phase 2: Update EXPLANATION_GUIDE.md
3. Create 2-3 sample problems with memory traces
4. Build webapp visualization component
