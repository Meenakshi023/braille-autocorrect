# braille-autocorrect
# Braille AutoCorrect System

The Braille AutoCorrect System allows users to type Braille characters using a standard QWERTY keyboard, where keys D, W, Q, K, O, and P represent Braille dots 1 to 6. The program interprets each character based on Braille dot patterns, builds complete words, and suggests the most likely intended word using Levenshtein distance. It also supports real-time correction with BACKSPACE and SPACE, and learns from user feedback to improve future suggestions.

HOW TO RUN :
Clone or download the repository
Open the folder in a terminal
Install required library using pip install python-Levenshtein
Run the script 
Enter the Braille keys
Use SPACE for space and BACK to delete
Press Enter on empty line to finish input and see suggestions
