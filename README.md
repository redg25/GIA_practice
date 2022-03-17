# GIA_practice
Kivy app to reproduce GIA tests

I had to take the test for a job application and I realized that there was no easy way to practice exhaustively.<br>
Only paid practices...<br>
It surprised me as I didn't think the building of the tests were rocket sciences.<br>
The way results are calculated, I have no idea but it is easy to create your own score in a meaningful way.<br>
To know more about the  GIA test, see the official [page](https://www.thomas.co/sites/default/files/2019-08/GIA-Example-Booklet-2018.pdf)<br><br>
So here we are, this a simple kivy app where you can select any of the 5 tests<br>
and answer the maximum of questions in 3mn.<br>
The calculation of score is simple, one good answer +1, one bad answer -1, answer as many questions as you can in 3mn.<br><br>

To start the app run the **game_gia.py**<br><br>

When you click on one of the tests, the first question gets displayed instantly and the timer starts at the same time, so be ready.<br><br>

The data used for the word meaning and reasoning tests is not too exhaustive at the moment.<br>
I will add more soon but you can add some yourself to the csv files:<br>
- pairs.csv
- reasoning.csv<br>

In reasoning.csv, for each new word/expression to add, you need to assign the type:<br>
- 1: adjective, 2: comparative, 3: noun with more, 4: noun with less, 5 adjective with more or less<br>

and to assign the ids of words/expressions for the possible questions to be made. It is separated in 2 columns:<br>
- same: word/expression with the same meaning as the main word/expression
- opposite: word/expression with the opposite meaning as the main word/expression<br>

ex: **rich** has **richer** and **more money** in the **same** column, and **poorer** and **less money** in the **opposite** column<br>
*Note that **type 1** can't be use in the **same** and **opposite** columns. We can't make question out of simple adjective.*<br><br>
### Next steps
I will add a feature to export a detailed report of a test, giving the time it took for each question to be answered. 
