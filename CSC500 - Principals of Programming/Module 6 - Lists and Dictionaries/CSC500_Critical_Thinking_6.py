
def main():
    #Answers to the Exam
    answer_key = extract_answer_key('answer_key.txt')
    #Submitted Exam Responses
    responses = extract_answer_key('ExamResponses.txt')
    # Number of questions in Exam
    exam_question_count = len(answer_key)
    # Number of questions answered
    questions_answered_count = len(responses)
    incorrect_answer_count = 0
    questions_wrong = []
    
    i = 0
    while i < exam_question_count:
        try:
            correct_answer = answer_key[i]
            answer = responses[i]
            if answer != correct_answer:
                incorrect_answer_count +=1
                questions_wrong.append(i+1)
        except:
            # Prevents index errors
            if exam_question_count > questions_answered_count:
                #Question # and response not in the Exam Responses file. Incorrect
                incorrect_answer_count +=1
                questions_wrong.append(i+1)
        i+=1

    total_correct = exam_question_count - incorrect_answer_count
    exam_score = round((1 - incorrect_answer_count / exam_question_count) * 100,2)

    print("There were", total_correct, "questions answered correctly.")
    print("There were", incorrect_answer_count, "question(s) that were incorrect.")
    if incorrect_answer_count > 0:
        print("The questions that were missed were " + str(questions_wrong) + ".\n")
    print("Final Score: " + str(exam_score)+"%")

    # Determined passing grade as 75% to allow more questions to be added to the exam. 
    # 15/20 = 75%
    if exam_score >= 75:
        print("Congratulations. You passed the exam. Your Driver's License will be mailed to you in 5-10 business days.")
    else:
        print("You did not pass the exam. Please review the materials, and try again.")
    pass

def extract_answer_key(file_path):
    key = []
    with open(file_path,'r') as answer_key:
        for answer in answer_key:
            answer = answer.split('.')[1].strip().upper()
            key.append(answer)
    return key

if __name__ == '__main__' : main()
