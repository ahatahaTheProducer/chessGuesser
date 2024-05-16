
board_file = input()
opponent_file = input()
# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
import copy
#board_file = 'ex_board4.txt'
#opponent_file = 'ex_opponent4.txt'
#creating chess board
rows = list()
for i in range(8):
    rows.append([])
for row in rows:
    for i in range(8):
        rows[i].append(['--'])
#empty table is created

#reading the given board
file_holder = open(board_file, 'r')
given_board_list = ((file_holder.read()).strip()).split('\n')
file_holder.close()
#reading ended

#reading the opponent moves
f_holder = open(opponent_file, 'r')
opponent_moves_list = ((f_holder.read()).strip()).split('\n')
f_holder.close()
#reading ended

#now we are gonna place the pieces on our actual table list
def piece_locator(places_list, the_table):
    for info in places_list:
        column_index = ord(info[3]) - ord('a')
        row_index = int(info[4]) - 1
        the_table[row_index][column_index][0] = info[0:2]
    return the_table
#okay we now have our given table as a whole

#with this function we are gonna be able to visualize what we have on board
def table_prompter(table_list):
    indexer = [['   '], ['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7']]
    last_list = [['   '],['a'],['b'],['c'],['d'],['e'],['f'],['g'],['h']]
    index = 8
    for i in last_list:
        print(i[0] + '    ', end='')
    print()
    #for i in indexer:
    #    print(i[0] + '    ', end='')
    #print()
    line = '     ---- ---- ---- ---- ---- ---- ---- ---- '
    print(line)
    for row in reversed(table_list):
        print( index, '|', end=' ')
        for i in row:
            print(i[0] + ' | ', end='')
        print()
        index-=1
#yet, we are not gonna use this at the end but it will stay

#####variables#####
#given_board_list: we captured from the board file
#the_table: current table
#our_colour: our chess side
#possible_moves_list
###################

#print(given_board_list)
the_table = piece_locator(given_board_list[1:], rows)
table_prompter(the_table)
our_colour = given_board_list[0]
#print(the_table[5])
#print(possible_moves_list)


#####PIECES POSSIBLE MOVES FUNCTIONS:::::####
#we need to have a function that gives us all the locations of the pieces
def location_info(current_table, actual_piece):
    locations_list = list()
    which_row_index = 0
    no_more_pieces = False
    for row in current_table:
        which_column_index = 0
        for each_square in row:
            if each_square[0] == actual_piece:
                our_location = chr(ord('a') + which_column_index) + str(which_row_index + 1)
                locations_list.append(our_location)
                which_char = actual_piece[1]
                #this if block is here in order not to waste time
                if which_char == 'K' or which_char == 'Q':
                    no_more_pieces = True
                    break
                elif which_char != 'P' and len(locations_list) == 2:
                    no_more_pieces = True
                    break
            which_column_index += 1
            if no_more_pieces:
                break
        which_row_index += 1
    return locations_list
######
#now we have the position and we need to find possible squares that
#the current piece can move horizontally, vertically and diagonally
#first horizontal finder:
def horizontal_spots(current_table, colour, location):
    possible_spots = list()
    row_index = int(location[1]) - 1
    column_index = ord(location[0]) - ord('a')
    our_row = current_table[row_index]
    #to the left
    temp_column = column_index - 1
    if temp_column != 0:
        for each_square in reversed(our_row[:column_index]):
            if temp_column < 0:
                break
            if each_square[0] == '--':
                possible_spots.append(chr(temp_column + ord('a')) + str(row_index + 1))
                temp_column -= 1
            elif (colour[0]).upper() != each_square[0][0]:
                possible_spots.append(chr(temp_column + ord('a')) + str(row_index + 1))
                break
            else:
                break
    #to the right
    temp_column = column_index + 1
    if temp_column != 7:
        for each_square in our_row[column_index + 1:]:
            if temp_column > 7:
                break
            if each_square[0] == '--':
                possible_spots.append(chr(temp_column + ord('a')) + str(row_index + 1))
                temp_column += 1
            elif (colour[0]).upper() != each_square[0][0]:
                possible_spots.append(chr(temp_column + ord('a')) + str(row_index + 1))
                break
            else:
                break
    return possible_spots
