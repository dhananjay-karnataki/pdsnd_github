import time

import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

DAY = {'1': 'Sunday', '2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday', '7': 'Saturday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while 1:
        city = input(" Would you like to analyze bikeshare data for chicago, new york city or washington: ").lower()
        if city == "chicago" or city == "new york city" or city == "washington":
            break
    # Get user input for month (all, january, february, ... , june)
    while 1:
        group = input(
            "Would you like to analyze data by any specific month, day or both? Type 'none' for no time filter: ").lower()
        if group in ('month', 'day', 'both', 'none'):
            if (group == "month") | (group == "both"):
                while 1:
                    month = input("For which month(january, february, ... , june): ").lower()
                    if month in ("january", "february", "march", "april", "may", "june"):
                        break
            else:
                month = "all"

            if (group == "day") | (group == "both"):
                while 1:
                    day = input("Which day? Please type your response as an integer.(e.g.,1=Sunday): ")
                    if day in ('1', '2', '3', '4', '5', '6', '7'):
                        break
            else:
                day = "0"
            break
    # Get user input for day of week (all, monday, tuesday, ... sunday)

    print('-' * 40)
    return city, month, day


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
    city_df = pd.read_csv(CITY_DATA[city])
    city_df['Start Time'] = pd.to_datetime(city_df['Start Time'])
    city_df['End Time'] = pd.to_datetime(city_df['End Time'])
    city_df['Month'] = city_df['Start Time'].dt.month_name()
    city_df['Day'] = city_df['Start Time'].dt.day_name()
    city_df['Hour'] = city_df['Start Time'].dt.hour

    if (month == "all") & (day == "0"):
        df = city_df
    if (month != "all") & (day == "0"):
        df = city_df[city_df['Month'] == month.title()]
    if (month == "all") & (day != "0"):
        df = city_df[city_df['Day'] == DAY[day]]
    if (month != "all") & (day != "0"):
        df = city_df[(city_df['Month'] == month.title()) & (city_df['Day'] == DAY[day])]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Display the most common month
    if len(pd.unique(df['Month'])) > 1:
        popular_month = df['Month'].mode()[0]
        print("Most Common bikeshare month is: " + popular_month)
    # Display the most common day of week
    if len(pd.unique(df['Day'])) > 1:
        popular_day = df['Day'].mode()[0]
        print("Most common bikeshare day of the week is: " + popular_day)
    # Display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print("Most Common start hour is: " + str(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("Most Commonly used start station for bikeshare is: " + df['Start Station'].mode()[0])

    # Display most commonly used end station
    print("Most Commonly used end station for bikeshare is: " + df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    df1 = df.groupby(['Start Station', 'End Station']).size().reset_index()
    df1.rename(columns={0: "frequency"}, inplace=True)
    df2 = df1[df1.frequency == df1.frequency.max()].to_dict('records')[0]

    print("Most frequent combination of start station and end station for bikeshare trip is: " + df2['Start Station'] + \
          " and " + df2['End Station'] + ". Trip Count: " + str(df2['frequency']))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time is: " + str(total_travel))
    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time is: " + str(mean_travel))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("Counts per user type are: \n" + str(df['User Type'].value_counts()))

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts per gender are: \n" + str(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(
            "Earliest, most recent, and most common year of birth of users are: " + str(df['Birth Year'].min()) + "," + \
            str(df['Birth Year'].max()) + "," + str(df['Birth Year'].mode()[0]) + " respectively.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if view_data.lower() == "yes":
        start_loc = 0
        while True:
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_display = input("Do you wish to continue? Enter yes or no: ").lower()
            if view_display == "no":
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
