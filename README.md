# COVID:  School-level learning impact analysis

## Executive Summary

This project aims to analyze the impact of learning loss and the effectiveness of learning loss recovery interventions for Students in Tennessee.  For the purpose of this analysis, impact and recovery is measured in terms of changes in annual achievement assessment scores from the years 2018 - 2022.  The bulk of the data used in this analysis was provided by the Tennessee Department of Education.  In aggregate, the data contains 2,375,946 entries and represents approximateley 485 schools within Tennessee's 137 school districts for a combined

The motivation for this project stems from the observation that, contrary to my personal expectations, achievement metrics in some districts continued to decline during the post-COVID learning recovery phase. I hope that by measuring the rate of improvement (ROI) for each school I will be able to discern features in individual school performance that could be predictive of a district’s performance. Geospatial data and visualizations will be used to help users explore the data through a dashboard developed using the Plotly Dash package in Python.

## Motivation

When analyzing district-wide achievement data, I observed that achievement metrics in some school districts continued to decline during the post-COVID learning recovery phase. This was contrary to my original expectations and prompted an interest in exploring individual school achievement scores to identify any discernible features that could be indicative of continued loss or recovery. This project seeks to understand the extent of learning loss and recovery efforts in individual schools within all Tennessee districts, taking into account the significant disruption to education caused by the COVID-19 pandemic.

## Data Question

Given a school's learning loss impact compared to its previous pre-pandemic TNReady assessments, what was the rate of improvement/loss given learning loss interventions? Are there any discernible features in achievement scores for individual schools that could be indicative of continued loss or recovery for the district?

---

## Claytor's log

### 05/21/23

* Installed core packages for plotly dash.
* Identified that there were issues with naming conventions and compatability with the datasets used across the years.
* Looks like 2017 does not have a categorical columns `system_name` and `school_name` associated with the `system `and `school` present in the other data.  I need to figure out an efficent method to backfill this information.
  * I initially tried to backfill based on `data_2018` but it still resulted in several `nan` values where 2429 entries were unmapped.
  * something wierd is going on here.  I spot checked some of the missing schools associated with the systems.  They do not exist in the data past 2017!  I do not think my back filling was incorrect at all.  I have so many questions to ask about this, but I can do without this year for my analysis.  If I want to do lag scores, I could use it for county averages, but I don't feel comfortable including the schools that do not exist in my school-level analysis.
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
  * the resulting dataframe has **2,375,946** entries.  Many will be dropped because having a grade-level breakdown of each assessment does not assist in this analysis.  There are cases where
* I am **EXCITED** that where `grade =  All Grades` ,  `student_group` does seem to yeild some subpopulation data (gender, ethnicity, english language learner, students with disabilities, etc.) at the scool level!  I'm sure that availability must vairy on a school-by-school basis, but it might be enough to make an adequate analysis.
* It looks like there may be some solid charter school information in some of the later datasets.  I wonder if there are noticable differences between the two groups?  I'd love to dig deeper.  I'll keep in in my back pocket for later.

### 05/23/23

* I spoke with Neda.  She reccommended the I remove the "mislabeled" data and salvage what I can keep.  I'm inclined to agree.
* I standardized the naming of the 2017 dataset.  Only problem is, there is not a `test` Associated with each subject.  I'll have to generate that mapping too for the analysis to work.
* I sent an Email to TNED.Assessment@tn.gov to help clairify a few questions about data from 2017 and some assessments that appear some years, and those who do not.
* For the sake of time, I'm just going to have to leave 2017 alone.  Labeling is incomplete and ambiguous.  I cannot reconcile the ambiguity and make accurate predictions without subject matter assistance.
* I found out that the Charter School Comission was established in 2019.  So If I do have charter school data, It may be limited before COVID closures (or that could be an untested assumption on my part.  Will continue to keep that analysis in my back pocket).

| test                            | Algebra I | Algebra II | Biology I | Chemistry | ELA    | English I | English II | English III | Geometry | Integrated Math I | Integrated Math II | Integrated Math III | Math   | Science | Social Studies | US History |
| ------------------------------- | --------- | ---------- | --------- | --------- | ------ | --------- | ---------- | ----------- | -------- | ----------------- | ------------------ | ------------------- | ------ | ------- | -------------- | ---------- |
| EOC                             | 91205     | 73803      | 70002     | 17329     | 0      | 73930     | 74950      | 14473       | 84102    | 20064             | 17842              | 14228               | 0      | 0       | 0              | 68106      |
| MSAA                            | 0         | 0          | 0         | 0         | 39430  | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 39430  | 0       | 0              | 0          |
| MSAA/Alt-Science/Social Studies | 0         | 0          | 15087     | 0         | 110944 | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 110924 | 83458   | 56907          | 0          |
| TNReady                         | 0         | 0          | 0         | 0         | 406710 | 0         | 0          | 0           | 0        | 0                 | 0                  | 0                   | 405732 | 270697  | 216593         | 0          |

* Looks like I need to break this table down a bit further to aggregate by test and then subject. The data are noisy and I will filter by the aggregated scores reported in each school to account for that. The general heuristic is that the majority of students tend to take these tests in a specific grade.  However, some students take the tests in earlier or later grades than their peers.  In these cases, there can be much grade-level suppression.  Therefore, aggregatons are much less suppressed than grade-level reports.

### 05/24/23

* [X] Drop `MSAA` & `MSAA/Alt`
* [X] Filter to `Grade = 'All Grades`

