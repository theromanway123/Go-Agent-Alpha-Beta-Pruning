import random

def readInput():
    path = "input.txt"
    with open(path, 'r') as f:
        lines = f.readlines()
    piece_type = int(lines[0])

    prev_grid = get_mat(5, 5)
    for i in range(1, 6):
        var = lines[i]
        lenny = len(var)-1
        for j in range(0,lenny):
            prev_grid[i - 1][j] = int(var[j])



    curr_grid = get_mat(5, 5)
    for i in range(6,11):
        var = lines[i]
        lenny = len(var)-1
        print("VAR :  ",var)
        print("LENNY : ",lenny)
        for j in range(0,lenny):
            print("i : ",i,"j : ",j)
            curr_grid[i - 6][j] = int(var[j])

    return piece_type,prev_grid,curr_grid
def readOutput(path="output.txt"):
    with open(path, 'r') as f:
        position = f.readline().strip().split(',')

        if position[0] == "PASS":
            return "PASS", -1, -1

        x = int(position[0])
        y = int(position[1])

    return "MOVE", x, y


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def writePass(path="output.txt"):
    with open(path, 'w') as f:
        f.write("PASS")


def writeNextInput(piece_type, previous_board, board, path="input.txt"):
    res = ""
    res += str(piece_type) + "\n"
    for item in previous_board:
        res += "".join([str(x) for x in item])
        res += "\n"

    for item in board:
        res += "".join([str(x) for x in item])
        res += "\n"

    with open(path, 'w') as f:
        f.write(res[:-1]);



def get_mat(height,width):
    grid = []
    for i in range(0,height):
        row = []
        for j in range(0,width):
            row.append(0)
        grid.append(row)
    return grid


