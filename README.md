## General instructions and tasks
Read and pull in data from people.csv.
Fill in the requests in server.py where TODOs are stated in the comments.
Get as many done as you can.
If you have time create unit tests.
Feel free to add other systems to the application.
Also feel free to submit issues on this public branch with questions if you have any.

### Documentation
Use the format "python server.py PORT_NUMBER CSV_FILE"  
For example, "python server.py 8000 people.csv"  
Currently set to use localhost so address may be http://localhost:8000/  
I added a page "/update" that lets you add information  
I also create a file called output.json that keeps the added info persistent  
Some inputs are specific to HTML5 but should work okay on older versions  
I didn't add a way to delete a user, but I definitely would if this were a real app  
Additionally instead of storing a json file I would add a small SQLite db  