# COVID:  School-level learning impact analysis

## Executive Summary

This project aims to analyze the impact of learning loss and the effectiveness of learning loss recovery interventions for individual schools within all Tennessee districts. The motivation for this project stems from the observation that, contrary to my personal expectations, achievement metrics in some districts continued to decline during the post-COVID learning recovery phase. I hope that by measuring the rate of improvement (ROI) for each school I will be able to discern features in individual school performance that could be predictive of a district’s performance. Geospatial data and visualizations will be used to help users explore the data through a dashboard developed using the Plotly Dash package in Python.

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
* I was able to merge 18,19, and 2021.  It looks like in 2018 that `enrolled`, `tested`, and `participation_rate` data is missing.
* I am **EXCITED** that where `grade =  All Grades` ,  `student_group` does seem to yeild some subpopulation data (gender, ethnicity, english language learner, students with disabilities, etc.) at the scool level!
* It looks like there may be some solid charter school information in some of the later datasets.  I wonder if there are noticable differences between the two groups?  I'd love to dig deeper.  I'll keep in in my back pocket for later.
