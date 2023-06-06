# COVID:  School-level learning impact analysis

## Executive Summary

This project aims to analyze the impact of learning loss and the effectiveness of learning loss recovery interventions for Students in Tennessee.  For the purpose of this analysis, impact and recovery is measured in terms of changes in annual achievement assessment scores from the years 2018 - 2022.  The bulk of the data used in this analysis was provided by the Tennessee Department of Education.  In aggregate, the data contains 2,375,946 entries and represents approximately 485 schools within Tennessee's 137 school districts for a combined

The motivation for this project stems from the observation that, contrary to my personal expectations, achievement metrics in some districts continued to decline during the post-COVID learning recovery phase. I hope that by measuring the rate of improvement (ROI) for each school I will be able to discern features in individual school performance that could be predictive of a district’s performance. Geo-spatial data and visualizations will be used to help users explore the data through a dashboard developed using the Plotly Dash package in Python.

## Motivation

When analyzing district-wide achievement data, I observed that achievement metrics in some school districts continued to decline during the post-COVID learning recovery phase. This was contrary to my original expectations and prompted an interest in exploring individual school achievement scores to identify any discernible features that could be indicative of continued loss or recovery. This project seeks to understand the extent of learning loss and recovery efforts in individual schools within all Tennessee districts, taking into account the significant disruption to education caused by the COVID-19 pandemic.

## Data Question

Given a school's learning loss impact compared to its previous pre-pandemic TNReady assessments, what was the rate of improvement/loss given learning loss interventions? Are there any discernible features in achievement scores for individual schools that could be indicative of continued loss or recovery for the district?

---

## Claytor's log

### 05/21/23

* Installed core packages for plotly dash.
* Identified that there were issues with naming conventions and compatibility with the data-sets used across the years.
* Looks like 2017 does not have a categorical columns `system_name` and `school_name` associated with the `system `and `school` present in the other data.  I need to figure out an efficient method to back-fill this information.
  * I initially tried to back-fill based on `data_2018` but it still resulted in several `nan` values where 2429 entries were unmapped.
  * something weird is going on here.  I spot checked some of the missing schools associated with the systems.  They do not exist in the data past 2017!  I do not think my back filling was incorrect at all.  I have so many questions to ask about this, but I can do without this year for my analysis.  If I want to do lag scores, I could use it for county averages, but I don't feel comfortable including the schools that do not exist in my school-level analysis.
    * system - school(s)
      * 10            [105]
      * 11              [0]
      * 150             [0]
      * 190      [425, 520]
      * 231            [25]
      * 300             [0]
      * 470            [83]
      * 580         [0, 75]
      * 650             [0]
      * 792    [2075, 2760]
      * 794           [170]
      * 800            [35]
      * 820           [200]
      * 830             [0]
      * 860             [0]
      * 985    [8035, 8080]
* I was able to merge 2018,2019,2021, and 2022.  It looks like in 2017 and 2018 that `enrolled`, `tested`, and `participation_rate` data is missing.  I'm going to opt to drop those categories.
  * the resulting data-frame has **2,375,946** entries.  Many will be dropped because having a grade-level breakdown of each assessment does not assist in this analysis.  There are cases where
* I am **EXCITED** that where `grade =  All Grades` ,  `student_group` does seem to yield some sub-population data (gender, ethnicity, English language learner, students with disabilities, etc.) at the school level!  I'm sure that availability must vary on a school-by-school basis, but it might be enough to make an adequate analysis.
* It looks like there may be some solid charter school information in some of the later data-sets.  I wonder if there are noticeable differences between the two groups?  I'd love to dig deeper.  I'll keep in in my back pocket for later.

### 05/23/23