#secondly vertical spots-finder:
def vertical_spots(current_table, colour, location):
    possible_spots = list()
    row_index = int(location[1]) - 1
    loc_letter = location[0]
    colour_letter = (colour[0]).upper()

    column_index = ord(loc_letter) - ord('a')
    temp_row = row_index + 1
    can_go = True
    #for the upper part
    while can_go and temp_row <=7:
        if current_table[temp_row][column_index][0] == '--':
            possible_spots.append(loc_letter + str(temp_row + 1))
            temp_row += 1
        elif current_table[temp_row][column_index][0][0] != colour_letter:
            possible_spots.append(loc_letter + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    #below part
    can_go = True
    temp_row = row_index - 1
    while can_go and temp_row >= 0:
        if current_table[temp_row][column_index][0] == '--':
            possible_spots.append(loc_letter + str(temp_row + 1))
            temp_row -= 1
        elif current_table[temp_row][column_index][0][0] != colour_letter:
            possible_spots.append(loc_letter + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    return possible_spots
#finally diagonal spot finder:
def diagonal_spots(current_table, colour, location):
    possible_spots = list()
    row_index = int(location[1]) - 1
    loc_letter = location[0]
    colour_letter = (colour[0]).upper()
    column_index = ord(loc_letter) - ord('a')
    temp_row = row_index + 1
    temp_column = column_index + 1

    #rigt-top part
    can_go = True
    while can_go and temp_row <= 7 and temp_column <= 7:
        if current_table[temp_row][temp_column][0] == '--':
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            temp_row += 1
            temp_column += 1
        elif current_table[temp_row][temp_column][0][0] != colour_letter:
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    ####right-bottom part
    temp_row = row_index - 1
    temp_column = column_index + 1
    can_go = True
    while can_go and temp_row >= 0 and temp_column <= 7:
        if current_table[temp_row][temp_column][0] == '--':
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            temp_row -= 1
            temp_column += 1
        elif current_table[temp_row][temp_column][0][0] != colour_letter:
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    ####left-top part
    temp_row = row_index + 1
    temp_column = column_index - 1
    can_go = True
    while can_go and temp_row <= 7 and temp_column >= 0:
        if current_table[temp_row][temp_column][0] == '--':
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            temp_row += 1
            temp_column -= 1
        elif current_table[temp_row][temp_column][0][0] != colour_letter:
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    ####left-bottom part
    temp_row = row_index - 1
    temp_column = column_index - 1
    can_go = True
    while can_go and temp_row >= 0 and temp_column >= 0:
        if current_table[temp_row][temp_column][0] == '--':
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            temp_row -= 1
            temp_column -= 1
        elif current_table[temp_row][temp_column][0][0] != colour_letter:
            possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 1))
            can_go = False
        else:
            can_go = False
    ####
    return possible_spots
###spot finder functions ended
######
#KING
def king_moves(current_table, piece, colour):

    actual_piece = colour + piece
    position = location_info(current_table, actual_piece)
    if position == []:
        return []
    position = position[0]
    possible_spots = list()
    row_index = int(position[1]) - 1
    loc_letter = position[0]
    colour_letter = colour
    column_index = ord(loc_letter) - ord('a')
    goer_list = list()
    for i in range(1, 4):
        num = f'{bin(i)[2:]:0>2}'
        goer_list.append(((int(num[0]), int(num[1]))))
        goer_list.append(((int(num[0]) * -1, int(num[1]) * -1)))
    goer_list.append((-1, 1))
    goer_list.append((1, -1))
    for tuples in goer_list:
        x_cor = tuples[0]
        y_cor = tuples[1]
        if not (0 <= row_index + y_cor <= 7) or not (0 <= column_index + x_cor <= 7):
            continue
        look_for = current_table[row_index + y_cor][column_index + x_cor]
        if look_for[0] == '--':
            possible_spots.append(chr(ord('a') + column_index + x_cor) + str(row_index + y_cor + 1))
        elif look_for[0][0] != colour_letter:
            possible_spots.append(chr(ord('a') + column_index + x_cor) + str(row_index + y_cor + 1))
        else:
            continue
    return [[position],possible_spots]
#QUEEN
def queen_moves(current_table, piece, colour):
    actual_piece = colour + piece
    position = location_info(current_table, actual_piece)
    if position == []:
        return []
    position = position[0]
    queen_list = diagonal_spots(current_table, colour, position) + vertical_spots(current_table, colour, position) + horizontal_spots(current_table, colour, position)
    return [[position],queen_list]
#BISHOP
def bishop_moves(current_table, piece, colour):
    actual_piece = colour + piece
    positions = location_info(current_table, actual_piece)
    if positions == []:
        return []
    bishop_list = list()
    for position in positions:
        bishop_list.append([[position],diagonal_spots(current_table, colour, position)])
    return bishop_list
#ROOK
def rook_moves(current_table, piece, colour):
    actual_piece = colour + piece
    positions = location_info(current_table, actual_piece)
    if positions == []:
        return []
    rook_list = list()
    for position in positions:
        rook_list.append([[position], vertical_spots(current_table, colour, position) + horizontal_spots(current_table, colour, position)])

    return rook_list
