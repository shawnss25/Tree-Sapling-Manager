
import my_modules.Functions as mf
# import time

def main():
    """
    * Name: main
    * Inputs: None
    * Return: None
    * Purpose: Run program
    """

    pine_trees = []  # Create list to hold height of pine trees
    weather = []            # Store weather
    temperatures = []       # Store temperature
    avg_heights = []        # Store average heights
    all_tags = []   # Keep track of all tags
    files = []      # Holds all files
    avg_ht = 0      # Average height of saps

    # Open files and read in file data
    weather_file = mf.get_file_data(files, weather, 'files/Weather.txt')
    temps_file = mf.get_file_data(files, temperatures, 'files/Temps.txt')
    average_heights_file = mf.get_file_data(files, avg_heights, 'files/AverageHeights.txt')
    summary_file = open('files/Summary.txt', 'w')
    mf.file_input('files/PineTreeHeights.txt', all_tags, pine_trees, summary_file)
    pine_tree_heights = open('files/PineTreeHeights.txt', 'a')

    # Add files to files list to close for later
    files.append(average_heights_file)
    files.append(pine_tree_heights)

    # Get user's input
    continue_program = True
    while continue_program:

        # User selection menu
        selection = input('\n---\nPlease type one of the following\n---\
                           \n1 Create new sapling\
                           \n2 Add new height to existing sapling\
                           \n3 Print all saplings\
                           \n4 Average latest heights\
                           \n5 Get weather\
                           \n6 Delete sapling\
                           \nQ Quit\n---\
                           \nSelection: ')
        print('---\n')

        # Create new sapling
        if selection == '1':

            add_another = True
            mf.add_sapling(pine_trees, all_tags)

            summary_file.write('\nCREATE_SAPLING: TAG: ' + str(pine_trees[-1].get_tag())\
                               + ', HEIGHT: ' + str(pine_trees[-1].get_latest_height()))

            # If user wants to add another sapling
            while add_another:
                add_sap = input('Would you like to enter another new sapling? (Y/N): ')

                if add_sap.lower() == 'y':
                    mf.add_sapling(pine_trees, all_tags)

                    summary_file.write('\nCREATE_SAPLING: TAG: ' + str(pine_trees[-1].get_tag())\
                                       + ', HEIGHT: ' + str(pine_trees[-1].get_latest_height()))
                elif add_sap.lower() == 'n':
                    add_another = False
                else:
                    print('\nInvalid input...\n')

            # Print updated list
            print('\n---Updated list: ')
            mf.print_pine_trees(pine_trees, all_tags)
            print('\n---')

        # Add new height to existing sapling
        elif selection == '2':

            # Add height and get the sapling for writing
            add_another = True
            sap_tag = mf.add_height(pine_trees, all_tags)
            sapling = mf.find_sapling(pine_trees, sap_tag)

            summary_file.write('\nADD_HEIGHT: TAG: ' + str(sap_tag)\
                               + ', HEIGHT: ' + str(sapling.get_latest_height()))

            # If user wants to add another height
            while add_another:
                add_sap = input('Would you like to enter another new height? (Y/N): ')

                if add_sap.lower() == 'y':
                    sap_tag = mf.add_height(pine_trees, all_tags)
                    sapling = mf.find_sapling(pine_trees, sap_tag)

                    summary_file.write('\nADD_HEIGHT: TAG: ' + str(sap_tag)\
                                       + ', HEIGHT: ' + str(sapling.get_latest_height()))
                elif add_sap.lower() == 'n':
                    add_another = False
                else:
                    print('\nInvalid input...\n')

        # Print all saplings
        elif selection == '3':
            mf.print_pine_trees(pine_trees, all_tags)
            summary_file.write('\nPRINT_SAPLINGS')

        # Average latest heights of saplings
        elif selection == '4':
            avg_ht = mf.get_average_height(pine_trees)
            avg_heights.append(avg_ht)
            print('\nAverage height:', avg_ht)
            print('\nAll averages:')
            print(avg_heights)
            average_heights_file.write(str(avg_ht) + '\n')
            summary_file.write('\nAVERAGE_HEIGHT: ' + str(avg_ht))

        # Get weather
        elif selection == '5':
            temperatures.append(mf.check_weather(temps_file, weather_file, weather))
            print(temperatures)
            print(weather)
            avg_heights.append(avg_ht)
            summary_file.write('\nGET_WEATHER: TEMP: ' + temperatures[-1]\
                               + ', WEATHER: ' + weather[-2])

        # Delete Sapling
        elif selection == '6':
            whole_delete_program = True

            all_tags.sort()
            print('\nCurrent tags: ')
            print(all_tags)

            while whole_delete_program:

                isnt_tag = True
                delete_another = True

                # Get tag and make sure it's an int
                while isnt_tag:
                    try:
                        tag = int(input('Enter the tag you would like to delete: '))

                        if tag not in all_tags:
                            print('Tag not found...Please try again')
                        else:
                            isnt_tag = False
                    except ValueError:
                        print('Invalid input. Please enter a valid int...')

                    # Delete sapling
                    mf.delete_sapling(all_tags, pine_trees, tag)
                    summary_file.write('\nDELETE_SAPLING_TAG: ' + str(tag))

                    while delete_another:
                        delete_again = input('Would you like to delete another (Y/N): ')

                        if delete_again.lower() == 'y':
                            delete_another = False
                        elif delete_again.lower() == 'n':
                            delete_another = False
                            whole_delete_program = False
                        else:
                            print('Invalid input...')

                print('\n---Updated list: ')
                mf.print_pine_trees(pine_trees, all_tags)
                mf.write_pine_trees(pine_trees, all_tags)
                print('\n---')

        # Quit
        elif selection.lower() == 'q':
            continue_program = False
            summary_file.write('\nQUIT')
            mf.write_pine_trees(pine_trees, all_tags)

        # Invalid input
        else:
            print('\nInvalid input...\n')

    # Check temperature every 24 hours
    # while (True):
    #     temperatures.append(check_weather(temps_file, weather_file, weather))
    #     print(temperatures)
    #     print(weather)
    #     print("Checking temperature in 24 hours...")
    #     time.sleep(86400)

    # Close files
    mf.close_files(files)

# Execute program
main()
