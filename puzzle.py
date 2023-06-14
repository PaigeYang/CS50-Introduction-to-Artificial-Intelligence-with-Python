from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."


# Query from Puzzle 0
Query0_a = And(AKnight, AKnave)

knowledge0 = And(

    # Define true and false for logical condition
    Biconditional(AKnight, Query0_a),
    Biconditional(AKnave, Not(Query0_a)),

    # each character can only blong to Knight or Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave))
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.

# Query from Puzzle 1
Query1_a = And(AKnave, BKnave)

knowledge1 = And(

    # Define true and false for logical condition
    Biconditional(AKnight, Query1_a),
    Biconditional(AKnave, Not(Query1_a)),

    # Each character can only blong to Knight or Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

# Query from Puzzle 2
Query2_a = And(
    Biconditional(AKnight, BKnight),
    Biconditional(AKnave, BKnave)
    )

Query2_b = And(
    Biconditional(AKnight, BKnave),
    Biconditional(AKnave, BKnight)
    )

knowledge2 = And(
    # Define true and false for logical condition
    Biconditional(AKnight, Query2_a),
    Biconditional(AKnave, Not(Query2_a)),
    Biconditional(BKnight, Query2_b),
    Biconditional(BKnave, Not(Query2_b)),


    # Each character can only blong to Knight or Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

# Query from Puzzle 3
Query3_a = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave))
    )

Query3_b = And(
    Implication(Query3_a, BKnave),
    CKnave
    )

Query3_c = AKnight

knowledge3 = And(
    # Define true and false for logical condition
    Biconditional(AKnight, Query3_a),
    Biconditional(AKnave, Not(Query3_a)),
    Biconditional(BKnight, Query3_b),
    Biconditional(BKnave, Not(Query3_b)),
    Biconditional(CKnight, Query3_c),
    Biconditional(CKnave, Not(Query3_c)),

    # Each character can only blong to Knight or Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
    print(knowledge0.formula())


if __name__ == "__main__":
    main()
