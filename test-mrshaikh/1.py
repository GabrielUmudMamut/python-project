made = int(input("How many did you make? ")) 
sold = int(input("How many did you sell? ")) 
 
if sold <= made: #the sold was needs to be less or equal to the made. previously it was more than or equal to, which was incorrect.
    remaining = made - sold 
    print("Record saved.") #it says record saved but it doesnt actually save anything
else: 
    print("You cannot sell more than you made.") 

#initialy the spacing was also incorrect. the if statement had its elements in the same place. it didnt have the tab spacing