import numpy as np
import pickle
import webscrape_amazon as wb

# These variables will be repeatedly used and modified by many functions

selection = 0           
laptop_pairs_list = []
laptops_list_of_dicts = []
no_of_laptops = -1 # To catch errors

def get_selection():

    '''
    Arguments: none
    Task: Has the user input the application they need to buy the laptop for the most
    Returns: the user's selection
    '''
    
    
    global selection


    while True: # until input is invalid, this loop keeps running
    
        print("Please enter what category of user describes you the best:")
        print( "1. Gamer")
        print("2. Artist/Designer")
        print("3. Business-person")
        selection = input("Enter either 1, 2 or 3: \n")
        valid_selections_list = ["1","2","3"]
        valid_satisfied_list = ["Y","N"]
        if selection in valid_selections_list:
            print("Your selection is: ", selection)
            satisfied = input("Are you satisfied with this selection? Enter Y or N:  \n")
            if satisfied in valid_satisfied_list:
                print("Get Ready to be matched with the PERFECT laptop!")
                selection = int(selection) # this type-conversion is necessary for later
                print("SELECTION is: ", selection)
                dont_care = input("Press any key to continue \n")
                break #valid input obtained

            else:
                print("Invalid Selection")
        else:
            print("Invalid Selection")
                
def get_valid_input (lower,upper,string):

    '''
    Arguments: 1) lower (a number)  2) upper (a number) 3) string (a string)
    Task: Displays the string to the user. Keeps asking for input until the input is an integer
          between the lower and upper numbers (the arguments) 
    Returns: the valid input
    '''
    
    global selection
    global laptop_pairs_list
    global laptops_list_of_dicts
    global no_of_laptops    
    
    while True: #keep asking until a valid input is obtained
        
            
            selection = input(string)
            print("\n")
            try:
                selection = int(selection)
                if (selection % 1 == 0) and (selection >= lower) and(selection <= upper):
                    break
                else:
                    raise ValueError # this will move us to the exception block below
                    
            except:
                print("INVALID SELECTION- Please try again") # if input cannot be type casted to an integer or is not an integer
                                                             # in the desired range
                
    return(selection)       

def debug(): # toggle debugging output
    return(False)

def verbose(): # toggle verbose debugging output
    return(False)

def open_backup_file():

    '''
    Arguments: 1) the user's selection of what application they need laptop for most
    Task: This function is called when webscraping fails to obtain more than 3 laptops. It opens a backup file
          that has stored laptops that have been webscraped previously
    Returns: nothing
    Side-effect: Modifies the global variable laptop_list_of_dicts
    '''
    
    global laptops_list_of_dicts


    if verbose():
        print(selection, type(selection))
    if selection == 1:
        
        with open("Gaming.laptops", "rb") as backup:
            laptops_list_of_dicts = pickle.load(backup)
        if debug():            
            print("Backup Gaming Opened")            
            
    elif selection == 2:
                    
        with open("Artist2.laptops", "rb") as backup:
            laptops_list_of_dicts = pickle.load(backup)
        if debug():            
            print("Backup Artist Opened")
            
    elif selection == 3:
                               
        with open("Business.laptops", "rb") as backup:
            laptops_list_of_dicts = pickle.load(backup)
        if debug():            
            print("Backup Business Opened")
    else:
        raise ValueError('This code should never have been reached due to checks on input variable selection earlier on ')


