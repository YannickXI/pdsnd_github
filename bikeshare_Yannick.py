import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data for the city of your choice!')
    # get user input for city (chicago, new york city, washington). 

    while True:
        city = input ('Which City are you interessted in: Chicago, New York City or Washington?\n').lower()
        if city not in ['chicago', 'new york city', 'washington']:
            print ('\nPlease check your information again. Has a typo maybe snuck in?: ')
            continue
        else:
            break

    # get user input for month (all, january, february, march, april, july , june)
    while True:
        month = input('Alright, next the relevant month: We have exciting data for January to June each! Alternatively "all" for the complete half of the year.\n').lower()
        if month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
            print ('\nPlease choose one speficic month (January, February... or all for the whole year): ')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday,  sunday)
    while True:
        day = input('Almost done, which day of the week are you interested in?:\n').lower()
        if day not in ('all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
            print ('\nPlease check your input! Do you want to see all or a specific day (e.g. Monday)?')
            continue
        else:
            break

    message = "Awesome! Let's have a look at the data we have for {}, {}, {}"
    print(message.format(city, month, day))
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):

# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def times_travel(df):
#1 Popular times of travel (i.e., occurs most often in the start time)

    print('\nCalculating the most popular times of travel...\n')
    start_time = time.time()

    #most common month

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most common start month: ', popular_month)

    #most common day

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day'] = df['Start Time'].dt.day
    popular_day = df['day'].mode()[0]
    print('Most common start day: ', popular_day)

    #most common hour of day

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour:', popular_hour)

    #calculation time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def stations_trip(df):
    
    #2 Popular stations and trip
    
    print('\nCalculating the most popular stations and trips...\n')
    start_time = time.time()

    # most common start station

    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most common start station:', Start_Station)

    # most common end station

    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost common end station:', End_Station)

    #most common trip from start to end (i.e., most frequent combination of start station and end station)  

    Combination_Station = df.groupby(['Start Station', 'End Station']).count().idxmax()
    print('\nMost common trip from start to end:', Start_Station, " & ", End_Station)


    #calculation time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration (df):

    #3 Trip duration
   
    print('\nCalculating the total travel and average travel time...\n')
    start_time = time.time()

    #total travel time
    
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", total_duration)

    # average travel time
    mean_duration = df['Trip Duration'].mean() / 60.0
    print("average travel time in minutes is: ", mean_duration)

    #calculation time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_info (df):

    #4 User info

    print('\nCalculating the user info...\n')
    start_time = time.time()

    #counts of each user type

    user_types = df['User Type'].value_counts()
    print('User types:\n', user_types)

    #counts of each gender (only available for NYC and Chicago)

    try:
      gender_types = df['Gender'].value_counts()
      earliest_year_of_birth = int(df['Birth Year'].min())
      most_recent_year_of_birth = int(df['Birth Year'].max())
      most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
      print('\nGender types:\n', gender_types)
      print('\nOldest driver:', earliest_year_of_birth)
      print('\nYoungest driver:', most_recent_year_of_birth)
      print('\nMost common year:', most_common_year_of_birth)
    except KeyError:
        print('\nWe can provide more detailed user info for NYC and Chicago. Have a look!')



    #calculation time

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        times_travel(df)
        stations_trip(df)
        trip_duration(df)
        user_info(df)
      
        restart = input('\nThat was fun! Would you like to do it again? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()