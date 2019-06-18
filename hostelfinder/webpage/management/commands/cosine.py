from django.core.management.base import BaseCommand
from hostelAdmin.models import Hostel, Location
from webpage.models import User, Student, Rating
import csv
import random
import math

def evaluate_cosine_similarity(user,similar_user):
    numerator = 0
    user_square_sum = 0
    similar_user_square_sum = 0

    for i in range(len(user)-1):
        numerator = numerator + (user[i]*similar_user[i])
        user_square_sum = user_square_sum + (user[i]*user[i])
        similar_user_square_sum = similar_user_square_sum + (user[i]*user[i])

    denominator = math.sqrt(user_square_sum) + math.sqrt(similar_user_square_sum)
    similarity = numerator/denominator
    return similarity

def predict_user_item_rating(user,similar_user,cosine_similarity):
    denominator = 0
    predictate_rating = []

    similar_user_average = []
    user_average = 0

    for i in range(len(cosine_similarity)):
        denominator = denominator + cosine_similarity[i]

    for i in range(len(similar_user)):
        average = 0;
        total = 0;
        for j in range(len(similar_user[0])):
            total = total + similar_user[i][j]
        average = total/len(similar_user[0])
        similar_user_average.append(average)

    total = 0
    for i in range(len(user)):
        total = total + user[i]
    user_average  = total/len(user)

    for j in range(len(similar_user[0])):
        numerator = 0
        for i in range(len(similar_user)):
            numerator = numerator + ((similar_user[i][j]-similar_user_average[i])*cosine_similarity[i])
        predict = user_average + (numerator/denominator)
        predictate_rating.append(predict)

    return predictate_rating

def similar_hostel(user_id):
    user_rated_hostel = []
    similar_rating_user_id = []
    similar_user_rated_hostels = []
    student = Student.objects.get(user_id=user_id)
    rating = Rating.objects.filter(user=student.user_id)

    if student.gender == 'M':
        hostel_type = 'B'
    else:
        hostel_type = 'G'

    #get the hostels rated by active user
    for rating in rating:
        user_rated_hostel.append(rating.hostel)

    #get the similar users who rated the hostels rated by active user
    similar_rating = Rating.objects.filter(hostel__in=user_rated_hostel,user__student__gender=student.gender).order_by('user_id').exclude(user_id=user_id)

    #prepare the list of similar rating users and the hostels they rated
    for s in similar_rating:
        similar_rating_user_id.append(s.user_id)

        for h in Rating.objects.filter(user_id=s.user_id,hostel__hostel_type='B'):
            similar_user_rated_hostels.append(h.hostel_id)

    # removing duplicates
    similar_rating_user_id = list(dict.fromkeys(similar_rating_user_id))
    similar_user_rated_hostels = list(dict.fromkeys(similar_user_rated_hostels))
    similar_rating_user_id.sort()
    similar_user_rated_hostels.sort()

    #create user-item matrix for both active user and similar users
    similar_user =  [[0] * len(similar_user_rated_hostels) for i in range(len(similar_rating_user_id))]
    user = []

    for i,similar_user_id in enumerate(similar_rating_user_id):
        for j,hostel_id in enumerate(similar_user_rated_hostels):
            if Rating.objects.filter(user_id=similar_user_id,hostel_id=hostel_id).exists():
                r = Rating.objects.values('rating').get(user_id=similar_user_id,hostel_id=hostel_id)
                rate = r['rating']
            else:
               rate = 0
            similar_user[i][j] = rate


    for j in similar_user_rated_hostels:
        if Rating.objects.filter(user_id=user_id, hostel_id=j).exists():
            r = Rating.objects.values('rating').get(user_id=user_id, hostel_id=j)
            rate = r['rating']
        else:
            rate = 0
        user.append(rate)

    print(user_rated_hostel)
    print(user)
    print(similar_user)

    #calculating similarity through cosine similarity
    # cosine_similarity = []
    #
    # for i in range(len(similar_rating_user_id)):
    #     similarity = evaluate_cosine_similarity(user,similar_user[i])
    #     cosine_similarity.append(similarity)
    #
    # #predicting the rating for the each item of active user
    # predictate_rating = predict_user_item_rating(user,similar_user,cosine_similarity)
    #
    # #now finding the top predictate hostel rating
    # predictate_similar_hostel = []
    # hostels = []
    # for j, hostel_id in enumerate(similar_user_rated_hostels):
    #     predictate_similar_hostel.append((hostel_id,predictate_rating[j]))
    # predictate_similar_hostel.sort(key=lambda x  : x[1],reverse=True)
    #
    # for p in predictate_similar_hostel:
    #     hostels.append(p[0])
    #
    # hostel = []
    # for h in hostels:
    #     hostel.append( Hostel.objects.get(id=h))
    #
    # for h in hostel:
    #     print(h)
    #
    # return hostel

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        similar_hostel(3067)