def preprocess_data_2(): #FIXME - Make preprocess_data_1 from Justin's code,

    '''
    Arguments: nothing
    Task: Normalizes the data so that it is in a form that can be used by the functions used in the algorithm later
    Returns: nothing
    Side-effect: Modifies the global variable laptop_list_of_dicts

    '''
    
 
    global laptops_list_of_dicts
   

    if debug():
        print("Starting Preprocesssing")
    print(laptops_list_of_dicts)
    
    print(no_of_laptops)
    laptops_to_delete = []  # this will store indices of laptop to delete

    
    for i in range(no_of_laptops): # iterate through all laptops
        
        try: # the functions here can fail (such as type-casting)
            
            laptop = laptops_list_of_dicts[i]

            if verbose():
                print("In iteration ",i," the list of laptops is : ")

            # Step 1- We need to make sure the relevant specifications we will be comparing are not empty feilds       
            relevant_values = [laptop["Memory Size"], laptop["price"], laptop["Hard Disk Size"], laptop["Maximum Display Resolution"], laptop["Processor Type"], laptop["Graphics Coprocessor"], laptop["Item Weight"]]

            if "None" in relevant_values:
                print("None value found, deleting laptop: ", laptop["Laptop_index"])
                laptops_to_delete.append(laptop["Laptop_index"])
                continue #Skip the rest of the checks
                 
           
            # Step 2 - remove the text "CDN$" and convert price to an int 
            laptop["price"] = float((((laptop["price"]).split())[1]).replace(",",""))

            
            # Step 3 - Convert item weight to integer in same units (grams)
            if verbose():
                print(laptop["Item Weight"])
                
            if "Kg" in laptop["Item Weight"]:
                laptop["Item Weight"] = float((laptop["Item Weight"]).split()[0])*1000 # convert kg to g
            elif "g" in laptop["Item Weight"]:
                laptop["Item Weight"] = float((laptop["Item Weight"]).split()[0])
            else:
                laptops_to_delete.append(laptop["Laptop_index"])
                if debug():
                    print("neither kg nor g found in item weight value so delete")
                continue # Skip rest of the checks

            # STep 4 - Convert Hard Disk Size into an integer with same units (gigabytes)

            if "TB" in laptop["Hard Disk Size"]:
                laptop["Hard Disk Size"] = float((laptop["Hard Disk Size"]).split()[0])*1000 # Convert TB to GB for comparision later
            elif "GB" in laptop["Hard Disk Size"]:
                laptop["Hard Disk Size"] = float((laptop["Hard Disk Size"]).split()[0])
            else:
                if debug():
                    print("No GB or TB found in Hard Disk Size so delete")
                laptops_to_delete.append(laptop["Laptop_index"])
                continue # Skip rest of the checks 

            # Step 5 - Convert RAM size into integer

            if "GB" in laptop["Memory Size"]:
                laptop["Memory Size"] = float(laptop["Memory Size"].split()[0])
            else:
                if debug():
                    print("No GB found in Memory Size so delete")
                laptops_to_delete.append(laptop["Laptop_index"])
                continue     # skip rest of the checks 

            # STep 6 - Find number of pixels by multiplying dimensions 

            display_specs_list = laptop["Maximum Display Resolution"].replace("x"," ").replace("X"," ").replace("*"," ").split()
            laptop["Maximum Display Resolution"] = float(display_specs_list[0])*float(display_specs_list[1])

            # Step 7 - Score the graphics card - This is only for gaming laptops
            
            if selection == 1:  #only for gaming laptops
                words_in_grap_copro_value = laptop["Graphics Coprocessor"].split()

                GTX_index = words_in_grap_copro_value.index("GTX")

                score_GTX_dict = { "1080": 9, "1070": 7.5, "TITAN": 6, "1060": 4, "1050": 2, "980":1}
                score = score_GTX_dict[words_in_grap_copro_value[GTX_index +1]]
                laptop["Graphics_score"] = score #store the score as a key-value pair in the laptops dictionary
                
            
            
        
        except: # If the preprocessing fails, then also delete the laptop
            if debug():
                print("In except block of preprocessing")
            laptops_to_delete.append(laptop["Laptop_index"])
            print("Except clause reached- deleting laptop: ", laptop["Laptop_index"])
    
    if debug():
        print("Laptops to delete are:")
        print(laptops_to_delete)
    
    for num_deleted,laptop_index  in enumerate(sorted(laptops_to_delete), start = 0):
        print(laptop_index)
        del laptops_list_of_dicts[laptop_index - num_deleted] # after deleting we change indices in list, so the num_deleted variable
                                                              # helps to take care of this

    
    if verbose():
        print("Printing index of laptops still left")
        for lp in laptops_list_of_dicts:
            print(lp["Laptop_index"])
            print("Done")
    
        
        
            

