import random
import numpy as np
import matplotlib.pyplot as plt

#lauko dydis N=l*l langeliu
l=30
#morku suteikiamas energijos keikis M, atstumas tarp morku 0.8M
M=15
#programa sustojai kai zuikis pasiekia Q kartu didesni energijos kieki nei pradinis
Q=2
#vilko ejimu kryptys
kryptys=[[1,1], [-1,1], [1,-1], [-1,-1]]
#zuikio ejimu kryptys
zuikio_ejimai=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
#Zuikio ir vilku pradines padetys
zuikis_yra=[random.choice(range(0, l, 1)),random.choice(range(0, l, 1))]
vilkas1=[[random.choice(range(1, l-1, 1)),random.choice(range(1, l-1, 1))], random.choice(kryptys)]
vilkas2=[[random.choice(range(1, l-1, 1)),random.choice(range(1, l-1, 1))], random.choice(kryptys)]
#zuikio energija zaidimo pradzioje
zuikio_E=l*l
#parametrai skirti reguliuoti zuikio ejima nesant nei morkoms nei vilkui salia jo
clock, H, V = 0, 1, 1

#sukuriame zuikio matymo lauka kaip koordinaciu zodyna
def zuikis_start():
    Zuikis_mato={}
    for i in range(1,5):
        Zuikis_mato[(i,0)], Zuikis_mato[(-i,0)], Zuikis_mato[(0,i)], Zuikis_mato[(0,-i)] = 0, 0, 0, 0
        for j in range(1,5):
            if i+j>4:
                continue
            Zuikis_mato[(i,j)], Zuikis_mato[(-i,-j)], Zuikis_mato[(-i,j)], Zuikis_mato[(i,-j)] = 0, 0, 0, 0
    return Zuikis_mato

#sukuriame vilko matymo lauka kaip koordinaciu zodyna
def vilkas_start():
    Vilkas_mato={}
    for i in range(1,5):
        Vilkas_mato[(i,0)], Vilkas_mato[(0,i)] = 0, 0
        for j in range(1,5):
            if i+j>4:
                continue
            Vilkas_mato[(i,j)]=0
    for i in range(1,4):
        Vilkas_mato[i,-1], Vilkas_mato[-1,i] = 0, 0
    Vilkas_mato[-2,2], Vilkas_mato[2,-2] = 0, 0
    return Vilkas_mato

#tikriname ka mato vilkas kontrecioje padetyje, 
#perkaiciuojam vilko matymo koordinate i koordinate aiksteles atzvilgiu
#ir tikrinam ar si koordinate sutampa su zuikio koordinate, jei taip, grazinam 
#zuikio koordinate vilko atzvilgiu
def vilkas_mato(vilkas):
    global zuikis_yra
    Vilkas_mato=vilkas_start()
    for key in Vilkas_mato:
        a,b=key[0],key[1]
        x=vilkas[0][0]+(vilkas[1][0]*a)
        y=vilkas[0][1]+(vilkas[1][1]*b)
        ziurim=[x,y]
        if ziurim == zuikis_yra:
            return key
    return False

#perskaiciuojam zuikio regejimo lauko koordinates i konkrecias koordinates aiksteles atzvilgiu
#tikriname ar sios koordinates sutampa su vilku ir morku koordinatemis
#jei sutampa, irasome i zuikio matymo lauko zodyna matomo objekto pavadinima 
def zuikis_mato():
    global zuikis_yra
    Zuikis_mato=zuikis_start()
    global vilkas1, vilkas2
    Vilkai=[vilkas1[0],vilkas2[0]]
    global Morku_zemelapis
    for key in Zuikis_mato:
        x=zuikis_yra[0]+key[0]
        y=zuikis_yra[1]+key[1]
        ziurim=[x,y]
        if ziurim in Morku_zemelapis:
            Zuikis_mato[key]='Morka'
        if ziurim in Vilkai:
            Zuikis_mato[key]='Vilkas'
    return Zuikis_mato

