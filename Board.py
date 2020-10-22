"""
The `Board` class represents an Othello board. Since `Board` objects need to contain more metadata 
than just the state of the board, like the methods needed to validate and make moves, the actual 
state of the game board is an instance variable called `state`.

The `state` variable is an 8 x 8 2d list where sublists represent ranks (rows) and elements in sublists
are Tiles that optionally contain a `GamePiece` (if no `GamePiece` is in the Tile, the type of `tile.gamePiece`
will be None.

In the board state below, every rank (row) and file (column) is labeled with two numbers - the first is the 
letter or number that would conventionally be used to refer to that line of squares. Most games using a chesslike
board of squares use Algebraic Notation to transcribe games. You can get the gist here: 
https://en.wikipedia.org/wiki/Algebraic_notation_(chess)). The second numbers represent the index locations
in the `Board`'s `state` that would be used to access the `GamePiece` object stored there. Recall how double
indexing works: ((1, 2), (3, 4))[0][1] = (1, 2)[1] = 2

Here's a blank board state (empty Tiles):

        ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
    8/0 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    7/1 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    6/2 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    5/3 │      │      │      │      │      │      │      │ "h5" │  <—— Normally called h5 when speaking and playing over-the-board
        │      │      │      │      │      │      │      │[3][7]│  <—— Access the `GamePiece` here with `b.state[3][7]` for a `Board b`
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    4/4 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    3/5 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    2/6 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        ├──────┼──────┼──────┼──────┼──────┼──────┼──────┼──────┤
    1/7 │      │      │      │      │      │      │      │      │
        │      │      │      │      │      │      │      │      │
        └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
           a/0    b/1    c/2    d/3    e/4    f/5    g/6    h/7

Fields
------
    Constant Class Vars
    -------------------
        B_CHAR : Character to print to terminal in board spaces containing black `GamePieces`
        W_CHAR : Character to print to terminal in board spaces containing white `GamePieces`
        EMPTY_CHAR : Character to print to terminal in board spaces containing no `GamePiece`
        BLANK_STATE : The board state containing 
        STARTING_STATE
    Instance Vars
    -------------
        state : Current state of the board as a 2d list of `Tile` objects, each of which
                optionally contains a `GamePiece` object (see `Tile` class documentation)

"""

from GUIElement import GUIElement


class Board(GUIElement):
    
    ''' ========== Constant Class Variables ========== '''

    B_CHAR = '○'
    W_CHAR = '●'
    EMPTY_CHAR = ' '
    BLANK_STATE = [[None for file in range(8)] for rank in range(8)]
    STARTING_STATE = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, 'w', 'b', None, None, None],
        [None, None, None, 'b', 'w', None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]


    ''' ========== Regular Class Variables ========== '''


    ''' ========== Constructor ========== '''
    
    def __init__(self, state=BLANK_STATE):
        self.state = state


    ''' ========== Magic Methods ========== '''

    def __str__(self):
        # Quick check to make sure board is correct dimensions and
        # only contains 'b', 'w', or None in every square
        # (assert statements throw an AssertionError if given expression is False)
        assert Board.is_valid_state(self.state)

        # Build board string
        output_string = '┌───┬───┬───┬───┬───┬───┬───┬───┐\n'

        for index, row in enumerate(self.state):
            for col in row:
                if col is None:
                    char_to_fill = Board.EMPTY_CHAR
                elif col.lower() == 'b':
                    char_to_fill = Board.B_CHAR
                elif col.lower() == 'w':
                    char_to_fill = Board.W_CHAR
                else:
                    # Should never reach here - will be helpful for debugging later -JH
                    raise Exception('custom error: Bad formatting of Board.state')

                output_string += f'│ {char_to_fill} '

            if index != len(self.state) - 1:
                # Not the last row, use ├───┼...
                output_string += '│\n├───┼───┼───┼───┼───┼───┼───┼───┤\n'
            else:
                # Last row, use └───┴...
                output_string += '│\n└───┴───┴───┴───┴───┴───┴───┴───┘\n'

        return output_string


    ''' ========== Static Methods ========== '''
    
    @staticmethod
    def is_valid_state(state):
        """
            Return true iff given state is an 8x8 2d list with sublists containing 
            only 'b', 'w', or None.
        """
        return all([
            type(state) == list,
            len(state) == 8,
            all([type(row) == list for row in state]),
            all([len(row) == 8 for row in state]),
            all([all([col in ['b', 'w', None] for col in row]) for row in state]),
        ])


    ''' ========== Instance Methods ========== '''

    def set_state(self, new_state):
        """ If new_state is valid, set state to new_state. """
        if Board.is_valid_state(new_state):
            self.state = new_state
        else:
            # Should never reach here - will be helpful for debugging later -JH
            raise ValueError('custom error: Invalid new_state given to Board.set_state()')

    def draw(self):
        # TODO
        pass