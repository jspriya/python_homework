class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

class Board:
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]
        self.turn = "X"

    def __str__(self):
        lines = []
        lines.append(f" {self.board_array[0][0]} | {self.board_array[0][1]} | {self.board_array[0][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[1][0]} | {self.board_array[1][1]} | {self.board_array[1][2]} \n")
        lines.append("-----------\n")
        lines.append(f" {self.board_array[2][0]} | {self.board_array[2][1]} | {self.board_array[2][2]} \n")
        return "".join(lines)
    
# print(Board())
    
    def move(self, move_string):
        if move_string not in Board.valid_moves:
            raise TictactoeException("That's not a valid move.")

        move_index = Board.valid_moves.index(move_string)
        row = move_index // 3
        column = move_index % 3

        if self.board_array[row][column] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][column] = self.turn

        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def whats_next(self):
        # Check for full board (cat's game)
        cat = True
        for i in range(3):
            for j in range(3):
                if self.board_array[i][j] == " ":
                    cat = False
                    break
            if not cat:
                break
        
        # Check rows
        for i in range(3):
            if self.board_array[i][0] != " " and \
               self.board_array[i][0] == self.board_array[i][1] == self.board_array[i][2]:
                winner = self.board_array[i][0]
                return (True, f"{winner} wins!")
            
        # Check columns
        for i in range(3):
            if self.board_array[0][i] != " " and \
               self.board_array[0][i] == self.board_array[1][i] == self.board_array[2][i]:
                winner = self.board_array[0][i]
                return (True, f"{winner} wins!")
            
        if self.board_array[1][1] != " ":
            if self.board_array[0][0] == self.board_array[1][1] == self.board_array[2][2] or \
               self.board_array[0][2] == self.board_array[1][1] == self.board_array[2][0]:
                winner = self.board_array[1][1]
                return (True, f"{winner} wins!")

        if cat:
            return (True, "Cat's Game.")

        return (False, f"{self.turn}'s turn.")
    
if __name__ == "__main__":
    board = Board()

    while True:
        print(board)

        game_over, message = board.whats_next()
        print(message)

        if game_over:
            break

        move = input("Enter your move: ").lower()

        try:
            board.move(move)
        except TictactoeException as e:
            print(e)
    
            

