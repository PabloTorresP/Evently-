import pygsheets

#authorization
gc = pygsheets.authorize(service_file='evently_credentials.json')

def fetcher():
    cred_sheet = gc.open('Credentials')
    cred_sheet = cred_sheet.worksheet('index', 0)
    usernames = cred_sheet.get_col(1, include_tailing_empty=False)
    passwords = cred_sheet.get_col(2, include_tailing_empty=False)
    login(cred_sheet, usernames, passwords)
def login(cred_sheet, usernames, passwords):
    input_username = input('Enter your Username')
    input_password = input('Enter your Password')
    for a in usernames:
        if (a == input_username) and (passwords[usernames.index(a)] == input_password):
            print('Login Successful')
            return()
    while True:
        create = int(input('Account not found. Want to create an account? Enter 0 to retry and 1 to create account'))
        if create == 1:
            account_create(cred_sheet, usernames)
        elif create == 0:
            login(cred_sheet, usernames, passwords)

def account_create(cred_sheet, usernames):
    new_username=input('Enter your new Username')
    new_password=input('Enter your new password')
    new_age=int(input('Enter your age'))
    new_preferences=input('xx')

    cred_sheet.link()
    cred_sheet.insert_rows(len(usernames),
                           values=[new_username, new_password, new_age, new_preferences]
                           )
    cred_sheet.unlink()
    fetcher()


fetcher()