* When dropping `MSAA` tests, the resulting dataframe contains **1,919,766** rows. This removes **456,180** rows from the dataset.
* Using the aggregate of `All Grades` , the data now represent the average subject proficiency for each school. The dataframe was reduced to **525,044** rows
* I think I maybe able to salvage more demographic information by performing some simple subtraction.  The data wont have as many dimensions as the non-suppressed data, but maybe I can still compare Non-Proficient vs Proficeient.

### 05/25/23

* [X] Drop `pct_approaching`, `pct_met_expectations`, `pct_exceeded_expectations` achievement categories.
* [X] Drop `*`  There is no way to infer the proficiency of student_groups that do not have at-least 10 valid tests.

* I honestly think that the data will be easier to work with if I can make expectations a binary classifier.

  * If a student_group's proficiency scores for a building are suppressed due to achievement outliers, the `pct_met_exceeded` is still reported.  If I subtract that number from 1, I will be left with the percent that did not meet expectations.  I cannot infer categories inbetween, but I can make a simple "pass/fail" comparison.
  * There is nothing I can do about `*`  because it suggests that enrollment (or number of valid tests ) of of that student_group is less than 10 at the individual school.
* Assumptions really being challenged here.  Not so simple to calculate missing values without a little extra logic.  Apparrently there can be `**` in some of the `pct_met_exceeded`.  There were **44,454** entries where `pct_met_exceeded` was suppressed.  If filtered to "All Students" `student_group`, **2,405** entries are `**` suppressed.

  * I know that I'm going to have to remove the fully suppressed `**` data from my main dataframe, But I'm going to capture it into a separate df for some light analysis.

### 05/27/23

* Spoke with Neda.  Lots of encouragement.  I'm stoked!  I'm almost ready to joing NCES data
* I am going to merge geo data before splitting off the fully suppressed data.  I think it would be good to have geographic data as a part of my full suppression information.

### 05/28/23

- Researched datasets From NCES.  Pulled Common Core data files for each year as well.  The data isn't as nice for getting some of the descriptive labels that I thought I could . . . but it does save me a lot of work in not haveing to use an API to geoencode addresses.

  - Looks like **geoencoding** will not be needed for this project as NCES provides lat/long and addressess for all schools in a given year.  They also include shapefiles for both school and district boundaries.
  - Created the following data directory structure

    - Common Core Data
    - Geoencode - School
    - Geoencode - LEA
- No shape files for 2018.  I wonder what the best way to deal with that would be?

### 05/29/23

- Merged all CCD data from NCES for the years in quesiton.  Set encoding to `latin_1` and low memory to `False` because Pandas wanted to encode as `utf-8` and `us_ascii` did not work either, Though that's what the original files were encoded in.
  - Dropped all schools except those in Tennessee
- . . . Then I took a long hard look at the data that I needed to merge and what else I wanted to include.  I poked around the NCES website and found their ElSi table generator and I decided to generate my own custom file per year.  This keeps me from having to clean the CCD data of what I don't need and allows me to avoid having to merge the geoencode data and other additional data.
- And that's what I get for trying to be clever.  Using the tool to grab one year at a time and then merging resulted in unneccisary complication and, more critically, misaligned datasets.  I changed approach instead to dumping all years in wide form and translating to long form.  The data looks fully merged and free from most human error.

### 05/30/23

* [X] Reorder df cols for assessment and elsi data
* [X] merge assessment and elsi
* [X] deal with the nan values that resulted from the merging
* [X] Split off `**` suppressed data.  Put it in its own pkl to avoid overwriting it.  I cannot convert proficiencies to numbers with `**` still in the `pct_met_exceeded` rows.

* Fixed naming and order of columns in NCES Data.
* Exported NCES data for merging with school-level testing data data.

  * I exported this as elsi_clean.pkl 🥒 to my school_based folder.
* Merged the dataframes.  It appears that **693** rows from the assessment dataset went unmatched when merging.
* Spoke with Rohit, he gave me some good info.  He always has the coolest hats 🛹

  * [https://gis.stackexchange.com/questions/113799/reading-shapefile-in-python](https://gis.stackexchange.com/questions/113799/reading-shapefile-in-python)
  * import geopandas as gpd
  * shapefile = gpd.read_file("shapefile.shp")
  * print(shapefile)
* Looks like there are **17 schools** that are managed by the state or do not appear more than once before the year 2021.  The vast majority of the reported scores are `**` supressed.  These will be removed from the **assessments df**.  However, they will be a part of my fully suppressed scores analysis.
* **44,454** scores across all years, schools, and subjects were fully suppressed in the data they were removed.
* **335,452** non-suppressed datapoints are now available in the dataset.

### 05/31/23

* [X] make a new column `not_met` elss of performance
* [X] Remove assessments that only apear in one year
* [X] Add subject_level column which associates each type of test with its subject content( e.g., literacy, numeracy, science, and social studies)
* [X] Create mapping dictionary to apply content_area labels to subjects.

* I added added a calculated column,  `not_met`. This will allow me to see the total percentage of student_groups that did not meet expectations, regard.
* Made a pivot table to look at average state-wide proficiencies for each subject each year, grouped by test type.
* My new subject_area column was a success.  I created a dictionary and mapped it to associate each test type with a subject area descriptor.
* I made some cool plotly visuals while I was waiting and entire eternity for conda to install GeoPandas
* Exported prepped dataset to be used in EDA notebooks

### 06/01/23

* [X] Create Plotly Notebook
* [X] Create EDA Notebook
* [ ] Briefly analyze  `**` suppressed data.

* I made a new EDA and Plotly notebook.  I'm ready to begin diving deeper into the data and to visualize it.
