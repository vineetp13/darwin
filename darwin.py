
from random import randint
import numpy as np #for random.permutation

print "**************************"

#TODO-write how to use this code

NUM_ITERATIONS = 100

#number of players
N = 10

#number of folks receiving feedback
k = 3

#threshold to decide whether you will see feedbacks or not
#TODO-this will affect the payoffs - make note of that - and edit payoffs accordingly
l = 2

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
    f[i] = (i)*1.0/N #hack to ensure fractional part is taken
    #TODO-change deno value above..
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

#Store sum of payoffs and people kicked out to see correlations
sums_all = [0] * NUM_ITERATIONS
kicked_all = [-1] * NUM_ITERATIONS
replacers = [-1] * NUM_ITERATIONS
final_freq_matrix = [-1] * NUM_ITERATIONS
for i in range(0,NUM_ITERATIONS):
    final_freq_matrix[i] = [-1] * N

#TODO-remove all variables not being used

#TODO-create a matrix of who gives feedback to whom - To preseve the condition that everyone receives just as many feedbacks
#TODO-check if doing this ensures there are no negative payoffs

feedback_matrix = [-1] * k
for i in range(0,k):
    feedback_matrix[i] = [-1] * N

count_feedback = [0] * N # how many feedbacks has ith player received

for i in range(0,k):
    for j in range(0,N):
        feedback_matrix[i][j] = j
    #v print feedback_matrix[i]

print "####"

#feedback_flag = 1 #flag =1  denotes that the list needs to be repermuted


def create_feedback_matrix():
    for i in range(0,k):
        feedback_flag=1
        while(feedback_flag==1):
            #v print i
            feedback_matrix[i] = np.random.permutation(N)
            #print "permuuuuuu", feedback_matrix[i]
    #TODO-check if same number has been assigned by chance
            for jj in range(0,N):
    #TODO-ensure that you dont give feedback to same player across rounds
                cur_list = [-1] * (i+1)
                for iii in range(1,i+1):
                    cur_list[iii] = feedback_matrix[iii-1][jj] #this list contains the elements chosen for the same player so far
                #v print "!!!!!!!"
                bool_check = feedback_matrix[i][jj] in cur_list
                #v print cur_list, feedback_matrix[i][jj], bool_check

                #v print "!!!!!"
                if((feedback_matrix[i][jj]==jj) or bool_check): #jj player cannot provide feedback to itself
                    #v print bool_check
                    feedback_flag=1
                else:
                    feedback_flag=0

for i in range(0,k):
    print feedback_matrix[i]

print "$$$$"

#TODO-have clear metrics variables - and named so
#TODO-maybe use numpy, scipy for performance

#TODO-dont call it min_player - its not min_player bro

for ii in range(0,NUM_ITERATIONS):
    print "ITERATION ##########", ii
    create_feedback_matrix() #create new feedback matrix for every iteration
    for i in range(0,N):
        #choose k number of recipients randomly to provide feedback to
        chosen_few = [-1] * k
        for j in range(0,k):
            #TODO-dont need to do the chosen crap anymore - can just delete this during code clean up
            #chosen = randint(0,N-1)
            #while(chosen in chosen_few or chosen==i):# or count_feedback[chosen]==k):
            #    chosen = randint(0,N-1)
            chosen = feedback_matrix[j][i]
            chosen_few[j] = chosen
            count_feedback[chosen] +=1
            # and (chosen not in chosen_few)): cannot provide feedback to self and to someone else already provided feedback to
            #print count[chosen], value[chosen], cost [i], "count, value, cost"
            count[chosen]+=1 #increment number of feedback received by chosen
            value[chosen]+=f[i]*v[i] #increment value of feedbacks received by chosen
            cost[i] += c[i]*f[i]#cost incurred to "i"th player in providing feedback
            #print count[chosen], value[chosen], cost [i], "count, value, cost new"
        #v print i, "   ", chosen_few
    #print count_feedback
    #print feedback_matrix

    #TODO-ensure all default values are not crappy or wrong
    #TODO - all the above need to be reset to zero at the end of loop and beginning of next step

    avg_score = [-1] * N
    #Now: choose who dies based on lowest payoff value


    #min = 10000 #randomly selected high number
    min_player = randint(0,N-1)
    sum_p = 0

    pass_l_threshold = 0
    fail_l_threshold = 0

#calculating payoff values in p[i]
    for i in range(0,N):
        #print p[i], value[i], cost[i], "<-- p[i]"
        #payoff calculation changes with the introduction of parameter l
        ##print "original cost", cost [i]
        #p[i] = value[i] - cost[i];
        if (cost[i] > l):
            #then the player crosses our threshold of providing feedback
            p[i] = value[i] - cost[i]
            pass_l_threshold +=1
        else:
            p[i] = 0
            fail_l_threshold += 1
        #print p[i], "<-- p[i]"
        avg_score[i] = value[i]/k
        sum_p += p[i]

