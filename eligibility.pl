:- use_module(library(http/http_server)).
:- use_module(library(http/http_json)).
:- use_module(library(http/http_cors)).

% Enable CORS: Allow all origins
:- http_handler('/', cors_handler, [prefix]).

% CORS handler - Allow all origins
cors_handler(Request) :-
    http_set_header('Access-Control-Allow-Origin', '*'),
    http_set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
    http_set_header('Access-Control-Allow-Headers', 'Content-Type'),
    (   member(method(options), Request)
    ->  reply_json(json([status=ok]))
    ;   handle_request(Request)
    ).

% Define eligibility rules
eligible_for_scholarship(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, CGPA),
    Attendance_percentage >= 75, CGPA >= 9.0.

permitted_for_exam(Student_ID) :-
    student(Student_ID, _, Attendance_percentage, _),
    Attendance_percentage >= 75.

% Sample student data
student(1, 'John', 80, 9.5).
student(2, 'Jane', 70, 8.0).
student(3, 'Alex', 90, 9.2).

% Scholarship eligibility handler
:- http_handler('/scholarship', scholarship_handler, []).

scholarship_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (   eligible_for_scholarship(Student_ID)
    ->  Reply = json([status='eligible', reason='Meets the attendance and CGPA criteria'])
    ;   Reply = json([status='not_eligible', reason='Does not meet the criteria'])
    ),
    reply_json(Reply).

% Exam permission handler
:- http_handler('/exam', exam_handler, []).

exam_handler(Request) :-
    http_parameters(Request, [student_id(Student_ID, [integer])]),
    (   permitted_for_exam(Student_ID)
    ->  Reply = json([status='permitted', reason='Meets the attendance criteria'])
    ;   Reply = json([status='not_permitted', reason='Does not meet the attendance criteria'])
    ),
    reply_json(Reply).

% Start the HTTP server
:- http_server(http_dispatch, [port(8000)]).

