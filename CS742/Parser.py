from functools import reduce
import http
import operator
from datetime import timedelta, date, datetime
import random
#from requests import async
from statistics import median
import async as async
import grequests
from dateutil import relativedelta
import powerlaw as powerlaw
import numpy
import scipy
__author__ = 'Ben'
import json
import csv
import matplotlib
from collections import defaultdict

class Parser:

    def __init__(self):
        self.number_of_videos = 0
        self.number_of_users = 0
        self.users_list = []
        self.number_of_views = 0
        self.number_of_comments = 0
        self.views_for_most_popular_video = 0
        self.views_for_most_commented_video = 0
        self.comments_for_most_viewed_video = 0
        self.comments_for_most_commented_video = 0
        self.data = dict()
        self.data_category_tuples = dict()
        self.timeline_uploads = dict()
        self.timeline_uploaders = dict([])
        self.video_size = []
        self.category_popularity = {}
        self.categories= {}
        self.most_popular_authors_freq = {}
        self.hot_author_list = []

    def parse_dataset(self, path):

         with open(path) as data_file:
            self.data = json.load(data_file)
    def find_longest_vid(self):
        duration = []
        for keys in self.data.keys():
            if self.is_int(self.data[keys]['runtime']):
                duration.append(self.data[keys]['runtime'])
            elif not self.is_int(self.data[keys]['runtime']):
                duration.append(0)
        x=len(duration)
        trimmed_duration = []
        for length in duration:
            if(length > 21600):
                pass
            elif length <= 21600:
                trimmed_duration.append(length)

        print("Number of vidoes shorter than 3 hours ", len(trimmed_duration), len(trimmed_duration)/x)
        duration.sort(reverse=True)
        print("Longest video: ", duration[0])

        #mean content duration
        print ("Average: " ,reduce(lambda x, y: x + y,trimmed_duration)/len(trimmed_duration))
        print("Median: ",median(trimmed_duration))
        trimmed_duration.sort(reverse=True)
        with open('trimmed_duration.csv','w', newline='\n') as csvfile:
            #fieldnames = ['Date', 'Number of videos', 'Number of Active Users']
            writer = csv.writer(csvfile)
            i = 1
            for keys in trimmed_duration:
                writer.writerow([keys, i])
                i += 1

    def get_final_date(self):
        latest_date = None
        for keys in self.data.keys():
            if(latest_date == None):

                latest_date = datetime.strptime(self.data[keys]['upload_date'], "%Y-%m-%d")
                latest_date = datetime(latest_date.year, latest_date.month, latest_date.day).date().isoformat()
            if(self.data[keys]['upload_date'] == 'NA'):
                continue
            temp = datetime.strptime(self.data[keys]['upload_date'], "%Y-%m-%d")
            temp = datetime(temp.year, temp.month, temp.day).date().isoformat()
            if(temp > latest_date):
                latest_date = temp
        number_of_views_per_day = dict()
        for keys in self.data.keys():
            if(self.data[keys]['upload_date'] != 'NA'):
                temp = temp = datetime.strptime(self.data[keys]['upload_date'], "%Y-%m-%d")
                temp = datetime(temp.year, temp.month, temp.day).date().isoformat()
                if(temp not in number_of_views_per_day):
                    number_of_views_per_day[temp] = self.data[keys]['nb_views']
                elif(temp in number_of_views_per_day):
                    number_of_views_per_day[temp] += self.data[keys]['nb_views']

        with open('views_vs_Content_Age.csv','w', newline='\n') as csvfile:
            #fieldnames = ['Date', 'Number of videos', 'Number of Active Users']
            writer = csv.writer(csvfile)
            i = 1
            for keys in sorted(number_of_views_per_day, reverse=True):
                writer.writerow([keys, number_of_views_per_day[keys], i])
                i += 1
        print(latest_date)
    def get_number_of_videos(self):
        temp_top_views = 0
        key_top_views = ''
        temp_top_comments = 0
        key_top_comments = ''
        for keys in self.data.keys():
            self.number_of_videos += 1
        #Now views and comments shall be accumulated
            if(self.is_int(self.data[keys]['nb_views'])):
                self.number_of_views += int(self.data[keys]['nb_views'])
            if(self.is_int(self.data[keys]['nb_comments'])):
                self.number_of_comments += int(self.data[keys]['nb_comments'])

            if(self.is_int(self.data[keys]['nb_views']) and self.data[keys]['nb_views'] > temp_top_views):
                temp_top_views = self.data[keys]['nb_views']
                key_top_views = keys
            if(self.is_int(self.data[keys]['nb_comments']) and self.data[keys]['nb_comments'] > temp_top_comments):
                temp_top_comments = self.data[keys]['nb_comments']
                key_top_comments = keys
        print("Number of videos: ")
        print(self.number_of_videos)
        print("Number of total views")
        print(self.number_of_views)
        print("Number of total comments")
        print(self.number_of_comments)
        print("Number of unique users: ")
        print(len(self.users_list))
        print("Most popular video: ")
        print(key_top_views, temp_top_views)
        print("Most commented video: ")
        print(key_top_comments, temp_top_comments)
        print("Views for most commented video: ", self.data[key_top_comments]['nb_views'])
        print("Comments for most popular video: ", self.data[key_top_views]['nb_comments'])

    def get_number_of_users(self):
        for keys in self.data.keys():
            uploader = self.data[keys]['uploader']
            if uploader in self.users_list:
                continue;
            else:
                self.users_list.append(uploader)

        print(len(self.users_list))
       # for keys in self.users_dict.keys():

    def timeline_video_uploads(self):
        for keys in self.data.keys():
            if self.data[keys]['upload_date'] in self.timeline_uploads:
                self.timeline_uploads[self.data[keys]['upload_date']] += 1
            else:
                self.timeline_uploads[self.data[keys]['upload_date']] = 1

            if self.data[keys]['upload_date'] in self.timeline_uploaders:
                if self.data[keys]['uploader'] not in self.timeline_uploaders[self.data[keys]['upload_date']]:



                        self.timeline_uploaders[self.data[keys]['upload_date']].append(self.data[keys]['uploader'])
                else:
                    #self.timeline_uploaders[self.data[keys]['upload_date']] = 1
                    pass
            else:
                #Create list
                self.timeline_uploaders[self.data[keys]['upload_date']] = [(self.data[keys]['uploader'])]
        print("Completed upload info")
        self.write_timeline()

    def write_timeline(self):
        with open('timeline.csv','w', newline='\n') as csvfile:
            #fieldnames = ['Date', 'Number of videos', 'Number of Active Users']
            writer = csv.writer(csvfile)

            for keys in sorted(self.timeline_uploads):
                writer.writerow([keys, self.timeline_uploads[keys], len(self.timeline_uploaders[keys])])

    def video_size_dist(self):
        for keys in self.data.keys():
            if self.is_int(self.data[keys]['runtime']):

                self.video_size.append([self.data[keys]['runtime'], keys])
        print("Sorting")
        self.video_size.sort(reverse=True)
        print("Sorted")
        #self.video_size.sort()
        #self.video_size.reverse()
        #print(self.video_size[0])
        self.write_video_dist()
    def write_video_dist(self):
        with open('video_dist.csv','w', newline='\n') as csvfile:
            #fieldnames = ['Date', 'Number of videos', 'Number of Active Users']
            writer = csv.writer(csvfile)

            for keys in self.video_size:

                writer.writerow(keys)

    def most_popular_category(self):
        #This function will make a dictionary which will have the category and aggregated views 'channels'
        #e.g. ['amateur', 'milf'] : 69

        print("At start of first loop")

        for keys in self.data_category_tuples.keys():
            if self.data_category_tuples[keys]['channels'] in self.category_popularity and self.is_int(self.data_category_tuples[keys]['nb_views']):
                self.category_popularity[self.data_category_tuples[keys]['channels']] += self.data_category_tuples[keys]['nb_views']

            elif (self.data_category_tuples[keys]['channels'] not in self.category_popularity.keys()) and (self.is_int(self.data_category_tuples[keys]['nb_views'])):
                #when the channels are not yet in the dictionary
                self.category_popularity[self.data[keys]['channels']] = self.data_category_tuples[keys]['nb_views']

        #Make printable version
       # sorted_by_views = sorted(self.data_category_tuples.items()['channels'], key=operator.itemgetter(1))
        #Make list of lists
        #category_list = []
        #print("At start of second loop")
        #for keys in self.data_category_tuples:
         #   if self.is_int(self.data_category_tuples[keys]['nb_views']) and  self.data_category_tuples[keys]['channels'] not in category_list:
         #       category_list.append([self.data_category_tuples[keys]['channels'], self.data_category_tuples[keys]['nb_views']])

       # category_list.sort(key=lambda x:x[1])

        with open('category_pop_dist.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing")
            for keys in self.category_popularity.keys():
                writer.writerow([keys, self.category_popularity[keys]])

    def most_popular_category_single_category(self):
        print("At start of first loop")
        single_category_popularity_videos ={}
        single_category_popularity_views = {}
        for keys in self.data_category_tuples.keys():
            for i in self.data_category_tuples[keys]['channels']:#keys is a tuple, for each tuple we shall add to dictionary
                if len(i) > 1:
                    if(i not in single_category_popularity_videos):
                        single_category_popularity_videos[i] = 1
                    elif(i in single_category_popularity_videos):
                        single_category_popularity_videos[i] += 1
                    if(i not in single_category_popularity_views and self.is_int(self.data_category_tuples[keys]['nb_views'])):
                        single_category_popularity_views[i] = self.data_category_tuples[keys]['nb_views']
                    elif(i in single_category_popularity_views and self.is_int(self.data_category_tuples[keys]['nb_views'])):
                        single_category_popularity_views[i] += self.data_category_tuples[keys]['nb_views']
        with open('category_pop_videos_single_cat.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing")
            for keys in single_category_popularity_videos.keys():
                writer.writerow([keys, single_category_popularity_videos[keys], single_category_popularity_views[keys]])
        #with open('category_pop_views_single_cat.csv', 'w', newline='\n') as csvfile:
        #    writer = csv.writer(csvfile)
        #    print("About to start writing")
        #    for keys in single_category_popularity_views.keys():
        #        writer.writerow([keys, single_category_popularity_views[keys]])

    def views_number_categories(self):
        categories = {}
        number_vids_per_category = {}
        for keys in self.data.keys():
            if(len(self.data[keys]['channels']) in categories and self.is_int(self.data[keys]['nb_views'])):
                number_vids_per_category[len(self.data[keys]['channels'])] += 1
                categories[len(self.data[keys]['channels'])] += int(self.data[keys]['nb_views'])
            elif len(self.data[keys]['channels']) not in categories and self.is_int(self.data[keys]['nb_views']):
                categories[len(self.data[keys]['channels'])] = int(self.data[keys]['nb_views'])
                number_vids_per_category[len(self.data[keys]['channels'])] = 1
        with open('views_vs_number_cats.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing")
            for keys in categories.keys():
                writer.writerow([keys, categories[keys]])
        with open('avg_views_vs_number_cats.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing")
            for keys in categories.keys():
                writer.writerow([keys, categories[keys]/number_vids_per_category[keys]])

    def ratings_per_video(self):
        ratings_vid = {}
        for keys in self.data.keys():
            #if(keys in ratings_vid):
            if self.is_int(self.data[keys]['nb_votes']):
                ratings_vid[keys] = self.data[keys]['nb_votes']

        ratings_list = []
        for keys in ratings_vid.keys():
            ratings_list.append(ratings_vid[keys])

        ratings_list.sort()
        with open('ratings_per_video.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing")

            for keys in sorted(ratings_vid.keys()):
                writer.writerow([ratings_vid[keys]])



    def power_law2(self):
        views = []
        for keys in self.data.keys():
            if (self.is_int(self.data[keys]['nb_views'])):
                views.append(self.data[keys]['nb_views'])
        numpy.seterr(divide='ignore', invalid='ignore')
        views.sort(reverse=True)

        #data.sort(reverse=True)
        fit = powerlaw.Fit(views,discrete=True,estimate_discrete=True)
        fit.power_law.plot_pdf(linestyle='--')
        print("Alpha: ", fit.power_law.alpha)
        print("Sigma: ", fit.power_law.sigma)
        fit.plot_pdf()
        #a = fit.plot_cdf(color='b', linestyle='--', label="fit powerlaw")
        #b = fit.plot_cdf()
        #x = fit.plot_pdf(color='b', linestyle='--', label="fit powerlaw")
        #y = fit.plot_pdf()
        #print(a, b, x, y)
        #matplotlib.pyplot.show(a)
        matplotlib.pyplot.plot()
        matplotlib.pyplot.show()
        #matplotlib.pyplot.show(b)
        #matplotlib.pyplot.show(x)
        #matplotlib.pyplot.show(y)

    def power_law(self):
        views = []
        for keys in self.data.keys():
            if(self.is_int(self.data[keys]['nb_views'])):
                views.append(self.data[keys]['nb_views'])
        numpy.seterr(divide='ignore', invalid='ignore')
        views.sort(reverse=True)
        #views = [1, 1, 1, 1,1 ,1 , 2, 2, 2,2 ,2 ,2 ,2 ,2, 2, 4, 4, 4,4 ,4, 4,0 ]
        fit= powerlaw.Fit(views)
        print("Alpha: ", fit.power_law.alpha)
        print("Sigma: ", fit.power_law.sigma)
        a = fit.power_law.plot_ccdf( color='b', linestyle='--', label="fit powerlaw")

        b = fit.plot_ccdf()
        #x = fit.plot_pdf( color='b', linestyle='--', label="fit powerlaw")
        #y = fit.plot_pdf()
       # print(a, b , x, y)
       # matplotlib.pyplot.show(fit)
        matplotlib.pyplot.plot()
        #matplotlib.pyplot.show(b)
        matplotlib.pyplot.show()
       # matplotlib.pyplot.show(x)
       # matplotlib.pyplot.show(y)

    #    with open('views_with_rank.csv', 'w', newline='\n') as csvfile:
    #        writer = csv.writer(csvfile)
    #        print("About to start writing")
    #        i = 1
    #        for keys in views:
    #            writer.writerow([keys, i])
    #            i+=1
    def make_categories_tuples(self):
        self.data_category_tuples = self.data
        for keys in self.data.keys():
            temp = self.data[keys]['channels']
            temp_tuple = tuple(temp)
            self.data_category_tuples[keys]['channels'] = temp_tuple
            if(self.data[keys]['channels'] not in self.categories ):
                    self.categories[self.data_category_tuples[keys]['channels']] = 1
            elif self.data[keys]['channels'] in self.categories:
                    self.categories[self.data[keys]['channels']] += 1

        with open('videos_per_category.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing videos per category")
            for keys in self.categories.keys():
                writer.writerow([keys, self.categories[keys]])
    def calculate_table_3(self):
        mean_content_duration = []
        unique_uploaders = []
        total_uploaders = 0
        total_views = 0
        total_videos = 0
        total_comments = 0
        number_of_ratings = 0
        categories = []
        categories_on_video_count = 0
        views = []
        for keys in self.data.keys():
            #Calculating results for Table 3 in Measurements and Analysis of a Adult Video Portal
            #Poptularity skew: get a list of the views, then order them in descending, aggreagate first 10%
            if self.is_int(self.data[keys]['nb_views']):
                views.append(self.data[keys]['nb_views'])
            else:
                views.append(0)
            #Mean Content Duration
            if(self.is_int(self.data[keys]['runtime'])):
                mean_content_duration.append(self.data[keys]['runtime'])

            #Number of uploaders
            if(self.data[keys]['uploader'] not in unique_uploaders):
                total_uploaders += 1
            #Number of visits per day - number of views per day
            #total views / days

            #Popularity skew - Top 10% of videos, % of views
            #Calculate the top ten percent

            #Mean views per video
            if(self.is_int(self.data[keys]['nb_views'])):
                total_views += self.data[keys]['nb_views']
            #Mean number of comments
            if(self.is_int(self.data[keys]['nb_comments'])):
                total_comments += self.data[keys]['nb_comments']
            total_videos += 1
            #%Comments per View

            #Number of ratings
            if(self.is_int(self.data[keys]['nb_votes'])):
                number_of_ratings += self.data[keys]['nb_votes']
            #% Ratings per View

            #Number of categories
            for category in self.data[keys]['channels']:
                if(category in categories):
                    continue
                else:
                    categories.append(category)
            #Mean categories per video
            categories_on_video_count += len(self.data[keys]['channels'])
        length = (len(views))/5
        views  = sorted(views, reverse=True)
        length = int(length)
        sum_of_views = sum(views[:length])
        print("Top 10% gets ", sum_of_views, " which is ", (sum_of_views/total_views)*100, "% of all views" )
        #print("Mean content duration: ", reduce(lambda x, y: x +y, mean_content_duration)/len(mean_content_duration))
       #print ("Mean views per day :" , self.number_of_views / len(self.timeline_uploads))
        #print("Mean views per video: ", total_views/total_videos)
        #print("Mean comments per video", (total_comments/total_videos))
        #print("Comments per view", (total_comments/total_views)*100, "%")
        #print("Percentage ratings per view", (number_of_ratings/total_views)*100, "%")
        #print("Number of ratings", number_of_ratings/total_videos)
        #print("Number of categories", len(categories))
        #print("Mean categories per video", categories_on_video_count/total_videos)

    def dataset_summary(self):
        #median views
        views = []
        number_no_views = 0
        number_one_views = 0
        number_ratings = []
        number_no_ratings = 0
        number_one_ratings = 0
        uploaders = []
        one_upload = 0
        duration = []
        print ("Starting")
        for keys in self.data.keys():
            if(self.data[keys]['nb_views'] == 0 or not self.is_int(self.data[keys]['nb_views'])):
                number_no_views += 1
                views.append(self.data[keys]['nb_views'])
            elif(self.data[keys]['nb_views'] == 1):
                number_one_views += 1
                views.append(self.data[keys]['nb_views'])
            else:
                views.append(self.data[keys]['nb_views'])

            if self.data[keys]['nb_votes'] == 0 or not self.is_int(self.data[keys]['nb_votes']):
                number_no_ratings += 1
                number_ratings.append(self.data[keys]['nb_votes'])
            elif self.data[keys]['nb_votes'] == 1:
                number_one_ratings += 1
                number_ratings.append(self.data[keys]['nb_votes'])
            else:
                number_ratings.append(self.data[keys]['nb_votes'])

            if self.data[keys]['uploader'] not in uploaders:
                uploaders.append(self.data[keys]['uploader'])
            if self.is_int(self.data[keys]['runtime']):
                duration.append(self.data[keys]['runtime'])
            elif not self.is_int(self.data[keys]['runtime']):
                duration.append(0)

        print("Through loop")
        for index, item in enumerate(views):
            if not(self.is_int(item)):
                views[index] = 0

        views.sort()
        median_views = median(views)
        print("Median views: ", median_views)
        for index, item in enumerate(number_ratings):
            if not(self.is_int(item)):
                number_ratings[index] = 0

        number_ratings.sort()
        total_ratings = sum(number_ratings)
        print("Total ratings:", total_ratings)
        median_ratings = median(number_ratings)
        print("Median ratings: ", median_ratings)
        print("Either top or bottom: ", number_ratings[0], number_ratings[len(number_ratings)-1] )
        print("Number of videos with no rating: ", number_no_ratings)
        print("Number of videos wtih one rating: ", number_one_ratings)
        print("Number of uploaders: ", len(uploaders))
        #get one rating from Excel
        print("Average duration of content: ", reduce(lambda x, y: x  + y, duration) / len(duration))
        duration.sort()
        print("Median duration of content: ", median(duration))


    def video_uploads_per_author(self):
        videos_per_author = {}
        views_per_author = {}
        comments_per_author = {}
        comments_per_video = {}
        for keys in self.data:
            if(self.data[keys]['uploader'] not in views_per_author and self.is_int(self.data[keys]['nb_views'])):
                views_per_author[self.data[keys]['uploader']] = self.data[keys]['nb_views']
            elif(self.data[keys]['uploader'] in views_per_author and self.is_int(self.data[keys]['nb_views'])):
                views_per_author[self.data[keys]['uploader']] += self.data[keys]['nb_views']

            if(self.data[keys]['uploader'] not in videos_per_author):
                videos_per_author[self.data[keys]['uploader']] = 1
            else:
                videos_per_author[self.data[keys]['uploader']] += 1

            if(self.data[keys]['uploader'] not in comments_per_author and self.is_int(self.data[keys]['nb_comments'])):
                comments_per_author[self.data[keys]['uploader']] = self.data[keys]['nb_comments']
            elif(self.data[keys]['uploader'] in comments_per_author and self.is_int(self.data[keys]['nb_comments'])):
                comments_per_author[self.data[keys]['uploader']] += self.data[keys]['nb_comments']

            if(self.data[keys]['nb_comments'] not in comments_per_video and self.is_int(self.data[keys]['nb_comments'])):
                comments_per_video[keys] = self.data[keys]['nb_comments']
            elif(self.data[keys]['nb_comments'] in comments_per_video and self.is_int(self.data[keys]['nb_comments'])):
                comments_per_video[keys] += self.data[keys]['nb_comments']

        with open('videos_per_author.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing videos per author")
            for keys in videos_per_author.keys():
                writer.writerow([keys, videos_per_author[keys]])

        with open('views_per_author.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing views per author")
            for keys in views_per_author.keys():
                writer.writerow([keys, views_per_author[keys]])
        with open('comments_per_author.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing comments per author")
            for keys in comments_per_author.keys():
                writer.writerow([keys, comments_per_author[keys]])
        with open('comments_per_video.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing comments per author")
            for keys in comments_per_video.keys():
                writer.writerow([keys, comments_per_video[keys]])
  #  def comments_per_video(self):


    def hotset_analysis(self):
        #In this method we try to find the popular authors for each 6 month period
        #Firstly find how long, then we shall split into 6 month groups
        author_dict = {}
        dates = []
        for keys in self.data.keys():
            if(self.data[keys]['upload_date'] not in dates):
                dates.append(self.data[keys]['upload_date'])
            else:
                pass

        dates.sort()
        length_of_study = len(dates)
        print("Length of study: ", length_of_study)
        #with open('dates.csv', 'w', newline='\n') as csvfile:
        #    writer = csv.writer(csvfile)
        #    print("About to start writing dates")
        #    for keys in dates:
        #        writer.writerow(keys)
        start_date = date(2007, 5, 23)
        end_date = date(2007, 11, 23)
        popular_authors =  {}
        #add_six_months = relativedelta(months=+6)
        date_list = []
        l =[]
        for n in range(0, 11):
            #0-11, 67.6 months, so final loop will be more custom
            if(n == 0):
                l = self.create_six_month_list(start_date, end_date, date_list)
            #Find the hottest authors! woo
                author_dict[n] = self.find_hottest_authors(l)
                #self.compare_hot_authors(author_dict[n], start_date)
            else:
                start_date = start_date +relativedelta.relativedelta(months=+6)
                end_date = end_date +relativedelta.relativedelta(months=+6)
                l = self.create_six_month_list(start_date, end_date, date_list)
            #Find the hottest authors! woo
                author_dict[n] = self.find_hottest_authors(l)
                #self.compare_hot_authors(author_dict[n], start_date)
    def compare_hot_authors(self, author_dict, start_date):
        #this function is designed to compare each hotset: Shall put on excel
        #for each hotset, find how many are new to the hot set
        self.hot_author_list
        new_authors = 0
        for keys in author_dict:
            if(keys not in  self.hot_author_list):
                self.hot_author_list.append(keys)
                new_authors += 1
              #  print(keys, " new to the hotset!")
            #else:
             #print(keys, " already appeared in the hotset")

        print(start_date, ", amount of new authors in this period: ", new_authors)

    def create_six_month_list(self, start_date, end_date, date_list=None) -> list:
        if not date_list:
            date_list = []
        for single_date in self.daterange(start_date, end_date):
            # Build up a list profile
            date_list.append(single_date.isoformat())
        return date_list

    def find_hottest_authors(self, date_list) -> dict:
        #Hotset on number of videos! NOT VIEWS
        #Need to compare each author
        authors = {} # contains, {author: views }
        authors_videos = {}
        total_views = 0
        total_videos = 0
        for keys in self.data.keys():
            if not (self.data[keys]['upload_date'] == "NA" ):
                data_date = datetime.strptime(self.data[keys]['upload_date'], "%Y-%m-%d" )
                data_date = datetime(data_date.year, data_date.month, data_date.day).date().isoformat()
                if(data_date in date_list): #need to convert date string into datetime.date object
                    total_views += self.data[keys]['nb_views']
                    total_videos += 1
                    if(self.data[keys]['uploader'] in authors):
                        authors[self.data[keys]['uploader']] += self.data[keys]['nb_views']
                        authors_videos[self.data[keys]['uploader']] += 1

                    elif(self.data[keys]['uploader'] not in authors):
                        authors[self.data[keys]['uploader']] = self.data[keys]['nb_views']
                        authors_videos[self.data[keys]['uploader']] = 1
                else:
                    pass

        #Now find total views so we can find all authors above a certain popularity %
        #Return those that have a value of at least 1%
        print("Total views: ", total_views)
        hot_authors = {}
        for keys in authors.keys():

            hot_authors[keys] = authors_videos[keys]
        hotset_list = list(hot_authors.items())
        top_hotset_list =  sorted(hotset_list, key=lambda x:x[1], reverse=True)
        top_hotset_list = top_hotset_list[0:int(len(top_hotset_list)/10)]
        PATH = 'dates_'+ date_list[0]
        PATH = PATH +'_'+ date_list[len(date_list)-1]+'.csv'
        PATH = PATH.replace("/", "_")
        with open(PATH, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing hot authors from", date_list[0], " to ", date_list[len(date_list)-1])
            for keys in top_hotset_list:
                writer.writerow([keys[0], keys[1]])
                #Finding frequency of these authors in the hotsets
                if(keys in self.most_popular_authors_freq):
                    self.most_popular_authors_freq[keys] += 1
                else:
                    self.most_popular_authors_freq[keys] = 1
        print("Number of Authors in ", date_list[0],": ", len(top_hotset_list))

        new_authors = 0
        for keys in top_hotset_list:
            if(keys[0] not in  self.hot_author_list):
                self.hot_author_list.append(keys[0])
                new_authors += 1

        print(date_list[0], ", amount of new authors in this period: ", new_authors)
              #  print(keys, " new to the hotset!")
            #else:
             #print(keys, " already appeared in the hotset")

        #with open("videos_"+date_list[0] + "_" + date_list[len(date_list)-1]+"half%threshold", 'w', newline='\n') as csvfile:
        #   writer = csv.writer(csvfile)
        #   print("About to start writing number of videos each hot author made", date_list[0], " to ", date_list[len(date_list)-1])
        #   for keys in top_hotset_list:
        #        writer.writerow([keys, authors_videos[keys]])
        #        #Finding frequency of these authors in the hotsets
        #        if(keys in self.most_popular_authors_freq):
        #            self.most_popular_authors_freq[keys] += 1
        #        else:
        #            self.most_popular_authors_freq[keys] = 1
        return top_hotset_list

    def daterange(self, start_date, end_date):
        for n in range(int((end_date-start_date).days)):
            yield start_date + timedelta(n)

    def videos_per_day(self):
        videos_per_day_dict = {}
        for keys in self.data.keys():
            if(self.data[keys]['upload_date'] not in videos_per_day_dict):
                videos_per_day_dict[self.data[keys]['upload_date']] = 1
            else:
                videos_per_day_dict[self.data[keys]['upload_date']] += 1
        total_number_of_vids = 0
        for keys in videos_per_day_dict.keys():
            total_number_of_vids += videos_per_day_dict[keys]
        print("Mean videos uploaded every day: ", total_number_of_vids/len(videos_per_day_dict) )
        print("Total videos: ", total_number_of_vids)
        print("Number of days: ", len(videos_per_day_dict))
    def is_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False


class Poller:

    def __init__(self):
        self.bottom1k = []
        self.middle1k = []
        self.top1k = []
        self.rank_data = []
        self.bottom_responses = []
        self.middle_responses = []
        self.top_responses = []
        self.data = {}
        with open('video_dist.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.rank_data.append(tuple(row))

    def parse_dataset(self, path):

         with open(path) as data_file:
            self.data = json.load(data_file)

    def select_1000_in_range(self, starting_rank, ending_rank, group):
        #Starting rank and ending rank are the rank of videos by length
        random.seed()
        #use this to build random URL's
        for n in range(0, 1000):
            index = random.randrange(starting_rank, ending_rank)
            title = self.rank_data[index]#video id
            title = title[1]
            title = self.data[title]['title']
            title = title.replace(" ", "_")
            vid_id = self.rank_data[index][0]

            if(group == "bottom"):
                self.bottom1k.append("http://xhamster.com/movies/"+vid_id+"/"+title)
            elif(group == "middle"):
                self.middle1k.append("http://xhamster.com/movies/"+vid_id+"/"+title)
            else:
                self.top1k.append("http://xhamster.com/movies/"+vid_id+"/"+title)





    def analyse_res(self, list):
        count = 0
        map = {}
        map_htmlcheck = {}
        for res in list:
            if(not(res == None)):
                if(res.status_code not in map.keys()):
                    map[res.status_code] = 1
                elif(res.status_code in map.keys()):
                    map[res.status_code] +=1
                if res.status_code not in map_htmlcheck.keys():
                    if self.check_content(res):
                        map_htmlcheck[res.status_code] =1
                elif res.status_code in map_htmlcheck.keys():
                    if self.check_content(res):
                        map_htmlcheck[res.status_code] += 1
        if(200 in map.keys()):
            print("200: ", map[200]/len(list))
        if(200 in map_htmlcheck.keys()):
            print("200 (content check): ", map_htmlcheck[200]/len(list))
        if(301 in map.keys()):
            print("301: ", map[301]/len(list))
        if(301 in map_htmlcheck.keys()):
            print("301 (content check): ", map_htmlcheck[301]/len(list))
        if(404 in map.keys()):
            print("404: ", map[404]/len(list))
        if(404 in map_htmlcheck.keys()):
            print("404 (content check): ", map_htmlcheck[404]/len(list))
        if(410 in map.keys()):
            print("410: ", map[410]/len(list))
        if(410 in map_htmlcheck.keys()):
            print("410 (content check): ", map_htmlcheck[410]/len(list))
        if(500 in map.keys()):
            print("500: ", map[500]/len(list))
        if(500 in map_htmlcheck.keys()):
            print("500 (content check): ", map_htmlcheck[500]/len(list))
        if(503 in map.keys()):
            print("503: ", map[503]/len(list))
        if(503 in map_htmlcheck.keys()):
            print("503 (content check): ", map_htmlcheck[503]/len(list))
        if(504 in map.keys()):
            print("504: ", map[504]/len(list))
        if(504 in map_htmlcheck.keys()):
            print("504 (content check): ", map_htmlcheck[504]/len(list))
    def poll_address(self, uris, group):


        rs = (grequests.get(u, timeout=100, allow_redirects=True) for u in uris)

            # Add the task to our list of things to do via async


        # Do our list of things to do via async
        responses = grequests.map(rs)


        return responses

    def check_content(self, response):
        #for response in responses:
        if(response.status_code == 200):

            #print(response.url, len(response))
            init_title = response.url
            temp_title = init_title[init_title.rfind('/')+1:len(init_title)-5]
            title = temp_title.replace('_', ' ')
        #print(response.content)
            content = response.content.decode("utf-8")
            title_final = title.lower()
            content_final = content.lower()
            if title_final in content_final or temp_title.lower() in content_final:#Need to come up with a classification based on the response
                return True
            else:
                return False
#print(title, "was found in ", response.url
if __name__ == '__main__':

    xhamsterParser = Parser()
    xhamsterParser.parse_dataset('xhamster.json')
    xhamsterParser.power_law()
    #xhamsterParser.find_longest_vid()
    #xhamsterParser.dataset_summary()
    #xhamsterParser.get_final_date()
    #print("Number of videos: ")
    #xhamsterParser.ratings_per_video()
    #xhamsterParser.views_number_categories()
    #xhamsterParser.get_number_of_videos()
    #xhamsterParser.timeline_video_uploads()
    #xhamsterParser.video_size_dist()
    #xhamsterParser.make_categories_tuples()
    #xhamsterParser.most_popular_category_single_category()
    #xhamsterParser.calculate_table_3()
    #xhamsterParser.most_popular_category()
    #xhamsterParser.video_uploads_per_author()
    #xhamsterParser.videos_per_day()
    #xhamsterParser.hotset_analysis()
    #poller = Poller()
    #print(1)
    #poller.parse_dataset('xhamster.json')
    #print(2)
    #poller.select_1000_in_range(0,(int(len(poller.rank_data)/10)), 'bottom') #bottom 10%
    #poller.analyse_res(poller.poll_address(poller.bottom1k, 'bottom'))
    #print(3)
    #poller.select_1000_in_range(int(len(poller.rank_data)*0.45), int((len(poller.rank_data)*0.55)), 'middle')
    #poller.analyse_res(poller.poll_address(poller.middle1k, 'middle'))
    #print(4)
    #poller.select_1000_in_range(int(len(poller.rank_data)*0.9), int(len(poller.rank_data)-1), 'top')
    #poller.analyse_res(poller.poll_address(poller.top1k, 'top'))

    print("Complete")
   # print("Number of users: ")
 #   xhamsterParser.get_number_of_users()