#generuojam pagal zaidimo salyga apskaiciuota skaiciu morku atsitiktinese aiksteles vietose
def morkos_start():
    morku_skaicius=int(np.round((l*l)/(np.pi*0.16*M*M)))
    Morku_zemelapis=[]
    for i in range(morku_skaicius):
        Morku_zemelapis.append([random.choice(range(0, l, 1)),random.choice(range(0, l, 1))])
    return Morku_zemelapis

def vilkas_eina(vilkas):
    matau_zuiki=vilkas_mato(vilkas)
    if matau_zuiki==False:
        #vilkas eina ramybes busenoje
        vilkas[0][0]=vilkas[0][0]+vilkas[1][0]
        vilkas[0][1]=vilkas[0][1]+vilkas[1][1]      
    else:
        #eina du langelius artyn zuikio
        if matau_zuiki[0]>0 and matau_zuiki[1]>0:
            vilkas=[[vilkas[0][0]+(vilkas[1][0]*2),vilkas[0][1]+(vilkas[1][1]*2)],vilkas[1]]
        elif matau_zuiki[0]<0 and matau_zuiki[1]>0:
            vilkas=[[vilkas[0][0]-(vilkas[1][0]*2),vilkas[0][1]+(vilkas[1][1]*2)],[-vilkas[1][0],vilkas[1][1]]]
        elif matau_zuiki[0]>0 and matau_zuiki[1]<0:
            vilkas=[[vilkas[0][0]+(vilkas[1][0]*2),vilkas[0][1]-(vilkas[1][1]*2)],[vilkas[1][0],-vilkas[1][1]]]
        elif matau_zuiki[0]==0:
            vilkas[0][1]=vilkas[0][1]+(vilkas[1][1]*2)
            if vilkas[1][0]==vilkas[1][1]:vilkas[1][0]=-vilkas[1][0]
        elif matau_zuiki[1]==0:
            vilkas[0][0]=vilkas[0][0]+(vilkas[1][0]*2)
            if vilkas[1][0]!=vilkas[1][1]:vilkas[1][1]=-vilkas[1][1]
    #jeigu vilkas pateko uz aiksteles ribu..
    if vilkas[0][0]<0 or vilkas[0][1]<0 or vilkas[0][0]>l-1 or vilkas[0][1]>l-1:    
        #apsukam vilko krypti kampe
        if vilkas[0][0]<0 and vilkas[0][1]<0 or vilkas[0][0]<0 and vilkas[0][1]>l-1 or vilkas[0][0]>l-1 and vilkas[0][1]>l-1 or vilkas[0][0]>l-1 and vilkas[0][1]<0:
            vilkas[1][0],vilkas[1][1]=-vilkas[1][0],-vilkas[1][1]
        #apsukam vilko krypti soninese krastinese
        elif vilkas[0][0]<0 or vilkas[0][0]>l-1:vilkas[1][0]=-vilkas[1][0]
        elif vilkas[0][1]<0 or vilkas[0][1]>l-1:vilkas[1][1]=-vilkas[1][1]
        #perkeliam vilka atgal i aikstele
        if vilkas[0][0]<0:vilkas[0][0]=-vilkas[0][0]
        elif vilkas[0][0]>l-1:vilkas[0][0]=2*(l-1)-vilkas[0][0]
        if vilkas[0][1]<0:vilkas[0][1]=-vilkas[0][1]
        elif vilkas[0][1]>l-1:vilkas[0][1]=2*(l-1)-vilkas[0][1]
    return vilkas

#kai zuikis paeina, jo issaugotos morku koordinates paties zuikio atzvilgiu 
#irgi turi buti pastumtos taip, kaip paejo zuikis
def morku_zemelapis_naujas(ejimas):
    global Morkos
    for i in range(0,len(Morkos),1):
        Morkos[i]=(Morkos[i][0]-ejimas[0],Morkos[i][1]-ejimas[1])
    return None

