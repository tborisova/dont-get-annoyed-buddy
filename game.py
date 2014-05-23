class Game:
    IN_PROGRESS = 0

    def __init__(self, players ,board=None):
        self._board = board or [0]*57
        self._player = players[0]
        self._players = players
        self._current_player = 0

    def play(self, pawn, moves):
        old_position = self._player.get_pawn_position(pawn)
        position = self._player.move_pawn(pawn, moves)
        self.update_position_on_board(position, pawn, old_position)
        self.change_player()

    def at(self, position):
        return self._board[position]

    def outcome(self):
        for player in self._players:
            if player.all_pawns_are_in_house():
                return player.color
        return Game.IN_PROGRESS

    def update_position_on_board(self, position, pawn, old_position):
        if self._board[position] and self._board[position] != self._player.color + str(pawn):
            player_color = self._board[position][0]
            player = [player for player in self._players if player.color == player_color][0]
            player.remove_pawn_from_position(position)
        self._board[position] = self._player.color + str(pawn)
        if old_position != -1:
            self._board[old_position] = 0

    def change_player(self):
        if self._current_player == 3:
            self._player = self._players[0]
            self._current_player = 0
        else: 
            self._player = self._players[self._current_player + 1]
            self._current_player += 1   