import sys

arg1 = sys.argv[1]
tex_file = open(arg1,'r') #Open the .tex file
tex_file_lines = tex_file.readlines() #Create a list of all the lines in the .tex file

q_data = [{}] #Initialise list of dictionaries for question data

i = 0 #Initialise line counter
while i <= len(tex_file_lines)-1: #Clean the lines of all unnecessary characters
    tex_file_lines[i] = tex_file_lines[i].strip('\t%\n')
    i += 1

i = 0 #Re-initialise line counter
j = 0 #Initialise question counter
while i <= len(tex_file_lines)-1:
    if tex_file_lines[i].removeprefix('question_name: ') == f'Question {j+1}': #Check if we are at the beginning of a question
        if j >= 1: #If there is more than one question we expand the size of the question dictionary list
            q_data = q_data + [{}]
        q_data[j]['question[question_name]'] = tex_file_lines[i].removeprefix('question_name: ')
        i += 1
        q_data[j]['question[points_possible]'] = tex_file_lines[i].removeprefix('points_possible: ')
        i += 1
        if tex_file_lines[i].removeprefix('question_type: ') == 'numerical_question': #Check if the question is a numerical question
            q_data[j]['question[question_type]'] = 'numerical_question'
            i += 1
            q_data[j]['question[answers][0][numerical_answer_type]'] = tex_file_lines[i]
            q_data[j]['question[answers][0][answer_weight]'] = 100
            i += 2
            q_data[j]['question[question_text]'] = tex_file_lines[i]
            i += 2
            q_data[j]['question[answers][0][answer_exact]'] = tex_file_lines[i]
        elif tex_file_lines[i].removeprefix('question_type: ') == 'fill_in_multiple_blanks_question': #Check if the question is a fill in multiple blanks question
            q_data[j]['question[question_type]'] = 'fill_in_multiple_blanks_question'
            i += 1
            k = 0 #Initialise blanks counter
            while tex_file_lines[i] != 'question_text': #Check all lines up to the question text
                if 'blank_id' in tex_file_lines[i]: #Test if the line gives a blank id. If so we create a dictionary entry for the appropriate answer
                    q_data[j][f'question[answers][{k}][blank_id]'] = tex_file_lines[i].removeprefix('blank_id: ')
                    q_data[j][f'question[answers][{k}][answer_weight]'] = 100
                    k += 1
                i += 1
            i += 1
            q_data[j]['question[question_text]'] = tex_file_lines[i]
            i += 1
            for l in range(0,k): #Iterate over the number of blank ids we found earlier to assign to them their respective answer text
                i += 1
                q_data[j][f'question[answers][{l}][answer_text]'] = tex_file_lines[i].removesuffix('\\\\')
                l += 1
        elif tex_file_lines[i].removeprefix('question_type: ') == 'multiple_choice_question': #Check if the question is a multiple choice question
            q_data[j]['question[question_type]'] = 'multiple_choice_question"'
            i += 2
            q_data[j]['question[question_text]'] = tex_file_lines[i]
            i += 2
            k = 0 #Initialise multiple choice answers counter
            while tex_file_lines[i] != '\\end{oneparchoices}': #Check entire list of choices
                if '\\CorrectChoice' in tex_file_lines[i]: #Check if the current line has the correct choice
                    q_data[j][f'question[answers][{k}][answer_text]'] = tex_file_lines[i].removeprefix('\\CorrectChoice ')
                    q_data[j][f'question[answers][{k}][answer_weight]'] = 100
                    k += 1
                else:
                    q_data[j][f'question[answers][{k}][answer_text]'] = tex_file_lines[i].removeprefix('\\choice ')
                    q_data[j][f'question[answers][{k}][answer_weight]'] = 0
                    k += 1
                i += 1
        j += 1
    i += 1

print(q_data[0])
print(q_data[1])
print(q_data[2])
