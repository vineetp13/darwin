
from random import randint

#number of players
N = 10
#number of folks receiving feedback
l = 3

#frequency of providing feedback
f = [0.00] * N

#f = []
#for i in range(N):

#cost of providing feedback fpr "i"th player
c = [0] * N
#value of feedback of "i"th player
v = [0] * N

#payoff_value for players
p = [0] * N

#if using constant values for Cost and Value of feedback for all players
C = 1
V = 10

#populate all the values above
for i in range(0,N):
    f[i] = (i+1)*1.0/N #hack to ensure fractional part is taken
    c[i] = C
    v[i] = V

#TODO-how should I vary c and v above in interesting and useful ways

#DONT NEED - matrix of N * L size showing who is being provided feedback

#count of how many feedbacks has "i"th player received
count = [0] * N
#value of feedbacks received by "i"th player
value = [0.00] * N
#cost incurred by "i"th in providing feedback
cost = [0.00] * N

NUM_ITERATIONS = 10

for ii in range(0,NUM_ITERATIONS):
    for i in range(0,N):
        #choose l number of recipients randomly to provide feedback to
        chosen_few = [-1] * l
        for j in range(0,l):
            chosen = randint(0,N-1)
            while(chosen in chosen_few or chosen==i):
                chosen = randint(0,N-1)
            chosen_few[j] = chosen
            # and (chosen not in chosen_few)): cannot provide feedback to self and to someone else already provided feedback to
            print count[chosen], value[chosen], cost [i], "count, value, cost"
            count[chosen]+=1 #increment number of feedback received by chosen
            value[chosen]+=f[i]*v[i] #increment value of feedbacks received by chosen
            cost[i] += c[i]*f[i]#cost incurred to "i"th player in providing feedback
            print count[chosen], value[chosen], cost [i], "count, value, cost"
        print i, "   ", chosen_few

    #TODO-ensure all default values are not crappy or wrong
    #TODO - all the above need to be reset to zero at the end of loop and beginning of next step

    avg_score = [-1] * N
    #Now: choose who dies based on lowest payoff value

    min = 10000 #randomly selected high number
    min_player = -1
    sum_p = 0

    for i in range(0,N):
        print p[i], value[i], cost[i], "<-- p[i]"
        p[i] = value[i] - cost[i];
        print p[i], "<-- p[i]"
        avg_score[i] = value[i]/l
        sum_p += p[i]
        if p[i] < min:
            min = p[i]
            min_player = i

    print sum_p, "<-- sum_p"
    print "min_player is", min_player
    sum_p = sum_p - p[min_player] #take min_player out of probability distribution
    print sum_p, "<-- sum_p"

    print p, "entire payoff array"
    print f[min_player], c[min_player], v[min_player], "details of min_player before"

    #TODO-replace the min_player with a new player using a probability distribution over the remaining folks
    for i in range(0,N):
        f[min_player] = 0
        c[min_player] = 0
        v[min_player] = 0
        if (i != min_player):
            f[min_player] += f[i]*p[i]
            f[min_player] /= sum_p
            c[min_player] += c[i]*p[i]
            c[min_player] /= sum_p
            v[min_player] += v[i]*p[i]
            v[min_player] /= sum_p

    print f[min_player], c[min_player], v[min_player], "details of min_player now"

    #TODO-now, clear out the values for next iteration
    #TODO-maybe we want to store the round by round details - think?


#Now repeat the whole experiment again with NUM_ITERATIONS loop above

#TODO-potential optimizations
#1. use numpy/scipy

