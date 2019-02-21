# hangman.py
from random import randrange
from graphics import *
from button import Button

win= GraphWin("Hangman", 500,500)
win.setCoords(-20,-20,20,20)
win.setBackground("red")

##Draw Hanger
line1= Line(Point(-16,-8), Point(-16,18))
bottomLine=Line(Point(-19,-8),Point(-8,-8))
topLine= Line(Point(-16,18),Point(-8,18))
hanger= Line(Point(-8,18),Point(-8,14))
hanger.draw(win)
topLine.draw(win)
bottomLine.draw(win)
line1.draw(win)


class GraphicInterface:
    def __init__(self, win):
        self.win=win
        ##Draw Man
        self.head= Circle(Point(-8,12),2)
        self.body= Line(Point(-8,10),Point(-8,4))
        self.leftArm= Line(Point(-8,7),Point(-11,10))
        self.rightArm= Line(Point(-8,7),Point(-5,10))
        self.leftLeg= Line(Point(-8,4),Point(-5,1))
        self.rightLeg= Line(Point(-8,4),Point(-11,1))
        self.nothing= Point(20,20)
        self.bodyParts=[self.head, self.body,self.leftArm,self.rightArm,self.leftLeg, self.rightLeg,self.nothing]
        self.buttons=[]
        
        self.createButtons()
    def drawLimb(self, index):
        self.bodyParts[index].draw(self.win)

    def createButtons(self):
        buttonInfo=[(4,18,'A'),(8,18,'B'),(12,18,'C'), (16,18,'D'),
                    (4,16,'E'),(8,16,'F'),(12,16,'G'), (16,16,'H'),
                    (4,14,'I'),(8,14,'J'),(12,14,'K'),(16,14,'L'),
                    (4,12,'M'),(8,12,'N'),(12,12,'O'),(16,12,'P'),
                    (4,10,'Q'),(8,10,'R'),(12,10,'S'),(16,10,'T'),
                    (4,8,'U'),(8,8,'V'),(12,8,'W'),(16,8,'X'),
                    (4,6,'Y'),(8,6,'Z')]
        for(x,y,label) in buttonInfo:
            self.buttons.append(Button(self.win,Point(x,y),2,1.5,label))
        for i in self.buttons:
            i.activate()







class HangmanApp:

    'Implements a hangman game with a "pluggable" interface'

    def __init__(self, interface):
        self.interface = interface
        self.words = self.getWordList("words.txt")
        
    def getWordList(self, file):
        'Reads words from file and RETURNS them in a randomized list'
        file = open("words.txt", "r")
        words = []
        for line in file.readlines():
            word = line.strip() #Takes out all unnecessary white space.
            words.append(word.upper())
        for done in range(len(words)):
            pos = randrange(done, len(words))
            words[done], words[pos] = words[pos], words[done]
        return words
    
    def run(self):
        # Interactive loop to play multiple games of hangman
        playAgain = True
        while playAgain:
            word = self.words.pop(0)
            self.playGame(word)
            if self.words != []:
                playAgain = self.interface.askPlayAgain()
            else:
                self.interface.outOfWords()
                playAgain = False
        self.interface.closing()


    def playGame(self, word):
        'Plays a single game of hangman with word as the secret' 
        misses = 0
        hword = HangmanWord(word)
        self.interface.reset()
        self.interface.showWord(hword.getText())
        while not hword.isComplete() and misses < 7:
            letter = self.interface.getGuess()
            hit = hword.guess(letter)
            if hit:
                self.interface.showWord(hword.getText())
            else:
                misses = misses + 1
                self.interface.showMiss(misses)
        if hword.isComplete():
            self.interface.showWin()
        else:
            self.interface.showLoss(word)


class HangmanWord:
    
    def __init__(self, secret):
        self.secret = secret
        self.guesses = []
        
            
    def getText(self):
        # Get the letter that the user guesses.
        result = ""
        for ch in self.secret:
            if ch in self.guesses:
                #Insert the guessed letter.
                result = result + ch
            else:
                #Insert an underscore for the letter.
                result = result + '_'         
        return result
    
    def guess(self, letter):
        if letter in self.guesses:
            return 0
        self.guesses.append(letter)
        return letter in self.secret

    def isComplete(self):
        result = self.getText()
        if '_' in result:
            return 0
        else:
            return 1

class TextInterface:

    'Minimal text interface for the hangman game'

    def __init__(self, win):
        self.win=win
        self.text=Text(Point(6,-10),"Welcome To Hangman!")
        self.wordText= Text(Point(-14,-13),"Secret Word: ")
        self.revealWord= Text(Point(-5,-13),"")
        self.winOrLose= Text(Point(-0,-18),"")
        self.outWord=Text(Point(5,6),"")
        self.close= Text(Point(5,10),"")
        self.chances= Text(Point(-3,16),"7 chances")
        self.graphicInfo= GraphicInterface(win)
        self.limbIndex=0
        self.existingLimbs=[]
        
        
        self.outWord.draw(self.win)
        self.close.draw(self.win)
        self.chances.draw(self.win)
        self.winOrLose.draw(self.win)
        self.revealWord.draw(self.win)
        self.wordText.draw(self.win)
        self.text.draw(self.win)
        

    def askPlayAgain(self):
        self.text.setText("Do you want to try another word? ")
        yes= Button(self.win,Point(4,-14),3,2,"YES")
        no= Button(self.win,Point(10,-14),3,2,"NO")
        
        no.activate()
        yes.activate()
        while True:
            p= win.getMouse()
            if(no.clicked(p)):
                yes.deactivate()
                no.deactivate()
                win.close()
                quit()
            elif(yes.clicked(p)):
                yes.deactivate()
                no.deactivate()
                return True

    def reset(self):
        self.winOrLose.setText("")
        self.chances.setText("7 chances")
        self.limbIndex=0

        ##undraw limbs
        for i in self.existingLimbs:
            listOfLimbs=self.graphicInfo.bodyParts
            if(i ==listOfLimbs.index(listOfLimbs[i])):
                listOfLimbs[i].undraw()
            
        
        pass

    def showWord(self, word):
        self.revealWord.setText(word)

    def getGuess(self):
        while True:
            p= win.getMouse()
            for letter in self.graphicInfo.buttons:
                if(letter.clicked(p)):
                   return letter.getLabel().upper()

    def showMiss(self, num):
        self.graphicInfo.drawLimb(self.limbIndex)
        self.existingLimbs.append(self.limbIndex)
        self.limbIndex=self.limbIndex+1
        num= 7-num
        self.chances.setText("" + str(num)+ " chances")

    def showWin(self):
        self.winOrLose.setText("Congratulations, you win!")

    def showLoss(self, word):
        self.winOrLose.setText("I'm sorry, you're out of chances, It was "+ word.upper())


    def outOfWords(self):
        self.outWord.setText("Well, that's all the words I have!")

    def closing(self):
        self.close.setText("Thanks for playing. Goodbye!")







def textMain():
    #'Testing function for the text-based version of hangman'
    interface = TextInterface(win)
    HangmanApp(interface).run()    

if __name__ == '__main__':
    textMain()