def zuikis_eina():
    global kryptys, zuikis_yra, zuikio_ejimai, Morkos
    Zuikis_mato=zuikis_mato()
    vilkai=[]
    #registruojame ka mato zuikis. Jeigu mato morka, uzsiraso jos koordinate i 
    #daugelio ejimu metu kaupiama sarasa Morkos. Jeigu pamato vilka/vilkus 
    #issaugo ju koordinates tik dabartinio ejimo metu masyve vilkai.
    for key,value in Zuikis_mato.iteritems():
        if value=='Vilkas':
            vilkai.append(key)
        if value=='Morka':
            if key not in Morkos:Morkos.append(key)
    #sukuriame erdve langu aplink zuiki, i kuria patenkantys objektai bus svarbus 
    #zuikio tolimesnio ejimo pasirinkimui            
    world = init_world(vilkai)
    #pasirenkame ejima, kuris butu geidziamiausias pagal susikurta zuikio 
    #vaiksciojimo strategija, jeigu neatsiras gyvybiskai svarbiu ejimu
    pirm=pirmenybe(world)
    #apskaiciuojame zuikio nauja padeti, jeigu bus palanku pasirinkti anksciau 
    #apskaiciuota geidziamiausia krypti.
    zuikis_new=[zuikis_yra[0]+pirm[0],zuikis_yra[1]+pirm[1]]  
    
    #jeigu zuikis nemato salia vilko arba visos morkos yra toli nuo jo, renkasi 
    #eiti rambybes busenos ejima kryptimi 'pirm' ir atnaujina savo morku zemelapi 
    if len(world['sinks'])==0:
        morku_zemelapis_naujas([zuikis_new[0]-zuikis_yra[0],zuikis_new[1]-zuikis_yra[1]])    
        return zuikis_new
      
    #jeigu salia zuikio yra morku, o vilko nera, einame link artimiausios morkos        
    if len(vilkai)==0:
        msuma=100
        for morka in Morkos:
            if abs(morka[0])+abs(morka[1])<msuma:
                msuma=abs(morka[0])+abs(morka[1])
                best=morka
        a,b=best[0],best[1]
        if best[0]!=0: a=best[0]/abs(best[0])
        if best[1]!=0: b=best[1]/abs(best[1])
        zuikis_new=[zuikis_yra[0]+a,zuikis_yra[1]+b]
        morku_zemelapis_naujas([zuikis_new[0]-zuikis_yra[0],zuikis_new[1]-zuikis_yra[1]])
        return zuikis_new

    #Apskaiciuojame kiekvieno world laukelio geidziamuma atsizvelgiant i tai, 
    #kiek ejimu reikia padaryt iki morkos
    Ui = init_U(world)
    U = val_iterate_backup(Ui, world)
    U = val_iterate_backup(U, world)  
    #paliekam tik tuos langelius, kurie yra salia zuikio
    dic={}    
    for d in zuikio_ejimai:
        if d in U:dic[d]=U[d]
    #paliekam tik labiausiai pageidaujamus gretimus langelius
    maxU=max(dic.values())
    best=[]
    for k in dic.keys():
        if dic[k] == maxU:
            best.append(k)
    #jei turim kelis geriausius ejimus, renkames ta, kuris atitinka ejima pirm, 
    #arba jei nera tokio, renkames atsitiktini ejima
    if pirm in dic and dic[pirm] in best:
        zuikis_new=[zuikis_yra[0]+pirm[0],zuikis_yra[1]+pirm[1]]
    else:
        ejimas=random.choice(best)
        zuikis_new=[zuikis_yra[0]+ejimas[0],zuikis_yra[1]+ejimas[1]]
    #atnaujinam zuikio turima morku sarasa atsizvelgiant i nauja zuikio padeti
    morku_zemelapis_naujas([zuikis_new[0]-zuikis_yra[0],zuikis_new[1]-zuikis_yra[1]])  
    return zuikis_new

