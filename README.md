Real life scenario:
   - A total of 150 students submits their work
   - We have a CSV of student name and their group name
   - We don't know from which group does the student submit


This problem will print out the information 
in the format of  
`Group Number: {number}, name: {name} submitted {'NOT LATE' if late else ''} LATE`

Uses:

Google classroom API, SequenceMatcher to check for difference in name google and CSV, pickle to store google account's credential.

Data from CSV in format "group, name"