* I spoke with Neda.  She recommended the I remove the "mislabeled" data and salvage what I can keep.  I'm inclined to agree.
* I standardized the naming of the 2017 data-set.  Only problem is, there is not a `test` Associated with each subject.  I'll have to generate that mapping too for the analysis to work.
* I sent an Email to TNED.Assessment@tn.gov to help clarify a few questions about data from 2017 and some assessments that appear some years, and those who do not.
* For the sake of time, I'm just going to have to leave 2017 alone.  Labeling is incomplete and ambiguous.  I cannot reconcile the ambiguity and make accurate predictions without subject matter assistance.
* I found out that the Charter School Commission was established in 2019.  So If I do have charter school data, It may be limited before COVID closures (or that could be an untested assumption on my part.  Will continue to keep that analysis in my back pocket).

| test                            | Algebra I | Algebra II | Biology I | Chemistry | ELA    | English I | English II | English III | Geometry | Integrated Math I | Integrated Math II | Integrated Math III | Math   | Science | Social Studies | US History |
| ------------------------------- | --------- | ---------- | --------- | --------- | ------ | --------- | ---------- | ----------- | -------- | ----------------- | ------------------ | ------------------- | ------ | ------- | -------------- | ---------- |
| EOC                             | 91205     | 73803      | 70002     | 17329     | 0      | 73930     | 74950      | 14473       | 84102    | 20064             | 17842              | 14228               | 0      | 0       | 0              | 68106      |
| MSAA                            | 0         | 0          | 0         | 0         | 39430  | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 39430  | 0       | 0              | 0          |
| MSAA/Alt-Science/Social Studies | 0         | 0          | 15087     | 0         | 110944 | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 110924 | 83458   | 56907          | 0          |
| TNReady                         | 0         | 0          | 0         | 0         | 406710 | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 405732 | 270697  | 216593         | 0          |

* Looks like I need to break this table down a bit further to aggregate by test and then subject. The data are noisy and I will filter by the aggregated scores reported in each school to account for that. The general heuristic is that the majority of students tend to take these tests in a specific grade.  However, some students take the tests in earlier or later grades than their peers.  In these cases, there can be much grade-level suppression.  Therefore, aggregations are much less suppressed than grade-level reports.

### 05/24/23

* [x] Drop `MSAA` & `MSAA/Alt`

* [x] Filter to `Grade = 'All Grades`

* When dropping `MSAA` tests, the resulting data-frame contains **1,919,766** rows. This removes **456,180** rows from the data-set.

* Using the aggregate of `All Grades` , the data now represent the average subject proficiency for each school. The data-frame was reduced to **525,044** rows

* I think I maybe able to salvage more demographic information by performing some simple subtraction.  The data wont have as many dimensions as the non-suppressed data, but maybe I can still compare Non-Proficient vs Proficient.

### 05/25/23

* [x] Drop `pct_approaching`, `pct_met_expectations`, `pct_exceeded_expectations` achievement categories.

* [x] Drop `*`  There is no way to infer the proficiency of student_groups that do not have at-least 10 valid tests.

* I honestly think that the data will be easier to work with if I can make expectations a binary classifier.
  
  * If a student_group's proficiency scores for a building are suppressed due to achievement outliers, the `pct_met_exceeded` is still reported.  If I subtract that number from 1, I will be left with the percent that did not meet expectations.  I cannot infer categories in-between, but I can make a simple "pass/fail" comparison.
  * There is nothing I can do about `*`  because it suggests that enrollment (or number of valid tests ) of of that student_group is less than 10 at the individual school.

* Assumptions really being challenged here.  Not so simple to calculate missing values without a little extra logic.  Apparently there can be `**` in some of the `pct_met_exceeded`.  There were **44,454** entries where `pct_met_exceeded` was suppressed.  If filtered to "All Students" `student_group`, **2,405** entries are `**` suppressed.
  
  * I know that I'm going to have to remove the fully suppressed `**` data from my main data-frame, But I'm going to capture it into a separate dataframe for some light analysis.

### 05/27/23

* Spoke with Neda.  Lots of encouragement.  I'm stoked!  I'm almost ready to join NCES data
* I am going to merge geodata before splitting off the fully suppressed data.  I think it would be good to have geographic data as a part of my full suppression information.

### 05/28/23