#When min_player was being chosen according to lowest payoff, now choosing it randomly at the end of the comment block
 #       if p[i] < min:
  #          min = p[i]
   #         min_player = i

    print "number of players who passed and failed threshold are", pass_l_threshold, fail_l_threshold
    #print sum_p, "<-- sum_p"
    #v print "min_player is", min_player

    #TODO-fix sum_p when you account for taking out min_player from the distribution
    #sum_p = sum_p - p[min_player] #take min_player out of probability distribution
    ##print sum_p, "<-- sum_p"

    #v print p, "entire payoff array"
    #v print f, "frequency array"
    #v print f[min_player], c[min_player], v[min_player], p[min_player],"details of min_player before"

#TODO-following three lines are redundant
    #f[min_player] = 0
    #c[min_player] = 0
    #v[min_player] = 0

    #TODO-replace the min_player with a new player using a probability distribution over the remaining folks

    #This weighted approach is wrong
    #for i in range(0,N):
     #   if (i != min_player):
      #      #print i, "inside"
       #     #print f[i],c[i],v[i], p[i], "f,c,v,p[i]"
       #     f[min_player] += f[i]*p[i]
        #    c[min_player] += c[i]*p[i]
         #   v[min_player] += v[i]*p[i]
          #  #print f[min_player], c[min_player], v[min_player], "inside loop"
    #print f[min_player], c[min_player], v[min_player], "before div"
    #f[min_player] *= (1.0)/sum_p
    #c[min_player] *= (1.0)/sum_p
    #v[min_player] *= (1.0)/sum_p
    #p[min_player] = 0.0
    #print f[min_player], c[min_player], v[min_player], "after div"
    ##print "****"

    #TODO-use multiline comments preserving indentation - not fixing it right now

    #choosing new min_player using a prob distribution over existing players
    #TODO-not doing it entirely correctly now, since the two end points (min and max) have almost no chance of being chosen - How to fix
        #Maybe the above will be auto fixed when the algo ensures everyone receives feedback ensuring that no one has negative payoffs
    #TODO - skip current min_player

    min = 0
    max = 0
    for i in range(0,N):
        if(i!=min_player):
            if p[i]<p[min]:
                min = i
            if p[i]>p[max]:
                max = i
    #Now we have the players with min and max payoffs, so divide up the number line

    #TODO-check if i have negative payoff values and to handle them...
    #currently assuming positive values only, not using "start" and "end"
    start = 0
    end = p[max]-p[min]

    #TODO-currently the dist_array includes the current min_player, this needs to be tweaked out - but it's okay right now  - easy to fix
    distr_array = [0] * N #this array stores the end-point for ith player to be chosen
    distr_array[0] = p[0]
    for i in range(1,N):
        distr_array[i] = p[i] + distr_array[i-1]

    ##print "distr_array is ", distr_array

    #for i in range(0,N-1):
     #   print distr_array[i+1] - distr_array[i]

    #now get a random number in the range of the number line (0,sum_p) and see where it fails
    toss = randint(0,int(sum_p))
    ##print "toss is", toss
    min_player_new = -1

    for i in range(0,N):
        if toss < distr_array[i]:
            min_player_new = i
            break

    #min_player = min_player_new
    #v print "new min_player is", min_player_new

    #assign the min_player the chosen guys value
    f[min_player] = f[min_player_new]
    c[min_player] = c[min_player_new]
    v[min_player] = v[min_player_new]

    #now we have our new min_player
    #v print f[min_player], c[min_player], v[min_player], p[min_player], "details of min_player now"
    print f, "entire freuqnecy array"
    #print count, "entire count array"

    #TODO-now, clear out the values for next iteration
    #TODO-maybe we want to store the round by round details - think?
    for i in range(0,N):
        value[i] = 0.0
        cost[i] = 0.0
        count[i] = 0.0


    sums_all[ii] = sum_p
    kicked_all[ii] = min_player
    replacers[ii] = min_player_new
    final_freq_matrix[ii] = f
    print final_freq_matrix[ii]


#Now repeat the whole experiment again with NUM_ITERATIONS loop above
#print "%.2f" % sums_all
#print sums_all
#print kicked_all

#TODO-fix final_freq_matrix storing+printing..
print final_freq_matrix

for i in range(0,NUM_ITERATIONS):
    print i, sums_all[i]
    print kicked_all[i], replacers[i]
    print final_freq_matrix[i]
    #print " |"
    #print " |"
    #print "\ /"


#TODO-potential optimizations
#1. use numpy/scipy

