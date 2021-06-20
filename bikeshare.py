#Ahmed Mousa
#s-ahmed.mosa@zewailcity.edu.eg

import pandas as pd
import numpy as np
'''The code is divided by question, answering five questions:
     1- Do you want to see rows of city data
     2- What are the most popular hours, months, or days (after filtering according to the user's desire)?
     3- What are most popular station and trips
     4- What are total and average trip duration?
     5- What is the user type, gender, and birth years, according to availability '''

cont = 'y'
#A while loop to repeat indefinitely
while cont == 'y':
    #The user chooses from menu
    menu = input('Please, choose the desired city:\n1- Chicago, 2- New York City, 3- Washington: ')
    #This function deals with invalid inputs since it is repeated a lot in the code
    def input_error(valid_list, variable, valid_input):
        '''Takes the input and tests if it is correct or mistaken, and
        redefines the input variable giving a message to user to give
        the correct inputs, then returns the variable

        3 Args
        1- valid_list: a list with the valid possible input
        2- variable: the tested variable
        3- valid_input: a string containing the accepted inputs '''
        while variable not in valid_list:
            variable = input('Error! Enter ' + valid_input + ': ')
        return variable
    #Checking erroneous input
    menu = input_error(['1', '2', '3'], menu, 'a valid integer <1-3>')

    #Using simple integer instead of having to enter the city name
    CITY_DATA = {'1': 'chicago.csv', '2': 'new_york_city.csv', '3': 'washington.csv'}
    #Loading data into the dataframe
    city = pd.read_csv(CITY_DATA[menu])

    #Question (Q)1 starts
    #Asking user if they wish to display five rows
    display = input('Would you like to check five rows of the data? y/n: ')
    #Checking erroneous input
    display = input_error(['y', 'n'], display.lower(), 'y/n')
    #This loop continues displaying data rows as user desires
    for row in range(0, len(city), 5):
        if display == 'y':
            print('\nData rows:\n', city.loc[row:row+4])
            #Although highly improbable, in case the user continues until displaying all rows
            #-6 since rows start from zero
            if row == len(city)-6:
                print(city.loc[row:row+4])
                print('You have been shown all the data rows')
                break
            #Asking user if they want to display more rows
            display = input('Continue displaying the next five rows? y/n: ')
            #Checking erroneous input
            display = input_error(['y', 'n'], display.lower(), 'y/n')
    #Q1 ends

    #Q2 Starts
    #Popular times
    #Asking user if they want to filter
    filter = input('Filter start time data? y/n: ')
    filter = input_error(['y', 'n'], filter.lower(), 'y/n')

    #These two functions help with the next section
    #A function to create month, day, and hour columns since this occurs a lot
    def time_columns(column):
        #From Start time, month, day, and hour extracted
        column = pd.to_datetime(column)
        month = column.dt.month
        day = column.dt.weekday_name
        hour = column.dt.hour
        return month, day, hour

    #Since it repeats twice, a function to return day list and dictionary
    def day_processing():
        day_list = ['1- Saturday', '2- Sunday',
                                      '3- Monday', '4- Tuesday',
                                      '5- Wednesday', '6- Thursday',
                                      '7- Friday']
        #Creating a dictionary to correspond input integer with day name
        day_dic = {'1': 'Saturday', '2': 'Sunday',
                                      '3': 'Monday', '4': 'Tuesday',
                                      '5': 'Wednesday', '6': 'Thursday',
                                      '7': 'Friday'}
        return day_list, day_dic

    #Filter is chosen?
    if filter == 'y':
        #Filter by month?
        month_filter = input('Would you like to filter by month? y/n: ')
        month_filter = input_error(['y', 'n'], month_filter.lower(), 'y/n')
        #Filter by month is chosen
        if month_filter == 'y':
            month_list = ['1- January', '2- February',
                          '3- March', '4- April',
                          '5- May', '6- June']
            #Choose a month from list
            month_choose = input('Choose the month {}: '.format(month_list))
            #Using numpy for easier creating of the string list of integers
            month_choose = input_error([str(num) for num in np.arange(1, 7)], month_choose,
                                       'valid integer <1-6>')
            #Creating required columns using the function
            city['month'], city['day'], city['hour'] = time_columns(city['Start Time'])
            city = city[city['month'] == int(month_choose)]

            #Further filter by day?
            day_filter = input('Would you like to filter by day? y/n: ')
            day_filter = input_error(['y', 'n'], day_filter.lower(), 'y/n')
            if day_filter == 'y':
                #Using the function to create the needed list and dictionary
                day_list, day_dic = day_processing()
                #The day choice input 1-7
                day_choose = input('Choose the day {}: '.format(day_list))
                day_choose = input_error([str(num) for num in np.arange(1, 8)], day_choose,
                                                       'valid integer <1-7>')
                #Changing dataframe to contain only chosen day along with chosen month
                city = city[city['day'] == day_dic[day_choose]]
                #Most poular hour
                #Dropping NaN
                city['hour'].dropna()
                print('\nMost popular hour in chosen month and day:\n', city['hour'].mode()[0])

            #No day filter
            elif day_filter == 'n':
                #Displaying day and hour
                #Dropping NaN
                city['day'].dropna()
                city['hour'].dropna()
                print('\nMost popular day in chosen month:\n', city['day'].mode()[0])
                print('\nMost popular hour in chosen month:\n', city['hour'].mode()[0])

        #No month filter
        elif month_filter == 'n':
            #Ask about day filter
            day_filter = input('Would you like to filter by day? y/n: ')
            day_filter = input_error(['y', 'n'], day_filter.lower(), 'y/n')
            #Day filter chosen
            if day_filter == 'y':
                #Using the function to create the needed list and dictionary
                day_list, day_dic = day_processing()
                #The day choice input 1-7
                day_choose = input('Choose the day {}: '.format(day_list))
                day_choose = input_error([str(num) for num in np.arange(1, 8)], day_choose,
                                                       'valid integer <1-7>')
                #Creating required columns using the function
                city['month'], city['day'], city['hour'] = time_columns(city['Start Time'])
                city = city[city['day'] == day_dic[day_choose]]
                city['month'].dropna()
                city['hour'].dropna()
                #Printed if no day filtering
                print('\nMost popular month containing chosen day:\n', city['month'].mode()[0])
                print('\nMost popular hour in chosen day:\n', city['hour'].mode()[0])

    #This part is executed if no filter is chosen
    elif filter == 'n':
        #Dropping NaN
        city['Start Time'].dropna()
        #Creating required columns for each time format
        city['month'], city['day'], city['hour'] = time_columns(city['Start Time'])
        #Printing most popular day, month and hour
        print('\nMost popular month:\n', city['month'].mode()[0])
        print('\nMost popular day:\n', city['day'].mode()[0])
        print('\nMost popular hour:\n', city['hour'].mode()[0])
        #Q2 ends

    #Q3 starts
    #Stations and trips
    #Checking for NaN
    city['Start Station'].fillna('Unspecified Station')
    city['End Station'].fillna('Unspecified Station')
    #Creating a new column for trips
    city['Trip'] = city['Start Station'] + ' To ' + city['End Station']
    #Disaplaying most popular start, end, and trip
    print('\nMost popular start station(s):\n', city['Start Station'].mode()[0])
    print('\nMost popular end station(s):\n', city['End Station'].mode()[0])
    print('\nMost popular trip(s):\n', city['Trip'].mode()[0])
    #Q3 ends

    #Q4 starts
    #Trip duration
    #Check for any NaN values and replace
    city['Trip Duration'].fillna(0)
    #Store the total travel time in a variable for easiness of use in format function
    total = city['Trip Duration'].sum()
    #Total time is very large in seconds, so it is useful to turn into minutes and hours
    print('\nTotal traveling time is {} seconds,i.e {} minutes, i.e {} hours.'.format(total, total/60, total/3600))
    #Average time is easy to read, so left in seconds
    print('Average traveling time is {} seconds'.format(city['Trip Duration'].mean()))
    #Q4 ends

    #Q5 starts
    #User info
    #Check for any NaN values and replace
    city['User Type'].fillna('Unspecified')
    #Display each user type count
    print('\nUser type counts:\n', city['User Type'].value_counts())
    #Displaying gender and birth years info for chicago and NYC
    if menu in ['1', '2']:
        #Check for NaN
        city['Gender'].fillna('Unspecified')
        #Display each gender count
        print('\nGender counts:\n', city['Gender'].value_counts())

        #Birth years
        #Dropping NaN
        city['Birth Year'].dropna(axis = 0)
        #Showing most common, earliest, and latest birth years
        print('\nMost common birth year(s):\n', city['Birth Year'].mode()[0])
        print('Earliest birth year:\n', min(city['Birth Year']))
        print('Most recent birth year:\n', max(city['Birth Year']))
    #Q5 ends

    #The user is asked if they wish to continue:
    cont = input('Continue? y/n: ')
    cont = input_error(['y', 'n'], cont.lower(), 'y/n')