#KNIGHT
def knight_moves(current_table, piece, colour):
    actual_piece = colour + piece
    positions = location_info(current_table, actual_piece)
    if positions == []:
        return []
    last_list = list()
    for position in positions:
        possible_spots = list()
        row_index = int(position[1]) - 1
        loc_letter = position[0]
        colour_letter = colour
        column_index = ord(loc_letter) - ord('a')
        goer_list = [(1, 2), (2, 1), (2, -1), (1, -2), (-2, -1), (-1, -2), (-2, 1), (-1, 2)]
        for tuples in goer_list:
            x_cor = tuples[0]
            y_cor = tuples[1]
            if not (0 <= row_index + y_cor <= 7) or not (0 <= column_index + x_cor <= 7):
                continue
            look_for = current_table[row_index + y_cor][column_index + x_cor]
            if look_for[0] == '--':
                possible_spots.append(chr(ord('a') + column_index + x_cor) + str(row_index + y_cor + 1))
            elif look_for[0][0] != colour_letter:
                possible_spots.append(chr(ord('a') + column_index + x_cor) + str(row_index + y_cor + 1))
            else:
                continue
        last_list.append([[position],possible_spots])
    return last_list
#PAWN
def pawn_moves(current_table, piece, colour, our_colour):
    actual_piece = colour + piece
    positions = location_info(current_table, actual_piece)
    if positions == []:
        return []
    last_list = list()
    for position in positions:
        possible_spots = list()
        row_index = int(position[1]) - 1
        loc_letter = position[0]
        column_index = ord(loc_letter) - ord('a')
        max_forw = 1
        temp_row = row_index
        temp_column = column_index
        if (our_colour[0]).upper() == colour:
            if row_index == 1:
                max_forw = 2
            if temp_row + 1 <=7 and temp_column + 1 <= 7 and (current_table[temp_row+1][temp_column+1][0] != '--' and current_table[temp_row+1][temp_column+1][0][0] != colour):
                possible_spots.append(chr(ord('a') + temp_column + 1) + str(temp_row + 2))
            if temp_row + 1 <=7 and temp_column - 1 >=0  and (current_table[temp_row+1][temp_column-1][0] != '--' and current_table[temp_row+1][temp_column-1][0][0] != colour):
                possible_spots.append(chr(ord('a') + temp_column - 1) + str(temp_row + 2))
            if max_forw == 2 and current_table[temp_row+1][temp_column][0] == '--' and current_table[temp_row+2][temp_column][0] == '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 3))
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 2))
            if max_forw == 2 and current_table[temp_row + 1][temp_column][0] == '--' and current_table[temp_row + 2][temp_column][0] != '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 2))
            if max_forw == 1 and current_table[temp_row+1][temp_column][0] == '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row + 2))
        else:
            if row_index == 6:
                max_forw = 2
            if temp_row - 1 >= 0 and temp_column - 1 >= 0 and (current_table[temp_row-1][temp_column-1][0] != '--' and current_table[temp_row-1][temp_column-1][0][0] != colour):
                possible_spots.append(chr(ord('a') + temp_column - 1) + str(temp_row))
            if temp_row - 1 >= 0 and temp_column + 1 <= 7  and (current_table[temp_row-1][temp_column+1][0] != '--' and current_table[temp_row-1][temp_column+1][0][0] != colour):
                possible_spots.append(chr(ord('a') + temp_column + 1) + str(temp_row))
            if max_forw == 2 and current_table[temp_row-1][temp_column][0] == '--' and current_table[temp_row-2][temp_column][0] == '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row - 1))
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row))
            if max_forw == 2 and current_table[temp_row-1][temp_column][0] == '--' and current_table[temp_row-2][temp_column][0] != '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row))
            if max_forw == 1 and current_table[temp_row-1][temp_column][0] == '--':
                possible_spots.append(chr(ord('a') + temp_column) + str(temp_row))
        last_list.append([[position],possible_spots])
    return last_list
######FINDING POSSIBLE MOVES HAS ENDED
#SO NOW WHAT WE HAVE?.. 'WK','WQ','WB','WN','WR','WP','BK','BQ','BB','BN','BR','BP'
#THEN LETS HAVE ALL THE POSSIBLE MOVES FOR EVERY SINGLE ELEMENT ON THE BOARD
#first we need to distribute the pieces to the correct functions
def distributor(piece, the_table, our_colour):
    colour = piece[0]
    what_piece = piece[1]
    if what_piece == 'K':
        return king_moves(the_table, what_piece, colour)
    elif what_piece == 'Q':
        return queen_moves(the_table, what_piece, colour)
    elif what_piece == 'B':
        return bishop_moves(the_table, what_piece, colour)
    elif what_piece == 'N':
        return knight_moves(the_table, what_piece, colour)
    elif what_piece == 'R':
        return rook_moves(the_table, what_piece, colour)
    elif what_piece == 'P':
        return pawn_moves(the_table, what_piece, colour, our_colour)
