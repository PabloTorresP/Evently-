##Imports
import pygsheets
import pandas as pd
from datetime import date
import datetime as dt
from heapq import heappush, heapify
import PySimpleGUI as sg
import sys

###Load the CSV File containing concerts
concerts =pd.read_csv('concerts.csv', header=0)


##Cleaning and formating data (date column to datetime, time to integer, energy to integer and price to float
concerts['Date (dd-mm-yyyy)'] = (pd.to_datetime(concerts['Date (dd-mm-yyyy)'], dayfirst=True, format='mixed'))
timearray=[]

for i in range (len(concerts['Time'])):
    timearray.append(int(concerts.iloc[i,3].replace(':','')))

concerts['Time'] = timearray
concerts['Energy (Scale of 1 to 10)'].astype(int)
concerts[('Price')].astype(float)

#authorization to credentials database
gc = pygsheets.authorize(service_file='evently_credentials.json')

def fetcher():
    """Function to fetch the usernames and passwords from the credentials database"""
    cred_sheet = gc.open('Credentials')  ##Open the database
    cred_sheet = cred_sheet.worksheet('index', 0)  ##Select the correct sheet
    usernames = cred_sheet.get_col(1, include_tailing_empty=False)  ##Fetch the usernames
    passwords = cred_sheet.get_col(2, include_tailing_empty=False)  ##Fetch the passwords
    login(cred_sheet, usernames, passwords)
def login(cred_sheet, usernames, passwords):
    """Function for the login window"""

    ##Layout of the login window
    login_layout = [[sg.Text('Welcome to Evently!')],
              [sg.Text('Enter your username and password to login')],
              [sg.Text('Username'), sg.InputText(key='us')],
              [sg.Text('Password'), sg.InputText(key='pass')],
              [sg.Button('Log In'), sg.Button('Create Account')]]

    login_window = sg.Window(title="Evently Log In", layout=login_layout)
    event, values = login_window.read()
    login_window.close()

    ##Function call to create account if button clicked
    if event == "Create Account":
        account_create(cred_sheet, usernames)

    ##Fetch inputs from the GUI and store un variables
    input_username = values['us']
    input_password = values['pass']

    ##Loop to search for username, and if found check the match with the password
    for a in usernames:
        if (a == input_username) and (passwords[usernames.index(a)] == input_password):
            ##Creation of the output window
            success_layout = [[sg.Text('Login Successful!')],
                      [sg.Button('Access')]]
            success_window = sg.Window(title="Successful Login", layout=success_layout)
            events, values = success_window.read()
            success_window.close()

            ##Under button click, function call to main menu
            if events == 'Access':
                mainmenu()
            else:
                return()

    ##If all of the above failed, user is not found so creation of failure window
    failure_layout = [[sg.Text('Login Failed! Retry or Create Account')],
                      [sg.Button('Retry'), sg.Button('Create Account')]]
    failure_window = sg.Window(title="Failed Login", layout=failure_layout)
    event, values = failure_window.read()
    failure_window.close()

    ##Function calls to redirect user based on their input
    if event == 'Retry':
        login(cred_sheet, usernames, passwords)
    elif event == 'Create Account':
        account_create(cred_sheet, usernames)
    else:
        sys.exit()



def account_create(cred_sheet, usernames):

    ##Create layout for the account creation window
    create_layout = [[sg.Text('Welcome to Evently!')],
                    [sg.Text('Create your account')],
                    [sg.Text('Username'), sg.InputText(key='us')],
                    [sg.Text('Password'), sg.InputText(key='pass')],
                    [sg.Text('Age'), sg.InputText(key='age')],
                    [sg.Button('Create Account'), sg.Button('Cancel')]]

    create_window = sg.Window(title="Create Account", layout=create_layout)
    event, values = create_window.read()
    create_window.close()

    if event == 'Create Account':
        ##Link the credentials sheet and add the user to the database
        cred_sheet.link()
        cred_sheet.insert_rows(len(usernames),
                               values=[values['us'], values['pass'], values['age']]
                               )
        cred_sheet.unlink()
        ##Refetch values and return to login
        fetcher()
    else:
        sys.exit()

