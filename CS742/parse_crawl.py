import json
import re
from jsonmerge import merge
class parse_crawl:

    def __init__(self):

        #self.data = self.combine_json()
        self.data = Parser.data
        self.dates = ["27-11-2016", "28-11-2016", "29-11-2016", "30-11-2016"]


    def trim_data_to_day(self):
        trim_data = []
        for line in self.data:
            if line["upload_date"] in self.dates :
                views = line['nb_views']
                plays = views.split(":", 1)[1]
                line['nb_views'] = plays

                trim_data.append(line)
        self.parse_time(trim_data)
        with open("/Users/Ben/PycharmProjects/CS742/Crawl_Data/29-11-2016_trim.json", 'w') as outfile:
            json.dump(trim_data, outfile, indent=4)

        self.data = trim_data

    def parse_time(self, data):
        for line in data:
            time = line['duration']
            times = re.findall(r'\d+', time)
            time_in_seconds = 0
            i = len(times)-1
            j = 1
            while i >= 0:
                time_in_seconds += (int(times[i]) * j)
                j *= 60
                i -= 1
           # print("Original: ", time, " Post-conversion: ", time_in_seconds)
            line['duration'] = time_in_seconds
    def create_summary(self):
        #This method will be used to create a summary of the day
        #Basically there will be an aggregation of all of the fields along with an average
        number_of_vids = len(self.data)
        avg_views = 0
        total_views = 0
        avg_comments = 0
        total_comments = 0
        total_tags = 0
        avg_tags = 0
        total_duration = 0
        avg_duration = 0
        #use the loop for aggregation then use number_of_vids for calculating averages.
        for line in self.data:
            if self.is_int(line['nb_views']):
                total_views += int(line['nb_views'])
            if self.is_int(line['nb_comments']):
                total_comments += int(line['nb_comments'])

            total_tags += len(line['tags'])

            total_duration += line['duration']
        avg_views = total_views/number_of_vids
        avg_comments = total_comments/number_of_vids
        avg_tags= total_tags/number_of_vids
        avg_duration = total_duration/number_of_vids

        print("The total number of views: ", total_views, " and the average number of views: ", avg_views)

        print("The total number of comments: ", total_comments, " and the average number of comments: ", avg_comments)

        print("The total number of tags: ", total_tags, " and the average number of tags: ", avg_tags)

        print("The total duration of videos: ", total_duration, " and the average duration of videos: ", avg_duration)



    def combine_json(self):
        ##In this method, we plan to combine all of the json, then trim out only the crawled data from the 27-11-2016 --> 4-12-2016

        with open("/Users/Ben/PycharmProjects/CS742/Crawl_Data/28-11-2016.json") as file:
            first = json.load(file)
        with open("/Users/Ben/PycharmProjects/CS742/Crawl_Data/29-11-2016.json") as file:
            second = json.load(file)

        with open("/Users/Ben/PycharmProjects/CS742/Crawl_Data/30-11-2016.json") as file:
            third = json.load(file)

      #  fourth = json.load("1-12-2016.json")
        first.extend(second)
        first.extend(third)
        return first
    def is_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False