##########FINDING PIECES POSSIBLE MOVES FUNCTIONS ENDED#########
def find_all_possible_moves(the_table, our_colour):
    all_the_possible_moves = list()
    for each_element in ['WK', 'WQ', 'WB', 'WN', 'WR', 'WP', 'BK', 'BQ', 'BB', 'BN', 'BR', 'BP']:
        possibilities = distributor(each_element, the_table, our_colour)
#just trying to understand that i needed to put this if block took my at least two hours
        if possibilities == []:
            continue
        if each_element[1] == 'K' or each_element[1] == 'Q':
            all_the_possible_moves.append(possibilities)
        else:
            for line in possibilities:
                all_the_possible_moves.append(line)
    return all_the_possible_moves
#####this is gonna be useful
def what_is_there(current_table, location):
    row_index = int(location[1]) - 1
    loc_letter = location[0]
    column_index = ord(loc_letter) - ord('a')
    return current_table[row_index][column_index][0]
def table_changer(the_table, move_from, move_to):
    in_func_table = copy.deepcopy(the_table)
    from_row_index = int(move_from[1]) - 1
    from_loc_letter = move_from[0]
    from_column_index = ord(from_loc_letter) - ord('a')
    to_row_index = int(move_to[1]) - 1
    to_loc_letter = move_to[0]
    to_column_index = ord(to_loc_letter) - ord('a')
    our_stone = in_func_table[from_row_index][from_column_index][0]
    in_func_table[from_row_index][from_column_index][0] = '--'
    in_func_table[to_row_index][to_column_index][0] = our_stone
    return in_func_table
def is_valid(the_table, our_colour, white_king_pos, black_king_pos, move_from,  move_to):
    from_row_index = int(move_from[1]) - 1
    from_loc_letter = move_from[0]
    from_column_index = ord(from_loc_letter) - ord('a')
    to_row_index = int(move_to[1]) - 1
    to_loc_letter = move_to[0]
    to_column_index = ord(to_loc_letter) - ord('a')
    new_table = (table_changer(the_table, move_from, move_to))
    our_stone_colour = what_is_there(new_table, move_to)[0]
    new_all_pos_moves = find_all_possible_moves(new_table, our_colour)
    the_king_to_check = '--'
    if our_stone_colour == 'W':
        the_king_to_check = location_info(new_table, 'WK')[0]
    elif our_stone_colour == 'B':
        the_king_to_check = location_info(new_table,'BK')[0]
    for line in new_all_pos_moves:
        if the_king_to_check in line[1]:
            return False
    return True
#possible to valid format converter
def my_converter(a_list):
    my_list = sorted(a_list)
    headder = my_list[0][0:2]
    last_list = list()
    last_list.append([[headder], []])
    counter = 0
    for i in my_list:
        if i[0:2] == headder:
            last_list[counter][1].append(i[3:])
        else:
            headder = i[0:2]
            last_list.append([[headder], [i[3:]]])
            counter += 1
    return last_list

