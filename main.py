from board import go_board,get_mat
blob_grid = get_mat(5,5)
width,height = 5,5

def player_plays(go):
    '''
    update_flag = 1                      ... Player made move successfully
    update_flag = 2                      ... Player didn't make move successfully
    update_flag = 3                      ... Player made an invalid move and lost
    '''
    player = 1  #Initial Value of Player = 1
    go.print_state()  # Print blank board
    move = "qqw"
    while (str(move) != 'q'):
        update_flag = 2 #Initial value of update flag = 2 to loop atleast once in while

        while (update_flag != 1): #Loop until valid move is made, break and exit for an illegal move
            print("DISPLAY POSSIBLE MOVES")
            moves = go.get_possible_moves(player)
            print(moves)
            print("CAN DO %d moves."%(len(moves)))
            move = input("Player %d's turn :"%(player))
            if move == 'q':
                update_flag = 3
                break
            if len(move) > 2 or len(move) < 2:
                print("Please Enter a value between 0 and 5")
                continue
            x, y = int(move[0]), int(move[1])
            update_flag = go.make_move((x,y), player)
            if update_flag == 3:
                print("Player %d made an illegal move. Player %d loses" % (player, player))
                break
            if update_flag == 2:
                print("Place already occupied play again")
        if update_flag == 3:
            break
        go.print_state()  # Print blank board

        player = 1 if player == 2 else 2



def print_current_blobs(blobs):
    for i in blobs.blobs:
        print(i,end="")
        print(" :: ",end="")
        print(len(blobs.blobs[i][0].liberties))
go = go_board(width,height)
#player_plays(go)

go.grid[0][2] = 1
go.grid[1][2] = 1
go.grid[2][2] = 1
go.grid[2][1] = 1
go.grid[2][0] = 1
go.grid[0][1] = 2
go.grid[1][1] = 2
go.grid[1][0] = 2

go.print_state()
print(go.check_if_liberty((0,0),player=1))