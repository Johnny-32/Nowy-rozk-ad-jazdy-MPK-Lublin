# Example 1. (Made in July 2026 - Holiday timetable) ------------------------------------------------------------------------------------------------
# Line: 32
# Direction: Daszyńskiego
# Bus stop: Plac Litewskiego 02 (Index - 1022)
# Timetable:
# 
#     5   6    7    8   9   10  11   12  13   14  15   16   17   18   19   20   21   22   23 
#    05  07   26   15  02   14  02   14  02   14  02   17   04   05   03   03   06   06   05
#    37  34   51   38  26   38  26   38  26   38  29   41   35   33   33   36   36   36  NaN
#   NaN  59  NaN  NaN  50  NaN  50  NaN  50  NaN  53  NaN  NaN  NaN  NaN  NaN  NaN  NaN  NaN
# 
# In this example we will be sticking to hours 5-9
# 1. Calculating differences
# 5:37 - 5:05 = 32
# 6:07 - 5:37 = -30 + 60 = 30
# 6:34 - 6:07 = 27
# 6:59 - 6:34 = 25
# 7:26 - 6:59 = -33 + 60 = 27
# 7:51 - 7:26 = 25
# 8:15 - 7:51 = -36 + 60 = 24
# 8:38 - 8:15 = 23
# 9:02 - 8:38 = 24
# 9:26 - 9:02 = 24
# 9:50 - 9:26 = 24
# 
# So using our common sense we can see that frequencies are:
# 5:05 - 6:07 --- 30 minutes
# 6:07 - 7:51 --- it makes sense to make it 24 minutes, but in reality it's 26 minutes
# 7:51 - 9:50 --- 24 minutes
# 
# 
# Now we can group the differences, let's say that the tolerance between differences is 2 minutes
# |32 - 30| = 2 -> group 1.
# |30 - 30| = 0 -> group 1.
# |27 - 24| = 3 and |27 - 30| = 3 -> not matched
# |25 - 24| = 1 -> group 2.
# |27 - 24| = 3 and |27 - 30| = 3 -> not matched
# |25 - 24| = 1 -> group 2.
# |24 - 24| = 0 -> group 2
# |23 - 24| = 1 -> group 2
# |24 - 24| = 0 -> group 2
# |24 - 24| = 0 -> group 2
# 
# Now we have two unmathed elements that have neighboring elements that are groups,
# so we can add them to a group, which has a neighboring element that is closest to an unmatched element.

# In both cases we add unmatched elements to the group 2. and finally we get:
# [[32, 30], [27, 25, 27, 25, 24, 23, 24, 24]]
# 
# HARDER TO IMPLEMENT FREQUENCY ALGORITHM, BUT IT COULD WORK BETTER WITH UNCOMMON FREQUENCIES (35, 42 minutes etc.) 
# COULD BE USED IN THE FUTURE
# 
# Now we can group the differences, let's say that the tolerance between differences is 2 minutes
# 32 - 30 = 2 -> Start of group 1.
# 30 - 27 = 3 -> End of group 1.
# 27 - 25 = 2 -> Start of group 2.
# 25 - 27 = 2 -> Both in group 2.
# 27 - 25 = 2 -> Both in group 2
# 25 - 24 = 1 -> Both in group 2
# 24 - 23 = 1 -> Both in group 2
# 23 - 24 = 1 -> Both in group 2
# 24 - 24 = 0 -> Both in group 2
# 24 - 24 = 0 -> Both in group 2
# 
# So now we have 2 groups and now we can calculate the mean from all values in each group and see which predefined frequency (for ex. 20, 24, 30, ...) will be the closest to the mean and assign that label
# for ex. group 1. (32 + 30) / 2 = 31 -> which is close to 30, so we will asign a 30 minute frequency label to that group
# group 2. after calculations will have 24 minute frequency label
# 
# We can see that the last difference for the group 1 is 30, and the first for the group 2. is 27,
# so that means if we skip "End of group 1." we have all the differences in correct groups (obviously we need to delete duplicates)
# 
# Now we need to extract timestamps from key differences (30 and 27)
# We can do this by - extracting the key from dictionary:
# in group 1. we have a key difference of 30, which translates to 6:07 - 5:37
# in group 2. we have a key difference of 27, which translates to 6:34 - 6:07
# 
# Beacuse the first number of the 1. group and the second number of the 2. group matches, that means that 6:07 will be a breakpoint for frequency labels
# 
# As a result we got frequencies which are the same as we got above using common sense
# 
# ??? Maybe add calculating frequencies by getting the timetable from the first stop of a route, beacuse the departures there are more consistent

import timetable
from math import isnan


minute_list_container = []
difference_list_container = []
difference_list_container = []
group_list_for_a_timetable_period_container = []
not_matched_index_list_container = []
tolerance = 2
predefined_frequency_list = [15, 20, 24, 30, 40, 45, 60]