def my_recursive_main(the_table, our_colour, opponent_moves, last_two, make_checkmate_next, returning_list):
    my_precious_list = []
    #base_condition
    last_two = False
    if len(opponent_moves) == 1:
        last_two = True

    all_moves = find_all_possible_moves(the_table, our_colour)

    #lets store kings' locations for checking valid moves
    white_king_pos = location_info(the_table, 'WK')
    black_king_pos = location_info(the_table, 'BK')
    #lets store all valid moves in another list

    valid_moves = []
    for each_pieces_possibles in all_moves:
        move_from = each_pieces_possibles[0][0]
        possible_move_tos = each_pieces_possibles[1]
        temp_list = [[move_from], []]
        for move_to in possible_move_tos:
            is_it = is_valid(the_table, our_colour, white_king_pos, black_king_pos, move_from, move_to)
            if is_it:
                (temp_list[1]).append(move_to)
        valid_moves.append(temp_list)
        # now we are gonna check wheter its a checkmate or not

        # print(is_checkmate)
    our_colour_letter = our_colour[0].upper()
    #bu koca for bloğu bize karşı tarafın verdiğimiz olası hamlelere göre yapabileceği tüm olası valid hamleleri veriyor
    #ama eğer artık mat aşamasına gelmiş isek gerek yok bile
    for each_valid_line in valid_moves:
        moving_stone = each_valid_line[0][0]
        second_part = each_valid_line[1]
        for valid_destination in second_part:
            temp_board = table_changer(the_table, moving_stone, valid_destination)
            if make_checkmate_next:
                checkmate_found = False
                all_of_them = find_all_possible_moves(temp_board, our_colour)
                if our_colour == 'black':
                    col_let = 'W'
                if our_colour == 'white':
                    col_let = 'B'
                loc_info_of_rival_king = location_info(temp_board, col_let + 'K')[0]
                our_movements_list = []
                rivals_movements_list = []
               # table_prompter(temp_board)



                for line in all_of_them:
                    if what_is_there(temp_board, line[0][0])[0] == our_colour[0].upper():
                        our_movements_list.append(line)
                    else:
                        rivals_movements_list.append(line)
                # for i in our_movements_list:
                #     print(i)
                # print('##############################')
                case_a = False
                a = 0
                for line in our_movements_list:
                    index = 0
                    for i in line[1]:
                        if loc_info_of_rival_king == i:
                            case_a = True
                            move_from = our_movements_list[a][0][0]
                            move_to = our_movements_list[a][1][index]
                        index+=1
                    a+=1
                if case_a:
                    case_b = False
                   # print('aha burası')
                    valid_rival_movements = []
                    for line in rivals_movements_list:
                        move_from = line[0][0]
                        for i in line[1]:
                            move_to = i
                            if is_valid(temp_board, our_colour, 5, 5, move_from, move_to):
                                valid_rival_movements.append(move_from + move_to)
                    if valid_rival_movements == []:
                        case_b = True
                        checkmate_found = True
                        #print([moving_stone + ' ' + valid_destination])
                        returning_list = returning_list + [moving_stone + ' ' + valid_destination]
                        for i in returning_list:
                            print(i)
                        return
            if make_checkmate_next and checkmate_found == False:
                continue

            temp_valid_moves = list()
            temp_all_moves = find_all_possible_moves(temp_board, our_colour)
            for each_pieces_possibles in temp_all_moves:
                move_from = each_pieces_possibles[0][0]
                possible_move_tos = each_pieces_possibles[1]
                if what_is_there(temp_board, move_from)[0] == our_colour_letter:
                    continue
                temp_list = [[move_from], []]
                for move_to in possible_move_tos:
                    is_it = is_valid(temp_board, our_colour, white_king_pos, black_king_pos, move_from, move_to)
                    if is_it:
                        (temp_list[1]).append(move_to)
                temp_valid_moves.append(temp_list)



            formatted_list = list()
            for each_temp_valid_line in temp_valid_moves:
                pos_movtos = each_temp_valid_line[1]
                move_from = each_temp_valid_line[0][0]
                if pos_movtos == []:
                    continue
                for i in pos_movtos:
                    formatted_list.append(move_from+' '+i)
            formatted_list.sort()
            our_opponent_moves = opponent_moves[0].split(',')
            our_opponent_moves.sort()
            #burada da eğer karşının yapabileceği tüm hamleler verilen dosyadaki ile aynı ise o hamleyi kaydediyoruz
            if sorted(our_opponent_moves) == sorted(formatted_list):
                my_precious_list.append(moving_stone+' '+valid_destination)
   # print(my_precious_list)

    make_checkmate_next = False
    if last_two == True:
        make_checkmate_next = True
        what_to_send = []
    else:
        what_to_send = opponent_moves[1:]
    for each_precious_possibility in my_precious_list:
        move_from = each_precious_possibility[0:2]
        move_to = each_precious_possibility[3:]
        new_board = table_changer(the_table, move_from, move_to)
        if opponent_moves == []:
            pass
        else:
            our_opponent_moves = (opponent_moves[0].split(','))[0]
            move_from = our_opponent_moves[0:2]
            move_to = our_opponent_moves[3:]
            new_board = table_changer(new_board, move_from, move_to)
        sending_resulting_list = returning_list + [each_precious_possibility]
        #table_prompter(new_board)
        my_recursive_main(new_board, our_colour, what_to_send, last_two, make_checkmate_next, sending_resulting_list)

my_recursive_main(the_table, our_colour, opponent_moves_list, False, False, [])
#note for continueing: store the places of the kings, iterate over evvveerrry movement and check if they are valid or not
#make all the valid movements with given opponent moves
#if opponent has to do it this way, store the path
#recommendation for myself: never ever wait for the last day of a cmpe hw or even the day before the end
# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

