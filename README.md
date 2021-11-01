# Canvas-API-Scripts
Useful API scripts for various tasks in the Canvas LMS

The "jewel" here is the parse.py script. This is developed to read .tex file using the exam documentclass and appropriately formatted. To detail how to format the .tex file I will provide a template. For now all I have uploaded is an example file, test-quiz.tex. In this file I have included three types of questions; numerical questions; fill in multiple blanks questions; and multiple choice questions. The parse.py script is able to identify all the necessary information from within test-quiz.tex and compile it into a list of dictionaries that will then be used in create-quiz-questions.py to send an API call to Canvas to create all the questions provided from test-quiz.tex.

Apart from this, there are more API scripts which are far more trivial. Please check the use of .sysargv in all the scripts to identify what arguments are needed when running the scripts. Each .sysargv has been appropriately labelled in order for the user to immediately identify what each is in reference to.

Lastly, you will need to change the authorization header. Currently it is using my details for my local machine. I recommend using the keyring module in python to securely store your access tokens and allow you to share you scripts with others without compromising your digital security.