- Researched data-sets From NCES.  Pulled Common Core data files for each year as well.  The data isn't as nice for getting some of the descriptive labels that I thought I could . . . but it does save me a lot of work in not having to use an API to geoencode addresses.
  
  - Looks like **geoencoding** will not be needed for this project as NCES provides lat/long and addresses for all schools in a given year.  They also include Shapefiles for both school and district boundaries.
  
  - Created the following data directory structure
    
    - Common Core Data
    - Geoencode - School
    - Geoencode - LEA

- No shape files for 2018.  I wonder what the best way to deal with that would be?

### 05/29/23

- Merged all CCD data from NCES for the years in question.  Set encoding to `latin_1` and low memory to `False` because Pandas wanted to encode as `utf-8` and `us_ascii` did not work either, Though that's what the original files were encoded in.
  - Dropped all schools except those in Tennessee
- . . . Then I took a long hard look at the data that I needed to merge and what else I wanted to include.  I poked around the NCES website and found their ElSi table generator and I decided to generate my own custom file per year.  This keeps me from having to clean the CCD data of what I don't need and allows me to avoid having to merge the geoencode data and other additional data.
- And that's what I get for trying to be clever.  Using the tool to grab one year at a time and then merging resulted in unnecessary complication and, more critically, misaligned datasets.  I changed approach instead to dumping all years in wide form and translating to long form.  The data looks fully merged and free from most human error.

### 05/30/23

* [x] Reorder dataframe cols for assessment and elsi data

* [x] merge assessment and elsi

* [x] deal with the nan values that resulted from the merging

* [x] Split off `**` suppressed data.  Put it in its own pkl to avoid overwriting it.  I cannot convert proficiency to numbers with `**` still in the `pct_met_exceeded` rows.

* Fixed naming and order of columns in NCES Data.

* Exported NCES data for merging with school-level testing data data.
  
  * I exported this as elsi_clean.pkl 🥒 to my school_based folder.

* Merged the DataFrames.  It appears that **693** rows from the assessment DataFrames went unmatched when merging.

* Spoke with Rohit, he gave me some good info.  He always has the coolest hats 🛹
  
  * [https://gis.stackexchange.com/questions/113799/reading-shapefile-in-python](https://gis.stackexchange.com/questions/113799/reading-shapefile-in-python)
  * import geopandas as gpd
  * shapefile = gpd.read_file("shapefile.shp")
  * print(shapefile)

* Looks like there are **17 schools** that are managed by the state or do not appear more than once before the year 2021.  The vast majority of the reported scores are `**` suppressed.  These will be removed from the **assessments dataframe**.  However, they will be a part of my fully suppressed scores analysis.

* **44,454** scores across all years, schools, and subjects were fully suppressed in the data they were removed.

* **335,452** non-suppressed datapoints are now available in the dataset.

### 05/31/23

* [x] make a new column `not_met` ElSi of performance

* [x] Remove assessments that only appear in one year

* [x] Add subject_level column which associates each type of test with its subject content( e.g., literacy, numeracy, science, and social studies)

* [x] Create mapping dictionary to apply content_area labels to subjects.

* I added added a calculated column,  `not_met`. This will allow me to see the total percentage of student_groups that did not meet expectations, regard.

* Made a pivot table to look at average state-wide proficiencies for each subject each year, grouped by test type.

* My new subject_area column was a success.  I created a dictionary and mapped it to associate each test type with a subject area descriptor.

* I made some cool plotly visuals while I was waiting an entire eternity for Conda to install GeoPandas

* Exported prepped dataset to be used in EDA notebooks

### 06/01/23

* [x] Create Plotly Notebook

* [x] Create EDA Notebook

* [x] Finish planning how you are going to accomplish the objectives Michael gave you.

* [ ] Briefly analyze  `**` suppressed data.

* I made a new EDA and Plotly notebook.  I'm ready to begin diving deeper into the data and to visualize it.

* Read some documentation about plotly dash.

* Could not get the basic Plotly Dash App to run :-)

* Had a great checkin with Michael.  He gave some really solid advice.  I spent some time unpacking what he said and adding action items to my list.

