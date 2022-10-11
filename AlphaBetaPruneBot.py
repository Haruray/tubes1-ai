from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from BotStep import BotStep
import numpy as np

class RandomBot(Bot):
    def obj_function(self, state:GameState):
        #get player modifier
        player_modifier = -1 if state.player1_turn else 1
        result = 0
        for row in state.board_status:
            for square in row:
                if (square == player_modifier * 4):
                    #Fungsi nilai(kotak) akan memberikan nilai 1 untuk kotak player tersebut
                    result+=1
                elif (square == player_modifier * 3):
                    # 0.75 untuk kotak dengan 3 sisi
                    result+=0.75
                elif (square == player_modifier * 1 or square==0):
                    #0.5 untuk kotak dengan 0 atau 1 sisi
                    result+=0.5
        return result

    def check_if_board_full(state:GameState):
        all_row_marked = np.all(state.row_status == 1)
        all_col_marked = np.all(state.col_status == 1)
        return all_row_marked and all_col_marked

    def minimax(self,curr_state:GameState, alpha:BotStep, beta:BotStep, player_modifier):
        #function ini bakal rekursif, jadi basisnya adalah board_statusnya udah penuh
        
        if self.check_if_board_full(curr_state):
            return self.obj_function(self, curr_state)

        #minimizing
        if (player_modifier == -1):

            minVal = BotStep(float('-inf')) # negative infinity

            #loop dari data garis row yang belum diisi
            rows,cols = np.where(curr_state.row_status == 0)
            for i in rows:
                for j in cols:
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    pass
            
            #loop dari data garis col yang belum diisi
            rows,cols = np.where(curr_state.col_status == 0)
            for i in rows:
                for j in cols:
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    pass

        #maximizing
        if (player_modifier == 1):

            maxVal = BotStep(float('inf')) # positive infinity

            #loop dari data garis row yang belum diisi
            rows,cols = np.where(curr_state.row_status == 0)
            for i in rows:
                for j in cols:
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    pass
            
            #loop dari data garis col yang belum diisi
            rows,cols = np.where(curr_state.col_status == 0)
            for i in rows:
                for j in cols:
                    #generate semua kemungkinan langkah yang mungkin terjadi
                    pass
        
    
    def get_action(self, state: GameState) -> GameAction:
        pass