def form_pairs(list_of_elements_to_group):
       
    
    # Arguments: 1) A list of elements to form pairs from
    # Task: Forms pairs of elements from the arguments list. Note that the (a,b) and (b,a) are considered the same pair.
    # Returns: List of tuples of pairs

    pair_tuples_list = []
    
    for i in range(len(list_of_elements_to_group)):
        
        for j in range(i+1,len(list_of_elements_to_group)):
            
            pair_tuples_list.append((list_of_elements_to_group[i], list_of_elements_to_group[j]))
    
    if verbose():
        print(pair_tuples_list)
        
    
    return(pair_tuples_list)

def get_comparison_matrix(criteria_name):

    '''
    Arguments: criteria to build comparision matrix for
    Task: goes through each pair in list of laptops, scores the value of a criteria for each pair and builds a matrix
          from those scores
    Return: the matrix
    '''
    
    global laptop_pairs_list
    global laptops_list_of_dicts

    
    comparison_matrix = [[None]*no_of_laptops for _ in range(no_of_laptops)] # initialize a nested list (matrix-like) with
                                                                             # None values for efficiency
    check_done = False
    for pair in laptop_pairs_list: # iterate through each pair of laptops and call the  scoring function with the appropriate range we wish to 
                                  # consider for each criteria.
        
        if criteria_name == "price":
            criteria_max_ratio = 4
        if criteria_name == "Item Weight":
            criteria_max_ratio = 5
        if criteria_name == "Hard Disk Size":
            criteria_max_ratio = 6
        if criteria_name == "Memory Size":
            criteria_max_ratio = 8
        if criteria_name == "Maximum Display Resolution":
            criteria_max_ratio = 8
        if criteria_name == "Graphics Coprocessor":
            score, preffered_tuple_index = get_score_graphics(pair) # different scoring method for this criteria
            check_done = True
        if not(check_done):
            score, preffered_tuple_index = get_score(pair, criteria_name, criteria_max_ratio)
            
        i = (pair[preffered_tuple_index])["Laptop_index"] # matrix row index i
        if verbose():
            print("i is ", i)
        j = (pair[not(preffered_tuple_index)])["Laptop_index"]  # matrix column index j
        if verbose():
            print("j is ", j)

        comparison_matrix[i][j] = score # store the score in matrix

        if verbose():
            print("Therefore a",i,j, " is ", comparison_matrix[i][j])

        comparison_matrix[j][i] = 1/score # store the score in matrix

        if verbose():
            print("And a",j,i," is ",comparison_matrix[j][i])
            print(" The overall matrix right now is ", comparison_matrix)
            
    for i in range(no_of_laptops):
        comparison_matrix[i][i] = 1 # fill in 1 as teh diagonal enteries of teh matrix

    if verbose():
        print(comparison_matrix)

    np_comparison_matrix = np.array(comparison_matrix) # convert the nested list to a numpy matrix to use numpy functions
                                                       # on it later
    
    return(np_comparison_matrix)
                
