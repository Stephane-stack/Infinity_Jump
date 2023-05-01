import pyxel

# taille de la fenetre 128x128 pixels
taille=128
pyxel.init(taille, taille, title="Infinity jump")
liste_PF=[[20,100],[70,65],[25,25],[76,-5],[20,-40],[50,-70],[76,-105],[20,-140],[60,-180],[25,-220],[70,-250],[25,-285],[76,-325],[20,-360],[70,-390],[25,-425],[70,-450],[25,-485],[76,-515],[20,-545],[50,-575],[76,-605],[20,-640],[60,-680],[25,-720],[70,-750],[25,-785],[76,-825],[20,-860],[70,-890],[25,-925],[70,-960],[25,-1000],[76,-1030],[20,-1065],[50,-1100],[76,-1130],[20,-1165],[60,-1195],[25,-1225],[70,-1255],[25,-1290],[76,-1330],[20,-1365],[70,-1395],[25,-1430],[70,-1455],[25,-1495],[76,-1525],[20,-1555],[50,-1585],[76,-1620],[20,-1655],[60,-1695],[25,-1735],[70,-1765],[25,-1800],[76,-1840],[20,-1875],[70,-1905],[25,-1945]]
perso_x=liste_PF[0][0]+16
perso_y=liste_PF[0][1]-8
perso_x0 = 0
perso_y0 = 0
x0=0
y0=0
repos = True
i=1
gagné=True
score = 0
longueur=32
#chargement du gamePack
pyxel.load("14.pyxres")

def draw():
    global perso_x, perso_y, gagné, repos
    pyxel.cls(0)
    #Blitter les murs
    pyxel.blt(0,0,1,6,0,20,taille,2)
    pyxel.blt(taille-20,0,1,48,0,20,taille,2)
    #Blitter la cascade
    pyxel.blt(20,6,2,14,0,88,116,2)
    #Blitter le personnage en fonction de son orientation
    if i == 1:
        pyxel.blt(perso_x, perso_y,0,0,16,8,8,2)
    if i == 2:
        pyxel.blt(perso_x, perso_y,0,0,64,8,8,2) 
    #Plateformes
    for plateforme in liste_PF:
        pyxel.blt(plateforme[0], plateforme[1],0,0,72,longueur,5,2)
    #Score
    pyxel.text(102,8,str(score),9)
    #Gagner
    if (liste_PF[-1][0]-4<perso_x<liste_PF[-1][0]+28) and (liste_PF[-1][1]-9<perso_y<liste_PF[-1][1]-7):
        repos=True
        gagné=False
        pyxel.blt(36,6,0,0,80,58,13)
    #Perdre
    if perso_y>taille:
        repos=True
        gagné=False
        pyxel.text(50,20,"Perdu !",9)
    #Code triche
    if pyxel.btn(pyxel.KEY_A) and gagné==False:
        gagné=True
        perso_x=liste_PF[score][0]+16
        perso_y=liste_PF[score][1]-8
        
def deplacer_perso(x, y):
    global perso_y, perso_x0, perso_y0, repos, i, score
    #déplacement avec les touches de directions
    d = 3
    if gagné and repos:
        if pyxel.btn(pyxel.KEY_RIGHT) and perso_x < taille-29 :
            x = x + d
            i = 1
        if pyxel.btn(pyxel.KEY_LEFT) and perso_x > 21 :
            x = x - d
            i = 2
        for plateforme in liste_PF:
            if plateforme[0]-4<perso_x<plateforme[0]+28 and 3<plateforme[1]-perso_y<=8 and perso_x>=20 and perso_x<=taille-28:
                if pyxel.btnr(pyxel.KEY_SPACE):
                    #declenche le saut
                    perso_y=perso_y-3
                    perso_x0=perso_x
                    perso_y0=perso_y
                    repos = not repos
                    score = score + 1
    return x,y

def sauter():
    global perso_x, perso_y
    if not repos :
        dx = perso_x - perso_x0
        #Paramètres parabole
        a = .03
        b = -1.6
        c = perso_y0
        if i == 1 :
            perso_y = a*dx**2+b*dx+c
            perso_x = perso_x + 1 #translation rectiligne uniforme selon x
            tester_collision()
        if i == 2 :
            perso_y = a*(-dx)**2+b*(-dx)+c
            perso_x = perso_x - 1
            tester_collision()
   
def tester_collision():
    global perso_y, repos
    for plateforme in liste_PF:
        #Après un saut
        if plateforme[0]-4<perso_x<plateforme[0]+28 and 3<plateforme[1]-perso_y<=8:
            repos = True
            perso_y=plateforme[1]-8
            perso_y=perso_y+.5
            break
        #Sortie de plateforme et tomber avec la plateforme
        if repos and (perso_x<=plateforme[0]-4 or perso_x>=plateforme[0]+28):
            perso_y=perso_y+.1
    #Contre un mur
    if not repos and (perso_x+8>=taille-20 or perso_x<=20):
        repos = True
            
def deplacer_plateformes():
    if gagné:
        for plateforme in liste_PF:
            plateforme[1]=plateforme[1]+.5

def update():
    global perso_x, perso_y
    perso_x, perso_y = deplacer_perso(perso_x, perso_y)
    sauter()
    tester_collision()
    deplacer_plateformes()
        
pyxel.run(update, draw)