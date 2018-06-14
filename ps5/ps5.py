# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import sys
sys.setrecursionlimit(10000)

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
        
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate
    
    
    

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, trig_phrase):
        self.trig_phrase = trig_phrase
    
    def get_trig_phrase(self):
        return self.trig_phrase
    
    def is_phrase_in(self, text):
        flag = True
        text = text.lower()
        trig_phrase = self.get_trig_phrase().lower().split()
        for punc in string.punctuation:
            text = text.replace(punc, ' ')
        text = text.split()
        
        for elem in text:
            if trig_phrase[0] == elem:
                for n in range(len(trig_phrase)):
                    try:
                        flag = flag and trig_phrase[n] == text[text.index(elem)+n]
                    except IndexError:
                        flag = flag and False
                if flag:
                    return True
        return False
            
# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, trig_phrase):
        PhraseTrigger.__init__(self, trig_phrase)
#        print('Title received trigger phrase', self.trig_phrase)
    def evaluate(self, story):
#        print('trig is', self.trig_phrase,'return is', self.is_phrase_in(story.get_title()))
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, trig_phrase):
        PhraseTrigger.__init__(self, trig_phrase)
#        print('Desc received trigger phrase', self.trig_phrase)
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
        #3 Oct 2016 17:00:10
class TimeTrigger(Trigger):
    def __init__(self, trig_time):
        self.trig_time = trig_time
#        print('Time received trigger phrase', self.trig_time)
    def get_strtrig_time(self):
        return self.trig_time       
    
    def get_trig_datetime(self):
        return datetime.strptime(self.get_strtrig_time(), "%d %b %Y %H:%M:%S")
    def get_EST_trig_datetime(self):
        return self.get_trig_datetime().replace(tzinfo = pytz.timezone('EST'))

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
        #1987-10-15 00:00:00

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        if story.get_pubdate().tzinfo != None:
            trig_datetime = self.get_EST_trig_datetime()
        else:
            trig_datetime = self.get_trig_datetime()
        
        if story.get_pubdate() < trig_datetime:
            return True
        else:
            return False
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        """ 
        check tzinfo and compare time. 
        Return True if story time after trigger time
        """
        if story.get_pubdate().tzinfo != None:
            trig_datetime = self.get_EST_trig_datetime()
        else:
            trig_datetime = self.get_trig_datetime()
        
        if story.get_pubdate() > trig_datetime:
            return True
        else:
            return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    """
    Input a trigger
    Attribute "evaluate" Return a invert trigger's evaluation.
    """
    def __init__(self, a_trigger):
        self.a_trig = a_trigger
    def get_a_trig_eva(self, story):
        return self.a_trig.evaluate(story)
    def evaluate(self, story):
        return not self.get_a_trig_eva(story)
    
    
        
# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    """
    Input two triggers
    Attribute "evaluate" Return True if both tirggers fire""" 
    def __init__(self, a_trigger, b_trigger):
        self.a_trig = a_trigger
        self.b_trig = b_trigger
#        print('and received trigger phrase', self.a_trig, self.b_trig)
    def get_a_trig_eva(self, story):
        return self.a_trig.evaluate(story)
    def get_b_trig_eva(self, story):
        return self.b_trig.evaluate(story)
    def evaluate(self, story):
        return self.get_a_trig_eva(story) and self.get_b_trig_eva(story)
    
    

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    """
    Input two triggers
    Attribute "evaluate" Return True if either one (or both) tirggers fire""" 
    def __init__(self, a_trigger, b_trigger):
        self.a_trig = a_trigger
        self.b_trig = b_trigger
    def get_a_trig_eva(self, story):
        return self.a_trig.evaluate(story)
    def get_b_trig_eva(self, story):
        return self.b_trig.evaluate(story)
    def evaluate(self, story):
        return self.get_a_trig_eva(story) or self.get_b_trig_eva(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    triggerlist = []
    trig_dict = {}
    
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line.split(','))
    # make each line a list
    # check the index[0] of a list, 
    for elem in lines:
        if elem[1] == 'TITLE' or elem[1] == 'DESCRIPTION' or elem[1] == 'AFTER' or elem[1] == 'BEFORE':
            trig_dict[elem[0]] = trigger_convert(elem[1])(elem[2])
#            print(elem, trig_dict[elem[0]])
            
    for elem in lines:
        if elem[1] == 'NOT':
            trig_dict[elem[0]] = trigger_convert(elem[1])(trig_dict[elem[2]]) # trig_dict[elem[2]] is a name like 't1'
#            print(elem, trig_dict[elem[0]])# trig_dict[elem[2]] is a name like 't1'
    for elem in lines: 
        if elem[1] == 'AND' or elem[1] == 'OR':
            trig_dict[elem[0]] = trigger_convert(elem[1])(trig_dict[elem[2]],trig_dict[elem[3]])
#            print(elem, trig_dict[elem[0]])
    for elem in lines:
        if elem[0] == 'ADD': # 'ADD'
            for unit in elem[1:len(elem)]:
                triggerlist.append(trig_dict[unit])
                
    # check input are phrases, time, or triggers
    # make a triggerlist
    
    
    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

#    print(lines) # for now, print it so you see what it contains!
    return triggerlist



SLEEPTIME = 120 #seconds -- how often we poll


def trigger_convert(a_str):
    trig_pointer = {'TITLE':TitleTrigger, 'DESCRIPTION':DescriptionTrigger, 
                    'AFTER':AfterTrigger, 'BEFORE':BeforeTrigger, 
                    'NOT':NotTrigger, 'AND':AndTrigger, 'OR':OrTrigger}
    return trig_pointer[a_str]

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
#        t1 = TitleTrigger("election")
#        t2 = DescriptionTrigger("Trump")
#        t3 = DescriptionTrigger("Clinton")
        t1 = TitleTrigger("Trump")
        t2 = DescriptionTrigger("North")
        t3 = AfterTrigger('3 Oct 2017 17:00:10')
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]
#        print(triggerlist)

        # Problem 11
#         TODO: After implementing read_trigger_config, uncomment this line 
#        triggerlist = read_trigger_config('triggers.txt')
        triggerlist = read_trigger_config('debate_triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))
            
            stories = filter_stories(stories, triggerlist)
            
            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

