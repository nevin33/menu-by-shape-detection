# menu-by-shape-detection
This project was done by a group of 5 including me.

The customer chooses the menu for the meal they want to order  by selecting the objects on their table in four different colours and three different shapes of each color.
Things to watch out for;
* The customer cannot choose more than one object of the same color when choosing their food, if happened, the program warning message prints;
"only one of the same color object you can select"
* He/she has to choose at least one main course and one starter to create the menu.
* If only one meal selected, program warning to choose more
* The customer can place the objects on top of each other or next to each other.
* The colors do not have to be in a specific sequence or order.
* For every color and every shape in the menu,must be a corresponding dish and price.
* After taking a picture and reading the picture with cv2.imread("yourorder.png", 0) in the program, it should understand the ordered dishes and ask the customer "Your order is ....., do you confirm?"
* After the customer confirms, your food is prepared and finally, the total amount you have to pay:
TL'
at the end of the calculation.
* For this calculation, you need to set up a structure in the program where you define the color-shape-price information for each dish.
* You are expected to use this structure in your class definitions.
* You should definitely include object oriented programming and image processing with open in the application.
