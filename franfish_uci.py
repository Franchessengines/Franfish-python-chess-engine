import sys
import time
import chess
import chess.polyglot

PIECE_VALUES = {chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0}

PAWN_TABLE = [
      0,   0,   0,   0,   0,   0,   0,   0,
     50,  50,  50,  50,  50,  50,  50,  50,
     10,  10,  20,  30,  30,  20,  10,  10,
      5,   5,  10,  25,  25,  10,   5,   5,
      0,   0,   0,  20,  20,   0,   0,   0,
      5,  -5, -10,   0,   0, -10,  -5,   5,
      5,  10,  10, -20, -20,  10,  10,   5,
      0,   0,   0,   0,   0,   0,   0,   0
]
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]
BISHOP_TABLE = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,  10,  10,   5,   0, -10,
    -10,   5,   5,  10,  10,   5,   5, -10,
    -10,   0,  10,  10,  10,  10,   0, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,   5,   0,   0,   0,   0,   5, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]
ROOK_TABLE = [
      0,   0,   0,   0,   0,   0,   0,   0,
      5,  10,  10,  10,  10,  10,  10,   5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
     -5,   0,   0,   0,   0,   0,   0,  -5,
      0,   0,   0,   5,   5,   0,   0,   0
]
QUEEN_TABLE = [
    -20, -10, -10,  -5,  -5, -10, -10, -20,
    -10,   0,   0,   0,   0,   0,   0, -10,
    -10,   0,   5,   5,   5,   5,   0, -10,
     -5,   0,   5,   5,   5,   5,   0,  -5,
      0,   0,   5,   5,   5,   5,   0,  -5,
    -10,   5,   5,   5,   5,   5,   0, -10,
    -10,   0,   5,   0,   0,   0,   0, -10,
    -20, -10, -10,  -5,  -5, -10, -10, -20
]
KING_TABLE_MID = [
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -10, -20, -20, -20, -20, -20, -20, -10,
     20,  20,   0,   0,   0,   0,  20,  20,
     20,  30,  10,   0,   0,  10,  30,  20
]
KING_TABLE_END = [
    -50, -40, -30, -20, -20, -30, -40, -50,
    -30, -20, -10,   0,   0, -10, -20, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  30,  40,  40,  30, -10, -30,
    -30, -10,  20,  30,  30,  20, -10, -30,
    -30, -30,   0,   0,   0,   0, -30, -30,
    -50, -30, -30, -30, -30, -30, -30, -50
]

PST = {
    chess.PAWN: PAWN_TABLE,
    chess.KNIGHT: KNIGHT_TABLE,
    chess.BISHOP: BISHOP_TABLE,
    chess.ROOK: ROOK_TABLE,
    chess.QUEEN: QUEEN_TABLE,
}

def pst_value(piece_type, square, color, endgame):
    if piece_type == chess.KING:
        table = KING_TABLE_END if endgame else KING_TABLE_MID
    else:
        table = PST[piece_type]
    idx = square if color == chess.WHITE else chess.square_mirror(square)
    return table[idx]

def is_endgame(board):
    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    minors = (len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.WHITE)) +
              len(board.pieces(chess.KNIGHT, chess.BLACK)) + len(board.pieces(chess.BISHOP, chess.BLACK)))
    return queens == 0 or (queens <= 2 and minors <= 2)

def king_safety(board, color, endgame):
    if endgame:
        return 0
    king_sq = board.king(color)
    if king_sq is None:
        return 0
    score = 0
    file = chess.square_file(king_sq)
    rank = chess.square_rank(king_sq)
    direction = 1 if color == chess.WHITE else -1
    for df in (-1, 0, 1):
        f = file + df
        if 0 <= f <= 7:
            r = rank + direction
            if 0 <= r <= 7:
                sq = chess.square(f, r)
                piece = board.piece_at(sq)
                if piece and piece.piece_type == chess.PAWN and piece.color == color:
                    score += 10
    return score

def passed_pawn_bonus(board, color):
    score = 0
    enemy = not color
    for sq in board.pieces(chess.PAWN, color):
        file = chess.square_file(sq)
        rank = chess.square_rank(sq)
        blocked = False
        for f in (file - 1, file, file + 1):
            if f < 0 or f > 7:
                continue
            for enemy_sq in board.pieces(chess.PAWN, enemy):
                if chess.square_file(enemy_sq) != f:
                    continue
                enemy_rank = chess.square_rank(enemy_sq)
                if color == chess.WHITE and enemy_rank > rank:
                    blocked = True
                elif color == chess.BLACK and enemy_rank < rank:
                    blocked = True
        if not blocked:
            advancement = rank if color == chess.WHITE else (7 - rank)
            score += 10 + advancement * 5
    return score

def mobility(board, color):
    if board.turn == color:
        return sum(1 for _ in board.generate_pseudo_legal_moves())
    return 0

