# M07Assessment
 
## Introduction
Martin Luther King Day, Presidents Day, St. Patrick's Day, Easter, May Day, Independence Day for multiple cultures, International Talk Like a Pirate Day... these are just some of the many holidays out there.

You will be designing a text-based application to track holidays.

## High-Level Requirements
The application user is a member of the marketing team.

* The admin needs to be able to manage holidays in an easy-to-use interface.
* The admin already knows about a starting JSON file named holidays.json and appreciates that we have seeded the application with a base of holidays.
* They want all of the holidays from [https://www.timeanddate.com/holidays/us/](https://www.timeanddate.com/holidays/us/) to also be preloaded. Only preload holidays with concrete dates. Do not calculate holiday dates. The team expects you to include holidays from the present year, 2 years of past holidays, and 2 years of future holidays
* The holidays must be saved in JSON, following the formatting of the provided file.
* With the holidays approaching, the marketing person may want to know what the weather looks like so they can determine what to market more. Use a weather API to show what the weather looks like for the current period. (See the notes below for details.) We recommend [Open Weather Map API](https://rapidapi.com/community/api/open-weather-map), but you are free to use any weather API you would like.
## Sample UI
This is a sample UI which you can use as your base UI. While your UI may be different, make sure functionality outlined in the sample UI is accounted for in your UI.

### Start Up

```
Holiday Management
===================
There are 10 holidays stored in the system.
```


### Main Menu
<code>Holiday Menu
================
1. Add a Holiday
2. Remove a Holiday
3. Save Holiday List
4. View Holidays
5. Exit</code>
### Add a Holiday
<code>Add a Holiday
=============
Holiday: Internat'l Talk Like a Pirate Day
Date: 20210-09-19

Error:
Invalid date.  Please try again.

Date for Internat'l Talk Like a Pirate Day: 2021-09-19

Success:
Internat'l Talk Like a Pirate Day (2021-09-19) has been added to the holiday list.</code>
### Remove a Holiday
<code>Remove a Holiday
================
Holiday Name: International Talk Like a Pirate Day

Error: 
International Talk Like a Pirate Day not found.

Holiday Name: Internat'l Talk Like a Pirate Day

Success:
Internat'l Talk Like a Pirate Day has been removed from the holiday list.</code>
### Save Holiday List
<code>Saving Holiday List
====================
Are you sure you want to save your changes? [y/n]: n

Canceled:
Holiday list file save canceled.

Are you sure you want to save your changes? [y/n]: y

Success:
Your changes have been saved.</code>
### View Holidays
<code>View Holidays
=================
Which year?: 2021
Which week? #[1-52, Leave blank for the current week]: 2

These are the holidays for 2021 week #2:
Margaret Thatcher Day (2020-01-10)
World Sketchnote Day (2021-01-11)
Zanzibar Revolution Day (2021-01-12)
National Rubber Ducky Day (2021-01-13)
Tamil Thai Pongal Day (2021-01-14)
National Bagel Day (2021-01-15)
Signing of the Peace Accords (2021-01-16)
For the current week, the user should have an option to indicate whether they want to see the weather as well.

View Holidays
=================
Which year?: 2021
Which week? #[1-52, Leave blank for the current week]: 
Would you like to see this week's weather? [y/n]: y

These are the holidays for this week:
Margaret Thatcher Day (2020-01-10) - Sunny
World Sketchnote Day (2021-01-11) - Partly cloudy
Zanzibar Revolution Day (2021-01-12) - Thunderstorms
National Rubber Ducky Day (2021-01-13) - Partly cloudy
Tamil Thai Pongal Day (2021-01-14) - Partly cloudy
National Bagel Day (2021-01-15) - Scattered thunderstorms
Signing of the Peace Accords (2021-01-16) - Sunny
### Exit
If there are no changes to be saved:</code>

<code>Exit
=====
Are you sure you want to exit? [y/n] y

Goodbye!</code>

If there are changes to be saved:

'''
Exit
=====
Are you sure you want to exit? 
Your changes will be lost.
[y/n] y

Goodbye!
'''

## Technical Requirements
Do not use pandas. If you use pandas for this assessment, you will have to refactor your code.

* Use the provided starter code which includes pseudo-code and some instructions so instructional staff can automatically test your code. You may need more functions then the provided functions in the starter code.
* There is a starting JSON file named holidays.json to give you an idea of what kind of data will be used.
* Holidays should be represented as objects in Python.
* The List of Holidays should be represented as an object in Python (see starter code for details)
* The holiday class should include a way to display a holiday in the following format:
  <code> Holiday Name (Date)</code>
* Use a lambda expression for printing out holidays for a selected week.
* Use flowcharts or pseudo code to visualize the design plan for your application based on your interpretation of the starter code.
## Approach
* Objects are commonly used when working with formatted data - such as JSON or XML.

* These are questions that should be answered by demonstrating them in your code:

  * What is a lambda expression?
  * What are classes?
  * How do you use Beautiful Soup for web scraping?
  * How do you consume an API?
  * How do you store data in JSON?
## Stretch Goals
* Allow searching for a single date and return all holidays for that date.

* Add tags for holidays to find things such as food-related holidays, religious holidays, and cultural holidays. Then, allow for searching for all holidays by tag.

* Save the file in another (additional) file format. Note: This would require a way for the user to specify which format to save in. JSON must be implemented. An additional file format is the stretch part.

* Calculate dates for variable holidays - such as Mother's Day, Father's Day, Easter, and Election Day (Difficult stretch goal).

* Please note: Some of the stretch goals will require you to change your menu and menu logic as well as add functions to the HolidayList Class.