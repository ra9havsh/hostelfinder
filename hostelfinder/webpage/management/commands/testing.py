from django.core.management.base import BaseCommand
from webpage.models import User, HostelOwner, Student, Rating
from hostelAdmin.models import Hostel
import csv
import math
import random

def evaluate_cosine_similarity(user,similar_user):
    numerator = 0
    user_square_sum = 0
    similar_user_square_sum = 0

    for i in range(len(user)):
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

    predictate_similar_hostel = []

    if similar_user_rated_hostels and similar_rating_user_id:
        # removing duplicates
        similar_rating_user_id = list(dict.fromkeys(similar_rating_user_id))
        similar_user_rated_hostels = list(dict.fromkeys(similar_user_rated_hostels))
        similar_rating_user_id.sort()
        similar_user_rated_hostels.sort()

        # create user-item matrix for both active user and similar users
        similar_user = [[0] * len(similar_user_rated_hostels) for i in range(len(similar_rating_user_id))]
        user = []

        for i, similar_user_id in enumerate(similar_rating_user_id):
            for j, hostel_id in enumerate(similar_user_rated_hostels):
                if Rating.objects.filter(user_id=similar_user_id, hostel_id=hostel_id).exists():
                    r = Rating.objects.values('rating').get(user_id=similar_user_id, hostel_id=hostel_id)
                    rate = r['rating']
                else:
                    rate = 0
                similar_user[i][j] = rate

        # for i, similar_user_id in enumerate(similar_rating_user_id):
        #     for j, hostel_id in enumerate(similar_user_rated_hostels):
        #         print(str(similar_user_id) + '-' + str(hostel_id) + "=" + str(similar_user[i][j]))
        #     print()

        for j in similar_user_rated_hostels:
            if Rating.objects.filter(user_id=user_id, hostel_id=j).exists():
                r = Rating.objects.values('rating').get(user_id=user_id, hostel_id=j)
                rate = r['rating']
            else:
                rate = 0
            user.append(rate)

        # print(user)

        # calculating similarity through cosine similarity
        cosine_similarity = []

        # print("cosine similarity:")
        for i in range(len(similar_rating_user_id)):
            similarity = evaluate_cosine_similarity(user, similar_user[i])
            cosine_similarity.append(similarity)
            # print(str(similar_rating_user_id[i]) + '-' + str(round(similarity, 3)))

        if cosine_similarity:
            # predicting the rating for the each item of active user
            predictate_rating = predict_user_item_rating(user, similar_user, cosine_similarity)

            # print("predictate rating:")
            # for i in range(len(similar_user_rated_hostels)):
            #     print((str(similar_user_rated_hostels[i]) + '-' + str(round(predictate_rating[i], 2))))

            # now finding the top predictate hostel rating

            for j, hostel_id in enumerate(similar_user_rated_hostels):
                predictate_similar_hostel.append((hostel_id, predictate_rating[j]))
            predictate_similar_hostel.sort(key=lambda x: x[1], reverse=True)

    return predictate_similar_hostel

class Command(BaseCommand):

    def add_arguments(self,parser):
        parser.add_argument('user_file_name', type=str, help="hostel detail")

    def handle(self,*args,**kwargs):
        test_data = kwargs['user_file_name']

        with open(f'{test_data}.csv','r') as file:
            test_data_reader = csv.reader(file)
            header=next(test_data_reader)

            hostels =[]
            users = []

            for h in header:
                if h != 'rating':
                    hostel_id=int(h)
                    hostels.append(hostel_id)


            for line in test_data_reader:
                user_id=[]
                users.append(line[0])

            with open('prediction_data.csv', mode='w', newline='') as rate_file:
                predict_data_writer = csv.writer(rate_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                predict_data_writer.writerow(['rating']+hostels)

                for u in users:
                    line=[]
                    prediction=similar_hostel(u)
                    print(u)
                    line.append(u)

                    for h in hostels:
                        for p in prediction:
                            if h==p[0]:
                                rate=p[1]
                                break
                            else:
                                rate=0
                        line.append(round(rate,2))

                    predict_data_writer.writerow(line)


