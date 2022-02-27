from logic import *

"""
Knights/Knaves puzzle to show Darin can implement logical statements
into a python interpreter to let the AI solve a problem. 

Logic is processed via model checking in logic.py.
"""

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
statement = And(AKnave, AKnight)
knowledge0 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),  # A is a Knight or a Knave, but not both.
    Implication(AKnave, Not(statement)),  # If A is a knave, don't trust what they say.
    Implication(AKnight, statement)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
a_statement = And(AKnave, AKnight)
knowledge1 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),  # A/B are Knights XOR Knaves
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnave, Not(a_statement)),  # If A is a knave, don't trust what they say.
    Implication(AKnight, a_statement)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
a_statement = Or(And(AKnight, BKnight), And(AKnave, BKnave))
b_statement = And(Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave)))
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),  # A/B are Knights XOR Knaves
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    Implication(AKnave, Not(a_statement)),  # If A is a knave, don't trust what they say.
    Implication(AKnight, a_statement),
    Implication(BKnave, Not(b_statement)),  # If B is a knave, don't trust what they say.
    Implication(BKnight, b_statement)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
a_statement = Or(AKnight, AKnave)
b_statement = And(CKnave, Implication(a_statement, AKnave))
c_statement = AKnight
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),  # A/B/C are Knights XOR Knaves
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    Implication(AKnave, Not(a_statement)),  # If A is a knave, don't trust what they say.
    Implication(AKnight, a_statement),

    Implication(BKnave, Not(b_statement)),  # If B is a knave, don't trust what they say.
    Implication(BKnight, b_statement),

    Implication(CKnave, Not(c_statement)),  # If B is a knave, don't trust what they say.
    Implication(CKnight, c_statement)
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


if __name__ == "__main__":
    main()
