__author__ = 'Sergio'

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import array

Period_Between_Slopes = 30 #days
Length_Sample_Data = 8 #days
Significative_Slope_variation = 0.2 #degrees

#Structure to store input data
User = array('i')
Group = array(User)

#Structure to store the slopes through time
Slope_Values = list
Slope_Variations = list

#Structure for returning results. For each user, and for each Period_Between_Slopes we will store which user have influenced
#the user. For example, if user 3 at Period_Between_Slopes[4] has been influenced by users 1 and two, the position in the matrix
# Group_Influence[3][4] will be equal = "1,2".
User_influence = array("")
Group_influence = array(User_influence)


class Engine(webapp.RequestHandler):

    def interpretateInfluence(self):
        # This function will determine who is influencing who and to what extent
        # In order to do that, we will look at the variations that each user has suffered and compare them with the rest of the
        # users variations. We will consider that a user has been influenced if his variation is greater than the Significative_Slope_Variation value.
        for i in range (len(Group)):
            a = 1,


    def Influences(self):
        global Group
        global Period_Between_Slopes
        global Length_Sample_Data
        global Slope_Variations
        global Slope_Values
        global Group_influence

        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #We calculate the initial mood tendency of each user
        for i in range(len(Group)):
            arrayUser = Group[i][0:Length_Sample_Data]
            initialSlope = Calc_Slope(arrayUser)  #TBD (Kevin)
            Slope_Values[i].append(initialSlope)

        #//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        #We calculate the mood after each month.
        #1. dataset_moment will point to the different points in time we will take
        #   samples from each user's dataset to obtain the scope. Initially will be the first period (first month)
        #2. Length_Sample_Data will be the amount of days we will be taking as a sample. Given the dataset_moment, we will
        #   take both from the future as from the past to obtain an average value of the slope at that given moment.
        iterations = 1
        dataset_moment = Period_Between_Slopes
        while (len(Group[0])> dataset_moment + (Length_Sample_Data/2)):
            #We calculate the slope after each month for each user
            for i in range(len(Group)):
                arrayUser = Group[i][(dataset_moment - (Length_Sample_Data/2)):(dataset_moment + (Length_Sample_Data/2))]
                slopeForUserI = Calc_Slope(arrayUser)  #TBD (Kevin)
                #We store the value of the slope obtained this month compared to the value of the previous monthx
                Slope_Variations[i].append(slopeForUserI - Slope_Values[i][-1])
                Slope_Values[i].append(slopeForUserI)

            iterations += 1
            dataset_moment = Period_Between_Slopes*iterations
        #Now we have the slopes of every user at every month of the dataset that we have been provided. We will have to
        #   to compare them to see who is influencing who.
        #self.interpretateInfluence()


        def __init__(self, groupInput):
             #variables initialization. Supposition: we will not have a null input and the given data will be a square
            #matrix, not a set of different length arrays. Every value will be initialized (NO NULL VALUES)
            Group = groupInput
            lengthOfArrays = len(Group[0])
            #initially, nobody has influence over anybody
            Group_influence = [[0 for x in xrange(len(Group))] for j in xrange(lengthOfArrays)]
            #initially we have no scopes but the list is not empty
            for x in range (len(Group)):
                Slope_Values.append([])
                Slope_Variations.append([])