def get_score(pair_tuple, criteria_name, ratio_max):

    '''
    Arguments: pair of laptops, criteria to compare, the upper limit for ratio to map to 1-9
    Task: determines laptop with bigger value for criteria name, finds ratio and maps the range (1 to ratio_max) to (1 to 9)
    Return: score and index of laptop in pair with greater score
    '''
        

    if verbose():
        print("Comparing laptops: ", pair_tuple[0]["Laptop_index"], "and ",pair_tuple[1]["Laptop_index"])
        
    tuple_index_for_bigger_value = get_tuple_index_for_greater_value(pair_tuple,criteria_name) # find laptop wiith bigger value
    tuple_index_for_smaller_value = not(tuple_index_for_bigger_value)
    
    ratio = pair_tuple[tuple_index_for_bigger_value][criteria_name] / pair_tuple[tuple_index_for_smaller_value][criteria_name]
    score = 1 + (8/(ratio_max-1))*(ratio-1)  # Maps (1 to ratio_max) to (1-9)
    score = round(score,5) # 5 dp for safety + fastness
    if score > 9:  # score cant exceed 9 in algoritm implementation
            score = 9
    if verbose():   
        print("Laptop ", pair_tuple[tuple_index_for_bigger_value]["Laptop_index"], " has a greater value of ", pair_tuple[tuple_index_for_bigger_value][criteria_name], " and Laptop ", pair_tuple[tuple_index_for_smaller_value]["Laptop_index"], " has a smaller value of ", pair_tuple[tuple_index_for_smaller_value][criteria_name])
        print("So we rate the score of the bigger one as", score)
    
    
    return(score, tuple_index_for_bigger_value)

def get_score_graphics(pair_tuple):

    '''
    Arguments: pair of laptops
    Task: determines laptop with bettwe graphics card and scores it
    Return: score and index of laptop in pair with greater score
    '''
        

    if verbose():
        print("Comparing laptops: ", pair_tuple[0]["Laptop_index"], "and ",pair_tuple[1]["Laptop_index"])
        
    tuple_index_for_bigger_graphics = get_tuple_index_for_greater_value(pair_tuple,"Graphics_score")
    tuple_index_for_smaller_graphics = not(tuple_index_for_bigger_graphics)
    
    graphics_score = pair_tuple[tuple_index_for_bigger_graphics]["Graphics_score"] - pair_tuple[tuple_index_for_smaller_graphics]["Graphics_score"] + 1
    
    if verbose():   
        print("Laptop ", pair_tuple[tuple_index_for_bigger_graphics]["Laptop_index"], " has a greater graphics of ", pair_tuple[tuple_index_for_bigger_graphics]["Graphics_score"], " and Laptop ", pair_tuple[tuple_index_for_smaller_graphics]["Laptop_index"], " has a smaller graphics of ", pair_tuple[tuple_index_for_smaller_graphics]["Graphics_score"])
        print("So we rate the graphics score of the bigger one as", graphics_score)
    
    return(graphics_score, tuple_index_for_bigger_graphics)
    

def get_tuple_index_for_greater_value(pair_tuple,criteria_name):
    
    '''
    Arguments: pair, criteria name to compare
    Task: compares the value for criteria name and returns index in pair with greater value
    Return: an index ( 0 or 1)
    '''    
    
    print("criteria name : ",criteria_name)
    print("laptop indices being compared : ",pair_tuple[0]["Laptop_index"]," and ", pair_tuple[1]["Laptop_index"])
    print("Values are : ", pair_tuple[0][criteria_name]," and ",pair_tuple[1][criteria_name])
    if pair_tuple[0][criteria_name] >= pair_tuple[1][criteria_name]:
        tuple_index_for_greater_value = 0
                
    else:
        tuple_index_for_greater_value = 1
        
    return(tuple_index_for_greater_value)   


def form_pairs_2(list_of_elements_to_group):


    
    '''
    Arguments: lsit of elements
    Task: forms pairs
    Return: a list of pair tuples
    '''       
    
    #Input: List, Output: List of Tuples; Purrpose: Forms pairs of elements in list passed as argument
    
    pair_tuples_list = []
    
    for i in range(len(list_of_elements_to_group)):
        
        for j in range(i+1,len(list_of_elements_to_group)):
            
            pair_tuples_list.append((list_of_elements_to_group[i], list_of_elements_to_group[j]))    
    
    return(pair_tuples_list)