def artistsearch():
    """Function to search by artist"""

    ##Create layout and fetch values from window
    query_layout = [[sg.Text('Search by Artist Name')],
                    [sg.Text('Artist Name'), sg.InputText(key='para')],
                    [sg.Button('Run'), sg.Button('Cancel')]]

    query_window = sg.Window(title="Artist Search", layout=query_layout)
    event , values = query_window.read()
    query_window.close()
    parameter=values['para']
    if event == 'Cancel':
        sys.exit()

    ##Create array to store index of matches
    matches=[]

    ##Iterate through database checking for matches
    for i in range (len(concerts['Artist'])):
        if parameter.lower() == (concerts.iloc[i, 1]).lower():
            matches.append(i)

    searchoutput(matches)



def timesearch():
    """Function to search by max time"""

    ##Create layout and fetch values from window
    query_layout = [[sg.Text('Search by Maximum Time')],
                    [sg.Text('Time ommitting colon (Ex. 22:30 to 2230)'), sg.InputText(key='para')],
                    [sg.Button('Run'), sg.Button('Cancel')]]

    query_window = sg.Window(title="Time Search", layout=query_layout)
    event, values = query_window.read()
    query_window.close()
    parameter = int(values['para'])
    if event == 'Cancel':
        sys.exit()

    ##Create array to store index of matches
    matches = []

    ##Iterate through database checking for matches
    for i in range (len(concerts['Time'])):
        if parameter >= concerts.iloc[i, 3]:
            matches.append(i)

    searchoutput(matches)

def genresearch():
    """Function to search by genre"""

    ##Create layout and fetch values from window
    query_layout = [[sg.Text('Search by Genre')],
                    [sg.Listbox(values=['Hip Hop', 'Reggaeton', 'Trap', 'Urbana', 'Rock', 'Flamenco',
                                        'R&B', 'Punk ', 'Indie', 'Metal', 'Electronic', 'Pop', 'Jazz'],
                                select_mode='multiple', key='para', size=(30, 6))],
                    [sg.Button('Run'), sg.Button('Cancel')]]

    query_window = sg.Window(title="Genre Search", layout=query_layout)
    event, values = query_window.read()
    query_window.close()
    parameter = values['para']
    if event == 'Cancel':
        sys.exit()

    ##Create array to store index of matches
    matches = []

    ##Iterate through database checking for matches
    for i in range (len(concerts['Genre'])):
        for genre in parameter:
            if genre == concerts.iloc[i, 7]:
                matches.append(i)

    searchoutput(matches)

def pricesearch():
    """Function to search by price"""

    ##Create layout and fetch values from window
    query_layout = [[sg.Text('Search by Maximum Price')],
                    [sg.Text('Maximum Price'), sg.InputText(key='para')],
                    [sg.Button('Run'), sg.Button('Cancel')]]

    query_window = sg.Window(title="Price Search", layout=query_layout)
    event, values = query_window.read()
    query_window.close()
    parameter = float(values['para'])
    if event == 'Cancel':
        sys.exit()

    ##Create array to store index of matches
    matches = []

    ##Iterate through database checking for matches
    for i in range (len(concerts['Price'])):
        if parameter >= concerts.iloc[i, 9]:
            matches.append(i)

    searchoutput(matches)

