#######################################################################
#                   Slope Calculating Fuction                         #
# getcontext().prec sets the number of digits after the decimal Point #
#                                                                     #
#                                                                     #
#######################################################################

__author__="Kevin Aloysius"

from decimal import *
getcontext().prec = 3

def calculateSlope(*dataSet):
    number_of_data=len(*dataSet)
    sum_of_data=sum(*dataSet)
    slope=Decimal(sum_of_data)/Decimal(number_of_data)
    return slope




