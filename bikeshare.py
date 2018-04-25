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
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=""
    city = input('Please select a city (chicago, new york city, or washington): \n')
    while city.lower() not in CITY_DATA.keys():
      city = input('Please try again, select a city from chicago, new york city and washington: \n')
    print('You\'ve selected {}'.format(city.title()))


    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month=input('Would you like to filter the data by month?\nChoose from January, February, March, April, May and June. Type \'all\' for no time filter.\n')
    while month.lower() not in months:
      month = input('Please try again, select a month from January to June, or choose all: \n')
    print('You\'ve selected {}'.format(month.title()))
    month = months.index(month.lower())



    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week=['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day=input('Would you like to filter the data by day?\n Choose from Monday to Sunday. Type \'all\' for no time filter.\n')
    while day.lower() not in day_of_week:
        day= input('Please try again, select a day from Monday to Sunday, or choose all: \n')
    print('You\'ve selected {}'.format(day.title()))

    print('-'*40)

    return city.lower(), month, day.title()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 0:
    # use the index of the months list to get the corresponding int
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    month = df['month'].mode()[0]
    popular_month=months[month-1]

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    popular_day=df['day_of_week'].mode()[0]


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print('The most popular month for traveling is {}.\n\
The most popular day for traveling is {}.\n\
The most popular hour to start your travels is {} o\'Clock.'.format(popular_month, popular_day, popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly used start station of your selected city:')
    pstation=df['Start Station'].mode()[0]
    popular_start_station=df[df['Start Station']==pstation]['Start Station'].value_counts()
    print(popular_start_station)
    print('*'*20)

    # TO DO: display most commonly used end station
    print('\nThe most commonly used end station of your selected city:')
    estation=df['End Station'].mode()[0]
    popular_end_station=df[df['End Station']==estation]['End Station'].value_counts()
    print(popular_end_station)
    print('*'*20)
    # TO DO: display most frequent combination of start station and end station trip
    combined_trip=df.groupby(['Start Station','End Station'])['Start Time'].count().idxmax()
    combined_time=df.groupby(['Start Station','End Station'])['End Station'].value_counts().max()
    print('\nThe most popular trip from start to end:')
    print('Start Station:{}\nEnd Station:{}'.format(combined_trip[0], combined_trip[1]))
    print('Total traveled {} times'.format(combined_time))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: {:.2f} seconds".format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print("Mean travel time: {:.2f} seconds".format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Breakdown of users:\n{}".format(user_types))
    print('*'*20)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender=df['Gender'].value_counts()
        print("Gender counts:\n{}".format(gender))
    else: print('No gender data to share')
    print('*'*20)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("Oldest: {:.0f}".format(df['Birth Year'].min()))
        print("Youngest: {:.0f}".format(df['Birth Year'].max()))
        common_birth=df['Birth Year'].mode()[0]
        common_birth_count=df[df['Birth Year']==common_birth]['Birth Year'].count()
        print("Most popular birth year: {:.0f}, {:.0f} people in total ".format(common_birth, common_birth_count))
    else: print('No birth year data to share')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
