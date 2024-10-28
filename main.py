class ChessPiece:
    def __init__(self, color):
        self.color = color

    def is_valid_move(self, start, end, board):
        raise NotImplementedError("Этот метод должен быть реализован в подклассах.")

    def __str__(self):
        return self.symbol.upper() if self.color == 'white' else self.symbol.lower()

class Pawn(ChessPiece):
    symbol = 'P'
    
    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        direction = 1 if self.color == 'white' else -1

        # Пешка может двигаться на одну клетку вперед
        if start_col == end_col and board[end_row][end_col] == '.' and end_row == start_row + direction:
            return True

        # Пешка может двигаться на две клетки вперед с начальной позиции
        if start_col == end_col and board[end_row][end_col] == '.' and end_row == start_row + 2 * direction and ((self.color == 'white' and start_row == 1) or (self.color == 'black' and start_row == 6)):
            return True

        # Пешка может бить фигуру противника по диагонали
        if abs(start_col - end_col) == 1 and end_row == start_row + direction and isinstance(board[end_row][end_col], ChessPiece) and board[end_row][end_col].color != self.color:
            return True

        return False

class Rook(ChessPiece):
    symbol = 'R'
    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:
            step = 1 if start_col < end_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] != '.':
                    return False

        if start_col == end_col:
            step = 1 if start_row < end_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] != '.':
                    return False

        return True

class Knight(ChessPiece):
    symbol = 'N'
    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)

        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Bishop(ChessPiece):
    symbol = 'B'
    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1

        for i in range(1, abs(start_row - end_row)):
            if board[start_row + i * row_step][start_col + i * col_step] != '.':
                return False

        return True

class Queen(ChessPiece):
    symbol = 'Q'
    def is_valid_move(self, start, end, board):
        return Rook(self.color).is_valid_move(start, end, board) or Bishop(self.color).is_valid_move(start, end, board)

class King(ChessPiece):
    symbol = 'K'
    def is_valid_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

class ChessBoard:
    def __init__(self):
        self.board = [['.' for _ in range(9)] for _ in range(9)]
        self.initialize_board()
        self.white_turn = True

    def initialize_board(self):
        # Расставляем белые фигуры
        self.board[0][0] = Rook('white')
        self.board[0][1] = Knight('white')
        self.board[0][2] = Bishop('white')
        self.board[0][3] = Queen('white')
        self.board[0][4] = King('white')
        self.board[0][5] = Bishop('white')
        self.board[0][6] = Knight('white')
        self.board[0][7] = Rook('white')
        self.board[1] = [Pawn('white') for _ in range(9)]

        # Расставляем черные фигуры
        self.board[8][0] = Rook('black')
        self.board[8][1] = Knight('black')
        self.board[8][2] = Bishop('black')
        self.board[8][3] = Queen('black')
        self.board[8][4] = King('black')
        self.board[8][5] = Bishop('black')
        self.board[8][6] = Knight('black')
        self.board[8][7] = Rook('black')
        self.board[7] = [Pawn('black') for _ in range(9)]

    def print_board(self):
        for row in self.board:
            print(' '.join([str(piece) if isinstance(piece, ChessPiece) else '.' for piece in row]))
        print()

    def get_valid_moves(self, color):
        valid_moves = []
        for row in range(9):
            for col in range(9):
                piece = self.board[row][col]
                if isinstance(piece, ChessPiece) and piece.color == color:
                    for r in range(9):
                        for c in range(9):
                            if piece.is_valid_move((row, col), (r, c), self.board):
                                valid_moves.append((self.format_square(row, col), self.format_square(r, c)))
        return valid_moves

    def format_square(self, row, col):
        return f"{chr(col + ord('a'))}{8 - row}"

    def make_move(self, from_square, to_square):
        from_row, from_col = self.parse_square(from_square)
        to_row, to_col = self.parse_square(to_square)

        piece = self.board[from_row][from_col]
        if piece == '.' or not piece.is_valid_move((from_row, from_col), (to_row, to_col), self.board):
            print("Невалидный ход!")
            return False

        # Проверка на шах
        if self.is_in_check(piece.color, (from_row, from_col), (to_row, to_col)):
            print("Ход ставит короля под шах!")
            return False

        # Выполнение хода
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = '.'
        self.white_turn = not self.white_turn
        return True

    def parse_square(self, square):
        row = 8 - int(square[1])
        col = ord(square[0]) - ord('a')
        return row, col

    def is_in_check(self, color, from_pos, to_pos):
        # Временное выполнение хода для проверки шаха
        piece = self.board[from_pos[0]][from_pos[1]]
        target_piece = self.board[to_pos[0]][to_pos[1]]
        
        self.board[to_pos[0]][to_pos[1]] = piece
        self.board[from_pos[0]][from_pos[1]] = '.'

        king_pos = self.find_king(color)
        is_check = self.is_square_attacked(king_pos, 'black' if color == 'white' else 'white')

        # Возврат доски в исходное состояние
        self.board[from_pos[0]][from_pos[1]] = piece
        self.board[to_pos[0]][to_pos[1]] = target_piece

        return is_check

    def find_king(self, color):
        for row in range(9):
            for col in range(9):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_square_attacked(self, square, attacker_color):
        for row in range(9):
            for col in range(9):
                piece = self.board[row][col]
                if isinstance(piece, ChessPiece) and piece.color == attacker_color:
                    if piece.is_valid_move((row, col), square, self.board):
                        return True
        return False

    def is_checkmate(self):
        king_pos = self.find_king('black' if self.white_turn else 'white')
        if not king_pos or not self.is_square_attacked(king_pos, 'black' if self.white_turn else 'white'):
            return False

        # Проверка всех возможных ходов для короля
        for row in range(9):
            for col in range(9):
                if isinstance(self.board[row][col], King) and self.board[row][col].color == ('black' if self.white_turn else 'white'):
                    for r in range(max(0, row - 1), min(9, row + 2)):
                        for c in range(max(0, col - 1), min(9, col + 2)):
                            if (r, c) != (row, col):
                                original_piece = self.board[r][c]
                                self.board[r][c] = self.board[row][col]
                                self.board[row][col] = '.'
                                if not self.is_square_attacked((r, c), 'black' if self.white_turn else 'white'):
                                    self.board[row][col] = self.board[r][c]
                                    self.board[r][c] = original_piece
                                    return False
                                self.board[row][col] = self.board[r][c]
                                self.board[r][c] = original_piece
        return True

def main():
    board = ChessBoard()
    board.print_board()

    while True:
        turn = "Белые" if board.white_turn else "Черные"
        print(f"Ход {turn}. Введите ваш ход (например, a8 a7) или введите 'exit' для выхода: ")
        move = input().strip()
        if move.lower() == "exit":
            print("Игра завершена.")
            break
        try:
            from_square, to_square = move.split()
            if board.make_move(from_square, to_square):
                board.print_board()

                # Проверка на мат
                if board.is_checkmate():
                    print(f"{turn} в шахе! Игра завершена.")
                    break
            else:
                valid_moves = board.get_valid_moves('white' if board.white_turn else 'black')
                print("Невалидный ход! Возможные ходы:")
                for move in valid_moves:
                    print(f"{move[0]} {move[1]}")

        except ValueError:
            print("Неверный ввод! Пожалуйста, введите ход в формате 'a8 a7'.")

if __name__ == "__main__":
    main()
