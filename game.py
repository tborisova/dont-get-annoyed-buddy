import PodSixNet


class Game:
    IN_PROGRESS = 0

    def __init__(self, players, board=None):
        self._board = board or [0]*57
        self._players = players
        self._player_index = 0

    @property
    def current_player(self):
        return self._players[self._player_index]

    def play(self, pawn, moves):
        old_position = self.current_player.get_pawn_position(pawn)
        position = self.current_player.move_pawn(pawn, moves)
        self.update_position_on_board(position, pawn, old_position)
        self.change_player(moves)

    def at(self, position):
        return self._board[position]

    def outcome(self):
        for player in self._players:
            if player.all_pawns_are_in_house():
                return player.color
        return Game.IN_PROGRESS

    def update_position_on_board(self, position, pawn, old_position):
        board_pos = self.at(position)
        if board_pos and board_pos.count(self.current_player.color) == 0:
            player_color = self._board[position][0]
            player = next(player for player in self._players
                          if player.color == player_color)
            player.remove_pawn_from_position(position)
        self._board[position] = self.current_player.color + str(pawn)
        if old_position != -1:
            self._board[old_position] = 0

    def change_player(self, dice=None):
        if dice != 6:
            if self._player_index == 3:
                self._player_index = 0
            else:
                self._player_index += 1