class board:

    def __init__(self,go,player,prev):
        self.grid = get_mat(5,5)
        self.player = player
        self.prev = prev
        for i in range(0,5):   #MAKE A COPY OF THE ORIGINAL BOARD
            for j in range(0, 5):
                self.grid[i][j] = go[i][j]
        self.blob_def = get_mat(5,5)
        self.blobs = self.define_blobs()
        #self.print_current_blobs()
        #self.print_grid()

    # def print_current_blobs(self):
    #     print("PRINTING THE BLOBS FOR CURRENT STATE")
    #     for hashes in self.blobs:
    #         print(hashes," : ",end="")
    #         print(self.blobs[hashes],end="")
    #         print(len(self.blobs[hashes]),end="")
    #         print("LIBERTIES : ",self.get_liberties_of_blob(self.blobs[hashes]))

    def define_blobs(self):
        blobs = {}
        for i in range(0,5):
            for j in range(0,5):
                new_blob = self.get_blob((i,j))
                x,y = new_blob[0]
                if self.grid[x][y] != 0:
                    blobs[new_blob[0]] = new_blob
        return blobs

    def get_liberties_of_blob(self,list_of_positions):

        liberties  = set([])

        for position in list_of_positions:
            x,y = position
            neighbours = self.get_neighbours(x,y)
            for neighbour in neighbours:
                i,j = neighbour
                if self.grid[i][j] == 0 and neighbour not in list_of_positions:
                    liberties.add((i,j))

        return list(liberties)


    def get_neighbours(self,x,y):
        neighbours = []
        left,right,up,down = y-1,y+1,x-1,x+1
        if 0 <=  x < 5 and 0 <= y < 5:
            if 0 <= left < 5:
                neighbours.append((x,left))
            if 0 <= right < 5:
                neighbours.append((x, right))
            if 0 <= up < 5:
                neighbours.append((up, y))
            if 0 <= down < 5:
                neighbours.append((down, y))
            return neighbours
        else:
            #print("CANNOT FIND NEIGHBOURS OUTSIDE THE GRID :'( ")
            return []

    def get_blob(self,position):
        x,y = position
        player_value = self.grid[x][y]
        frontier = [position]
        explored = []
        blobs = set([position])

        while(len(frontier)!=0):
            current_position = frontier.pop(0)
            x_curr,y_curr = current_position
            neighbours_of_current_position = self.get_neighbours(x_curr,y_curr)
            for neighbour in neighbours_of_current_position:
                x_neighbour,y_neighbour = neighbour
                if self.grid[x_neighbour][y_neighbour] == player_value:
                    if neighbour not in frontier and neighbour not in explored:
                        frontier.append(neighbour)
                        blobs.add(neighbour)

            explored.append(current_position)

        list_of_blobs = list(blobs)
        list_of_blobs.sort(key=lambda x:x[0]*10+(x[1]))
        return list_of_blobs

    #
    def print_grid(self):
        print("")
        sym = 'X' if self.player == 1 else 'O'
        for i in range(0,5):
            for j in range(0,5):
                if self.grid[i][j] == 0:
                    sym = "_"
                if self.grid[i][j] == 1:
                    sym = "X"
                if self.grid[i][j] == 2:
                    sym = "O"
                print(" " + sym + " ", end="")
            print()

    def check_removal(self):
        new_blobs = self.define_blobs()
        new_grid = get_mat(5,5)
        for i in range(0,5):
            for j in range(0,5):
                new_grid[i][j] = self.grid[i][j]
        total_captured = 0
        for hashes in new_blobs:
            x,y = hashes
            if self.grid[x][y] != self.player:
                positions = new_blobs[hashes] #THIS IS A BLOB OF THE OTHER PLAYER
                if len(self.get_liberties_of_blob(positions)) == 0: #IF THAT BLOB, NOW HAS A LIBERTY OF ZERO
                    for position in positions:
                        o,p = position
                        new_grid[o][p] = 0
                    total_captured += len(positions)

        return total_captured,new_grid

    def get_liberties_of_opposition(self,flag): #gives u the value for the next state

        if flag:
            new_blobs = self.define_blobs()
        else:
            new_blobs = self.blobs

        total_opponent_liberties = 0
        for hashes in new_blobs:
            x,y = hashes
            if self.grid[x][y] != self.player:
                total_opponent_liberties += len(self.get_liberties_of_blob(new_blobs[hashes]))

        return total_opponent_liberties

    def heuristic(self,move):
        x,y = move[0]
        dist = abs(x-2) + abs(y-2)
        return move[3] + move[4] + move[5] + (1/(1+dist)) + (1/(1+move[6]))

    def normal_heuristic(self,move):
        x,y = move[0]
        dist = abs(x-2) + abs(y-2)
        return move[3] + move[4] + move[5] + (1/(1+dist))


    def get_possible_moves(self,depth):
        empty = []
        for i in range(0,5):
            for j in range(0,5):
                if self.grid[i][j] == 0:
                    prev = self.grid[i][j]
                    self.grid[i][j] = self.player
                    liberties = 0
                    removal = 0
                    if len(self.get_liberties_of_blob(self.get_blob((i,j)))) > 0 or self.check_removal()[0] > 0:
                        empty.append((i,j))
                    elif self.check_removal() > 0:
                        empty.append((i, j))
                    self.grid[i][j] = 0

        finale = []


        #FOR EVERY POSITION ALSO APPEND THE PROFIT OF THE OPPONENT FOR EACH MOVE (IN THIS CASE, THE HEURISTIC OF THE OPPONENT's BEST MOVE IN NEXT ITERATION)
        for position in empty:
            prev = self.grid
            x,y = position
            removal,self.grid = self.check_removal()
            #THE NEXT STATE
            #THINKING LIKE THE OPPONENT NOW ie depth = 2
            if depth > 0:
                opponent = 2 if self.player == 1 else 1
                opponent_board = board(self.grid,opponent,prev=prev)
                opponent_moves = opponent_board.get_possible_moves(depth-1)
                if len(opponent_moves) > 0:
                    opponent_moves.sort(key = lambda x: self.heuristic(x),reverse=True) #BEST OPPONENT MOVE IS ON TOP FOR THE GIVEN SCNRARIO
                    #print("OPPONENT's BEST MOVE FOR ",position," IS : ",opponent_moves[0][0])
                    #print("IE FOR ")
                    #self.print_grid()
                    #print("THE OPP IS ")
                    j,k = opponent_moves[0][0]
                    opponent_board.grid[j][k] = opponent
                    #opponent_board.print_grid()
                    opponent_board.grid[j][k] = 0
                    opp_profit = self.heuristic(opponent_moves[0])
                else:
                    opp_profit = 1000
            else:
                opp_profit = 0

            new_liberties_of_opposition = self.get_liberties_of_opposition(flag=True)
            blob = self.get_blob(position)
            liberties = self.get_liberties_of_blob(blob)
            length_of_liberties = len(liberties)
            self.grid = prev
            original_liberties_of_opposition = self.get_liberties_of_opposition(flag=False)
            loss_of_opposition_liberties = abs(original_liberties_of_opposition-new_liberties_of_opposition)
            finale.append((position,blob,liberties,length_of_liberties,removal,loss_of_opposition_liberties,opp_profit))

        return finale

class ManualPlayer():
    def __init__(self):
        self.type = 'manual'


    def get_next_action(self,go,piece_type,prev):
        '''
        :param go: A go board object
        :param piece_type: the piece used by the current player
        :return:
        '''
        current_board = board(go=go,player=piece_type,prev=prev)
        '''
        moves is a tuple of
        0 - move
        1 - blob of move
        2 - liberties of that blob after the move
        3 - len of liberties
        4 - removal
        5 - loss_of_opposition liberties
        '''

        moves = current_board.get_possible_moves(1) #get next_moves
        moves.sort(key= lambda x: current_board.heuristic(x),reverse=True) #USING THE WORST POSSIBLE SCENARIO FOR THE OPPONENT
        print("POSSIBLE MOVES FOR PLAYER %d: "%(piece_type))
        for i in moves:
            print("MOVE : ",i[0]," : LIBERTIES ",i[3]," CAPTURES : ",i[4]," LOSS OF OPPOSITION LIBERTIES : ",i[-1])
        if len(moves) == 0:
            action = "PASS"
        else:
            action = moves[0][0]
        return action

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
                    possible_placements.append((i,j))
        if not possible_placements:
            return "PASS"
        else:
            my_player = ManualPlayer()
            action =  my_player.get_next_action(go=go.board,prev=go.previous_board,piece_type=piece_type)
            #x,y = action

            writeOutput(action)
            return action


# piece_type,pp,go = readInput()
# my_player = ManualPlayer()
# action =  my_player.get_next_action(go,piece_type)
# writeOutput(action)

