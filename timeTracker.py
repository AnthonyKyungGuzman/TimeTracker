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

                print(previous_window) #prints in which window I am
                print(previous_url)
                print(time_entry.serialize())

                start_time = datetime.datetime.now()
            first_time = False
            previous_url = url
            previous_window = window_name
            

        time.sleep(1)