#jeigu zuikis ir kuris nors vilkas atsiranda tame paciame langelyje, 
#zuikis praranda ketvirtadali pradines energijos, perkeliamas per 3 langelius
#ir is streso pamirsta visas anksciau matytas morkas
def vilkas_puola():
    global zuikio_E, vilkas1, vilkas2, zuikis_yra, Morkos, zuikio_ejimai
    if zuikis_yra==vilkas1[0] or zuikis_yra==vilkas2[0]:
        zuikio_E-=(l*l)/4
        print 'zuiki uzpuole vilkas...', zuikis_yra, 'Zuikio_E = ',zuikio_E
        galimos_kryptys=[]
        for ejimas in zuikio_ejimai:
            if zuikis_yra[0]+3*ejimas[0]>=0 and zuikis_yra[0]+3*ejimas[0]<=l-1 and zuikis_yra[1]+3*ejimas[1]>=0 and zuikis_yra[1]+3*ejimas[1]<=l-1:
                galimos_kryptys.append(ejimas)
        zuiki_keliam=random.choice(galimos_kryptys)
        zuikis_yra=[zuikis_yra[0]+3*zuiki_keliam[0],zuikis_yra[1]+3*zuiki_keliam[1]]
        Morkos=[]
    return None

#jeigu zuikis ir morka yra tame paciame langelyje, zuikis gauna M energijos 
#ir morka regeneruojama kitur, suvalgyta morka istrinama is masyvo Morkos
def zuikis_valgo_morka():
    global Morku_zemelapis, zuikio_E, zuikis_yra, Morkos
    if zuikis_yra in Morku_zemelapis:
        zuikio_E+=M
        print 'zuikis suvalge morka, Zuikio_E = ',zuikio_E
        Morku_zemelapis[Morku_zemelapis.index(zuikis_yra)]=[random.choice(range(0, l, 1)),random.choice(range(0, l, 1))]
        if (0,0) in Morkos: del Morkos[Morkos.index((0,0))]
    return None

#zaidimo paleidimo kodas. zuikis ir vilkai vaiksto tol, 
#kol zuikis turi energijos arba laimi surinkes daug energijos
def zaidziam():
    global Morku_zemelapis, zuikio_E, vilkas1, vilkas2, zuikis_yra,Morkos
    Morkos=[]
    Morku_zemelapis=morkos_start()
    i=0
    while zuikio_E>0 and zuikio_E<(Q*l*l):
        nauja_zuikio_vieta=zuikis_eina()
        vilkas1=vilkas_eina(vilkas1)
        vilkas2=vilkas_eina(vilkas2)
        zuikis_yra=nauja_zuikio_vieta
        vilkas_puola()
        zuikis_valgo_morka()
        zuikio_E-=1
        i+=1
    print  'pradine E =', l*l, 'Galutine E =',zuikio_E,', ejimai', i,'\nzuikis baige zaidima:',zuikis_yra
    return None

#nubraizo visas morkas aiksteleje ir zuikio matytas morkas kurios yra masyve Morkos
def morkos_zuikio_akimis_graf():
    global Morku_zemelapis, Morkos, zuikis_yra
    for morka in Morku_zemelapis:
        plt.scatter(morka[0],morka[1])
    for mork in Morkos:
        plt.scatter(mork[0]+zuikis_yra[0],mork[1]+zuikis_yra[1], marker="^", color='y',s=20)
    plt.show()
    return None
        

def init_world(vilkai):
    global Morkos, zuikis_yra  
    world = {}
    sinks = {}
    p=4
    grid = ([(c,r) for c in range(-p,p+1,1)
                 for r in range(-p,p+1,1)])
    i=len(grid)-1
    while i>=0:
        if grid[i][0]+zuikis_yra[0]<0 or grid[i][1]+zuikis_yra[1]<0 or grid[i][0]+zuikis_yra[0]>l-1 or grid[i][1]+zuikis_yra[1]>l-1: 
            grid.remove(grid[i])
        i-=1
    for morka in Morkos:
        sinks[morka]=M        
        #if morka in grid: sinks[morka]=M
    for vilkas in vilkai:
        x = vilkas[0]-(2*vilkas[0]/abs(vilkas[0])) if vilkas[0]!=0 else 0
        y = vilkas[1]-(2*vilkas[1]/abs(vilkas[1])) if vilkas[1]!=0 else 0
        if (x,y) in grid: sinks[(x,y)]=-(l*l)/4
    world['grid']  = grid   # Grid tiles
    world['sinks'] = sinks  # Final states
    return world

