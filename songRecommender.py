import sys
PREF_FILE = "songRecommendations.txt"
#TODO: FIX drop function, doesn't return list properly

def loadUsers(file):
    '''loads current users from file
    returns dictionary with mapping of usernames to
    lists of preferred artists/bands'''
    file = open(file, "r")
    userDict = {}
    for line in file:
        [username, prefs] = line.strip().split(":")
        prefList = prefs.split(",")
        userDict[username] = prefList
    file.close()
    return userDict

def getPreferences(username, userMap):
    '''gets preferences from user and stores them in userMap
    creates new user if username is not in userMap'''
    if username in userMap:
        prefs = userMap[username]
        welcomeBackScreen(username)
        print()
        print("I see that you have used our system before.")
        print("Your current music preferences are:")
        print("--------------------------------------------------------------------")
        for artist in prefs:
            centerLine(artist)
        print("--------------------------------------------------------------------")
        print("Please enter another artist or band that you like,")
        print("or press enter to see your current recommendations.")
        newPref = input("You can also enter \"EDIT\" to see your current recommendations: ")
        if newPref.upper() == "EDIT":
            return editRecommendations(username, userMap)
    else:
        prefs = []
        welcomeScreen(username)
        print()
        print("I see that you are a new user.")
        newPref = input("Please enter the name of an artist or band that you like: ")        
    while newPref != "":
        prefs.append(newPref.strip().title())
        print()
        print("Please enter another artist or band that you like,")
        newPref = input("or press enter to see your current recommendations: ")
    #sort lists before returning
    prefs.sort()
    return prefs

def editRecommendations(username, userMap):
    '''edits current user's recommendation list and returns user's new prefs'''
    print()
    print("--------------------------------------------------------------------")
    print("-------------------------{ Artist Editor }--------------------------")
    print("--------------------------------------------------------------------")
    printArtists(username, userMap)
    print("--------------------------------------------------------------------")
    print()
    print("Type the number next to the artist or band that you wish to remove,")
    number = input("or press enter to see your current recommendations: ")
    newPrefs = []
    userPref = userMap[username]
    for artist in userPref:
        newPrefs.append(artist)
    while number != "":
        confirm = input(f"You have selected \"{userPref[int(number)-1]}\", do you wish to remove them? (Y/N): ")
        if confirm.upper() == "Y":
            newPrefs.remove(userPref[int(number)-1])
            saveUserPreferences(username, newPrefs, userMap, PREF_FILE)
            number = ""
            newPrefs = editRecommendations(username, userMap)
        else:
            number = ""
            newPrefs = editRecommendations(username, userMap)
    return newPrefs

def getRecommendations(currentUser, prefs, userMap):
    '''gets recommendations for user based on user's preferences and other users
    similar preferences using Collaborative Filtering (CF)'''
    bestUser = findBestUser(currentUser, prefs, userMap)
    if bestUser == None:
        return [-1]
    recommendations = drop(prefs, userMap[bestUser])
    return recommendations

def saveUserPreferences(username, prefs, userMap, fileName):
    '''writes all user preferences to file'''
    userMap[username] = prefs
    file = open(fileName, "w")
    for user in userMap:
        toSave = str(user) + ":" + ",".join(userMap[user]) + "\n"
        file.write(toSave)
    file.close()

def findBestUser(currentUser, prefs, userMap):
    '''find user from userMap that has the most similar
    preferences to currentUser'''
    users = userMap.keys()
    bestUser = None
    bestScore = -1
    for user in users:
        score = numMatches(prefs, userMap[user])
        if score > bestScore and currentUser != user:
            bestScore = score
            bestUser = user
    return bestUser

def numMatches(L1, L2):
    '''returns number of matches between two sorted lists, L1 and L2'''
    matches = 0
    i = 0
    j = 0
    while i < len(L1) and j < len(L2):
        if L1[i] == L2[j]:
            matches += 1
            i += 1
            j += 1
        elif L1[i] < L2[j]:
            i += 1
        else:
            j += 1
    return matches

def drop(L1, L2):
    '''returns single list of items that are contained in L2 but not in L1'''
    newL = []
    i = 0
    j = 0
    while i < len(L1) and j < len(L2):
        if L1[i] == L2[j]:
            i += 1
            j += 1
        elif L1[i] < L2[j]:
            i += 1
        else:
            newL.append(L2[j])
            j += 1
    if i == len(L1) and j < len(L2):
        return newL + L2[j:]
    return newL

def introScreen():
    '''prints intro screen for program'''
    print("--------------------------------------------------------------------")
    print("------------{ Welcome to the music recommender system! }------------")
    print("--------------------------------------------------------------------")

def welcomeScreen(username):
    '''prints username welcome screen for program'''
    nameLength = len(username)
    dashCount = (56 - nameLength) / 2
    print("--------------------------------------------------------------------")
    if dashCount.is_integer():
        dashCount = int(dashCount)
        print("-"*dashCount + f"{{ Welcome {username.title()} }}" + "-"*dashCount)
    else:
        dashCount = int(dashCount)
        print("-"*dashCount + f"{{ Welcome {username.title()} }}"+ "-"*dashCount + "-")
    print("--------------------------------------------------------------------")

def welcomeBackScreen(username):
    '''prints username welcome screen for returning user for program'''
    nameLength = len(username)
    dashCount = (51 - nameLength) / 2
    print("--------------------------------------------------------------------")
    if dashCount.is_integer():
        dashCount = int(dashCount)
        print("-"*dashCount + f"{{ Welcome Back {username.title()} }}" + "-"*dashCount)
    else:
        dashCount = int(dashCount)
        print("-"*dashCount + f"{{ Welcome Back {username.title()} }}"+ "-"*dashCount + "-")
    print("--------------------------------------------------------------------")

def printArtists(username, userMap):
    '''prints current user's preferred artists'''
    userPref = userMap[username]
    for i in range(len(userPref)):
        line = f"{i+1}) {userPref[i]}"
        print(f"                           {line}")
    
def centerLine(input):
    '''prints input centered'''
    inputLength = len(input)
    dashCount = (64 - inputLength) / 2
    
    if dashCount.is_integer():
        dashCount = int(dashCount)
        print(" "*dashCount + f"{{ {input.title()} }}" + " "*dashCount + " ")
    else:
        dashCount = int(dashCount)
        print(" "*dashCount + f"{{ {input.title()} }}"+ " "*dashCount)
    
def main():
    '''main function for song recommender'''
    userMap = loadUsers(PREF_FILE)
    
    introScreen()
    print()
    
    username = input("What is your name? ")
    username = username.title()
    print()

    prefs = getPreferences(username, userMap)
    recs = getRecommendations(username, prefs, userMap)
    print()
    print(f"{username}, based on current user preferences and your own,")
    if recs[0] == -1:
        print("there are no new song recommendations for you.")
        print()
        print("I will save your preferred artists and have new")
        print("recommendations for you in in the future!")
    else:
        print("I would recommend giving a listen to:")
        print("--------------------------------------------------------------------")
        for artist in recs:
            centerLine(artist)
        print("--------------------------------------------------------------------")
        print("I hope you enjoy them!")
        print("I will save your preferred artists and have")
        print("new recommendations for you in the future!")
    print()
    print("See ya next time!")
    
    saveUserPreferences(username, prefs, userMap, PREF_FILE)
    
    sys.exit()
    
    
if __name__ == "__main__":
    main()
