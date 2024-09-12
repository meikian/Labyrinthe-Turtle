import png
import json
import turtle
import random
import time

def load_maze_txt(chemin_fic):
    laby_txt = []
    fichier = open(chemin_fic,'r')
    i = 0
    myline = fichier.readline()
    while myline:
        laby_txt.append([])
        for j in range (0,len(myline)-1,1):
            laby_txt[i].append(myline[j])       
        myline = fichier.readline()
        i+=1
    fichier.close()
    return laby_txt

def save_maze_png(contenu_fic, case_largeur_pix, chemin_png):
    case_largeur = []
    for ligne in contenu_fic:
        nouvelle_ligne = []
        for elem in ligne:
            for counter in range(case_largeur_pix):
                nouvelle_ligne.append(elem)
        for counter in range(case_largeur_pix):
            case_largeur.append(nouvelle_ligne)
    pixel_colour = []
    i = 0
    for line in case_largeur:
        pixel_colour.append([])
        for case in line:
            if case == '0':
                pixel_colour[i].append(255)
                pixel_colour[i].append(255)
                pixel_colour[i].append(255)
            elif case == '1':
                pixel_colour[i].append(255)
                pixel_colour[i].append(0)
                pixel_colour[i].append(0)                
            elif case == '2':
                pixel_colour[i].append(0)
                pixel_colour[i].append(0)
                pixel_colour[i].append(0)                
            elif case == '3':
                pixel_colour[i].append(0)
                pixel_colour[i].append(255)
                pixel_colour[i].append(0)                
        i+=1

    fic_png = open(chemin_png, 'wb')
    w = png.Writer(len(pixel_colour), len(pixel_colour), greyscale=False)
    w.write(fic_png, pixel_colour)
    fic_png.close()
    
def load_maze_parameters(json_chemin):
    parametre = {}
    fichier = open(json_chemin,'r')
    contenu_fichier = fichier.read()
    parametre = json.loads(contenu_fichier)
    return parametre

def conversion(i,j,l,nbCases):
    x = int(-(nbCases-1)*0.5*l+i*l)
    y = int((nbCases-1)*0.5*l-j*l)
    return [x,y]

def voisins_libre(laby_txt, case):
    nb = 0
    liste = []

    if (laby_txt[case[1]][case[0]+1] == '0') and ((case[0]+1) <= (len(laby_txt)-1)):
        nb+=1
        liste.append([case[0]+1,case[1]])
    if (laby_txt[case[1]-1][case[0]] == '0') and ((case[1]-1) >= 0):
        nb+=1
        liste.append([case[0],case[1]-1])
    if (laby_txt[case[1]][case[0]-1] == '0') and ((case[0]-1) >= 0):
        nb+=1
        liste.append([case[0]-1,case[1]])
    if (laby_txt[case[1]+1][case[0]] == '0') and ((case[1]+1) <= (len(laby_txt)-1)):
        nb+=1
        liste.append([case[0],case[1]+1])
    return nb, liste

def search_exit(laby_txt, laby_img, style): 
    turtle.setup()
    turtle.title("Le labyrinthe") 
    turtle.bgpic(laby_img)
    t = turtle.Turtle()
    t.shape(style["pen_shape"])
    t.color("Blue")
    t.speed(style["pen_speed"])
    t.showturtle()
    #placement tortue au depart
    curent_pos = [0,1]
    turtle_pos = conversion(curent_pos[0],curent_pos[1],style["cell_size_png"],len(laby_txt))
    t.teleport(turtle_pos[0], turtle_pos[1])
    next_pos = [0,0]
    liste_path = []
    t.down

    while laby_txt[curent_pos[1]][curent_pos[0]+1] != '3':
        nb_v_libre, voisins = voisins_libre(laby_txt, curent_pos)
        if nb_v_libre == 0:
            next_pos = liste_path.pop(len(liste_path)-1)
            t.pencolor(style['pen_colors']['backward_pen_color'])
        else:
            next_pos = voisins[random.randint(1,nb_v_libre)-1]
            liste_path.append(next_pos)
            t.pencolor(style['pen_colors']['forward_pen_color'])

        turtle_pos = conversion(next_pos[0],next_pos[1],style["cell_size_png"],len(laby_txt)) 
        curent_pos = next_pos
        laby_txt[curent_pos[1]][curent_pos[0]] = '-1'
 
        t.goto(turtle_pos[0], turtle_pos[1])
        time.sleep(0.1)
    turtle_pos = conversion(curent_pos[0]+1,curent_pos[1],style["cell_size_png"],len(laby_txt)) 
    t.goto(turtle_pos[0], turtle_pos[1])




    



    turtle.done()

def generate_random_maze_txt(nb_case, chemin_fichier):
    laby_txt = []
    "initialisation de la liste avec des 0 partout"
    for i in range(0, nb_case):
        laby_txt.append([])
        for j in range (0,nb_case):
            if i == 0 or i == nb_case-1:
                laby_txt[i].append('2')
            elif j==0 or j== nb_case-1:
                laby_txt[i].append('2')
            else:
                laby_txt[i].append('0')
    laby_txt[1][0] = '1'
    sortie = [nb_case-1,random.randint(1,nb_case-2)]
    laby_txt[sortie[1]][sortie[0]] = '3'
    pos = [0,1]
     
    while laby_txt[pos[1]][pos[0]+1] !='3':

        direction = random.randint(0,1)
        sens = random.randint(0,30)
        if direction == 0:
            if (sens <20) and ((pos[0]+1) < nb_case-1):
                pos[0] += 1
            elif (sens >20) and ((pos[0]-1) >= 1):
                pos[0] = pos[0]-1

        else:
            diff = sortie[1] - pos[1]
            if diff > 0 and (sens < 25) and (pos[1]+1 < nb_case-1) and laby_txt[pos[1]+1][pos[0]]!='2':
                pos[1] += 1
            elif diff > 0 and (sens > 25) and (pos[1]-1 >0) and laby_txt[pos[1]+1][pos[0]]!='2':
                pos[1] -= 1
            elif diff <0 and (sens < 25) and (pos[1]-1 > 0) and laby_txt[pos[1]-1][pos[0]]!='2':
                pos[1] -= 1
            elif (pos[1]+1 < nb_case-1) and laby_txt[pos[1]+1][pos[0]]!='2':
                pos[1] += 1

 
        laby_txt[pos[1]][pos[0]] = '4'

    for i in range(0, nb_case):
        for j in range (0,nb_case):
            if laby_txt[j][i] == '0':
                if random.randint(0,10) < 8:
                    laby_txt[j][i] = '2'
            if laby_txt[j][i] == '4':
                laby_txt[j][i] = '0'

    laby_txt[1][0] = '1'
    return laby_txt

def main():
    parametre = load_maze_parameters("param.json")
    laby_txt = load_maze_txt(parametre["maze_files"]["description_file"])
    save_maze_png(laby_txt,parametre["style"]["cell_size_png"] , parametre["maze_files"]["maze_file_png"])
    
    laby_txt = generate_random_maze_txt(35,"laby/test.txt")
    save_maze_png(laby_txt,parametre["style"]["cell_size_png"],"laby/test.png")
    search_exit(laby_txt,parametre["maze_files"]["maze_file_png"], parametre["style"])

main()