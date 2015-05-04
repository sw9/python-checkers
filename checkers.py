import tkinter as tk
from checkersBackend import *
import datetime as dt
import json
import os

class CheckersUI (tk.Frame):
    STICKY = tk.N + tk.S + tk.E + tk.W

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.gameStartupDialog()

    def gameStartupDialog(self):

        self.start = tk.Frame(self)
        self.start.grid(row=0)

        self.p1Name = tk.StringVar()
        self.p2Name = tk.StringVar()
        self.timer = tk.BooleanVar()

        tk.Label(self.start, text="Player 1 Name").grid(
            row=0, column=0)
        tk.Entry(self.start, textvariable=self.p1Name).grid(
            row=0, column=1)

        tk.Label(self.start, text="Player 2 Name").grid(
            row=1, column=0)
        tk.Entry(self.start,  textvariable=self.p2Name).grid(
            row=1, column=1)

        self.timerCB = tk.Checkbutton(
            self.start, text="Use timer", variable=self.timer, command=self.timerCheckBoxToggled)
        self.timerCB.grid(row = 2)

        self.timerFrame = tk.Frame(self)
        tk.Label(self.timerFrame, text="Time limit (minutes)").grid(
            row=0, column=0)
        self.timeLimitSpinbox = tk.Spinbox(self.timerFrame, from_=3, to=540)
        self.timeLimitSpinbox.grid(row=0, column=1)
        tk.Label(self.timerFrame, text="Bonus time/turn (seconds)").grid(
            row=1, column=0)
        self.timeBonusSpinbox = tk.Spinbox(self.timerFrame, from_=0, to=200)
        self.timeBonusSpinbox.grid(row=1, column=1)

        self.okButton = tk.Button(self, text="Ok", command=self.beginGame)
        self.okButton.grid(row=3, column = 0)

        self.loadButton = tk.Button(self, text="Load previous game", command=self.loadGame)
        self.loadButton.grid(row=3, column = 1)

        if os.path.isfile("checkers_game_data"):
            pass
        else:
             self.loadButton["state"] = tk.DISABLED


    def timerCheckBoxToggled(self):
        if not self.timer.get():
            self.timerFrame.grid_forget()
            self.timerCB.deselect()
            
        else:
            self.timerCB.select()
            self.timerFrame.grid(row=1)



    

    def draw(self):
        self.boardCanvas.destroy()
        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)
        
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] != None:
                    self.boardCanvas.create_image((35 + 70*i, 35 + 70*j),
                                                  image=self.checkersPieceDict[self.positions[i][j]])
        
        self.boardCanvas.bind("<Button-1>", self.clickBoard)


    def loadGame(self):                
        self.beginGameHelper()

        f = open("checkers_game_data", "r")
        j = json.load(f)
        f.close()
        
        positions = j[0]
        names = j[1]
        boolean = j[2]
        timing = j [3]
        

        self.positions = initialBoard()
        
        for i in range(8):
            for j in range(8):
                color, king = positions[str((i, j))]
                if color == -1:
                    self.positions[i][j] = None
                else:
                    self.positions[i][j] = Piece(color, king)
        
        self.timer.set(boolean["timer.get"])        
        self.timeBonusValue = timing["timeBonusSpinbox.get"]
        self.turn = timing["turn"]

        self.draw()
        self.player1Name = names["player1Name"]
        self.player2Name = names["player2Name"]

        if self.turn == 0:
            self.playerTurnLabel = tk.Label(self.game, text= "* "+ self.player1Name)
            self.playerTurnLabel.grid(row=0, column=0)
            self.playerTurnLabel2 = tk.Label(self.game, text=self.player2Name)
            self.playerTurnLabel2.grid(row=0, column=1)        

        else:
            self.playerTurnLabel = tk.Label(self.game, text= self.player1Name)
            self.playerTurnLabel.grid(row=0, column=0)
            self.playerTurnLabel2 = tk.Label(self.game, text= "* "+ self.player2Name)
            self.playerTurnLabel2.grid(row=0, column=1)

        self.timerEnabled = self.timer.get()

        if (self.timerEnabled):
            self.timeNow = dt.datetime.now()

            self.player1Clock = dt.timedelta(minutes = int(self.timeLimitSpinbox.get()))
            self.player2Clock = dt.timedelta(minutes = int(self.timeLimitSpinbox.get()))

            hours, remainder = divmod(self.player1Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

            hours, remainder = divmod(self.player2Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)
            
            self.alarmID = self.game.after(250, self.updateClocks)

        else:
            self.pauseClocksButton.grid_forget()


    def saveGame(self):
        obj = dict()
        for i in range(8):
            for j in range(8):
                if self.positions[i][j] == None:
                    obj[str((i, j))] = (-1, False)
                else:
                    color = self.positions[i][j].color
                    king = self.positions[i][j].king
                    obj[str((i, j))] = (color, king)


        names = dict()
        names["player1Name"] = self.player1Name
        names["player2Name"] = self.player2Name

        boolean = dict()
        boolean["timer.get"] = self.timer.get()
        
        timing = dict()
        timing["player1Clock"] = self.player1Clock.seconds
        timing["player2Clock"] = self.player2Clock.seconds
        timing["timeBonusSpinbox.get"] = self.timeBonusValue
        timing["turn"] = self.turn

        ret = [obj, names, boolean, timing]
        
        json_str = json.dumps(ret)
        out = open("checkers_game_data", "w")
        out.write(json_str)
        out.close()

        self.quit()

    def beginGameHelper(self):
        self.timeBonusValue = self.timeBonusSpinbox.get()
        self.okButton.grid_forget()
        self.timerFrame.grid_forget()
        self.start.grid_forget()
        self.loadButton.grid_forget()

        self.game = tk.Frame(self)
        self.game.grid(row=0)        

        self.clockLabel1 = tk.Label(self.game, text="")
        self.clockLabel2 = tk.Label(self.game, text="")


        self.player1Clock = dt.timedelta(0)
        self.player2Clock = dt.timedelta(0)

        hours, remainder = divmod(self.player1Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        hours, remainder = divmod(self.player2Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)


        self.clockLabel1.grid(row=1, column=0)
        self.clockLabel2.grid(row=1, column=1)

        self.backgroundPhoto = tk.PhotoImage(file="diagram.gif")
        self.checkersPieceDict = dict()
        photo = tk.PhotoImage(file = "wm.gif")
        self.checkersPieceDict[Piece(0)] = photo
        photo = tk.PhotoImage(file = "bm.gif")
        self.checkersPieceDict[Piece(1)] = photo

        photo = tk.PhotoImage(file = "wk.gif")
        self.checkersPieceDict[Piece(0, True)] = photo

        photo = tk.PhotoImage(file = "bk.gif")
        self.checkersPieceDict[Piece(1, True)] = photo


        self.boardCanvas = tk.Canvas(self.game, width=560, height=560)
        self.boardCanvas.grid(row=2, column=0, columnspan=2)
        self.boardCanvas.create_image((280, 280), image=self.backgroundPhoto)
        self.boardCanvas.bind("<Button-1>", self.clickBoard)

        
        self.statusLabel = tk.Label(self.game, text="")
        self.statusLabel.grid(row = 3, column = 0, columnspan =2)

        tk.Button(self.game, text="Resign", command=self.resignGame).grid(
            row=4, column=0)

        self.offerDrawButton = tk.Button(
            self.game, text="Offer Draw", command=self.offerDraw)
        self.offerDrawButton.grid(row=4, column=1)

        self.acceptDrawButton = tk.Button(
            self.game, text="Accept Draw", command=self.acceptDraw)

        self.pauseClocksButton = tk.Button(
            self.game, text="Pause Clocks", command=self.pauseClocks)
        self.pauseClocksButton.grid(row=5, column=0)

        self.resumeClocksButton = tk.Button(
            self.game, text="Resume Clocks", command=self.resumeClocks)
        
        tk.Button(self.game, text="Save Game", command=self.saveGame).grid(row=5, column=1)

        self.selected = False
        self.drawOffered = False



    def beginGame(self):


        self.beginGameHelper()

        self.positions = initialBoard()
        self.draw()

        if (self.p1Name.get() == ""):
            self.player1Name = "Player 1"
        else:
            self.player1Name = self.p1Name.get()

        if (self.p2Name.get() == ""):
            self.player2Name = "Player 2"
        else:
            self.player2Name = self.p2Name.get()

        self.playerTurnLabel = tk.Label(self.game, text= "* "+ self.player1Name)
        self.playerTurnLabel.grid(row=0, column=0)
        self.playerTurnLabel2 = tk.Label(self.game, text=self.player2Name)
        self.playerTurnLabel2.grid(row=0, column=1)
        
        self.turn = 0
                
        self.timerEnabled = self.timer.get()
        if (self.timerEnabled):
            self.timeNow = dt.datetime.now()

            self.player1Clock = dt.timedelta(minutes = int(self.timeLimitSpinbox.get()))
            self.player2Clock = dt.timedelta(minutes = int(self.timeLimitSpinbox.get()))

            hours, remainder = divmod(self.player1Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

            hours, remainder = divmod(self.player2Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)
            
            self.alarmID = self.game.after(250, self.updateClocks)

        else:
            self.pauseClocksButton.grid_forget()


    def clickBoard(self, event):
        print(self.turn)
        if noMoveDetection(self.positions, self.turn):
            self.statusLabel["text"] = "No possible moves, you have lost"
            self.resignGame()

        jmpDetectLst = jumpDetection(self.positions, self.turn)

        if self.selected == False:
            ptx, pty = pixelToInt(event.x, event.y)

            if (self.positions[ptx][pty] == None):
                self.statusLabel["text"] = "No piece selected"
                return
            else:
                if (self.positions[ptx][pty].color != self.turn):
                    self.statusLabel["text"] = "Wrong color selected"
                    return
                else:
                    s = set(jmpDetectLst)
                    if len(jmpDetectLst) != 0 and ((ptx, pty) not in s):
                        self.statusLabel["text"] = "Incorrect selection. You have to jump"
                        return
                    else:
                        self.selected = True
                        self.selectedPt = (ptx, pty)
                        self.statusLabel["text"] = str(self.selectedPt) +  " selected"
                        return
        else:
            ptx, pty = pixelToInt(event.x, event.y)
            self.move(ptx, pty)
    
    def setPlayer1(self):
        
        if (self.timerEnabled):
            self.pauseClocks()
            self.player2Clock = self.player2Clock + dt.timedelta(seconds = int(self.timeBonusValue))
            self.resumeClocks()

        self.playerTurnLabel["text"] = "* "+ self.player1Name
        self.playerTurnLabel2["text"] = self.player2Name
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 0
        
        if (self.drawOffered):
            self.offerDrawButton.grid_forget()
            self.acceptDrawButton.grid(row =4, column = 1)
            self.drawOffered = False
        else:
            self.acceptDrawButton.grid_forget()
            self.offerDrawButton.grid(row =4, column = 1)
            self.offerDrawButton["state"] = tk.NORMAL


    def setPlayer2(self):
        if (self.timerEnabled):
            self.pauseClocks()
            self.player1Clock = self.player1Clock + dt.timedelta(seconds = int(self.timeBonusValue))
            self.resumeClocks()


        self.playerTurnLabel["text"] = self.player1Name
        self.playerTurnLabel2["text"] = "* " + self.player2Name
        self.selected = False
        self.statusLabel["text"] = ""
        self.turn = 1


        if (self.drawOffered):
            self.offerDrawButton.grid_forget()
            self.acceptDrawButton.grid(row =4, column = 1)
            self.drawOffered = False
        else:
            self.acceptDrawButton.grid_forget()
            self.offerDrawButton.grid(row = 4, column = 1)
            self.offerDrawButton["state"] = tk.NORMAL
            
    def move(self, x2, y2):
        ptx, pty = self.selectedPt
        jmplst = jumpPositions(self.positions[ptx][pty], ptx, pty, self.positions)
        mvlst = movePositions(self.positions[ptx][pty], ptx, pty, self.positions)
        
        if len(jmplst) != 0:
            s = set(jmplst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = str(self.selectedPt) +  " selected, you have to take the jump"
                return
            else:
                delX = int((x2+ptx)/2.0)
                delY = int((y2+pty)/2.0)
                self.positions[delX][delY] = None
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None
                self.selected = True
                self.selectedPt = (x2, y2)

                convertToKing(self.positions)
                self.draw()

                jmplst2 = jumpPositions(self.positions[x2][y2], x2, y2, self.positions)
                
                if len(jmplst2) != 0:
                    self.statusLabel["text"] = str(self.selectedPt) +  " selected, you must jump again"
                    return

                else:
                    if (noOpponentPieceDetection(self.positions, self.turn)):
                        self.winGame()
                        print ("won game")

                    else:
                        if self.turn == 0:
                            self.setPlayer2()
                        else:
                            self.setPlayer1()
        else:
            s = set(mvlst)
            if ((x2, y2) not in s):
                self.statusLabel["text"] = "Invalid move. Select a piece and try again"
                self.selected = False
                return
            else:
                self.positions[x2][y2] = self.positions[ptx][pty]
                self.positions[ptx][pty] = None

                convertToKing(self.positions)
                self.draw()

                if self.turn == 0:
                    self.setPlayer2()
                else:
                    self.setPlayer1()
                

    def endGame(self):
        self.game.destroy()

        self.endFrame = tk.Frame(self)
        self.endFrame.grid(row = 0)
        self.endGameResult = tk.Label(self.endFrame, text= "")
        self.endGameResult.grid(row=0)
        tk.Button(self.endFrame, text="New Game", command=self.endGameNew).grid(row=1)
        tk.Button(self.endFrame, text="Exit", command=self.quit).grid(row=2)
    
    def endGameNew(self):
        self.endFrame.destroy()
        self.loadButton.destroy()
        self.okButton.destroy()
        self.timerFrame.destroy()
        self.start.destroy()
        
        self.gameStartupDialog()

    def resignGame(self):
        self.endGame()

        if self.turn == 0:
            winner = self.player2Name
            loser = self.player1Name
            
        else:
            winner = self.player1Name
            loser = self.player2Name

        self.endGameResult["text"] = winner + " won this game. " + loser + " lost."
        
    def winGame(self):
        self.endGame()

        if self.turn == 0:
            winner = self.player1Name
            loser = self.player2Name
            
        else:
            winner = self.player2Name
            loser = self.player1Name

        self.endGameResult["text"] = winner + " won this game. " + loser + " lost."


    def pauseClocks(self):
        self.game.after_cancel(self.alarmID)
        self.timerEnabled = False
        time = dt.datetime.now()
        d = time - self.timeNow
        
        if (self.turn == 0):
            self.player1Clock = self.player1Clock - d
      
        else:
            self.player2Clock = self.player2Clock - d

        hours, remainder = divmod(self.player1Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        hours, remainder = divmod(self.player2Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)


        self.pauseClocksButton.grid_forget()
        self.resumeClocksButton.grid(row = 5, column = 0)

    def resumeClocks(self):
        self.timeNow = dt.datetime.now()
        self.timerEnabled = True
        self.alarmID = self.game.after(250, self.updateClocks)
        
        self.pauseClocksButton.grid(row = 5, column = 0)
        self.resumeClocksButton.grid_forget()

        hours, remainder = divmod(self.player1Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        hours, remainder = divmod(self.player2Clock.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

    def updateClocks(self):
        if (self.timerEnabled):
            time = dt.datetime.now()
            d = time - self.timeNow

            if (self.turn == 0):
                self.player1Clock = self.player1Clock - d      
            else:
                self.player2Clock = self.player2Clock - d

            hours, remainder = divmod(self.player1Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel1["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

            hours, remainder = divmod(self.player2Clock.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.clockLabel2["text"] = str(hours) + ":" + str(minutes) + ":" + str(seconds)

            self.timeNow = time
            self.alarmID = self.game.after(250, self.updateClocks)


    def acceptDraw(self):
        self.endGame()
        self.endGameResult["text"] = "This game was a draw"

    def offerDraw(self):
        self.drawOffered = True
        self.offerDrawButton["state"] = tk.DISABLED



def pixelToInt(x, y):
    retx = 0
    retx_tot = 70
    
    rety = 0
    rety_tot = 70
    
    while (x > retx_tot and retx < 7):
        retx = retx + 1
        retx_tot = retx_tot + 70
        
    while (y > rety_tot and rety < 7):
        rety = rety + 1
        rety_tot = rety_tot + 70
        
    return (retx, rety)
    
def tkinter_main():
    root = tk.Tk()
    app = CheckersUI(master=root)
    app.mainloop()

tkinter_main()