def searchoutput(matches):
    """Function to output the search results"""
    output_layout = [ [sg.Text('Search Results:')] ]
    x=0

    ##Append the matches to the window layout in the adequate format
    ##X variable limits the entries to a maximum of 8 to not crash the GUI
    for index in matches:
        x += 1
        output_layout.append([sg.Text(
            f'{concerts.iloc[index, 0]} '
            f'by {concerts.iloc[index, 1]} '
            f'at {concerts.iloc[index, 4]} '
            f'follow the link to buy tickets! \n {concerts.iloc[i, 11]}')])
        if x >= 8:
            break

    ##Add buttons and generate the window
    output_layout.append([sg.Button('Return to Menu'), sg.Button('Exit')])
    output_window = sg.Window(title="Search Output", layout=output_layout)
    event, values = output_window.read()
    output_window.close()

    ##Redirect based on button click
    if event == 'Return to Menu':
        mainmenu()
    else:
        sys.exit()

def recommender():
    """Function to recommend concerts"""

    ##Initialise the dictionary to store the score of each concert
    points_dict={}

    ##Window layout
    recommender_layout = [[sg.Text('Welcome to Evently!')],
              [sg.Text('Enter your username and password to login')],
              [sg.Text('Maximum number of days until the concert'), sg.InputText(key='days')],
              [sg.Text('Maximum time for the concert without colon (Ex 22:30 = 2230)'), sg.InputText(key='time')],
              [sg.Listbox(values=['Hip Hop', 'Reggaeton', 'Trap', 'Urbana', 'Rock', 'Flamenco',
                                  'R&B', 'Punk ', 'Indie', 'Metal', 'Electronic', 'Pop', 'Jazz'],
                          select_mode='multiple', key='genres', size=(30, 6))],
              [sg.Text('Desired level of average energy'), sg.InputText(key='energy')],
              [sg.Text('How much you are willing to spend'), sg.InputText(key='price')],
              [sg.Button('Search'), sg.Button('Cancel')]]

    recommender_window = sg.Window(title="Recommender", layout=recommender_layout)

    event, values = recommender_window.read()
    recommender_window.close()

    ##Associate the GUI input to the variables
    if event == 'Cancel':
        sys.exit()
    elif event == 'Search':
        inputdate=int(values['days'])
        time=int(values['time'])
        genres=values['genres']
        energy=int(values['energy'])
        price=float(values['price'])

        ##Creation of the heap to store the concerts
        concertheap = []
        heapify(concertheap)

        for i in range (len(concerts)):
            ##Creation of entry for concert i
            points_dict[i] = []

            ##Computation of points based on date
            if (pd.Timestamp(date.today() + dt.timedelta(inputdate))) >= concerts.iloc[i, 2]:
               points_dict[i].append(1)
            else:
                points_dict[i].append(0)

            ##Computation of points based on time
            if concerts.iloc[i, 3] <= time:
                points_dict[i].append(1)
            elif time < concerts.iloc[i, 3] <= (time + 100):
                points_dict[i].append(0.6)
            elif (time + 100) < concerts.iloc[i, 3] <= (time + 200):
                points_dict[i].append(0.3)
            else:
                points_dict[i].append(0)

            ##Computation of points based on genre
            points_dict[i].append(0)
            for genre in genres:
                if genre == concerts.iloc[i, 7]:
                    points_dict[i].pop()
                    points_dict[i].append(1)

            ##Computation of points based on energy
            if concerts.iloc[i, 8] == energy:
                points_dict[i].append(1)
            elif (concerts.iloc[i, 8] - 1) <= energy <= (concerts.iloc[i, 8] + 1):
                points_dict[i].append(0.6)
            elif (concerts.iloc[i, 8] - 2) <= energy <= (concerts.iloc[i, 8] + 2):
                points_dict[i].append(0.3)
            else:
                points_dict[i].append(0)

            ##Computation of points based on price
            if concerts.iloc[i, 9] <= price:
                points_dict[i].append(1)
            elif price < concerts.iloc[i, 9] <= (price + 10):
                points_dict[i].append(0.6)
            elif (price + 10) < concerts.iloc[i, 9] <= (price + 20):
                points_dict[i].append(0.3)
            else:
                points_dict[i].append(0)

            ##Push the entry into the heap (*-1) to convert to max heap instead of min
            heappush(concertheap, ([sum(points_dict[i])*(-1), i]))


        output_recommender(concertheap)



