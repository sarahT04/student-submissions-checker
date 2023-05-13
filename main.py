from dotenv import dotenv_values
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv
import os
import pickle
from utils import name_matches

# Load environment variables from .env file
env_vars = dotenv_values()

SCOPES = [
        'https://www.googleapis.com/auth/classroom.rosters.readonly',
        'https://www.googleapis.com/auth/classroom.courses.readonly',
        'https://www.googleapis.com/auth/classroom.student-submissions.students.readonly',
    ]
API_SERVICE_VERSION = 'v1'

def get_authenticated_service():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token_file:
            credentials = pickle.load(token_file)
            return build('classroom', API_SERVICE_VERSION, credentials=credentials)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        credentials = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(credentials, token_file)
        return build('classroom', API_SERVICE_VERSION, credentials=credentials)
    
def check_students_returned_work(course_id: str, assignment_id: str):
    global group_members
    # Initialize the service
    service = get_authenticated_service()
    # Retrieve all student profiles using pagination & put in memory
    student_profiles = {}
    page_token = None
    while True:
        students = service.courses().students().list(courseId=course_id, pageSize=100, pageToken=page_token).execute()
        for student in students.get('students', []):
            profile = student.get('profile')
            if profile:
                student_profiles[profile['id']] = profile['name']['fullName']
        page_token = students.get('nextPageToken')
        if not page_token:
            break
    # Get that assignment student submissions
    submissions = service.courses().courseWork().studentSubmissions().list(
        courseId=course_id, courseWorkId=assignment_id).execute()
    student_submissions = submissions.get('studentSubmissions', [])
    # Loop through the submissions
    for student_submission in student_submissions:
        # Check if user have submitted
        is_submitted = student_submission.get('state') == 'TURNED_IN'
        # If student has submitted the assignment
        if is_submitted:
             # Get the user id
            user_id = student_submission['userId']
            # Get user full name
            student_name = student_profiles.get(user_id)
            # Check if name exists in your group
            for member in group_members:
                # By removing the name in list
                # and the names that exist in the list
                # are the ones who haven't submitted
                name = member[1]
                group_number = member[0]
                if name_matches(name, student_name):
                    late = student_submission.get('late')
                    group_members.remove(member)
                    print(f"Kel: {group_number}. Nama: {student_name} telah mengumpulkan {'TIDAK ' if late is not True else ''}TERLAMBAT")

def get_group_names():
    file_path = 'group.csv'
    group_members = []
    # Group number
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip the header
        next(reader)
        for row in reader:
            group_members.append(row)
    return group_members

COURSE_ID = env_vars.get("COURSE_ID")
assignment_id = env_vars.get("ASSIGNMENT_ID")
group_members = get_group_names()

if __name__ == '__main__':
    check_students_returned_work(COURSE_ID, assignment_id)