def get_weights_vector(A):


    
    '''
    Arguments: matrix A
    Task: finds weight vector for A in accordance with AHP alogorithm
    Return: the weights vector
    '''      

    ones_col_vec = np.ones((A.shape[0],1)) # A column vector of 1s

    ones_row_vec =  ones_col_vec.transpose()

    weight_vectors_list = [0]
    i = 0
    stable_weights_found = False

    while (stable_weights_found == False):
        
        i+=1
        matrix_exponentiated = np.linalg.matrix_power(A,i) # raise matrix  A to power i
        weights_vec = ( (matrix_exponentiated @ ones_col_vec)/ (ones_row_vec @ matrix_exponentiated @ ones_col_vec) ) 
        weight_vectors_list.append(weights_vec) # add this weight vector to list 
        
        
            
        change_in_values_vec = weight_vectors_list[i] - weight_vectors_list[i-1]
        stability_reached_bool_vec = change_in_values_vec  <  0.00001 # if values of weight vectors have stabilized 
        if np.all(stability_reached_bool_vec):
            stable_weights_found = True # stop exponetiating matrix
        
    print(weights_vec, "\n", i)
    return(weights_vec)

def main():
    
    '''
    Arguments: note
    Task: Driver program
    Return: nothing
    '''    
    global selection
    global laptop_pairs_list
    global laptops_list_of_dicts
    global no_of_laptops
    get_selection() 
    
    try:
        print("Starting the webscraping")  # Try webscraping
        links = wb.web_environment(selection)
        laptops_list_of_dicts = wb.sort_and_pack(links)
        print("WEBSCRAPED SUCESS")
        #raise ValueError ("test exception block")
    
    except:  # If it fails then open backup
        
        if debug():
                print("Opening Backup 1- Webscraping is not avaliable at the moment")    
        open_backup_file()
        print("2:      ", laptops_list_of_dicts)
        
    
    if debug():        
        print("Laptop File has been loaded")
        
        print("laptops_list_of_dicts is:  ",laptops_list_of_dicts)
    
    
    no_of_laptops = len(laptops_list_of_dicts) # If too less laptops scraped then also  open backup
    if no_of_laptops <= 3:
            
            open_backup_file()
            if debug():
                print("OPening Backup 3 - because too less laptops were scraped")               
            no_of_laptops = len(laptops_list_of_dicts)         
            
    for i in range(no_of_laptops):
    
        
        #print(i)
        laptops_list_of_dicts[i]["Laptop_index"] = i
        
        #print(laptops_list_of_dicts[i])
    
    for i in range(no_of_laptops):
        
        print("Laptop index: ",i, " has CPU: ", laptops_list_of_dicts[i]["Processor Type"])
    for i in range(no_of_laptops):
        print("Laptop index: ",i, " has graphics card: ", laptops_list_of_dicts[i]["Graphics Coprocessor"])
    laptops_list_of_dicts[1]["price"] = None
    
    print(laptops_list_of_dicts[3]["price"])
    print("PREPROCESSING HAPPENS NOW")
    preprocess_data_2()   
            
    no_of_laptops = len(laptops_list_of_dicts) # Update this number
    
    if no_of_laptops <= 3:
        
        open_backup_file()
        print("OPening Backup because too less laptops passed preprocessing")
        preprocess_data_2()           
        no_of_laptops = len(laptops_list_of_dicts)    
        
    if debug():
        print("THE NUMBER OF LAPTOPS COMPARED WILL BE: ",no_of_laptops)
    
    #Renumber the indices
    
    for i in range(no_of_laptops):
    
        if verbose():
            print(i)
            print(laptops_list_of_dicts[i])
        laptops_list_of_dicts[i]["Laptop_index"] = i
    
    
         
    laptop_pairs_list = form_pairs(laptops_list_of_dicts) 
    
    if selection == 1:
        
        seven_criteria_list = ["price", "Hard Disk Size", "Memory Size", "Item Weight", "Maximum Display Resolution","Graphics Coprocessor"]
    
    else:
        seven_criteria_list = ["price", "Hard Disk Size", "Memory Size", "Item Weight", "Maximum Display Resolution"]
    
    criteria_example_list = [" (eg 699 CAD, 2699 CAD, etc.) ", " (for eg. 1000GB, 500 GB, etc.) ", " aka RAM (for eg. 8GB, 16GB, etc.) "," (eg. 5.08kg, 2.4 kg, etc.) ", " (eg. 1920 x 1080 pixels, 1440 x 900, etc.) "]
    
    criteria_pairs_list = form_pairs_2(seven_criteria_list)
    
    print("You will be shown two criteria that are used for judging the laptops at a time. You will have to enter which criteria you value more (i.e. the criteria you would be less willing to compromise on) by pressing a 1 for the criteria on the left and 2 for the criteria on the right. Then press enter. You will then be asked at score how much more you value the criteria selected by you over the other on a scale of 1 to 9. Here is a rough guidde for scoring: 1 means the two criterias you are scoring are equally important for you, 3 means one is weakly more important, 5 means one is more important, 7 means one i sstrongly more important, 9 means one of them is absoultely more important. You can also use intermediate values (2,4,6,8).  ")
    
    
    
    indices = { "price": 0,"Hard Disk Size": 1, "Memory Size": 2, "Item Weight": 3, "Maximum Display Resolution": 4, "Graphics Coprocessor":5}
    
    comparison_matrix = [[None]*len(seven_criteria_list) for _ in range(len(seven_criteria_list))]
       
    for pair in criteria_pairs_list:
        
        print(pair[0],"\t","vs","\t",pair[1])
        #get_1_or_2()
        criteria_preferred_pair_index = get_valid_input(1,2,"Which criteria do you value more (1 or 2): ")-1
        score = get_valid_input(1,9,"Enter an integer score (1-9): ")
        
        i =  indices[pair[criteria_preferred_pair_index]]
        j = indices[pair[not(criteria_preferred_pair_index)]]
            
        comparison_matrix[i][j] = score
        comparison_matrix[j][i] = 1/score
        
    for i in range(len(seven_criteria_list)):
            comparison_matrix[i][i] = 1
    
    A = np.array(comparison_matrix)
    print("The comparison matrix for CRITERIAS is:", A)
    
    criteria_weights_vector = get_weights_vector(A)
    print("The weight vectore for the CRITERIAS is ", criteria_weights_vector)
    
    al_w_v_list = []
    
    for criteria in seven_criteria_list:

        B = get_comparison_matrix(criteria)
        print("Matrix for ",criteria," is ",B)
        alternative_weights_vector = get_weights_vector(B)
        print("Weights vector for ",criteria," is ",alternative_weights_vector)
        print("\n")
        al_w_v_list.append(alternative_weights_vector)
    
    final_weights_vector = 0 # multiply criteria weights vector with weights vector for score for each criteria
        
    for i in range(len(seven_criteria_list)):
        final_weights_vector += criteria_weights_vector[i] * al_w_v_list[i]
        
    print("This is the final weights vector: ", final_weights_vector)

    
    print("\n","\n","\n","The TOP laptops are: ") # DIsplay to p results
    for j in range(1,4):
        max_score = final_weights_vector.max()
        if debug():
            print("Start Max Score: ",max_score," Finish")
    
        
        for i in range(len(final_weights_vector)):
            if final_weights_vector[i] == max_score:
                index_of_max_score = i #FIXME - possibility of max at more than one index
                print("\n","At Rank #",j, " is: ", laptops_list_of_dicts[index_of_max_score]["title"])
                final_weights_vector[index_of_max_score] = 0

if __name__ == "__main__":
    main()