def init_U(world):
    dic = {}
    grid,sinks = world['grid'], world['sinks']
    for tile in grid:
        dic[tile] = sinks[tile] if tile in sinks else 0
    return dic    

def grid_successors (state, world):
    dic = {}
    for d in range(len(zuikio_ejimai)):
        x = state[0]+zuikio_ejimai[d][0]
        y = state[1]+zuikio_ejimai[d][1]
        dic[zuikio_ejimai[d]] = (x,y) if (x,y) in world['grid'] else state
    return dic

def val_iterate_backup(U, world):
    Un = {}                 # Updated utility function
    grid = world['grid']
    # Absorbing states are unchanged
    for tile in world['sinks']:
        Un[tile] = world['sinks'][tile]
    # For each tile in grid...
    for _ in grid:
        choice, cneib, nneib, nutil = None, {}, 0, 0
        # ...find the best one to update
        for tile in grid:
            if tile not in Un:      # Not yet updated
                neib = grid_successors(tile, world)
                util = [Un[neib[t]] for t in neib if neib[t] in Un]
                # States with most updated neighbors and states with
                #           highest neighbor utilities have priority
                if (len(util)>nneib) or \
                    ((len(util)==nneib) and (sum(util)>nutil)):
                    nneib, nutil = len(util), sum(util)
                    choice = tile
                    for n in neib:
                        cneib[n] = (Un[neib[n]] if neib[n] in Un
                                    else U[neib[n]])
        # If suitable state is found...
        if choice is not None:
            #...update utility to the max(sum(P*U(s'))) + R
            qvals, qm, dm = cneib, None, None
            for d in qvals:
                (dm, qm) = ((d, qvals[d]) if (qm is None or qvals[d]>qm)
                            else (dm, qm))
            Un[choice] = qm - 1 
    return Un

#parenkame krypti kuria eisime jei nebus reikalo begt nuo vilko ar eit link morkos
#vaiksciosime aplink aikstele zigzagais, aukstyn/zemyn, jei prieinam virsu/apacia
#einame i sona 5 zingsnius, nes tiek laisvai apima zuikio regejimo laukas, 
#tokiu budu galesime pamatyti visas aiksteleje esancias morkas ir jas suvalgyti.
def pirmenybe(world):
    global clock, H, V, zuikis_yra
    #jei pasiekeme aiksteles virsu/apacia einam 5 zingsnius i sona, 
    #jei priejom krasta, apsisukam ir einam i kita sona
    if clock < 5:
        if zuikis_yra[0] <= 0 : H = 1
        if zuikis_yra[0] >= l-1: H = -1
        clock += 1
        pirm = (H,0)
        if zuikis_yra[1]>l-1:pirm = (H,l-1-zuikis_yra[1])
        if zuikis_yra[1]<0:pirm = (H,-zuikis_yra[1])
    #kol nepasiekem virsaus/apacios, einam aukstyn/zemyn. Kai prieinam virsu/apacia 
    #apsukam ejimo krypti ir paleidziam 'laikrodi' ejimui kairen/desnen 5 zingsnius
    else:
        if zuikis_yra[1] <= 0: V = 1; clock = 0
        if zuikis_yra[1] >= l-1: V = -1; clock = 0
        pirm = (0,V)
        if zuikis_yra[0]>l-1:pirm = (l-1-zuikis_yra[0],V)
        if zuikis_yra[0]<0:pirm = (-zuikis_yra[0],V)
        
    return pirm

zaidziam()
#morkos_zuikio_akimis_graf()