# CS 37 Concepts Checklist

Use this checklist to track your understanding of each concept. Mark items as you study them.

---

## 1. Control Structures & Operators

### Logical Operators
- [ ] `&&` operator behavior
- [ ] `||` operator behavior
- [ ] Short-circuit evaluation
- [ ] `!` logical NOT
- [ ] Double negation `!!`
- [ ] Boolean-to-integer conversion

### Conditional Operators
- [ ] `?:` ternary operator
- [ ] Ternary operator right-associativity
- [ ] Nested conditionals

### Selection Statements
- [ ] `if-else` selection
- [ ] `switch` statement
- [ ] `case` labels
- [ ] `break` statement in switch
- [ ] Fall-through behavior
- [ ] `default` case

### Loop Structures
- [ ] `for` loop syntax
- [ ] `while` loop
- [ ] `<` vs `<=` comparison in loops
- [ ] Iteration counting
- [ ] Loop boundaries (off-by-one)
- [ ] Loop termination conditions
- [ ] Truthy/falsy integer values in conditions

### Increment/Decrement Operators
- [ ] Pre-increment `++a`
- [ ] Post-increment `a++`
- [ ] Pre-decrement `--a`
- [ ] Post-decrement `n--` in condition
- [ ] Expression evaluation order with increments
- [ ] Operator side effects

### Operator Precedence
- [ ] General operator precedence rules
- [ ] Division by zero avoidance via short-circuit

---

## 2. Functions, Scope & References

### Variables & Scope
- [ ] Global variables
- [ ] Local variables
- [ ] Variable shadowing
- [ ] Scope resolution operator `::`
- [ ] Block scope `{}`
- [ ] Nested scopes
- [ ] Variable lifetime

### Function Parameters
- [ ] Function parameters basics
- [ ] Pass-by-value (copy)
- [ ] Pass-by-reference `&`
- [ ] Modifying original variables through reference
- [ ] Evaluation order of arguments (unspecified)
- [ ] Side effects in arguments

### References
- [ ] Reference declaration `&`
- [ ] Reference initialization (required)
- [ ] Reference rebinding (not possible)
- [ ] Assignment through reference
- [ ] `const` reference parameter
- [ ] Binding references to literals
- [ ] Binding references to temporaries
- [ ] Read-only access with const reference

### Return Types
- [ ] Returning `&` reference
- [ ] Lvalue return
- [ ] Function call on left-hand side of assignment

### Special Keywords
- [ ] `static` keyword
- [ ] Static local variable
- [ ] Static initialization (once only)
- [ ] Persistence across function calls

### Recursion
- [ ] Recursion basics
- [ ] Reference parameter sharing in recursion
- [ ] Call stack
- [ ] Unwinding behavior

---

## 3. Pointers & Dereferencing

### Pointer Basics
- [ ] Pointer declaration `*`
- [ ] Address-of operator `&`
- [ ] Dereference operator `*`
- [ ] Modifying through pointer

### Advanced Pointers
- [ ] Double pointer `**`
- [ ] Multiple levels of indirection
- [ ] Dereferencing chain
- [ ] Pointer reassignment
- [ ] Pointer vs pointed-to value

### Pointer Arithmetic
- [ ] Pointer arithmetic `ptr + n`
- [ ] Array-pointer equivalence
- [ ] `ptr[n]` bracket notation
- [ ] `*p++` precedence
- [ ] `++*p` vs `*p++`
- [ ] Post-increment on pointer
- [ ] Pre-increment on value

### Pointers as Parameters
- [ ] Pointer passed by value
- [ ] Local pointer copy
- [ ] Pointer reassignment in function scope
- [ ] Passing address `&x`
- [ ] Dereferencing to swap values
- [ ] Modifying original through pointer

### Arrays & Pointers
- [ ] Array decay to pointer
- [ ] `*arr` vs `arr[0]`
- [ ] Commutative property `a[b]` = `*(a+b)` = `b[a]`

### Null Pointers
- [ ] `nullptr`
- [ ] `0` as null pointer
- [ ] Pointer in boolean context
- [ ] Null check pattern

---

## 4. Arrays & Iteration

### Array Basics
- [ ] Array partial initialization
- [ ] Zero-initialization of remaining elements
- [ ] Array size

### Range-Based For Loops
- [ ] Range-based for syntax
- [ ] `for (T x : container)` - loop variable copy
- [ ] Original unchanged with copy
- [ ] `for (T& x : container)` - reference
- [ ] Modifying original with reference
- [ ] `const T&` for read-only
- [ ] Efficient iteration (no copying)

### Loop Control
- [ ] Nested `for` loops
- [ ] `break` exits innermost loop only
- [ ] `continue` (skip iteration)
- [ ] `break` (exit loop)
- [ ] Loop control flow

### Vectors
- [ ] `vector::size()`
- [ ] Size re-evaluated each iteration
- [ ] Modifying container during iteration
- [ ] `vector(n)` constructor
- [ ] `vector{...}` initializer list
- [ ] `()` vs `{}` syntax difference

### Arrays in Functions
- [ ] Array as function parameter
- [ ] Array decay
- [ ] `sizeof` on array vs pointer

### STL Containers
- [ ] `std::array<T,N>`
- [ ] `std::array` pass by value (copies)
- [ ] STL container behavior vs raw array

---

## 5. Classes & Constructors

### Constructors
- [ ] Default constructor
- [ ] Parameterized constructor
- [ ] Implicit conversion `Type x = value`
- [ ] Copy constructor
- [ ] Default parameter values in constructor
- [ ] Single constructor as default + parameterized

### Member Initialization
- [ ] Member initializer list `: member(value)`
- [ ] Initialization order = declaration order
- [ ] Undefined behavior from wrong order

