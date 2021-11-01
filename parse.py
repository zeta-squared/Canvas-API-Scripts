#This script expects the .tex file to be of a specific format. With this in mind, there are lines in this script
#which do not have any comments however they are assigning question data. This is because the due to the format
#of the .tex file we know a priori the number of steps required after a particular line to arrive at that particular
#data. For example, from the format of the .tex file we have that if the current tex_file_line[i] line contains
#the question name then the very next line will contain points possible. Hence setting i = i+1 we can then take
#tex_file_lines[i].removeprefix('points_possible') to be the data entry for points possible.

import re
import upload_file as upload

def build(tex_file, course_id):

    #Open the .tex file and create a list of all the lines in the file.
    tex_file = open(tex_file,'r')
    tex_file_lines = tex_file.readlines()

    #Intialise list of dictionaries for question data.
    q_data = [{}]

    #Due to the formatting of the .tex file we want to remove and tab-whitespaces; newline markers 
    #which are appended from the open command on line 7 and LaTeX comment character (%).
    #Initialise a counter and then run through all lines to clean away unnecessary characters.
    i = 0
    while i <= len(tex_file_lines)-1:
        tex_file_lines[i] = tex_file_lines[i].strip('\t%\n')
        i += 1
    
    #Now that all the lines of our .tex file are cleaned we want to beginning identifying questions and
    #prepare the question data to be sent to Canvas.

    #Initialise line counter.
    i = 0

    #Intialise question counter.
    j = 0

    while i <= len(tex_file_lines)-1:

        #Check if the current line indicates the beginning of a question.
        if 'question_name' in tex_file_lines[i]:
            #tex_file_lines[i].removeprefix('question_name: ') == f'Question {j+1}':

            #If there is more than one question in the .tex file we expand the length of q_data to accomdate the additional question(s).
            if j >= 1:
                q_data = q_data + [{}]

            q_data[j]['question[question_name]'] = tex_file_lines[i].removeprefix('question_name: ')
            i += 1
            q_data[j]['question[points_possible]'] = tex_file_lines[i].removeprefix('points_possible: ')
            i += 1

            #Check if the question is a numerical question.
            if tex_file_lines[i].removeprefix('question_type: ') == 'numerical_question':
                q_data[j]['question[question_type]'] = 'numerical_question'
                i += 1
                q_data[j]['question[answers][0][numerical_answer_type]'] = tex_file_lines[i]
                q_data[j]['question[answers][0][answer_weight]'] = 100

                #If the question expects an exact answer we will also need to identify and store data regarding a possible answer error margin.
                if q_data[j]['question[answers][0][numerical_answer_type]'] == 'exact_answer':
                    i += 1
                    q_data[j]['question[answers][0][answer_error_margin]'] = tex_file_lines[i].removeprefix('answer_margin: ')
                i += 2

                #Having all data regarding the question type and parameters we can now build the question text and answer data.
                #We begin by defining the question text to be a blank string which we can modify as we need moving forward.
                question_text = ''

                #We will continute to iterate on the lines read from the .tex file till we hit a line which has a string indicating
                #the beginning of the solutions (since due to the .tex file format we will know there will be no more question text
                #for the current question).
                while tex_file_lines[i] != '\\begin{solution}':

                    #Check if any line in the question text is italicised. If so append the appropriate html delimiters for italics.
                    if 'textit' in tex_file_lines[i]:
                        tex_file_lines[i] = re.search('{(.+?)}', tex_file_lines[i])
                        tex_file_lines[i] = '<i>'+tex_file_lines[i].group(1)+'</i>'

                    #Check if the question has any images included. If so, we extract the file name and make a call to the upload_files
                    #script. Uploading the image to the course Canvas file directory. Finally, we reconstruct the current line to
                    #include the appropriate html command to import and display the correct image from the course Canvas file directory.
                    if 'includegraphics' in tex_file_lines[i]:
                        tex_file_lines[i] = re.search('{(.+?)}', tex_file_lines[i])
                        tex_file_lines[i] = tex_file_lines[i].group(1)
                        img_id = upload.up(tex_file_lines[i],course_id)
                        tex_file_lines[i] = '<img src=/courses/{}/files/'.format(course_id)+str(img_id)+'/preview alt='+tex_file_lines[i]+' />&nbsp;'

                    #For each line of question text in the .tex file we append html paragraph delimiters. This ensures that if any
                    #line breaks are made in the .tex file (using '\\') then this will be accounted for and accurately represented in the
                    #Canvas post. Otherwise, if there are no line breaks in the .tex file then appending html paragraph delimiters to the
                    #line will not affect the appearance of the text on Canvas.
                    question_text = question_text+'<p>'+tex_file_lines[i].removesuffix('\\\\')+'</p>'
                    i += 1

                q_data[j]['question[question_text]'] = question_text
                i += 1
                q_data[j]['question[answers][0][answer_exact]'] = tex_file_lines[i]

            #Check if the question is a fill in multiple blanks question.
            elif tex_file_lines[i].removeprefix('question_type: ') == 'fill_in_multiple_blanks_question':
                q_data[j]['question[question_type]'] = 'fill_in_multiple_blanks_question'
                i += 1 

                #As this is a multiple blanks question we expect n blanks to be filled in. We do not know n a priori. We initialise a
                #blanks counter (k) which we will use later to know how many solutions to look for.
                k = 0

                #Make sure that the current line being read does not indicate the next line will be question text. Otherwise, the line
                #will contain information regarding a blank id which we will want to store.
                while tex_file_lines[i] != 'question_text':
                    q_data[j][f'question[answers][{k}][blank_id]'] = tex_file_lines[i].removeprefix('blank_id: ')
                    #Since each blank id will have an associated answer number and the correct answer, we can assign that answer to have
                    #100 weighting
                    q_data[j][f'question[answers][{k}][answer_weight]'] = 100
                    k += 1
                    i += 1

                i += 1

                #What follows is a replication of the procedure for question text as in numerical questions. Refer to the corresponding
                #section with the following while loop for a detailed comment.
                question_text = ''
                while tex_file_lines[i] != '\\begin{solution}':
                    if 'textit' in tex_file_lines[i]:
                        tex_file_lines[i] = tex_file_lines[i].removeprefix('\\textit{')
                        tex_file_lines[i] = tex_file_lines[i].removesuffix('}')
                        tex_file_lines[i] = '<i>'+tex_file_lines[i]+'</i>'
                    if 'includegraphics' in tex_file_lines[i]:
                        tex_file_lines[i] = re.search('{(.+?)}', tex_file_lines[i])
                        tex_file_lines[i] = tex_file_lines[i].group(1)
                        img_id = upload.up(tex_file_lines[i],course_id)
                        tex_file_lines[i] = '<img src=/courses/{}/files/'.format(course_id)+str(img_id)+'/preview alt='+tex_file_lines[i]+' />&nbsp;'
                    question_text = question_text+'<p>'+tex_file_lines[i].removesuffix('\\\\')+'</p>'
                    i += 1
                q_data[j]['question[question_text]'] = question_text

                #From above, we have that k is the number of blank ids and hence answers we should expect. Initialising a new counter (l)
                #for answers we can iterate l from 0 to k-1 and at each iteration associate a solution to their respective blank id.
                for l in range(0,k):
                    i += 1
                    q_data[j][f'question[answers][{l}][answer_text]'] = tex_file_lines[i].removesuffix('\\\\')
                    l += 1

            #Check if the question is a multiple choice question.
            elif tex_file_lines[i].removeprefix('question_type: ') == 'multiple_choice_question':
                q_data[j]['question[question_type]'] = 'multiple_choice_question'
                i += 2

                #What follows is a replication of the procedure for question text as in numerical questions. Refer to the corresponding
                #section with the following while loop for a detailed comment.
                question_text = ''
                while tex_file_lines[i] != '\\begin{solution}':
                    if 'textit' in tex_file_lines[i]:
                        tex_file_lines[i] = tex_file_lines[i].removeprefix('\\textit{')
                        tex_file_lines[i] = tex_file_lines[i].removesuffix('}')
                        tex_file_lines[i] = '<i>'+tex_file_lines[i]+'</i>'
                    if 'includegraphics' in tex_file_lines[i]:
                        tex_file_lines[i] = re.search('{(.+?)}', tex_file_lines[i])
                        tex_file_lines[i] = tex_file_lines[i].group(1)
                        img_id = upload.up(tex_file_lines[i],course_id)
                        tex_file_lines[i] = '<img src=/courses/{}/files/'.format(course_id)+str(img_id)+'/preview alt='+tex_file_lines[i]+' />&nbsp;'
                    question_text = question_text+'<p>'+tex_file_lines[i].removesuffix('\\\\')+'</p>'
                    i += 1
                q_data[j]['question[question_text]'] = question_text
                i += 2

                #Initialise a multiple choice answers counter to determine and differentiate the number of possible solutions.
                k = 0

                #Check if we have reached the end of solution choices. If not proceed to store the solution data.
                while tex_file_lines[i] != '\\end{oneparchoices}':

                    #For each candidate solution we need to associate a weighting to determine whether it is correct or wrong.
                    #If it is the correct answer (as indicated by the .tex file) we will assign a weighting of 100. Otherwise,
                    #the answer will have a 0 weighting.
                    if '\\CorrectChoice' in tex_file_lines[i]:
                        q_data[j][f'question[answers][{k}][answer_text]'] = tex_file_lines[i].removeprefix('\\CorrectChoice')
                        q_data[j][f'question[answers][{k}][answer_weight]'] = 100
                        k += 1
                    else:
                        q_data[j][f'question[answers][{k}][answer_text]'] = tex_file_lines[i].removeprefix('\\choice')
                        q_data[j][f'question[answers][{k}][answer_weight]'] = 0
                        k += 1
                    i += 1
            j += 1

        #Encountered an issue where if the .tex file did not have successively numbered questions then this script either fails
        #to read the file or truncates the contents of the file.
        #This seems to be arising from the 'j' counter and how and where in this script it is iterated.
        #I need to come back and rectify this issue.

        i += 1

    #Once the question data dictionary is built the function will return the list of dictionaries.
    return q_data
