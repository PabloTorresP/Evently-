# EVENTLY-
We are a group of students at IE University who are creating some algorithms that help you filter through the events in a .csv and give you recommendations.Evently is a concert recommendation system implemented in Python. It allows its users to search for concerts based on various criteria such as artist name, date, genre, and price. Additionally, it provides a recommendation feature that suggests concerts based on user preferences.

#  **Dataset**
The dataset presents relevant information about 52 concerts in Madrid, making it a valuable resource for individuals seeking for a concert based on their interests and taste.The data set contains various concerts in genres such as Pop, Techno, Rock, R&B, Flamenco, Trap, Reggaeton, Urbano, Jazz, Blues, and Rap, including Alternative. It encompasses various variables, including:
-   Artist specifications
-   Date of the concert
-   Concert time
-   Latitude and longitude coordinates for the concert location (for mapping)
-   Venue name
-   Energy scale
-   Genre
-   Price

The dataset has been manually created by the group.

#  **Functionalities**
Our platform has two main functions:

- Concert Search:
Users can search for concerts based on various criteria, including artist name, maximum time, genre, and maximum price.
The search results are displayed, and users have the option to return to the main menu or exit.

- Concert Recommendation:
Users can use the recommender system to find concerts based on specified preferences such as date, time, genre, energy level, and price.
The top 5 recommended concerts are displayed, and users can choose to return to the main menu or exit.

#  *External Libraries*
The project relies on several external libraries:

- pygsheets: Used for working with Google Sheets.
- pandas: Used for data manipulation with DataFrames.
- datetime: Used for working with date and time.
- heapq: Used for implementing the heap data structure.
- PySimpleGUI: Used for creating a simple GUI for user interaction.

#  *How to Install the Project*

### Prerequisites
1. Install the required libraries using the following command:
 ```bash
  pip install pygsheets pandas PySimpleGUI
 ```

### Importing the Required Libraries
```python
 Imports
import pygsheets
import pandas as pd
from datetime import date
import datetime as dt
from heapq import heappush, heapify
import PySimpleGUI as sg
import sys
  ```
### **Load the CSV File containing concerts**
  ```
concerts = pd.read_csv('concerts.csv', header=0)
  ```
#  *How to Use the Project*
Upon running the program, you will be prompted to log in or create an account. After logging in, you will be presented with the main menu, offering various search options and the concert recommender.

### Search Options:
- Search By Artist: Allows users to search for concerts by entering their favorite artist's name.
- Search By Maximum Time: Enables users to search for concerts based on a maximum time.
- Search By Genre: Provides the ability to search for concerts by selecting one or more genres.
- Search By Price: Allows users to search for concerts based on a maximum price.

### Concert Recommender
The recommender feature will then suggest concerts based on user preferences for maximum days until the concert, maximum time, desired genres, average energy level, and the budget for the ticket price.

#  *Further improvements*
 - Expand the data set with more genres of music
 - Expand the data set with more cities
 - Expand the data set with more variables such as ticket availability or artist popularity index.
 
#  *Credits*
- Pablo Torres
- Javier Arce
- Arturo Velilla
- Sofia Hervas
- Daniel Garcia
- Nacho Ascanio
- Adolfo Gutierrez


