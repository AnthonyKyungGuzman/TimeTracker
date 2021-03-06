from activity import *
from window import *

start_time = datetime.datetime.now()
previous_window = None
window_name = None
complete_window_string = None
url = None
previous_url = None
end_time = None
first_time = True #Flag so it does not adds the first none existing window
activity_window = None
activity_url = None
listOfActivities = ActivityList([])
listOfChromActivities = ActivityList([])

os_activities = ActivitySummary([])
chrome_activities = ActivitySummary([])


counter = 0

if __name__ == '__main__':
   
    while True:
        if('Windows' == os_platform):
            complete_window_string = get_current_window()
            window_name = get_microsoft_current_window(complete_window_string)
        else:
            window_name,complete_window_string = get_current_window()
        if(window_name == 'Google-Chrome' or 'Google Chrome' == window_name ):
            url = get_chrome_website(complete_window_string) # prints the website in which Im exploring

        if(previous_window != window_name or previous_url != url):
            activity_window = previous_window
            activity_url = previous_url
            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry.get_specific_times()

                exists = False
                if(activity_window == 'Google-Chrome' or 'Google Chrome' == activity_window ):
                    for activity in listOfChromActivities.activities:
                        if activity.name == activity_url:
                            exists = True
                            activity.time_entries.append(time_entry)
                else:
                    for activity in listOfActivities.activities:
                        if activity.name == activity_window:
                            exists = True
                            activity.time_entries.append(time_entry)

                if not exists:
                    if(activity_window == 'Google-Chrome' or 'Google Chrome' == activity_window ):
                        activity = Activity(activity_url, [time_entry])
                        listOfChromActivities.activities.append(activity)
                    else:
                        activity = Activity(activity_window, [time_entry])
                        listOfActivities.activities.append(activity)
                    counter = 1 +counter

                with open('os_activity.json', 'w') as json_file:
                    json.dump(listOfActivities.serialize(), json_file,indent=4, sort_keys=True) 
                with open('chrome_activity.json', 'w') as json_file:
                    json.dump(listOfChromActivities.serialize(), json_file,indent=4, sort_keys=True) 

                start_time = datetime.datetime.now()
            first_time = False
            previous_url = url
            previous_window = window_name
            
        if(counter == 5):
            break
        time.sleep(1)

    os_activities = os_activities.open_file('os_activity.json')
    os_activities.get_total_time_per_activity() #getting the total time of the day 
    chrome_activities = chrome_activities.open_file('chrome_activity.json')
    chrome_activities.get_total_time_per_activity()

    print(os_activities)
    with open('os_activity.json', 'w') as json_file:
        json.dump(os_activities.serialize(), json_file,indent=4, sort_keys=True)

    daily_activities = ActivitySummary([])
    daily_activities = daily_activities.open_file('daily_os_activity.json')
    daily_activities.merge_files(os_activities)
    print("Merging times")
    print(daily_activities)

    with open('daily_os_activity.json', 'w') as json_file:
        json.dump(daily_activities.serialize(), json_file,indent=4, sort_keys=True) 

    

