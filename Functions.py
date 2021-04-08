
from datetime import date
import requests
from bs4 import BeautifulSoup
from my_modules.Sapling import Sapling

def check_weather(temps_file, weather_file, weather_list):
    """
    * Name: check_temperature
    * Inputs: file, file, list
    * Return: str
    * Purpose: Check the weather and store it in a list
    """

    # Gets today's date
    today = date.today()

    # Connects to weather service website
    URL = 'https://forecast.weather.gov/MapClick.php?lat=40.5983&lon=-122.4909#.Xqd-7y3MzRY'
    headers = {
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Gets temperature and date
    temp = soup.find('p', class_='temp temp-high').get_text()
    climate = soup.find('p', class_='short-desc').get_text()

    # Append date, climate and temp to weather_list
    weather_list.append(str(today))
    weather_list.append(climate)
    weather_list.append(temp[-5:-3])

    # Print to console and write to files today's temp and date
    print("Today: ", today)
    print("Climate: " + climate)
    print("Temperature: " + temp[-5:-3])
    weather_file.write("Today: " + str(today))
    weather_file.write("\nClimate: " + climate)
    weather_file.write("\n" + temp[-5:-3] + "\n")
    temps_file.write("\n" + temp[-5:-3])

    # Return temp
    return temp[-5:-3]

def is_tag(tag, tag_list):
    """
    * Name: is_tag
    * Inputs: int, list
    * Return: bool
    * Purpose: check to see if tag already exists
    """

    is_found = False

    if tag not in tag_list:
        is_found = False
    else:
        is_found = True

    return is_found

def get_average_height(pine_trees):
    """
    * Name: get_average_height
    * Inputs: list
    * Return: float
    * Purpose: get average height of saplings
    """

    average = 0
    complete_total = 0

    for sap in pine_trees:
        complete_total += sap.get_latest_height()

    average = complete_total / len(pine_trees)

    return average

def add_sapling(pine_trees, all_tags):
    """
    * Name: add_sapling
    * Inputs: list, list
    * Return: None
    * Purpose: create new sapling manually
    """

    is_new_sapling = True   # If entered sapling is actually new
    isnt_float = True       # If entered float is a float

    # Prompt user if they want to add a new sapling
    while is_new_sapling:
        try:
            all_tags.sort()
            print('Tags in use:', all_tags)
            sap_tag = int(input('\nPlease enter the tag (int) for this sapling: '))

            if sap_tag in all_tags:
                print(sap_tag, 'already exists as a tag...')
            else:
                all_tags.append(sap_tag)
                is_new_sapling = False

        except ValueError:
            print('Input must be int...')

    while isnt_float:
        try:
            sap_height = float(input('Please enter height (float): '))

            new_sap = Sapling(sap_height, sap_tag)
            pine_trees.append(new_sap)
            print('\n---Sapling created---\n')
            isnt_float = False

        except ValueError:
            print('Input must be a float...')

def find_sapling(pine_trees, tag):
    """
    * Name: find_sapling
    * Inputs: list, int
    * Return: object if found, false if not found
    * Purpose: find sapling and return it
    """

    found = False
    found_sapling = None

    for elm in pine_trees:
        if elm.get_tag() == tag:
            found = True
            found_sapling = elm
            break

    if found == False:
        print('Sapling not found...')
    else:
        return found_sapling

def add_height(pine_trees, all_tags):
    """
    * Name: add_height
    * Inputs: list, list
    * Return: int
    * Purpose: add height to existing sapling
    """

    real_tag = True
    isnt_float = True

    all_tags.sort()
    print('\nExisiting tags:')
    print(all_tags)

    # Checks if the tag exists
    while real_tag:
        try:
            sap_tag = int(input('Please enter the existing tag (int) of the sapling you would like to fetch: '))

            # checks if tag already exists
            if sap_tag in all_tags:

                # Checks to see if inputted height is of type float
                while isnt_float:
                    try:

                        # Get current sapling from list and print all heights for specific sapling
                        current_sapling = find_sapling(pine_trees, sap_tag)
                        print(current_sapling.get_growth())

                        sap_height = float(input('Please enter height for sapling (must be greater than/equal to previous height): '))
                        current_sapling = find_sapling(pine_trees, sap_tag)

                        # Check if inputted height is a float & greater than or equal\
                        # to the latest height for the specific sapling
                        if sap_height >= current_sapling.get_latest_height():
                            isnt_float = False
                        else:
                            print('Height must be greater than/equal to previous height...')
                    except ValueError:
                        print('Input not float type...')

                # Search through list of pine trees to find specific\
                # sapling from the tag the user inputted
                for elm in pine_trees:
                    if elm.get_tag() == sap_tag:
                        elm.add_growth(sap_height)
                        print('\n---Height added---\n', elm.get_tag(),\
                              elm.get_growth(), '\n')
                        break
                real_tag = False
            else:
                print(sap_tag, 'tag was not found...')
        except ValueError:
            print('Input not int type...')

    return sap_tag

def print_pine_trees(pine_trees, all_tags):
    """
    * Name: print_pine_trees
    * Inputs: list, list
    * Return: None
    * Purpose: print list of pine trees
    """

    # Print out list of pine trees with each tag and respective heights
    all_tags.sort()
    print('Saplings:')

    for tag in all_tags:
        for sap in pine_trees:
            if tag == sap.get_tag():
                print(sap.get_tag(), sap.get_growth())

def write_pine_trees(pine_trees, all_tags):
    """
    * Name: write_pine_trees
    * Inputs: list, list
    * Return: None
    * Purpose: write list of pine trees to file
    """

    # Open PineTreeHeights for writing
    pine_tree_heights = open('files/PineTreeHeights.txt', 'w')
    all_tags.sort()

    for tag in all_tags:

        # Write out list of pine trees with each tag and heights
        for elm in pine_trees:

            if elm.get_tag() == tag:

                # Store growth of sapling for use in second for loop
                growth = elm.get_growth()
                for index in range(len(growth)):
                    pine_tree_heights.write('\n' + str(growth[index]) + ' ' +\
                                          str(elm.get_tag()))

def file_input(file_name, all_tags, pine_trees, summary_file):
    """
    * Name: file_input
    * Inputs: str, list, list, file
    * Return: file
    * Purpose: scan in sapling data from text file
    """

    counter = 0
    sap_count = 0

    # Open file and scan in data to pine_tree_heights list
    print('\nSaplings from file:')
    with open(file_name, 'r') as name_file:

        for line in name_file:

            print(line)

            for word in line.split():

                if counter == 0:
                    height = float(word)
                    counter += 1
                else:
                    tag = int(word)

                    # Check if tag already exists, if not create new sapling
                    if not is_tag(tag, all_tags):
                        new_sap = Sapling(height, tag)
                        pine_trees.append(new_sap)
                        all_tags.append(new_sap.get_tag())
                        summary_file.write('\nSAPLING_ADDED_FROM_FILE: TAG: ' +\
                                           str(pine_trees[-1].get_tag())\
                                           + ', HEIGHT: ' + str(pine_trees[-1].get_latest_height()))
                    else:
                        for temp_sap in pine_trees:
                            if temp_sap.get_tag() == tag:
                                temp_sap.add_growth(height)
                                summary_file.write('\nHEIGHT_ADDED_FROM_FILE: TAG: ' + str(pine_trees[-1].get_tag())\
                                                   + ', HEIGHT: ' + str(pine_trees[-1].get_latest_height()))

            counter = 0     # Reset counter for tag/height decision
            sap_count += 1  # Increase amount of saplings

    name_file.close()
    print('\n---File Data Inputted---\n')
    return name_file

def close_files(files):
    """
    * Name: close_files
    * Inputs: str
    * Return: True
    * Purpose: close all files
    """

    for file in files:
        file.close()

    return True

def delete_sapling(all_tags, pine_trees, tag):
    """
    * Name: delete_sapling
    * Inputs: list, list, int
    * Return: None
    * Purpose: delete sapling
    """

    # Remove sapling from pine_trees list
    for elm in pine_trees:
        if elm.get_tag() == tag:
            pine_trees.remove(elm)

    # Remove tag from all_tags list
    for elm in all_tags:
        if elm == tag:
            all_tags.remove(elm)
            print('\n---Sapling Deleted---\n')

def get_file_data(files, lst, file_name):
    """
    * Name: get_file_data
    * Inputs: list, list, str
    * Return: file
    * Purpose: read in data from files and add it to lists
    """

    new_file = open(file_name, 'r+')

    for line in new_file:

        for word in line.split():
            lst.append(word)

    files.append(new_file)

    return new_file