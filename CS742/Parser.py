__author__ = 'Ben'
import json
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

            #uploader = self.data[keys]['uploader']
            #if uploader in self.users_list:
            #    pass
            #else:
            #    self.users_list.append(uploader)

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
        #print("Number of users: ")
        #print(len(self.users_list))
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
    #print("Number of users: ")
 #   xhamsterParser.get_number_of_users()

