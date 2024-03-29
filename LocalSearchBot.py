from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from BotStep import BotStep
import numpy as np
import copy
import time

class LocalSearchBot(Bot):
    def obj_function(self, state:GameState):
        #get player modifier
        result = 0
        player_modifier = -1 if state.player1_turn else 1
        
        for row in state.board_status:
            for square in row:
                if (square ==  4 * player_modifier):
                    #Fungsi nilai(kotak) akan memberikan nilai 1 untuk kotak player tersebut
                    result+=1
                elif (abs(square) ==  2):
                    # 0.75 untuk kotak dengan 2 sisi
                    result+=0.75
                elif (abs(square) ==  1 or square==0):
                    #0.5 untuk kotak dengan 0 atau 1 sisi
                    result+=0.5
        return result

    
    def get_step_maximal(self,bs1:BotStep, bs2:BotStep):
        if (bs1 > bs2):
            res = BotStep(bs1.get_value())
            res.set_steps(copy.deepcopy(bs1.get_steps()))
            return res
        else:
            res = BotStep(bs2.get_value())
            res.set_steps(copy.deepcopy(bs2.get_steps()))
            return res

    def get_step_minimal(self,bs1:BotStep, bs2:BotStep):
        if (bs1 < bs2):
            res = BotStep(bs1.get_value())
            res.set_steps(copy.deepcopy(bs1.get_steps()))
            return res
        else:
            res = BotStep(bs2.get_value())
            res.set_steps(copy.deepcopy(bs2.get_steps()))
            return res

    
    def hill_climbing(self, curr_state:GameState, player_modifier):
        number_of_dots = 4

        time_start = time.time()
        max_val = BotStep(float('-inf'))
        end_loop = False
        rows, cols = np.where(curr_state.row_status == 0)
        for i, j in zip(rows, cols):
            new_state = GameState(
                copy.deepcopy(curr_state.board_status),
                copy.deepcopy(curr_state.row_status),
                copy.deepcopy(curr_state.col_status),
                curr_state.player1_turn
            )

            if i < (number_of_dots - 1) and j < (number_of_dots - 1):
                new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
            if (i > 0):
                new_state.board_status[i - 1][j] = (abs(new_state.board_status[i - 1][j]) + 1) * player_modifier
            new_state.row_status[i][j] = 1

            new_state_val = BotStep(self.obj_function(new_state))
            new_state_val.set_steps([["row", i, j]])

            max_val = self.get_step_maximal(max_val, new_state_val)

            time_current = time.time()
            if (round(time_current - time_start) >= 5):
                end_loop = True
                break
            
        rows, cols = np.where(curr_state.col_status == 0)
        if not end_loop:
            for i, j in zip(rows, cols):
                new_state = GameState(
                    copy.deepcopy(curr_state.board_status),
                    copy.deepcopy(curr_state.row_status),
                    copy.deepcopy(curr_state.col_status),
                    curr_state.player1_turn
                )

                if i < (number_of_dots - 1) and j < (number_of_dots - 1):
                    new_state.board_status[i][j] = (abs(new_state.board_status[i][j]) + 1) * player_modifier
                if (j > 0):
                    new_state.board_status[i][j - 1] = (abs(new_state.board_status[i][j - 1]) + 1) * player_modifier
                new_state.col_status[i][j] = 1

                new_state_val = BotStep(self.obj_function(new_state))
                new_state_val.set_steps([["col", i, j]])

                max_val = self.get_step_maximal(max_val, new_state_val)

        return max_val

    def get_action(self, state: GameState) -> GameAction:
        player_modifier = -1 if state.player1_turn else 1
        result = self.hill_climbing(state, player_modifier)

        step_type = result.get_first_step_type()
        step_pos = (result.get_first_step_y(), result.get_first_step_x())

        return GameAction(step_type, step_pos)