def output_recommender(concertheap):
    """Function to output results from the recommender"""

    ##Layout of the window, with the top 5 recommendations of the recommender (peeked from heap)
    output_layout = [ [sg.Text('Recommender Results')],
              [sg.Text('These are the top 5 concerts we recommend')],
              [sg.Text(
                  f'1. {concerts.iloc[(concertheap[0][1]), 0]} '
                  f'by {concerts.iloc[concertheap[0][1], 1]} '
                  f'at {concerts.iloc[concertheap[0][1], 4]} '
                  f'with a match score of {concertheap[0][0] * (-1)} out of 5, '
                  f'follow the link to buy tickets! \n {concerts.iloc[concertheap[0][1], 11]}')],
              [sg.Text(
                  f'2. {concerts.iloc[(concertheap[1][1]), 0]} '
                  f'by {concerts.iloc[concertheap[1][1], 1]} '
                  f'at {concerts.iloc[concertheap[1][1], 4]} '
                  f'with a match score of {concertheap[1][0] * (-1)} out of 5, '
                  f'follow the link to buy tickets! \n {concerts.iloc[concertheap[1][1], 11]}')],
              [sg.Text(
                  f'3. {concerts.iloc[(concertheap[2][1]), 0]} '
                  f'by {concerts.iloc[concertheap[2][1], 1]} '
                  f'at {concerts.iloc[concertheap[2][1], 4]} '
                  f'with a match score of {concertheap[2][0] * (-1)} out of 5, '
                  f'follow the link to buy tickets! \n {concerts.iloc[concertheap[2][1], 11]}]')],
              [sg.Text(
                  f'4. {concerts.iloc[(concertheap[3][1]), 0]} '
                  f'by {concerts.iloc[concertheap[3][1], 1]} '
                  f'at {concerts.iloc[concertheap[3][1], 4]} '
                  f'with a match score of {concertheap[3][0] * (-1)} out of 5, '
                  f'follow the link to buy tickets! \n {concerts.iloc[concertheap[3][1], 11]}]')],
              [sg.Text(
                  f'5. {concerts.iloc[(concertheap[4][1]), 0]} '
                  f'by {concerts.iloc[concertheap[4][1], 1]} '
                  f'at {concerts.iloc[concertheap[4][1], 4]} '
                  f'with a match score of {concertheap[4][0] * (-1)} out of 5, '
                  f'follow the link to buy tickets! \n {concerts.iloc[concertheap[4][1], 11]}]')],
              [sg.Button('Return to Main Menu'), sg.Button('Exit')] ]


    ##Window generation
    output_window = sg.Window(title="Recommender Output", layout=output_layout)
    event , values = output_window.read()
    output_window.close()

    ##Kill program or return to main menu
    if event == 'Return to Main Menu':
        mainmenu()
    else:
        sys.exit()

def mainmenu():
    """Function to generate the main menu"""
    menu_layout = [[sg.Text('Main Menu')],
                   [sg.Button('Search By Artist')],
                   [sg.Button('Search By Maximum Time')],
                   [sg.Button('Search By Genre')],
                   [sg.Button('Search By Price')],
                   [sg.Button('Recommender')],
                   [sg.Button('Exit')],
                   ]

    menu_window = sg.Window(title='Main Menu', layout=menu_layout)
    event, values = menu_window.read()
    menu_window.close()

    ##Redirect based on the user input
    if event == 'Search By Artist':
        artistsearch()
    elif event == 'Search By Maximum Time':
        timesearch()
    elif event == 'Search By Genre':
        genresearch()
    elif event == 'Search By Price':
        pricesearch()
    elif event == 'Recommender':
        recommender()
    else:
        sys.exit()


##Function call to initialise the program
fetcher()
