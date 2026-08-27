import sys
import random

COLOR_WHITE = 0
COLOR_BLACK = 1
PIECE_EMPTY = 0
PIECE_PAWN = 1
PIECE_KNIGHT = 2
PIECE_BISHOP = 3
PIECE_ROOK = 4
PIECE_QUEEN = 5
PIECE_KING = 6

PST_PAWN = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
PST_KNIGHT = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]
PST_BISHOP = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]
PST_ROOK = [
      0,  0,  0,  0,  0,  0,  0,  0,
      5, 10, 10, 10, 10, 10, 10,  5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      0,  0,  0,  5,  5,  0,  0,  0
]
PST_QUEEN = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
PST_KING_MID = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20
]
PST_KING_END = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

PIECE_VALUES = {PIECE_EMPTY: 0, PIECE_PAWN: 100, PIECE_KNIGHT: 320, PIECE_BISHOP: 330, PIECE_ROOK: 500, PIECE_QUEEN: 900, PIECE_KING: 20000}
ZOBRIST_PIECES = [[[random.getrandbits(64) for _ in range(7)] for _ in range(2)] for _ in range(64)]
ZOBRIST_COLOR = random.getrandbits(64)
ZOBRIST_CASTLE = [random.getrandbits(64) for _ in range(16)]
ZOBRIST_EP = [random.getrandbits(64) for _ in range(64)]
ZOBRIST_NO_EP = random.getrandbits(64)

FLAG_EXACT = 0
FLAG_ALPHA = 1
FLAG_BETA = 2