### Construction/Destruction Order
- [ ] Constructor/destructor call order
- [ ] LIFO destruction
- [ ] Member object construction order
- [ ] Declaration order matters

### Composition
- [ ] Composition (has-a relationship)

### Special Keywords
- [ ] `const` object
- [ ] `const` member function
- [ ] Calling restrictions on const objects
- [ ] `explicit` constructor
- [ ] Preventing implicit conversion
- [ ] Direct initialization only
- [ ] `static` member variable

### The `this` Pointer
- [ ] `this` pointer
- [ ] `this->member`
- [ ] `*this` for chaining
- [ ] Method chaining pattern

### Assignment vs Initialization
- [ ] Assignment operator
- [ ] Initialization vs assignment distinction

---

## 6. Operator Overloading & Object Behavior

### Increment/Decrement Operators
- [ ] `operator++()` pre-increment
- [ ] `operator++(int)` post-increment
- [ ] Return type difference (reference vs copy)
- [ ] Returning reference vs copy

### Binary Operators
- [ ] Member `operator+`
- [ ] Left operand must be object
- [ ] `a + b` vs `2 + a` difference
- [ ] Implementing `operator+` using `operator+=`
- [ ] Compound assignment
- [ ] Avoiding code duplication

### Assignment Operator
- [ ] `operator=` overload
- [ ] Right-associativity of assignment
- [ ] Returning `*this` for chaining

### Comparison Operators
- [ ] `operator<`
- [ ] `operator==`
- [ ] Bool return type
- [ ] Bool prints as 1/0

### Stream Operators
- [ ] `friend` function
- [ ] `operator<<` overload
- [ ] Non-member for ostream
- [ ] Returning `ostream&` for chaining

### Subscript Operator
- [ ] `operator[]` overload
- [ ] Const and non-const versions
- [ ] Returning reference for assignment

### Other Operators
- [ ] Unary `operator-`
- [ ] Returns new object (original unchanged)
- [ ] `const` member for operators
- [ ] `operator()` overload
- [ ] Functor pattern
- [ ] Object as callable

---

## 7. Inheritance & Polymorphism

### Inheritance Basics
- [ ] Inheritance concept
- [ ] Base constructor called first
- [ ] Derived constructor second
- [ ] Destructor order reversed from constructor
- [ ] Derived destructor first
- [ ] Base destructor second

### Virtual Functions
- [ ] `virtual` keyword
- [ ] `override` specifier
- [ ] Dynamic binding
- [ ] Runtime polymorphism
- [ ] Function hiding (non-virtual)
- [ ] Static binding
- [ ] Pointer type determines function called (non-virtual)

### Object Slicing
- [ ] Copying derived to base
- [ ] Slicing off derived part
- [ ] Reference/pointer preserves polymorphism

### Virtual Destructors
- [ ] Non-virtual destructor problems
- [ ] Deleting through base pointer
- [ ] Derived destructor not called (without virtual)
- [ ] Memory leak/undefined behavior risk
- [ ] `virtual ~Base()`
- [ ] Proper cleanup through base pointer
- [ ] Correct destruction order

### Calling Base Methods
- [ ] `Base::method()` explicit call
- [ ] Extending base behavior in derived
- [ ] Not recursive

### Abstract Classes
- [ ] `= 0` pure virtual
- [ ] Abstract class
- [ ] Cannot instantiate abstract class
- [ ] Concrete derived class

### Multi-Level Inheritance
- [ ] Multi-level inheritance chain
- [ ] Constructor order top-down
- [ ] Destructor order bottom-up

---

## 8. Dynamic Memory & Rule of 3

### Dynamic Allocation
- [ ] `new` operator
- [ ] Heap allocation
- [ ] `delete` operator
- [ ] `nullptr` after delete
- [ ] `new T[n]` array allocation
- [ ] `delete[]` for arrays
- [ ] Array initializer list with new

### Copy Semantics
- [ ] Default copy constructor
- [ ] Shallow copy (pointer copied)
- [ ] Double delete problem
- [ ] Undefined behavior from shallow copy
- [ ] Custom copy constructor
- [ ] Deep copy (new allocation)
- [ ] Independent heap memory

### Copy Constructor vs Assignment
- [ ] Copy constructor (initialization)
- [ ] Assignment operator (object already exists)
- [ ] `Type x = y` vs `x = y` distinction

### Assignment Operator Implementation
- [ ] `operator=` implementation
- [ ] `this != &rhs` self-assignment check
- [ ] Avoiding delete-before-copy bug

### Rule of 3
- [ ] Rule of 3 concept
- [ ] Destructor requirement
- [ ] Copy constructor requirement
- [ ] Copy assignment requirement
- [ ] All three needed together

### Return by Value
- [ ] Return by value
- [ ] Copy constructor for return
- [ ] Copy elision optimization

### Memory Leaks
- [ ] Memory leak concept
- [ ] Forgetting `delete` before reassignment
- [ ] Proper `reset()` pattern

### Arrays of Objects
- [ ] `new T[n]` object array
- [ ] Constructor order for arrays
- [ ] `delete[]` destructor order (reversed)

---

## Summary Progress

| Category | Total Items | Completed |
|----------|-------------|-----------|
| 1. Control Structures & Operators | 31 | ___ |
| 2. Functions, Scope & References | 32 | ___ |
| 3. Pointers & Dereferencing | 30 | ___ |
| 4. Arrays & Iteration | 26 | ___ |
| 5. Classes & Constructors | 27 | ___ |
| 6. Operator Overloading | 26 | ___ |
| 7. Inheritance & Polymorphism | 27 | ___ |
| 8. Dynamic Memory & Rule of 3 | 27 | ___ |
| **TOTAL** | **226** | ___ |
