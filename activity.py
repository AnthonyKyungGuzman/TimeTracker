import datetime
import json
from dateutil import parser


class ActivityList:
    def __init__(self, activities):
        self.activities = activities
    
    def initialize_me(self):
        activity_list = ActivityList([])
        with open('activities.json', 'r') as f:
            data = json.load(f)
            activity_list = ActivityList(
                activities = self.get_activities_from_json(data)
            )
        return activity_list
    
    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    name = activity['name'],
                    time_entries = self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list
    
    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time = 0,
                    end_time = 0,
                    days = entry['days'],
                    hours = entry['hours'],
                    minutes = entry['minutes'],
                    seconds = entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list
    
    def serialize(self):
        return {
            'activities' : self.activities_to_json()
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        
        return activities_
    
    def __str__(self):
        return 'activities:' + '\n' +''.join(self.print_activities_to_json())+ '\n'

    def print_activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.__str__())
        return activities_

    def get_total_time_per_activity(self):
        for activity in self.activities:
            activity.get_total_time_of_activity()
            
            


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name' : self.name,
            'time_entries' : self.make_time_entries_to_json()
        }
    
    def make_time_entries_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list
    
    def __str__(self):
        return '\tname:' +  str(self.name)+ '\n' +'\ttime_entries:' + '\n'+ ''.join(self.print_make_time_entries_to_json()) + '\n\n\n'
    
    def print_make_time_entries_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.__str__())
        return time_list

    def get_total_time_of_activity(self):
        total_time = TimeEntry(0,0,0,0,0,0)
        for time in self.time_entries:
            total_time.seconds =  total_time.seconds + time.seconds
            total_time.minutes =  total_time.minutes + time.minutes
            total_time.hours = total_time.hours + time.hours
            total_time.days = total_time.days + time.days
            if(total_time.seconds >= 60):
                total_time.seconds = total_time.seconds - 60
                total_time.minutes = total_time.minutes + 1
            if(total_time.minutes >= 60):
                total_time.minutes = total_time.minutes - 60
                total_time.hours = total_time.hours + 1
            if(total_time.hours >= 24):
                total_time.hours =  total_time.hours - 24 
                total_time.days = total_time.days + 1
        self.time_entries = [total_time]

class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'days' : self.days,
            'hours' : self.hours,
            'minutes' : self.minutes,
            'seconds' : self.seconds
        }
    
    def __str__(self):
        return  '\t\tdays:' +  str(self.days)+'\n'+\
                '\t\thours:' + str(self.hours)+'\n'+\
                '\t\tminutes:' + str(self.minutes)+'\n'+\
                '\t\tseconds:'  +str(self.seconds)+'\n\n'
        


class ActivitySummary(ActivityList):
    def __init__(self, activities):
        self.activities = activities
    
    def initialize_daily(self):
        activity_list = ActivitySummary([])
        with open('daily_activity.json', 'r') as f:
            data = json.load(f)
            activity_list = ActivitySummary(
                activities = self.get_activities_from_json(data)
            )
        return activity_list
    
    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:
            return_list.append(
                Activity(
                    name = activity['name'],
                    time_entries = self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list
    
    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time = 0,
                    end_time = 0,
                    days = entry['days'],
                    hours = entry['hours'],
                    minutes = entry['minutes'],
                    seconds = entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list


    def serialize(self):
        return {
            'activities' : self.activities_to_json()
        }
    
    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())
        
        return activities_
     
    def open_os(self):
        activity_list = ActivitySummary([])
        with open('os_activity.json', 'r') as f:
            data = json.load(f)
            activity_list = ActivitySummary(
                activities = self.get_activities_from_json(data)
            )
        return activity_list 
        
    def open_chrome(self):
        activity_list = ActivitySummary([])
        with open('chrome_activity.json', 'r') as f:
            data = json.load(f)
            activity_list = ActivitySummary(
                activities = self.get_activities_from_json(data)
            )
        return activity_list 