class Board:
    def __init__(self):
        self.pieces = [PIECE_EMPTY] * 64
        self.colors = [None] * 64
        self.turn = COLOR_WHITE
        self.castle_rights = 15
        self.ep_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.zobrist_key = 0
        self.history = []
        self.reset()

    def reset(self):
        self.pieces = [
            PIECE_ROOK, PIECE_KNIGHT, PIECE_BISHOP, PIECE_QUEEN, PIECE_KING, PIECE_BISHOP, PIECE_KNIGHT, PIECE_ROOK,
            PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN,
            PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY,
            PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY,
            PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY,
            PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY, PIECE_EMPTY,
            PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN, PIECE_PAWN,
            PIECE_ROOK, PIECE_KNIGHT, PIECE_BISHOP, PIECE_QUEEN, PIECE_KING, PIECE_BISHOP, PIECE_KNIGHT, PIECE_ROOK
        ]
        self.colors = [
            1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.turn = COLOR_WHITE
        self.castle_rights = 15
        self.ep_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.zobrist_key = self.compute_zobrist()
        self.history = [self.zobrist_key]

    def compute_zobrist(self):
        key = 0
        for sq in range(64):
            p = self.pieces[sq]
            if p != PIECE_EMPTY:
                key ^= ZOBRIST_PIECES[sq][self.colors[sq]][p]
        if self.turn == COLOR_BLACK:
            key ^= ZOBRIST_COLOR
        key ^= ZOBRIST_CASTLE[self.castle_rights]
        if self.ep_square is not None:
            key ^= ZOBRIST_EP[self.ep_square]
        else:
            key ^= ZOBRIST_NO_EP
        return key

    def set_fen(self, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        sq = 0
        self.pieces = [PIECE_EMPTY] * 64
        self.colors = [None] * 64
        for row in rows:
            for char in row:
                if char.isdigit():
                    sq += int(char)
                else:
                    color = COLOR_BLACK if char.islower() else COLOR_WHITE
                    p_type = {"p": 1, "n": 2, "b": 3, "r": 4, "q": 5, "k": 6}[char.lower()]
                    self.pieces[sq] = p_type
                    self.colors[sq] = color
                    sq += 1
        self.turn = COLOR_WHITE if parts[1] == 'w' else COLOR_BLACK
        self.castle_rights = 0
        if parts[2] != '-':
            if 'K' in parts[2]: self.castle_rights |= 1
            if 'Q' in parts[2]: self.castle_rights |= 2
            if 'k' in parts[2]: self.castle_rights |= 4
            if 'q' in parts[2]: self.castle_rights |= 8
        self.ep_square = None if parts[3] == '-' else (8 - int(parts[3][1])) * 8 + (ord(parts[3][0]) - 97)
        self.halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
        self.fullmove_number = int(parts[5]) if len(parts) > 5 else 1
        self.zobrist_key = self.compute_zobrist()
        self.history = [self.zobrist_key]

    def generate_moves(self, pseudo=False):
        moves = []
        us = self.turn
        them = 1 - us
        for sq in range(64):
            if self.colors[sq] != us:
                continue
            p = self.pieces[sq]
            r, c = divmod(sq, 8)
            if p == PIECE_PAWN:
                dir_m = -8 if us == COLOR_WHITE else 8
                start_r = 6 if us == COLOR_WHITE else 1
                promo_r = 0 if us == COLOR_WHITE else 7
                f_sq = sq + dir_m
                if 0 <= f_sq < 64 and self.pieces[f_sq] == PIECE_EMPTY:
                    if divmod(f_sq, 8)[0] == promo_r:
                        for pr in [PIECE_QUEEN, PIECE_ROOK, PIECE_BISHOP, PIECE_KNIGHT]:
                            moves.append((sq, f_sq, pr))
                    else:
                        moves.append((sq, f_sq, None))
                        f2_sq = f_sq + dir_m
                        if r == start_r and self.pieces[f2_sq] == PIECE_EMPTY:
                            moves.append((sq, f2_sq, None))
                for dc in [-1, 1]:
                    nc = c + dc
                    if 0 <= nc < 8:
                        t_sq = sq + dir_m + dc
                        if 0 <= t_sq < 64:
                            if self.colors[t_sq] == them:
                                if divmod(t_sq, 8)[0] == promo_r:
                                    for pr in [PIECE_QUEEN, PIECE_ROOK, PIECE_BISHOP, PIECE_KNIGHT]:
                                        moves.append((sq, t_sq, pr))
                                else:
                                    moves.append((sq, t_sq, None))
                            elif t_sq == self.ep_square:
                                moves.append((sq, t_sq, None))
            elif p == PIECE_KNIGHT:
                offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
                for o in offsets:
                    t_sq = sq + o
                    if 0 <= t_sq < 64 and self.colors[t_sq] != us:
                        if abs((t_sq % 8) - c) <= 2:
                            moves.append((sq, t_sq, None))
            elif p in [PIECE_BISHOP, PIECE_ROOK, PIECE_QUEEN]:
                dirs = []
                if p in [PIECE_BISHOP, PIECE_QUEEN]:
                    dirs.extend([-9, -7, 7, 9])
                if p in [PIECE_ROOK, PIECE_QUEEN]:
                    dirs.extend([-8, -1, 1, 8])
                for d in dirs:
                    curr = sq
                    while True:
                        cr, cc = divmod(curr, 8)
                        curr += d
                        if not (0 <= curr < 64): break
                        nr, nc = divmod(curr, 8)
                        if abs(cr - nr) > 1 or abs(cc - nc) > 1: break
                        if self.colors[curr] == us: break
                        moves.append((sq, curr, None))
                        if self.colors[curr] == them: break
            elif p == PIECE_KING:
                dirs = [-9, -8, -7, -1, 1, 7, 8, 9]
                for d in dirs:
                    t_sq = sq + d
                    if 0 <= t_sq < 64 and self.colors[t_sq] != us:
                        if abs((t_sq // 8) - r) <= 1 and abs((t_sq % 8) - c) <= 1:
                            moves.append((sq, t_sq, None))
                if us == COLOR_WHITE:
                    if (self.castle_rights & 1) and self.pieces[61] == PIECE_EMPTY and self.pieces[62] == PIECE_EMPTY:
                        if not pseudo and not self.is_square_attacked(60, them) and not self.is_square_attacked(61, them) and not self.is_square_attacked(62, them):
                            moves.append((60, 62, None))
                    if (self.castle_rights & 2) and self.pieces[59] == PIECE_EMPTY and self.pieces[58] == PIECE_EMPTY and self.pieces[57] == PIECE_EMPTY:
                        if not pseudo and not self.is_square_attacked(60, them) and not self.is_square_attacked(59, them) and not self.is_square_attacked(58, them):
                            moves.append((60, 58, None))
                else:
                    if (self.castle_rights & 4) and self.pieces[5] == PIECE_EMPTY and self.pieces[6] == PIECE_EMPTY:
                        if not pseudo and not self.is_square_attacked(4, them) and not self.is_square_attacked(5, them) and not self.is_square_attacked(6, them):
                            moves.append((4, 6, None))
                    if (self.castle_rights & 8) and self.pieces[3] == PIECE_EMPTY and self.pieces[2] == PIECE_EMPTY and self.pieces[1] == PIECE_EMPTY:
                        if not pseudo and not self.is_square_attacked(4, them) and not self.is_square_attacked(3, them) and not self.is_square_attacked(2, them):
                            moves.append((4, 2, None))
        if pseudo:
            return moves
        real_moves = []
        for m in moves:
            state = self.make_move(m)
            if not self.is_square_attacked(self.find_king(us), them):
                real_moves.append(m)
            self.unmake_move(m, state)
        return real_moves

    def is_square_attacked(self, sq, by_color):
        if sq is None or sq < 0 or sq >= 64: return False
        r, c = divmod(sq, 8)
        p_dir = -8 if by_color == COLOR_BLACK else 8
        for dc in [-1, 1]:
            nc = c + dc
            if 0 <= nc < 8:
                t_sq = sq - p_dir + dc
                if 0 <= t_sq < 64 and self.pieces[t_sq] == PIECE_PAWN and self.colors[t_sq] == by_color:
                    return True
        k_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
        for o in k_offsets:
            t_sq = sq + o
            if 0 <= t_sq < 64 and self.pieces[t_sq] == PIECE_KNIGHT and self.colors[t_sq] == by_color:
                if abs((t_sq % 8) - c) <= 2:
                    return True
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc_ in dirs:
            curr_r, curr_c = r, c
            step = 1
            while True:
                curr_r += dr
                curr_c += dc_
                if not (0 <= curr_r < 8 and 0 <= curr_c < 8): break
                t_sq = curr_r * 8 + curr_c
                p = self.pieces[t_sq]
                if p != PIECE_EMPTY:
                    if self.colors[t_sq] == by_color:
                        is_diag = (dr != 0 and dc_ != 0)
                        if p == PIECE_QUEEN: return True
                        if is_diag and p == PIECE_BISHOP: return True
                        if not is_diag and p == PIECE_ROOK: return True
                        if step == 1 and p == PIECE_KING: return True
                    break
                step += 1
        return False

    def find_king(self, color):
        for sq in range(64):
            if self.pieces[sq] == PIECE_KING and self.colors[sq] == color:
                return sq
        return None

    def make_move(self, move):
        f, t, prm = move
        state = (self.castle_rights, self.ep_square, self.halfmove_clock, self.pieces[t], self.colors[t], self.zobrist_key)
        
        self.zobrist_key ^= ZOBRIST_CASTLE[self.castle_rights]
        if self.ep_square is not None: self.zobrist_key ^= ZOBRIST_EP[self.ep_square]
        else: self.zobrist_key ^= ZOBRIST_NO_EP

        p = self.pieces[f]
        c = self.colors[f]
        captured_p = self.pieces[t]
        
        self.zobrist_key ^= ZOBRIST_PIECES[f][c][p]
        if captured_p != PIECE_EMPTY:
            self.zobrist_key ^= ZOBRIST_PIECES[t][self.colors[t]][captured_p]

        if p == PIECE_PAWN or captured_p != PIECE_EMPTY:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.pieces[f] = PIECE_EMPTY
        self.colors[f] = None
        
        if p == PIECE_PAWN and t == self.ep_square:
            ep_target = t + 8 if c == COLOR_WHITE else t - 8
            state = (self.castle_rights, self.ep_square, self.halfmove_clock, self.pieces[t], self.colors[t], self.zobrist_key, self.pieces[ep_target], self.colors[ep_target])
            self.zobrist_key ^= ZOBRIST_PIECES[ep_target][self.colors[ep_target]][self.pieces[ep_target]]
            self.pieces[ep_target] = PIECE_EMPTY
            self.colors[ep_target] = None

        if prm:
            self.pieces[t] = prm
            self.colors[t] = c
            self.zobrist_key ^= ZOBRIST_PIECES[t][c][prm]
        else:
            self.pieces[t] = p
            self.colors[t] = c
            self.zobrist_key ^= ZOBRIST_PIECES[t][c][p]

        if p == PIECE_KING:
            if c == COLOR_WHITE:
                if f == 60 and t == 62:
                    self.zobrist_key ^= ZOBRIST_PIECES[63][COLOR_WHITE][PIECE_ROOK] ^ ZOBRIST_PIECES[61][COLOR_WHITE][PIECE_ROOK]
                    self.pieces[63], self.colors[63] = PIECE_EMPTY, None
                    self.pieces[61], self.colors[61] = PIECE_ROOK, COLOR_WHITE
                elif f == 60 and t == 58:
                    self.zobrist_key ^= ZOBRIST_PIECES[0][COLOR_WHITE][PIECE_ROOK] ^ ZOBRIST_PIECES[59][COLOR_WHITE][PIECE_ROOK]
                    self.pieces[0], self.colors[0] = PIECE_EMPTY, None
                    self.pieces[59], self.colors[59] = PIECE_ROOK, COLOR_WHITE
                self.castle_rights &= ~3
            else:
                if f == 4 and t == 6:
                    self.zobrist_key ^= ZOBRIST_PIECES[7][COLOR_BLACK][PIECE_ROOK] ^ ZOBRIST_PIECES[5][COLOR_BLACK][PIECE_ROOK]
                    self.pieces[7], self.colors[7] = PIECE_EMPTY, None
                    self.pieces[5], self.colors[5] = PIECE_ROOK, COLOR_BLACK
                elif f == 4 and t == 2:
                    self.zobrist_key ^= ZOBRIST_PIECES[0][COLOR_BLACK][PIECE_ROOK] ^ ZOBRIST_PIECES[3][COLOR_BLACK][PIECE_ROOK]
                    self.pieces[0], self.colors[0] = PIECE_EMPTY, None
                    self.pieces[3], self.colors[3] = PIECE_ROOK, COLOR_BLACK
                self.castle_rights &= ~12

        if p == PIECE_PAWN and abs(f - t) == 16:
            self.ep_square = (f + t) // 2
        else:
            self.ep_square = None

        if f == 56 or t == 56: self.castle_rights &= ~2
        if f == 63 or t == 63: self.castle_rights &= ~1
        if f == 0 or t == 0: self.castle_rights &= ~8
        if f == 7 or t == 7: self.castle_rights &= ~4

        if self.turn == COLOR_BLACK:
            self.fullmove_number += 1
        self.turn = 1 - self.turn
        
        self.zobrist_key ^= ZOBRIST_COLOR
        self.zobrist_key ^= ZOBRIST_CASTLE[self.castle_rights]
        if self.ep_square is not None: self.zobrist_key ^= ZOBRIST_EP[self.ep_square]
        else: self.zobrist_key ^= ZOBRIST_NO_EP
        
        self.history.append(self.zobrist_key)
        return state

    def unmake_move(self, move, state):
        self.history.pop()
        f, t, prm = move
        self.turn = 1 - self.turn
        if self.turn == COLOR_BLACK:
            self.fullmove_number -= 1
            
        p = self.pieces[t] if not prm else PIECE_PAWN
        c = self.colors[t]
        
        if p == PIECE_KING:
            if c == COLOR_WHITE:
                if f == 60 and t == 62:
                    self.pieces[61], self.colors[61] = PIECE_EMPTY, None
                    self.pieces[63], self.colors[63] = PIECE_ROOK, COLOR_WHITE
                elif f == 60 and t == 58:
                    self.pieces[59], self.colors[59] = PIECE_EMPTY, None
                    self.pieces[0], self.colors[0] = PIECE_ROOK, COLOR_WHITE
            else:
                if f == 4 and t == 6:
                    self.pieces[5], self.colors[5] = PIECE_EMPTY, None
                    self.pieces[7], self.colors[7] = PIECE_ROOK, COLOR_BLACK
                elif f == 4 and t == 2:
                    self.pieces[3], self.colors[3] = PIECE_EMPTY, None
                    self.pieces[0], self.colors[0] = PIECE_ROOK, COLOR_BLACK

        self.pieces[f] = p
        self.colors[f] = c
        
        if len(state) == 8:
            self.castle_rights, self.ep_square, self.halfmove_clock, self.pieces[t], self.colors[t], self.zobrist_key, ep_p, ep_c = state
            ep_target = t + 8 if c == COLOR_WHITE else t - 8
            self.pieces[ep_target] = ep_p
            self.colors[ep_target] = ep_c
        else:
            self.castle_rights, self.ep_square, self.halfmove_clock, self.pieces[t], self.colors[t], self.zobrist_key = state

    def is_draw(self):
        if self.halfmove_clock >= 100: return True
        if len(self.history) >= 4:
            curr = self.history[-1]
            count = 0
            for k in reversed(self.history):
                if k == curr:
                    count += 1
                    if count >= 3: return True
        return False

def evaluate(board):
    score = 0
    non_pawns_count = 0
    for sq in range(64):
        p = board.pieces[sq]
        if p != PIECE_EMPTY and p != PIECE_PAWN and p != PIECE_KING:
            non_pawns_count += 1

    is_endgame = (non_pawns_count <= 3)

    for sq in range(64):
        p = board.pieces[sq]
        if p == PIECE_EMPTY:
            continue
        c = board.colors[sq]
        val = PIECE_VALUES[p]
        p_score = val
        if p == PIECE_PAWN:
            p_score += PST_PAWN[sq if c == COLOR_BLACK else 63 - sq]
        elif p == PIECE_KNIGHT:
            p_score += PST_KNIGHT[sq if c == COLOR_BLACK else 63 - sq]
        elif p == PIECE_BISHOP:
            p_score += PST_BISHOP[sq if c == COLOR_BLACK else 63 - sq]
        elif p == PIECE_ROOK:
            p_score += PST_ROOK[sq if c == COLOR_BLACK else 63 - sq]
        elif p == PIECE_QUEEN:
            p_score += PST_QUEEN[sq if c == COLOR_BLACK else 63 - sq]
        elif p == PIECE_KING:
            if is_endgame:
                p_score += PST_KING_END[sq if c == COLOR_BLACK else 63 - sq]
            else:
                p_score += PST_KING_MID[sq if c == COLOR_BLACK else 63 - sq]
        if c == COLOR_WHITE:
            score += p_score
        else:
            score -= p_score
    return score if board.turn == COLOR_WHITE else -score

class Engine:
    def __init__(self):
        self.tt = {}
        self.nodes = 0
        self.killer_moves = [[None, None] for _ in range(32)]
        self.history_moves = [[0] * 64 for _ in range(64)]

    def static_exchange_eval(self, board, target_sq, us, them, current_val, attackers):
        if not attackers: return current_val
        cheapest_idx = None
        cheapest_val = 999999
        for i, sq in enumerate(attackers):
            p_val = PIECE_VALUES[board.pieces[sq]]
            if p_val < cheapest_val:
                cheapest_val = p_val
                cheapest_idx = i
        if cheapest_idx is None: return current_val
        attackers.pop(cheapest_idx)
        next_val = PIECE_VALUES[board.pieces[target_sq]] - current_val
        return max(current_val, next_val - self.static_exchange_eval(board, target_sq, them, us, next_val, attackers))

    def order_moves(self, board, moves, depth_layer=0, tt_move=None):
        scores = []
        for m in moves:
            score = 0
            if m == tt_move:
                score = 200000
            else:
                f, t, prm = m
                vic = board.pieces[t]
                att = board.pieces[f]
                if vic != PIECE_EMPTY:
                    score = 100000 + (PIECE_VALUES[vic] * 10) - PIECE_VALUES[att]
                    if score > 100000:
                        attackers = [sq for sq in range(64) if board.colors[sq] == board.colors[f]]
                        see_score = self.static_exchange_eval(board, t, board.colors[f], board.colors[t], 0, attackers)
                        if see_score < 0: score -= 50000
                else:
                    if depth_layer < 32:
                        if m == self.killer_moves[depth_layer][0]: score = 90000
                        elif m == self.killer_moves[depth_layer][1]: score = 80000
                    score += self.history_moves[f][t]
                if prm:
                    score += 95000
                if board.ep_square == t and att == PIECE_PAWN:
                    score = 100000 + (PIECE_VALUES[PIECE_PAWN] * 10) - PIECE_VALUES[PIECE_PAWN]
            scores.append((score, m))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [m for s, m in scores]

    def qsearch(self, board, alpha, beta):
        self.nodes += 1
        stand_pat = evaluate(board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        moves = board.generate_moves()
        caps = [m for m in moves if board.pieces[m[1]] != PIECE_EMPTY or (board.ep_square == m[1] and board.pieces[m[0]] == PIECE_PAWN)]
        caps = self.order_moves(board, caps)
        for m in caps:
            state = board.make_move(m)
            score = -self.qsearch(board, -beta, -alpha)
            board.unmake_move(m, state)
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        return alpha

    def search(self, board, depth, alpha, beta, depth_layer=0, do_null=True):
        self.nodes += 1
        if board.is_draw(): return 0, None

        tt_entry = self.tt.get(board.zobrist_key & 0x7FFFFFFFFFFFFFFF, None)
        if tt_entry and tt_entry[1] >= depth:
            flag, d, val, move = tt_entry
            if flag == FLAG_EXACT: return val, move
            elif flag == FLAG_ALPHA and val <= alpha: return alpha, move
            elif flag == FLAG_BETA and val >= beta: return beta, move

        if depth <= 0:
            return self.qsearch(board, alpha, beta), None

        if depth == 1 and not board.is_square_attacked(board.find_king(board.turn), 1 - board.turn):
            base_eval = evaluate(board)
            if base_eval + 300 <= alpha:
                return self.qsearch(board, alpha, beta), None

        if do_null and depth >= 3 and not board.is_square_attacked(board.find_king(board.turn), 1 - board.turn):
            board.turn = 1 - board.turn
            board.zobrist_key ^= ZOBRIST_COLOR
            ep_state = board.ep_square
            board.ep_square = None
            if ep_state is not None: board.zobrist_key ^= ZOBRIST_EP[ep_state] ^ ZOBRIST_NO_EP
            score, _ = self.search(board, depth - 1 - 2, -beta, -beta + 1, depth_layer + 1, False)
            score = -score
            board.turn = 1 - board.turn
            board.zobrist_key ^= ZOBRIST_COLOR
            board.ep_square = ep_state
            if ep_state is not None: board.zobrist_key ^= ZOBRIST_EP[ep_state] ^ ZOBRIST_NO_EP
            if score >= beta:
                return beta, None

        moves = board.generate_moves()
        if not moves:
            if board.is_square_attacked(board.find_king(board.turn), 1 - board.turn):
                return -30000 + depth_layer, None
            return 0, None

        tt_move = tt_entry[3] if tt_entry else None
        ordered = self.order_moves(board, moves, depth_layer, tt_move)
        best_move = ordered[0] if ordered else None
        best_val = -999999
        pvs_first = True

        for i, m in enumerate(ordered):
            state = board.make_move(m)
            if pvs_first:
                val, _ = self.search(board, depth - 1, -beta, -max(alpha, best_val), depth_layer + 1)
                val = -val
                pvs_first = False
            else:
                lmr = 0
                if depth >= 3 and i >= 4 and board.pieces[m[1]] == PIECE_EMPTY:
                    lmr = 1
                val, _ = self.search(board, depth - 1 - lmr, -max(alpha, best_val) - 1, -max(alpha, best_val), depth_layer + 1)
                val = -val
                if val > alpha and lmr > 0:
                    val, _ = self.search(board, depth - 1, -max(alpha, best_val) - 1, -max(alpha, best_val), depth_layer + 1)
                    val = -val
                if max(alpha, best_val) < val < beta:
                    val, _ = self.search(board, depth - 1, -beta, -max(alpha, best_val), depth_layer + 1)
                    val = -val

            board.unmake_move(m, state)
            if val > best_val:
                best_val = val
                best_move = m
            if val >= beta:
                if board.pieces[m[1]] == PIECE_EMPTY and depth_layer < 32:
                    self.killer_moves[depth_layer][0] = self.killer_moves[depth_layer][1]
                    self.killer_moves[depth_layer][1] = m
                    self.history_moves[m[0]][m[1]] += depth * depth
                self.tt[board.zobrist_key & 0x7FFFFFFFFFFFFFFF] = (FLAG_BETA, depth, beta, best_move)
                return beta, best_move

        flag = FLAG_EXACT if best_val > alpha else FLAG_ALPHA
        self.tt[board.zobrist_key & 0x7FFFFFFFFFFFFFFF] = (flag, depth, best_val, best_move)
        return best_val, best_move

def move_to_uci(m):
    if not m: return "0000"
    f, t, prm = m
    files = "abcdefgh"
    ranks = "87654321"
    s = files[f % 8] + ranks[f // 8] + files[t % 8] + ranks[t // 8]
    if prm:
        s += {5: "q", 4: "r", 3: "b", 2: "n"}[prm]
    return s

def uci_to_move(board, s):
    files = "abcdefgh"
    ranks = "87654321"
    f = ranks.index(s[1]) * 8 + files.index(s[0])
    t = ranks.index(s[3]) * 8 + files.index(s[2])
    prm = None
    if len(s) > 4:
        prm = {"q": 5, "r": 4, "b": 3, "n": 2}[s[4]]
    return (f, t, prm)

def main():
    board = Board()
    engine = Engine()
    while True:
        try:
            line = sys.stdin.readline()
            if not line: break
            cmd = line.strip()
            if cmd == "uci":
                sys.stdout.write("id name Ultimate UCI Variant\n")
                sys.stdout.write("id author EliteEngine\n")
                sys.stdout.write("uciok\n")
                sys.stdout.flush()
            elif cmd == "isready":
                sys.stdout.write("readyok\n")
                sys.stdout.flush()
            elif cmd.startswith("position"):
                parts = cmd.split()
                if "startpos" in parts:
                    board.reset()
                    if "moves" in parts:
                        idx = parts.index("moves")
                        for m_str in parts[idx+1:]:
                            m = uci_to_move(board, m_str)
                            board.make_move(m)
                elif "fen" in parts:
                    idx = parts.index("fen")
                    fen_parts = parts[idx+1:idx+7]
                    board.set_fen(" ".join(fen_parts))
                    if "moves" in parts:
                        idx_m = parts.index("moves")
                        for m_str in parts[idx_m+1:]:
                            m = uci_to_move(board, m_str)
                            board.make_move(m)
            elif cmd.startswith("go"):
                depth = 4
                parts = cmd.split()
                if "depth" in parts:
                    depth = int(parts[parts.index("depth") + 1])
                alpha, beta = -999999, 999999
                val, best = engine.search(board, depth, alpha, beta)
                if val <= alpha or val >= beta:
                    val, best = engine.search(board, depth, -999999, 999999)
                sys.stdout.write(f"bestmove {move_to_uci(best)}\n")
                sys.stdout.flush()
            elif cmd == "quit":
                break
        except:
            continue

if __name__ == "__main__":
    main()