def development_score(board, color):
    back_rank = 0 if color == chess.WHITE else 7
    score = 0
    for piece_type in (chess.KNIGHT, chess.BISHOP):
        for sq in board.pieces(piece_type, color):
            if chess.square_rank(sq) != back_rank:
                score += 10
    return score

def early_queen_penalty(board, color):
    if board.fullmove_number > 10:
        return 0
    home_square = chess.D1 if color == chess.WHITE else chess.D8
    queens = board.pieces(chess.QUEEN, color)
    if not queens or home_square in queens:
        return 0
    back_rank = 0 if color == chess.WHITE else 7
    developed_minors = sum(
        1 for pt in (chess.KNIGHT, chess.BISHOP)
        for sq in board.pieces(pt, color)
        if chess.square_rank(sq) != back_rank
    )
    if developed_minors < 2:
        return -30
    return 0

def hanging_penalty(board, color):
    total = 0
    enemy = not color
    for piece_type in PIECE_VALUES:
        if piece_type in (chess.KING, chess.PAWN):
            continue
        for sq in board.pieces(piece_type, color):
            if board.attackers(enemy, sq) and not board.attackers(color, sq):
                total += PIECE_VALUES[piece_type]
    return total

def evaluate(board):
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    endgame = is_endgame(board)
    score = 0

    for piece_type in PIECE_VALUES:
        for square in board.pieces(piece_type, chess.WHITE):
            score += PIECE_VALUES[piece_type] + pst_value(piece_type, square, chess.WHITE, endgame)
        for square in board.pieces(piece_type, chess.BLACK):
            score -= PIECE_VALUES[piece_type] + pst_value(piece_type, square, chess.BLACK, endgame)

    score += king_safety(board, chess.WHITE, endgame) - king_safety(board, chess.BLACK, endgame)
    score += passed_pawn_bonus(board, chess.WHITE) - passed_pawn_bonus(board, chess.BLACK)
    score += (mobility(board, chess.WHITE) - mobility(board, chess.BLACK)) * 2
    if not endgame:
        score += development_score(board, chess.WHITE) - development_score(board, chess.BLACK)
        score += early_queen_penalty(board, chess.WHITE) - early_queen_penalty(board, chess.BLACK)
    score -= hanging_penalty(board, chess.WHITE)
    score += hanging_penalty(board, chess.BLACK)

    return score if board.turn == chess.WHITE else -score

EXACT, LOWERBOUND, UPPERBOUND = 0, 1, 2
transposition_table = {}

def tt_lookup(key, depth, alpha, beta):
    entry = transposition_table.get(key)
    if entry is None:
        return None, None
    entry_depth, entry_score, entry_flag, entry_move = entry
    if entry_depth >= depth:
        if entry_flag == EXACT:
            return entry_score, entry_move
        if entry_flag == LOWERBOUND and entry_score > alpha:
            alpha = entry_score
        elif entry_flag == UPPERBOUND and entry_score < beta:
            beta = entry_score
        if alpha >= beta:
            return entry_score, entry_move
    return None, entry_move

def tt_store(key, depth, score, flag, move):
    transposition_table[key] = (depth, score, flag, move)

killer_moves = {}
history_table = {}

def order_moves(board, depth, tt_move=None):
    killers = killer_moves.get(depth, [])

    def score(move):
        if tt_move is not None and move == tt_move:
            return 1_000_000
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            v = PIECE_VALUES.get(victim.piece_type, 0) if victim else 0
            a = PIECE_VALUES.get(attacker.piece_type, 0) if attacker else 0
            return 100_000 + v - a
        if move.promotion:
            return 90_000
        if move in killers:
            return 80_000
        return history_table.get((move.from_square, move.to_square), 0)

    return sorted(board.legal_moves, key=score, reverse=True)

def record_killer(move, depth):
    if move.promotion is None:
        moves = killer_moves.setdefault(depth, [])
        if move not in moves:
            moves.insert(0, move)
            del moves[2:]

def record_history(move, depth):
    key = (move.from_square, move.to_square)
    history_table[key] = history_table.get(key, 0) + depth * depth

def quiescence(board, alpha, beta, depth=6):
    stand_pat = evaluate(board)
    if depth == 0:
        return stand_pat
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    for move in order_moves(board, 0):
        if not board.is_capture(move):
            continue
        board.push(move)
        score = -quiescence(board, -beta, -alpha, depth - 1)
        board.pop()
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

NULL_MOVE_REDUCTION = 2

