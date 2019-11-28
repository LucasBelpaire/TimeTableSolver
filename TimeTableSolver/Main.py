import constructTimeTable
import initTimeTable
import processInput
import generateOutput

unplaced_events = constructTimeTable.construct_time_table()
#print(len(processInput.courses_dict))
count = 0

print(count)
print(len(unplaced_events))
for event in unplaced_events:
    course = processInput.courses_dict[event.course_code]
    print(str(course.code) + ", " + str(course.student_amount))

generateOutput.generate_output_from_time_table()