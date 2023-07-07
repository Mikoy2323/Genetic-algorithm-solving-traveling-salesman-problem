import numpy as np
import pandas as pd
import scipy as sp
import random
import copy
import matplotlib.pyplot as plt


def first_pop(m_first,n,city_numbers):
    populations = pd.DataFrame(np.zeros((m_first, n), dtype=int))
    temp = city_numbers

    for i in range(m_first):
        np.random.shuffle(temp)
        populations.loc[i, :] = temp
    return populations


def asses(m_first,populations,n,shortest_dist_list):
    for j in range(0, m_first):
        # print(m_first)
        sum_dist = sum([distance_table[populations.loc[j][i] - 1, populations.loc[j][i + 1] - 1] for i in range(0, n - 1)])
        sum_dist += distance_table[populations.loc[j][0] - 1, populations.loc[j][n - 1] - 1]
        # adding last vale to first to create cicle
        populations.loc[j, "distance"] = sum_dist.astype(int)
    populations.sort_values(by='distance', inplace=True)
    populations.reset_index(drop=True, inplace=True)
    shortest_dist_list.append(populations["distance"][0])
    return populations

def selection(populations,m_first,m,n):
    new_population=pd.DataFrame(np.zeros((m, n), dtype=int))
    new_population["distance"]=0
    new_population["p"]=0
    for i in range(0, m_first):
        populations.loc[i,"p"]=(shortest_dist_list[len(shortest_dist_list)-1]/populations.loc[i,"distance"])**4

    prob_factor = 1 / sum(populations["p"])
    populations["p"] = [prob_factor * p for p in populations["p"]]
    new_population.loc[0]=populations.loc[0]
    new_population.loc[1]=populations.loc[1]
    counter=2
    while (counter<m):
        elem=random.choices(list(populations.index),list(populations["p"]),k=1)
        new_population.loc[counter]=populations.loc[elem[0]]
        counter+=1
    new_population.sort_values(by='distance', inplace=True)
    new_population.reset_index(inplace=True, drop=True)
    return new_population

def crossover_2(m,n,p_cross,new_population):
    crossed_population=pd.DataFrame(np.zeros((m,n),dtype=int))
    crossed_population.loc[0]=new_population.loc[0,0:n-1]
    crossed_population.loc[1]=new_population.loc[1,0:n-1]

    for i in new_population.loc[2:len(new_population)].index:
        index = random.random()
        if p_cross > index:
            second_parent = random.randint(0, m - 1)
            start = random.randint(0, n - 1)
            stop = random.randint(start, n - 1)
            chrom_list = list(new_population.loc[i][start:stop])
            if chrom_list:
                item=copy.copy(new_population.loc[i])
                item[start:stop]=new_population.loc[second_parent][start:stop]
            else:
                crossed_population.loc[i] = new_population.loc[i]
                continue
            #legalisation
            duplicates_1 = [x for x in list(item) if
                            list(item).count(x) > 1]
            not_duplicated = [x for x in list(new_population.loc[i]) if x not in list(item)]
            n_counter=0
            for x in list(set(duplicates_1)):
                idx = list(item).index(x)
                item[idx] = list(set(not_duplicated))[n_counter]
                n_counter += 1
            crossed_population.loc[i]=item
        else:
            crossed_population.loc[i] = new_population.loc[i]
    return crossed_population

def mutation(m,p_mut,n,new_population):
    for i in range(m):
        index = random.random()
        if p_mut > index:
            gen_1 = random.randint(0, n - 1)
            gen_2 = random.randint(0, n - 1)
            while gen_2 == gen_1:
                gen_2 = random.randint(0, n - 1)
            temp = copy.copy(new_population.loc[i][gen_1])
            new_population.loc[i][gen_1] = new_population.loc[i][gen_2]
            new_population.loc[i][gen_2] = temp
    return new_population

#n cities with random coordinates
n=25 #amound of cities
m_first=250 #starting population size
m=250 #population size
p_cross=0.95 #probability od crossover
p_mut=0.20 #probability of mutation
stop_param=80
city_numbers=np.linspace(1,n,n).astype(int)
shortest_dist_list=[]
shortest_dist_list.append(100000)
shortest_dist_list.append(1000000)

x_point=np.random.randint(0,300,n)
y_point=np.random.randint(0,300,n)
points=list(zip(x_point,y_point))

#creating distance table
distance_table=sp.spatial.distance_matrix(points,points)


#first population
populations=first_pop(m_first,n,city_numbers)

#########################################


no_change_counter=0
while shortest_dist_list[len(shortest_dist_list)-1]!=shortest_dist_list[len(shortest_dist_list)-2] or no_change_counter<stop_param:
    if shortest_dist_list[len(shortest_dist_list)-1]==shortest_dist_list[len(shortest_dist_list)-2]:
        no_change_counter+=1
    else:
        no_change_counter=0


    populations.insert(n, "distance", 0)


    #population assesment
    populations=asses(m_first,populations,n,shortest_dist_list)
    ######################

    #population selection
    new_population=selection(populations,m_first,m,n)
    ###############
    #crossover
    new_population=crossover_2(m,n,p_cross,new_population)
    ##############################

    #mutation
    new_population=mutation(m,p_mut,n,new_population)
    ##############################

    populations = copy.copy(new_population)
    m_first=m
    print(shortest_dist_list)



del shortest_dist_list[0]
del shortest_dist_list[0]

fig,ax=plt.subplots(2,1,figsize=(20,15))
ax[0].plot(shortest_dist_list)
ax[0].set_xlim([0,len(shortest_dist_list)])
ax[0].set_ylim([min(shortest_dist_list)-50,max(shortest_dist_list)+50])
ax[0].set_xlabel("pokolenia")
ax[0].set_ylabel("funkcja celu(droga)")
ax[0].set_title("funkcja celu zależnie od kolejnych pokoleń")

populations.insert(n, "distance", 0)
for j in range(0, m_first):
    sum_dist = sum([distance_table[populations.loc[j][i] - 1, populations.loc[j][i + 1] - 1] for i in range(0, n - 2)])
    sum_dist += distance_table[populations.loc[j][0] - 1, populations.loc[j][n - 1] - 1]
    # adding last vale to first to create cicle
    populations.loc[j, "distance"] = sum_dist.astype(int)
populations.sort_values(by='distance', inplace=True)
populations.reset_index(drop=True, inplace=True)

x_point_2,y_point_2=zip(*[(x_point[i-1],y_point[i-1]) for i in populations.loc[0][0:n-1]])
ax[1].scatter(x_point_2,y_point_2,s=9,color="red")
ax[1].plot(x_point_2,y_point_2,color="blue")
ax[1].plot([x_point_2[len(x_point_2)-1],x_point_2[0]],[y_point_2[len(y_point_2)-1],y_point_2[0] ],color="blue")
ax[1].set_xlim([0,300])
ax[1].set_ylim([0,300])
ax[1].set_xlabel("X")
ax[1].set_ylabel("Y")
ax[1].set_title("miasta")
ax[1].set(adjustable='box', aspect='equal')

plt.tight_layout(pad=5)

plt.show()

