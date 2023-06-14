import itertools
import random
import secrets


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # if the number of cells equals to count, then all cells are mines
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # if the number of cells equals to count, then no cells are mines
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # Check if the cell in the sentence. If yes, then remove it from the sentence. Also, minus 1 for count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check if the cell in the sentence. If yes, then remove it from the sentence
        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        #check if neighbors are knowne
        def check(neighbors, count):

            for neighbor in neighbors.copy():
                if neighbor in self.mines:
                    count -= 1
                    neighbors.remove(neighbor)

                elif neighbor in self.safes:
                    neighbors.remove(neighbor)
            return count

        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe and any sentences that contain the cell
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base

        # if the cell on the top left-hand side
        if cell == (0,0):
            neighbors = {(0,1), (1,0), (1,1)}

        # if the cell is om the top right-hand side
        elif cell == (0,7):
            neighbors = {(0,6), (1,6), (1,7)}

        # if the cell is om the bottom left
        elif cell == (7,0):
            neighbors = {(6,0), (6,1), (7,1)}

        # if the cell is on the bottom right
        elif cell == (7,7):
            neighbors = {(6,6), (6,7), (7,6)}

        # if the cell is on the top side except for the corner
        elif cell[0] == 0 and cell[1] in range (1, 7):
            neighbors = {(0,cell[1]-1), (0,cell[1]+1), (1,cell[1]-1), (1,cell[1]+1), (1,cell[1])}

        # if the cell is on the bottom side except for the corner
        elif cell[0] == 7 and cell[1] in range (1, 7):
            neighbors = {(7,cell[1]-1), (7,cell[1]+1), (6,cell[1]-1), (6,cell[1]+1), (6,cell[1])}

        # if the cell is on the left side except for the corner
        elif cell[0] in range (1, 7) and cell[1] == 0:
            neighbors = {(cell[0]-1, 0), (cell[0]+1, 0), (cell[0]+1, 1), (cell[0]-1, 1), (cell[0], 1)}

        # if the cell is on the right side except for the corner
        elif cell[0] in range (1, 7) and cell[1] == 7:
            neighbors = {(cell[0]-1, 7), (cell[0]+1, 7), (cell[0]+1, 6), (cell[0]-1, 6), (cell[0], 6)}

        else:
            neighbors = {(cell[0], cell[1]+1), (cell[0], cell[1]-1), (cell[0]+1, cell[1]),
                         (cell[0]-1, cell[1]), (cell[0]-1, cell[1]-1), (cell[0]-1, cell[1]+1),
                         (cell[0]+1, cell[1]-1), (cell[0]+1, cell[1]+1)}

        # if neighbor alreadt existed, we should skip it, then update new neighbors and new counts
        count = check(neighbors, count)

        # if there is an neighbor that is undetermined, then add it in the knowledge
        if neighbors:
            new = Sentence(neighbors, count)

            # check if we can infer if they are mines or not mines
            if new.known_safes():
                for cell in neighbors:
                    self.mark_safe(cell)
            elif new.known_mines():
                for cell in neighbors:
                    self.mark_mine(cell)
            else:
                for sentence in self.knowledge:

                    # check if both the cells exist
                    if new.cells and sentence.cells:

                        # check the new is the subset of the sentence
                        if new.cells.issubset(sentence.cells):
                            for cell in new.cells:
                                sentence.cells.remove(cell)
                            sentence.count = sentence.count - new.count

                            if sentence.known_safes():
                                for cell in sentence.cells.copy():
                                    self.mark_safe(cell)
                            elif sentence.known_mines():
                                for cell in sentence.cells.copy():
                                    self.mark_mine(cell)

                        # check the sentence is the subset of the new
                        elif sentence.cells.issubset(new.cells):
                            for cell in sentence.cells:
                                new.cells.remove(cell)
                            new.count = new.count - sentence.count

                            if new.known_safes():
                                for cell in new.cells:
                                    self.mark_safe(cell)
                                break

                            elif new.known_mines():
                                for cell in new.cells:
                                    self.mark_mine(cell)
                                break

                # update the ultimate new sentence
                if new.cells:
                    self.knowledge.append(new)

            for sentence in self.knowledge:
                if sentence.known_safes():
                    for cell in sentence.cells.copy():
                        self.mark_safe(cell)
                elif sentence.known_mines():
                    for cell in sentence.cells.copy():
                        self.mark_mine(cell)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        cells = []

        for i in range(8):
            for j in range(8):
                cells.append((i, j))

        for move in self.moves_made:
            cells.remove(move)

        for move in self.mines:
            if move in cells:
                cells.remove(move)

        if cells:
            return secrets.choice(cells)

        return None