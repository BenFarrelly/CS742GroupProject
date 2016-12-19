import csv
import json

__author__ = 'Ben'

class xnxx():

    def __init__(self):
        self.data = {}
        self.category_list = []



    def parse_dataset(self, path):

         with open(path) as data_file:
            self.data = json.load(data_file)

    def number_of_comments_per_video(self):
        number_comments = 0
        number_videos = 0
        for keys in self.data.keys():
            if 'nb_comments' in self.data[keys]:
                if(self.is_int(self.data[keys]['nb_comments'])):
                    number_videos += 1
                    number_comments += self.data[keys]['nb_comments']
        mean_comments = number_comments / number_videos
        print("The mean number of comments is: ", mean_comments)

    def number_categories_per_video(self):

        aggregate_categories = 0
        number_vids = 0

        for keys in self.data.keys():
            if 'tags' in self.data[keys]:
                number_vids += 1
                aggregate_categories += len(self.data[keys]['tags'])

        mean_tags = aggregate_categories / number_vids
        print("The mean number of categories is:", mean_tags)

    def total_number_categories(self):
       # category_list = []
        for keys in self.data:
            if "tags" in self.data[keys]:
                for tags in self.data[keys]['tags']:
                    if tags in self.category_list:
                        continue
                    else:
                        self.category_list.append(tags)
        print("Number of categories: ", len(self.category_list))

    def category_popularity(self):
        category_dict = dict.fromkeys(self.category_list, 0)
        for keys in self.data.keys():
            if "tags" in self.data[keys]:
                for tags in self.data[keys]['tags']:
                    if(tags in category_dict):
                        category_dict[tags] += 1
                    else:
                        category_dict[tags] = 1
        with open('category_popularity_xnxx.csv', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            print("About to start writing videos per category")
            for keys in category_dict.keys():
                writer.writerow([keys, category_dict[keys]])

    def is_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False
        except TypeError:
            return False
if __name__ == '__main__':

    x  = xnxx()
    x.parse_dataset("xnxx.json")
    x.number_of_comments_per_video()
    x.number_categories_per_video()
    x.total_number_categories()
    x.category_popularity()
    print("Complete")