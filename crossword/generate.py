import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword

        # self.domains = {Variable1: (word1, word2, word3...), Variable2: (word1, word2, word3...), Variable3: (word1, word2, word3...), ...}
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Remove the length of words unequal that of the vatiable

        for var in self.domains:
            for word in self.domains[var].copy():
                if var.length != len(word):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        reversed = False

        # if x and y are overlap
        if self.crossword.overlaps[x ,y] != None:

            # ith character of x’s value and jth character of y’s value.
            i = self.crossword.overlaps[x ,y][0]
            j = self.crossword.overlaps[x ,y][1]
            characters = []

            # collect all possible characters from y
            for word in self.domains[y]:
                characters.append(word[j])

            # remove words in X that can't find corresponding value in y
            for word in self.domains[x].copy():
                if word[i] in characters:
                    continue
                else:
                    self.domains[x].remove(word)
                    reversed = True
        return reversed

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # Create queue that allow overlap words in it
        # queue = [(Variable1, Variable3), (Variable1, Variable4), ....]
        queue = []

        for var in self.crossword.overlaps:
            if self.crossword.overlaps[var]:
                queue.append(var)

        # Make all the values in each variable’s domain satisfy that variable’s binary constraints
        while queue:

            # Get the first variable
            x = queue[0][0]
            y = queue[0][1]
            queue.remove((x ,y))
            if self.revise(x, y):

                # if x domain is not 0
                if not self.domains[x]:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    queue.append((neighbor ,x))

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        #EX. assigment = {Variable1: word1, Variable2: word2, Variable3: word3, ...}

        # Check if variables in domain exist in assignment
        if len(self.domains) == len(assignment):
            for key in assignment:
                # Return False if there is variable that is no value.
                if not assignment[key]:
                    return False
            return True

        # Return False if the number of variables in domain unequal to the number of variables in assignment
        else:
            return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Check if there is the same value in the assignment
        for value in assignment.values():
            count = list(assignment.values()).count(value)
            if count != 1:
                return False

        # Check if every value is the correct length
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        # check there are no conflicts between neighboring variables
        for var in assignment:
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i = self.crossword.overlaps[var, neighbor][0]
                    j = self.crossword.overlaps[var, neighbor][1]

                    if assignment[var][i] != assignment[neighbor][j]:
                        return False


        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Find all neighbors
        neighbors = self.crossword.neighbors(var)

        #add all values in the domain's list
        domain = []
        for value in self.domains[var]:
            domain.append(value)

        #count the number of neighbor's values kept in that variable's value
        counts = { value: 0 for value in domain}

        for variable in neighbors:
            if variable in assignment:
                continue
            else:
                i = self.crossword.overlaps[var, variable][0]
                j = self.crossword.overlaps[var, variable][1]

                # for every value in var, how namy values can keepin other keep in other variables?
                for value in counts:
                    for value2 in self.domains[variable]:
                        if value[i] == value2[j]:
                            counts[value] += 1

        # sort in descending order
        return sorted(domain, key=counts.__getitem__, reverse=True)


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Collect all unassigned values
        unassigned = []

        for var in self.domains:
            if var in assignment:
                continue
            else:
                unassigned.append((var, len(self.domains[var])))

        # sorted by the minimum number of remaining values in its domain
        unassigned = sorted(unassigned, key=lambda value : value[1])

        # collect degree value
        degrees = []

        for i in unassigned:
            # if the minimum number of remaining values is the same
            if unassigned[0][1] == i[1]:
                num_degree = len(self.crossword.neighbors(i[0]))
                degrees.append((i[0], i[1], num_degree))
            else:
                continue

        # If there is a tie in remaining values, choose the variable with the highest degree.
        degrees = sorted(degrees, key=lambda value : value[2], reverse=True)

        return degrees[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if self.assignment_complete(assignment):
            return assignment
        else:
            var = self.select_unassigned_variable(assignment)

            for value in self.order_domain_values(var, assignment):
                if value not in assignment.values():
                    assignment[var] = value

                    if self.consistent(assignment):
                        result = self.backtrack(assignment)

                        if result:
                            return result
                        else:
                            del assignment[var]
                    else:
                        del assignment[var]

            return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
