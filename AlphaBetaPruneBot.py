from Bot import Bot
from GameAction import GameAction
from GameState import GameState
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

    def minimax(game_board, alpha, beta, player_modifier):
        #generate semua kemungkinan langkah yang mungkin terjadi
        #kemungkinan terjadi adalah semua garis (jumlahnya adalah 24) dikurangi garis yang sudah digambar
        possible_move_count = 24

    
    def get_action(self, state: GameState) -> GameAction:
        pass
