import itertools
import random

"""
minesweeper.py creates an AI to assist human minesweeper play.
The AI will automatically pick known safe moves, or pick random
ones when unable to do so. When the player "flags" all 
possible mines with a right click and the AI can no longer
make any moves, the game will be won.

This is part of an assignment in Harvard's AI50 course. 

@Author: Darin Kishore, 2/27/22
"""


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
        @ Author: Darin Kishore
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        @ Author: Darin Kishore
        """
        if self.count == 0:  # If count of possible mines is zero, return current sentence.
            return self.cells
        else:  # Else, we know no other cells can be guaranteed safe.
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        @ Author: Darin Kishore
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        @ Author: Darin Kishore
        """
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
        if self.knowledge:
            for sentence in self.knowledge:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        if self.knowledge:
            for sentence in self.knowledge:
                sentence.mark_safe(cell)

    def is_safe(self, cell):
        return cell in self.safes

    def is_mine(self, cell):
        return cell in self.mines

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            3.5) update and refactor values of sentences (see: step 5)
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        @ Author: Darin Kishore
        """
        # 1) Mark the cell as a move made.
        self.moves_made.add(cell)

        # 2) mark cell safe
        self.mark_safe(cell)

        # 3) Add new sentence based on value of cell and count.
        neighbors = self.mystery_neighbors(cell)
        if neighbors:
            sent = Sentence(neighbors, count)
            self.knowledge.append(sent)

        # 3.5) after any change to knowledge base,
        # we should see if any new inferences can be made
        self.trim_the_fat()

        # 4) mark safes/mines
        for sentence in self.knowledge:
            if len(sentence.cells) == sentence.count:  # mark mines
                while sentence.cells:
                    i = sentence.cells.pop()
                    self.mines.add(i)
                    sentence.mark_mine(i)
                    sentence.count -= 1
            elif sentence.count == 0:  # mark safes
                while sentence.cells:
                    i = sentence.cells.pop()
                    self.safes.add(i)
                    sentence.mark_safe(i)
            if sentence.count == 0:
                self.knowledge.remove(sentence)

        # 5) after change to knowledge, see if any new inferences can be made
        self.trim_the_fat()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        @ Author: Darin Kishore
        """
        for safe_cell in self.safes:  # This checks every safe cell every time we want to make a safe move.
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        @ Author: Darin Kishore
        """
        # if there is nothing to choose that would not blow you up and you haven't
        # already chosen, return None.
        count = 0
        while count < self.height * self.width:
            cell = random.randint(0, self.height - 1), random.randint(0, self.width - 1)
            if cell not in self.mines and cell not in self.moves_made:
                return cell
            count += 1
        return None
    # Helper functions below

    # @ Author: Darin Kishore
    def trim_the_fat(self):
        if len(self.knowledge) >= 2:
            # the_fat = every combination of sentences we know
            the_fat = list(itertools.combinations(self.knowledge, 2))
            for sentence_pair in the_fat:  # sent_pair is tuple (a,b)
                refactored_sentence = self.refactor(sentence_pair[0], sentence_pair[1])
                if refactored_sentence is not None and refactored_sentence.cells:
                    # self.knowledge.remove(sentence_pair[0])  # TODO: double check that we should not remove
                    # self.knowledge.remove(sentence_pair[1])
                    self.knowledge.append(refactored_sentence)

    def refactor(self, sentence_1: Sentence, sentence_2: Sentence):
        """
        @ Author: Darin Kishore
        combines two sentences to make a shorter sentence.
        :rtype: Sentence
        """
        new_sent = None
        if sentence_1.cells < sentence_2.cells:  # sent_1 is subset
            new_sent = Sentence(sentence_2.cells - sentence_1.cells,
                                sentence_2.count - sentence_1.count)
        elif sentence_1.cells > sentence_2.cells:  # sent_2 is subset
            new_sent = Sentence(sentence_2.cells - sentence_1.cells,
                                sentence_2.count - sentence_1.count)
        return new_sent

    # @ Author: Darin Kishore
    def mystery_neighbors(self, cell):
        """
        returns neighbors not known to be safe or mines.
        :param cell:
        :return: set() of neighboring cells
        """
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                temp_cell = (i, j)
                if 0 <= i < self.height and 0 <= j < self.width:
                    if not (self.is_safe(temp_cell) or self.is_mine(temp_cell)):
                        neighbors.add(temp_cell)
        neighbors.discard(cell)
        return neighbors