for idx in range(len(timetable.df_list)):
    current_df = timetable.df_list[idx]

    # Filling a list with departure values in tuples: ('hour', 'minute')

    minute_list = []

    for key, value in current_df.items():
        for minute in value:
            if not (isnan(float(minute))):
                minute_list.append((key, minute))
    minute_list_container.append(minute_list)

    # Filling a list with differences between departures in tuples: ('hour:minute-hour:minute', 'difference')

    current_minute_list = minute_list_container[idx]
    difference_list = []
    for idx_m in range(len(current_minute_list) - 1):
        current_hour, current_minute = current_minute_list[idx_m]
        next_hour, next_minute = current_minute_list[idx_m + 1]
        difference_value = 60 * (int(next_hour) - int(current_hour)) + (int(next_minute) - int(current_minute))
        difference_key = f"{current_hour}:{current_minute}-{next_hour}:{next_minute}"
        difference_list.append((difference_key, difference_value))
    difference_list_container.append(difference_list)

    # Making groups based on frequency, not_matched differences are not put in a group, they're bare elements
    # ex. (diff. between dep. are skipped in this ex. for simplicity) 
    # [[32, 30], 27, [25, 24]]

    current_difference_list = difference_list_container[idx]
    group_list_for_a_timetable_period = []
    not_matched_index_list = []

    current_group = []
    current_matched_freq = None

    for current_item in current_difference_list:
        current_two_timestamps, current_difference = current_item
        
        matched_freq = None
        for predefined_freq in predefined_frequency_list:
            if abs(current_difference - predefined_freq) <= tolerance:
                matched_freq = predefined_freq
                break
                
        if matched_freq is not None:
            if current_matched_freq is not None and matched_freq != current_matched_freq:
                if current_group:
                    group_list_for_a_timetable_period.append(current_group)
                current_group = []
                
            current_group.append(current_item)
            current_matched_freq = matched_freq
        else:
            if current_group:
                group_list_for_a_timetable_period.append(current_group)
                current_group = []
            
            group_list_for_a_timetable_period.append(current_item)

            idx_sublist = len(group_list_for_a_timetable_period) - 1
            not_matched_index_list.append(idx_sublist)

            current_matched_freq = None

    if current_group:
        group_list_for_a_timetable_period.append(current_group)

    group_list_for_a_timetable_period_container.append(group_list_for_a_timetable_period)
    not_matched_index_list_container.append(not_matched_index_list)


# Now we have a list of not matched elements and they can be sorted into three categories:
# Cat 1. Not matched elements that are surrounded by groups (ex. [..., group0, notmatched0, group1, ...])
# Cat 2. Not matched elements that have a neighboring element which is a group (either to the left or to the right) (ex. [..., group0, notmatched0, notmatched1, ...])
# Cat 3. Elements that are surrounded by not matched list elements (ex. [..., notmatched0, notmatched1, notmatched2, ...])
# 
# So my soultion is to append every element to a group in following steps:
# 1. If we find an element in Cat 1. we append it to the group that has the element that is the closest to an unmatched element
# ex. [[..., 30], 27, [25, ...]] we append that element to the group to the right, beacuse |27 - 30| > |27 - 25|
# 2. If we find an element in Cat 2. we append that element to the group that neighbors this element
# 
# By doing this two steps we should transform elements in Cat 3. to an element in either Cat 1. or Cat 2.

    current_group_list = group_list_for_a_timetable_period_container[idx]
    current_not_matched_index_list = not_matched_index_list_container[idx]

    idx_gr = 0
    while idx_gr < len(current_group_list):
        item = current_group_list[idx_gr]

        if not isinstance(item, list):
            left_is_group = (idx_gr > 0) and isinstance(current_group_list[idx_gr - 1], list)
            right_is_group = (idx_gr < len(current_group_list) - 1) and isinstance(current_group_list[idx_gr + 1], list)

            get_val = lambda x: x[1] if isinstance(x, tuple) else x

            current_val = get_val(item)

            # Finding a Cat 1. element - exactly one neighbor that is a group
            if left_is_group ^ right_is_group:
                if left_is_group:
                    left_group = current_group_list[idx_gr - 1]
                    left_group.append(item)
                else:
                    right_group = current_group_list[idx_gr + 1]
                    right_group.insert(0, item)

                current_group_list.pop(idx_gr)
                continue 

            # Finding a Cat 2. element - both neighbors are groups
            elif left_is_group and right_is_group:
                left_group = current_group_list[idx_gr - 1]
                right_group = current_group_list[idx_gr + 1]

                last_left_val = get_val(left_group[-1])
                first_right_val = get_val(right_group[0])

                dist_to_left = abs(current_val - last_left_val)
                dist_to_right = abs(current_val - first_right_val)

                if dist_to_left < dist_to_right:
                    left_group.append(item)
                    current_group_list.pop(idx_gr)
                elif dist_to_left > dist_to_right:
                    right_group.insert(0, item)
                    current_group_list.pop(idx_gr)
                # Join two lists and an element
                # ex. [..., group0, elem0, group1, ...] -> group0-elem0-group1
                else:
                    left_group.append(item)
                    left_group.extend(right_group)

                    current_group_list.pop(idx_gr)
                    current_group_list.pop(idx_gr)
                continue

        idx_gr += 1

# for group in group_list_for_a_timetable_period_container[0]:
#     print(f"Group:\n{group}\n")
