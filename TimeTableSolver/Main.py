import constructTimeTable
import initTimeTable
import processInput

unplaced_events = constructTimeTable.construct_time_table()
#print(len(processInput.courses_dict))
count = 0

for key, value in initTimeTable.time_table.items():
    if value is not None:
        print(key[0].fi_number, key[1], value.course_code)
        home_site_ok = 0
        for curriculum in value.curricula:
            if curriculum.home_site == processInput.class_rooms_dict[key[0].fi_number].site_id:
                home_site_ok += 1

        print("homeSite:" + str(home_site_ok))
        count += 1

print(count)
print(len(unplaced_events))
for event in unplaced_events:
    course = processInput.courses_dict[event.course_code]
    print(str(course.code) + ", " + str(course.student_amount))

