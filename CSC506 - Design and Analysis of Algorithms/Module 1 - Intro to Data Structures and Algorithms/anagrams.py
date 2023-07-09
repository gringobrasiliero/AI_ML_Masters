
def is_anagram(word_one, word_two):
    if word_one != word_two:
        #Convert the 2 strings into Lists of characters
        list_word_one = list(map(str,word_one))
        list_word_two = list(map(str,word_two))

        #Loop through the characters in the first list of characters
        i = len(list_word_one)-1
        character_match = True
        while i >= 0 and character_match:
            #Check to see if there is a matching character in the second list of characters.
            character_match = False
            for j in range(len(list_word_two)):
                if list_word_one[i] == list_word_two[j]:
                    #Remove the character from both lists
                    list_word_one.pop(i)
                    list_word_two.pop(j)
                    character_match = True
                    break

            i-=1
        #If both lists have a length of 0, return True
        if len(list_word_one) == 0 and len(list_word_two) == 0:
            return True
        else:
            return False
    return True

word_one = "teas"
word_two = "eats"
isAnagram = is_anagram(word_one, word_two)
print(isAnagram)


# 1- Convert the two Strings into Lists of Strings
# 2 - Loop through the characters in List 1
# 3 - Loop through the characters in List 2
# 4 - If the Character from the first list matches the character from second list, remove the letter from both List 1 and List 2
# 5 - At the end of loop, if both lists have a length of 0, return True, Else, return false. 