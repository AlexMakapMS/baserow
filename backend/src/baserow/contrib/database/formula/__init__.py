"""
The database formula module is a compiler for the Baserow Formula language which
looks like:

```baserow_formula
CONCAT(UPPER(LOWER('test')), "test\"", 'test\'") -- evaluates to `testtest"test'`
```

It consists of 3 sub modules:
    1. parser: responsible for taking a raw Baserow Formula string input,
    syntax checking it, parsing it and converting it to the internal Baserow
    Formula abstract syntax tree representation.
    2. ast: the definition of the internal Baserow Formula abstract syntax tree (AST).
    Essentially a graph which can be used to represent a Baserow Formula neatly.
    3. expression_generator: takes a Baserow Formula AST and generates a Django
    Expression object which calculates the result of executing the formula.

The abstract syntax tree abstraction is used to decouple the specifics of the antlr4
parser from the specifics of turning a Baserow formula into generated SQL. It lets us
separate the various concerns cleanly but also provides future extensibility. For
example we could create another parser module which takes an another formula language
different from the Baserow Formula language, but generates a Baserow Formula AST
allowing use of that language in Baserow easily.

The grammar definitions for the Baserow Formula language may be found in the
root folder formula_lang along with the scripts to generate the antlr4 parser found in
baserow.contrib.formula.parser.generated .
"""