def negamax(board, depth, alpha, beta, deadline, allow_null=True):
    if time.time() > deadline:
        raise TimeoutError

    key = chess.polyglot.zobrist_hash(board)
    orig_alpha = alpha

    tt_score, tt_move = tt_lookup(key, depth, alpha, beta)
    if tt_score is not None:
        return tt_score

    if board.is_repetition(3) or board.is_fifty_moves():
        return 0
    if board.is_game_over():
        return evaluate(board)

    in_check = board.is_check()
    if in_check:
        depth += 1

    if depth <= 0:
        return quiescence(board, alpha, beta)

    if allow_null and not in_check and depth >= 3 and not is_endgame(board):
        board.push(chess.Move.null())
        null_score = -negamax(board, depth - 1 - NULL_MOVE_REDUCTION, -beta, -beta + 1, deadline, allow_null=False)
        board.pop()
        if null_score >= beta:
            return beta

    best_score = -float("inf")
    best_move = None
    moves = order_moves(board, depth, tt_move)

    for i, move in enumerate(moves):
        is_capture = board.is_capture(move)
        gives_check = board.gives_check(move)

        board.push(move)

        if i >= 4 and depth >= 3 and not is_capture and not move.promotion and not gives_check and not in_check:
            reduced_score = -negamax(board, depth - 2, -alpha - 1, -alpha, deadline)
            if reduced_score > alpha:
                score = -negamax(board, depth - 1, -beta, -alpha, deadline)
            else:
                score = reduced_score
        elif i == 0:
            score = -negamax(board, depth - 1, -beta, -alpha, deadline)
        else:
            score = -negamax(board, depth - 1, -alpha - 1, -alpha, deadline)
            if alpha < score < beta:
                score = -negamax(board, depth - 1, -beta, -alpha, deadline)

        board.pop()

        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            if not is_capture and not move.promotion:
                record_killer(move, depth)
                record_history(move, depth)
            break

    flag = EXACT
    if best_score <= orig_alpha:
        flag = UPPERBOUND
    elif best_score >= beta:
        flag = LOWERBOUND
    tt_store(key, depth, best_score, flag, best_move)

    return best_score

def find_best_move(board, think_time):
    deadline = time.time() + think_time
    best_move = None
    depth = 1
    while True:
        try:
            current_best = None
            current_best_score = -float("inf")
            for move in order_moves(board, depth, best_move):
                board.push(move)
                score = -negamax(board, depth - 1, -float("inf"), float("inf"), deadline)
                board.pop()
                if score > current_best_score:
                    current_best_score = score
                    current_best = move
            if current_best:
                best_move = current_best
            depth += 1
            if depth > 80:
                break
        except TimeoutError:
            break
    return best_move if best_move else next(iter(board.legal_moves), None)

def compute_think_time(wtime, btime, winc, binc, movetime, movestogo, turn):
    if movetime is not None:
        return max(0.05, movetime / 1000.0)
    remaining = wtime if turn == chess.WHITE else btime
    increment = winc if turn == chess.WHITE else binc
    if remaining is None:
        return 5.0
    remaining_sec = remaining / 1000.0
    increment_sec = (increment or 0) / 1000.0
    slices = movestogo if movestogo else 30
    budget = remaining_sec / slices + increment_sec * 0.8
    return max(0.05, min(budget, remaining_sec * 0.5))

def uci_loop():
    board = chess.Board()

    while True:
        raw = sys.stdin.readline()
        if not raw:
            break
        line = "".join(ch for ch in raw if ch.isprintable()).strip()
        if not line:
            continue
        tokens = line.split()
        cmd = tokens[0]

        if cmd == "uci":
            print("id name Franfish")
            print("id author Fran")
            print("uciok")
            sys.stdout.flush()

        elif cmd == "isready":
            print("readyok")
            sys.stdout.flush()

        elif cmd == "ucinewgame":
            board = chess.Board()
            transposition_table.clear()
            killer_moves.clear()
            history_table.clear()

        elif cmd == "position":
            idx = 1
            if idx < len(tokens) and tokens[idx] == "startpos":
                board = chess.Board()
                idx += 1
            elif idx < len(tokens) and tokens[idx] == "fen":
                idx += 1
                fen_parts = []
                while idx < len(tokens) and tokens[idx] != "moves":
                    fen_parts.append(tokens[idx])
                    idx += 1
                board = chess.Board(" ".join(fen_parts))
            if idx < len(tokens) and tokens[idx] == "moves":
                idx += 1
                for mv in tokens[idx:]:
                    board.push_uci(mv)

        elif cmd == "go":
            wtime = btime = winc = binc = movetime = movestogo = None
            i = 1
            while i < len(tokens):
                if tokens[i] == "wtime":
                    wtime = int(tokens[i + 1]); i += 2
                elif tokens[i] == "btime":
                    btime = int(tokens[i + 1]); i += 2
                elif tokens[i] == "winc":
                    winc = int(tokens[i + 1]); i += 2
                elif tokens[i] == "binc":
                    binc = int(tokens[i + 1]); i += 2
                elif tokens[i] == "movetime":
                    movetime = int(tokens[i + 1]); i += 2
                elif tokens[i] == "movestogo":
                    movestogo = int(tokens[i + 1]); i += 2
                else:
                    i += 1

            think_time = compute_think_time(wtime, btime, winc, binc, movetime, movestogo, board.turn)
            move = find_best_move(board, think_time)
            if move:
                print(f"bestmove {move.uci()}")
            else:
                print("bestmove 0000")
            sys.stdout.flush()

        elif cmd == "quit":
            break

        elif cmd == "stop":
            pass

if __name__ == "__main__":
    uci_loop()
