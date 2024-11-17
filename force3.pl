% Définition du plateau
:- dynamic board/1.

% Initialise le plateau avec les cases vides et les pions carrés
init_board :-
    Board = [[_, _, _],
              [_, c1, _],
              [_, _, _]],
    assert(board(Board)),
    init_pawns.

% Initialise les pions ronds
init_pawns :-
    assert(pawn(black, 3)),
    assert(pawn(white, 3)).

% Affiche le plateau
print_board :-
    board(Board),
    nl,
    print_rows(Board).

print_rows([]).
print_rows([Row|Rest]) :-
    print_row(Row),
    print_rows(Rest).

print_row(Row) :-
    write(Row), nl.

% Vérifie si un joueur a gagné
check_win(Player) :-
    board(Board),
    (   row_win(Board, Player);
        col_win(Board, Player);
        diag_win(Board, Player)
    ).

row_win(Board, Player) :-
    member(Row, Board),
    three_in_a_row(Row, Player).

col_win(Board, Player) :-
    transpose(Board, Transposed),
    member(Col, Transposed),
    three_in_a_row(Col, Player).

diag_win(Board, Player) :-
    diagonals(Board, Diags),
    member(Diag, Diags),
    three_in_a_row(Diag, Player).

three_in_a_row([Player, Player, Player|_], Player).
three_in_a_row([_, Player, Player, Player|_], Player).
three_in_a_row([Player, _, Player, Player|_], Player).
three_in_a_row([Player, Player, _, Player|_], Player).

% Déplace un pion rond
move_pawn(X1/Y1, X2/Y2, Player) :-
    board(Board),
    nth1(X1, Board, Row1),
    nth1(Y1, Row1, Player),
    nth1(X2, Board, Row2),
    nth1(Y2, Row2, empty),
    replace(Row1, Y1, empty, NewRow1),
    replace(Row2, Y2, Player, NewRow2),
    replace(Board, X1, NewRow1, TempBoard),
    replace(TempBoard, X2, NewRow2, NewBoard),
    retract(board(Board)),
    assert(board(NewBoard)).

replace([_|T], 1, X, [X|T]).
replace([H|T], N, X, [H|R]) :-
    N > 1,
    N1 is N - 1,
    replace(T, N1, X, R).

% Exemple de démarrage du jeu
start_game :-
    init_board,
    print_board,
    play.

play :-
    % Logique du tour de jeu ici
    % Demander au joueur de faire un mouvement
    % Vérifier si un joueur a gagné
    % Alterner entre les joueurs
    true.

% Transpose une matrice
transpose([], []).
transpose([[H|T]|Rows], [ [H|Hs]|Ts]) :-
    transpose(T, Hs, Rows, Ts).
transpose([], [], [], []).
transpose([], [], Rows, [Row|Rows]) :-
    Row = [H|_],
    member(H, Rows).% Définition du plateau
:- dynamic board/1.

% Initialise le plateau avec les cases vides et les pions carrés
init_board :-
    Board = [[_, _, _],
              [_, c1, _],
              [_, _, _]],
    assert(board(Board)),
    init_pawns.

% Initialise les pions ronds
init_pawns :-
    assert(pawn(black, 3)),
    assert(pawn(white, 3)).

% Affiche le plateau
print_board :-
    board(Board),
    nl,
    print_rows(Board).
% Initialisation du plateau
init_board :-
    % Code pour initialiser le plateau
    write('Plateau initialisé.'), nl.

% Affichage du plateau
print_board :-
    % Code pour afficher le plateau
    write('Affichage du plateau.'), nl.

% Mouvement d'un pion
move_pawn(From, To) :-
    % Code pour déplacer un pion
    write('Déplacement de '), write(From), write(' à '), write(To), nl.

% Vérification de la victoire
check_win(Player) :-
    % Code pour vérifier si le joueur a gagné
    write(Player), write(' a gagné !'), nl.

% Gestion du jeu
play :-
    init_board,
    print_board,
    % Boucle de jeu ici
    write('C\'est au tour du joueur.'), nl,
    % Demander un mouvement
    read(Move),
    call(Move),  % Exécute le mouvement
    check_win('Joueur 1'),  % Vérifie si le joueur 1 a gagné
    play.  % Continue le jeu
print_rows([]).
print_rows([Row|Rest]) :-
    print_row(Row),
    print_rows(Rest).

print_row(Row) :-
    write(Row), nl.

% Vérifie si un joueur a gagné
check_win(Player) :-
    board(Board),
    (   row_win(Board, Player);
        col_win(Board, Player);
        diag_win(Board, Player)
    ).

row_win(Board, Player) :-
    member(Row, Board),
    three_in_a_row(Row, Player).

col_win(Board, Player) :-
    transpose(Board, Transposed),
    member(Col, Transposed),
    three_in_a_row(Col, Player).

diag_win(Board, Player) :-
    diagonals(Board, Diags),
    member(Diag, Diags),
    three_in_a_row(Diag, Player).

three_in_a_row([Player, Player, Player|_], Player).
three_in_a_row([_, Player, Player, Player|_], Player).
three_in_a_row([Player, _, Player, Player|_], Player).
three_in_a_row([Player, Player, _, Player|_], Player).

% Déplace un pion rond
move_pawn(X1/Y1, X2/Y2, Player) :-
    board(Board),
    nth1(X1, Board, Row1),
    nth1(Y1, Row1, Player),
    nth1(X2, Board, Row2),
    nth1(Y2, Row2, empty),
    replace(Row1, Y1, empty, NewRow1),
    replace(Row2, Y2, Player, NewRow2),
    replace(Board, X1, NewRow1, TempBoard),
    replace(TempBoard, X2, NewRow2, NewBoard),
    retract(board(Board)),
    assert(board(NewBoard)).

replace([_|T], 1, X, [X|T]).
replace([H|T], N, X, [H|R]) :-
    N > 1,
    N1 is N - 1,
    replace(T, N1, X, R).

% Exemple de démarrage du jeu
start_game :-
    init_board,
    print_board,
    play.

play :-
    % Logique du tour de jeu ici
    % Demander au joueur de faire un mouvement
    % Vérifier si un joueur a gagné
    % Alterner entre les joueurs
    true.

% Transpose une matrice
transpose([], []).
transpose([[H|T]|Rows], [ [H|Hs]|Ts]) :-
    transpose(T, Hs, Rows, Ts).
transpose([], [], [], []).
transpose([], [], Rows, [Row|Rows]) :-
    Row = [H|_],
    member(H, Rows).