---

#### Notes from My check-in with Michael

##### **(1) Focus on getting Dash up and running**

* [x] Simple averages and whatnot
* [x] Make a mock-up of the app
  * [x] What will the layout be?
  * [x] Figure out the groups you want to compare in a way that makes sense and is visually appealing
* [ ] Figure out how to make the map your centerpiece
  * [x] What shapefiles do you want to use?
    * [x] I have county and district.  Perhaps I can use both, but I may have to load in ElSi lat long coordinates for the district.
* [x] What will the color palette be?
  * [x] Tennessee of course!  Look up the state's colors!

##### **(2) - Make a solid EDA**

* [ ] Look at the drops (aka lag scores)
* [ ] What how to individual schools compare to the state and district?
* [ ] Create Lag Scores
  * [ ] What is the difference between year's 2019 and 2022? (Change Prepandemic and Now)
  * [ ] What is the difference between year's 2021 and 2022 (Impact Phase)
* [ ] County Level
  * [ ] How does the change in scores relate to the state Average in the dataset?
    * [ ] Impact Phase
    * [ ] Change Pre-pandemic vs. now
* [ ] How did the subpopulatons do?

##### **(3) - Figure out Linear Regression**

* [ ] What Variables Do I want to use?
  * [ ] School Type?
    * [ ] Title 1
    * [ ] Magnet
  * [ ] Student Subgroup?
  * [ ] Area (rural vs urban)

### 06/02/23

- Spent the day trying to get Plotly Dash up and running.  I have a simple app that makes effective use of callbacks.  It was a bit of a headache, and it's basic, but it works without error.
- Up until 2.  Finally got the app to a place where I can fiddle with the html layout without breaking.  Apparently you can use emoji in markdown on plotly dash.  Who knew 🤷‍♂️.

### 06/03/23

* [x] My priorities are to just get a simple map up and running in the dash app.
- School level shapefiles take forever to load.  Exploration of the file reveals it it contains all school districts in the US and its territories.  I will subset it to improve load times.  The same is also true for district shapefiles

- The geometry in my shape file is in CRS form.  I think that the errors in my mapping app want me to re-project my data to convert it from a curved to a flat surface.  Hopefully this will give me the flat map I'm looking for.

- Created function to change dtypes of lat and long assessment columns and then create a GeoPandas df.  I turned on the pkl generator and made a fresh batch.

### 06/03/23

- [x] Get A Simple Map Made

- Had a chance to speak with Michael today.  We discovered that the geometry in my data did not have polygons.  I was able to get some new shape files from the NCES.

- ⏰ Several hours later ⏰

- I have a pretty Map!!!!!!!! 

### 06/03/23

- [ ] Make aggregated dataframe from pivots

- [x] Make the weights (Use Valid tests to weight)
  
  - [x] pct_met_exceeded
  
  - [x] stu_tchr_ratio
  
  - [x] fte_teachers

- [ ] Make the weighted averages pivots
  
  - [ ] pct_met_exceeded
    
    - [ ] numerator
    
    - [ ] denominator
    
    - [ ] weighted average 
  
  - [ ] stu_tchr_ratio
    
    - [ ] numerator
    
    - [ ] denominator
  
  - [ ]   
  - [ ] fte_teachers
    
    - [ ] numerator
    
    - [ ] denominator
    
    - [ ] weighted average
  
  - [ ] 
- Made a pivot table to aggregate school data into district data.  I will use this so that I can merge with district geometry for my choropleth map.
  
  - I actually made several.  However, they are unweighted, so I'll need to remake them.

- I spoke with Michael again today.  It looks like my pivots to not take into account the differing sizes of the population.  I will need to weight the results.  I will weight them by number of valid tests.

- Made sure that numeric columns had the correct dtype

- I created three weight columns for 'pct_met_exceeded', 'stu_tchr_ratio', 'fte_teachers' based on valid tests as a weight

- Encoded 'magnet', 'charter', and 'title_1' columns to 1 and 0 values from 'yes', 'no' strings. 
