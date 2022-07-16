import random
# snake water gun game
game = ["stone", "paper", "scissor"]
query = '''
0.stone
1.paper
2.scissor
3.For quit
Select any value from three:
'''
userpoint=0
computerpoint=0
user = 1
while(1):
    print(query)
    user = int(input())
    pc = random.choice(game)
    if(user==3):
        break
    elif(user==0 and pc=="paper"):
        computerpoint = computerpoint+1
    elif(user==0 and pc=="stone"):
        userpoint = userpoint+1
        computerpoint  =computerpoint+1
    elif(user==0 and pc=="scissor"):
        userpoint = userpoint+1
    elif (user == 1 and pc == "paper"):
        computerpoint = computerpoint + 1
        userpoint  = userpoint+1
    elif (user == 1 and pc == "stone"):
        userpoint = userpoint + 1
        computerpoint = computerpoint + 1
    elif (user == 1 and pc == "scissor"):
        computerpoint = computerpoint+1
    elif (user == 2 and pc == "paper"):
        userpoint = userpoint+1
    elif (user == 2 and pc == "stone"):
        computerpoint = computerpoint + 1
    else:
        userpoint = userpoint + 1
        computerpoint = computerpoint+1

if(userpoint>computerpoint):
    print("YOU WIN")
elif(computerpoint>userpoint):
    print("YOU LOSS")
else:
    print("DRAW")


