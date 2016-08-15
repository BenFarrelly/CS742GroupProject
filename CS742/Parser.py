__author__ = 'Ben'
import json
import csv
import operator
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

    def parse_dataset(self, path):

         with open(path) as data_file:
            self.data = json.load(data_file)


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
                self.video_size.append(self.data[keys]['runtime'])

        self.video_size.sort()
        self.video_size.reverse()
        self.write_video_dist()
    def write_video_dist(self):
        with open('video_dist.csv','w', newline='\n') as csvfile:
            #fieldnames = ['Date', 'Number of videos', 'Number of Active Users']
            writer = csv.writer(csvfile)

            for keys in self.video_size:

                writer.writerow([keys])

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

    def make_categories_tuples(self):
        self.data_category_tuples = self.data
        for keys in self.data.keys():
            temp = self.data[keys]['channels']
            temp_tuple = tuple(temp)
            self.data_category_tuples[keys]['channels'] = temp_tuple
    def is_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False


if __name__ == '__main__':

    xhamsterParser = Parser()
    xhamsterParser.parse_dataset('xhamster.json')
    #print("Number of videos: ")
    xhamsterParser.get_number_of_videos()
   # xhamsterParser.timeline_video_uploads()
   # xhamsterParser.video_size_dist()
    xhamsterParser.make_categories_tuples()
    xhamsterParser.most_popular_category()
    print("Complete")
   # print("Number of users: ")
 #   xhamsterParser.get_number_of_users()

