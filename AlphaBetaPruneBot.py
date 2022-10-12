from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from BotStep import BotStep
import numpy as np
import copy
import time

class AlphaBetaPruneBot(Bot):
    def obj_function(self, state:GameState):
        #get player modifier
        result = 0
        player_modifier = -1 if state.player1_turn else 1
        for row in state.board_status:
            for square in row:
                if (square ==  4 * player_modifier):
                    #Fungsi nilai(kotak) akan memberikan nilai 1 untuk kotak player tersebut
                    result+=1
                elif (abs(square) ==  3):
                    # 0.75 untuk kotak dengan 3 sisi
                    result+=0.75
                elif (abs(square) ==  1 or square==0):
                    #0.5 untuk kotak dengan 0 atau 1 sisi
                    result+=0.5
        return result * player_modifier

    def check_if_board_full(self,state:GameState):
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        return all_row_marked and all_col_marked
    
    def get_step_minimal(self,bs1:BotStep, bs2:BotStep):
        if (bs1 < bs2):
            res = BotStep(bs1.get_value())
            res.set_steps(copy.deepcopy(bs1.get_steps()))
            return res
        else:
            res = BotStep(bs2.get_value())
            res.set_steps(copy.deepcopy(bs2.get_steps()))
            return res
    def get_step_maximal(self,bs1:BotStep, bs2:BotStep):
        if (bs1 > bs2):
            res = BotStep(bs1.get_value())
            res.set_steps(copy.deepcopy(bs1.get_steps()))
            return res
        else:
            res = BotStep(bs2.get_value())
            res.set_steps(copy.deepcopy(bs2.get_steps()))
            return res

    def minimax(self,curr_state:GameState, alpha:BotStep, beta:BotStep,player_modifier, steps_recorded:list, time_count, depth=0):
        #function ini bakal rekursif, jadi basisnya adalah board_statusnya udah penuh atau waktu udah 5 detik

        number_of_dots = 4

        max_depth = 24 #ini max_depth berdasarkan jumlah garisnya, idk, cuma biar operasinya makin hemat aja

        time_now = time.time()
        remainder = time_now - time_count
        
        if (self.check_if_board_full(curr_state) or round(remainder) >= 5 or depth >= max_depth):
            val = BotStep(self.obj_function(curr_state))
            val.set_steps(steps_recorded)
            return val

        #  === MINIMIZING === 
        end_loop = False
        if (player_modifier == -1):

            min_val = BotStep(float('inf')) # negative infinity

            #loop dari data garis row yang belum diisi
            rows,cols = np.where(curr_state.row_status == 0)
            for i, j in zip(rows, cols):
                #generate semua kemungkinan langkah yang mungkin terjadi row-wise

                #buat new state, habis itu copy 
                new_state = GameState(
                    copy.deepcopy(curr_state.board_status),
                    copy.deepcopy(curr_state.row_status),
                    copy.deepcopy(curr_state.col_status),
                    False if player_modifier==-1 else True
                )

                if i < (number_of_dots-1) and j < (number_of_dots-1):
                    new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
                if (i > 0):
                    new_state.board_status[i-1][j] = (abs(new_state.board_status[i-1][j]) + 1) * player_modifier
                new_state.row_status[i][j] = 1

                #state telah dibuat, saatnya rekursif
                steps_recorded.append(["row",i,j]) #ini biar mengetahui langkah yang bakal diambil kalau ternyata ini merupakan langkah optimal
                val = self.minimax(new_state, alpha, beta ,1, steps_recorded, time_count,depth+1)

                #bandingkan min_val dengan val yang didapat. Ambil paling kecil

                min_val = self.get_step_minimal(min_val, val) #comparison
                beta = self.get_step_minimal(beta, min_val) #comparison

                steps_recorded.clear()

                if beta <= alpha:
                    end_loop = True
                    break

            #loop dari data garis col yang belum diisi
            if not end_loop:
                rows,cols = np.where(curr_state.col_status == 0)
                for i, j in zip(rows, cols):
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    #buat new state, habis itu copy 
                    new_state = GameState(
                        copy.deepcopy(curr_state.board_status),
                        copy.deepcopy(curr_state.row_status),
                        copy.deepcopy(curr_state.col_status),
                        False if player_modifier==-1 else True
                    )

                    if i < (number_of_dots-1) and j < (number_of_dots-1):
                        new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
                    if (j > 0):
                        new_state.board_status[i][j-1] = (abs(new_state.board_status[i][j-1]) + 1) * player_modifier
                    new_state.col_status[i][j] = 1

                    #state telah dibuat, saatnya rekursif
                    steps_recorded.append(["col",i,j])
                    val = self.minimax(new_state, alpha, beta ,1, steps_recorded,time_count,depth+1)

                    #bandingkan min_val dengan val yang didapat. Ambil paling kecil
                    min_val = self.get_step_minimal(min_val, val)
                    beta = self.get_step_minimal(beta, min_val)

                    steps_recorded.clear()

                    if beta <= alpha:
                        break  
            return min_val 

        #  === MAXIMIZING === 
        if (player_modifier == 1):

            max_val = BotStep(float('-inf')) # positive infinity

            #loop dari data garis row yang belum diisi
            rows,cols = np.where(curr_state.row_status == 0)
            for i, j in zip(rows, cols):
                #generate semua kemungkinan langkah yang mungkin terjadi
                #buat new state, habis itu copy
                new_state = GameState(
                    copy.deepcopy(curr_state.board_status),
                    copy.deepcopy(curr_state.row_status),
                    copy.deepcopy(curr_state.col_status),
                    False if player_modifier==-1 else True
                )

                if j < (number_of_dots-1) and i < (number_of_dots-1):
                    new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
                if (i > 0):
                    new_state.board_status[i-1][j] = (abs(new_state.board_status[i-1][j]) + 1) * player_modifier
                new_state.row_status[i][j] = 1

                #state telah dibuat, saatnya rekursif
                steps_recorded.append(["row",i,j])
                val = self.minimax(new_state, alpha, beta ,-1, steps_recorded, time_count,depth+1)

                #bandingkan min_val dengan val yang didapat. Ambil paling kecil
                max_val = self.get_step_maximal(max_val, val)
                alpha = self.get_step_maximal(alpha, max_val)

                steps_recorded.clear()

                if beta <= alpha:
                    end_loop = True
                    break   
            
            #loop dari data garis col yang belum diisi
            if not end_loop:
                rows,cols = np.where(curr_state.col_status == 0)
                for i, j in zip(rows, cols):
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    #buat new state, habis itu copy 
                    new_state = GameState(
                        copy.deepcopy(curr_state.board_status),
                        copy.deepcopy(curr_state.row_status),
                        copy.deepcopy(curr_state.col_status),
                        False if player_modifier==-1 else True
                    )

                    if i < (number_of_dots-1) and j < (number_of_dots-1):
                        new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
                    if (j > 0):
                        new_state.board_status[i][j-1] = (abs(new_state.board_status[i][j-1]) + 1) * player_modifier
                    new_state.col_status[i][j] = 1

                    #state telah dibuat, saatnya rekursif
                    steps_recorded.append(["col",i,j])
                    val = self.minimax(new_state, alpha, beta ,-1, steps_recorded, time_count,depth+1)
                    #bandingkan min_val dengan val yang didapat. Ambil paling kecil
                    max_val = self.get_step_maximal(max_val, val)
                    alpha = self.get_step_maximal(alpha, max_val)

                    steps_recorded.clear()

                    if beta <= alpha:
                        break
            return max_val    
        
    
    def get_action(self, state: GameState) -> GameAction:
        alpha = BotStep(float("-inf"))
        beta = BotStep(float("inf"))
        result = self.minimax(state, alpha, beta, 1, [], time.time())

        step_type = result.get_first_step_type()
        step_pos = (result.get_first_step_y(), result.get_first_step_x())
        print(step_type, step_pos)

        return GameAction(step_type, step_pos)

