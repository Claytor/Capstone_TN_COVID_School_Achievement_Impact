# Executive Summary

This project aims to analyze the impact of learning loss and the effectiveness of learning loss recovery interventions for individual schools within all Tennessee districts. The motivation for this project stems from the observation that, contrary to my personal expectations, achievement metrics in some districts continued to decline during the post-COVID learning recovery phase. I hope that by measuring the rate of improvement (ROI) for each school I will be able to discern features in individual school performance that could be predictive of a district’s performance. Geospatial data and visualizations will be used to help users explore the data through a dashboard developed using the Plotly Dash package in Python.

# Motivation

When analyzing district-wide achievement data, I observed that achievement metrics in some school districts continued to decline during the post-COVID learning recovery phase. This was contrary to my original expectations and prompted an interest in exploring individual school achievement scores to identify any discernible features that could be indicative of continued loss or recovery. This project seeks to understand the extent of learning loss and recovery efforts in individual schools within all Tennessee districts, taking into account the significant disruption to education caused by the COVID-19 pandemic.

# Data Question

Given a school's learning loss impact compared to its previous pre-pandemic TNReady assessments, what was the rate of improvement/loss given learning loss interventions? Are there any discernible features in achievement scores for individual schools that could be indicative of continued loss or recovery for the district?

# Minimum Viable Product

The MVP will be a reactive dashboard visualization tool that allows users to explore changes in achievement metrics before, during, and after the onset of the Coronavirus pandemic. It will provide functionality for users to compare assessment metrics across schools and explore how certain student demographics were impacted by learning loss and recovery efforts. Additionally, geocoding techniques using Google Maps API will be employed to convert individual school addresses to latitude and longitude, enabling the use of geospatial data in the analysis and visualization.

# Schedule (through 6/15/2023)

| Milestone                                       | Completion Date |
| ----------------------------------------------- | --------------- |
| Primary Data Acquired and Merged (TDOE and Geo) | 05/23/23        |
| Supplaementary Dataset Acquired                 | 05/27/23        |
| Data Cleaned and Prepped                        | 06/01/23        |
| Plotly Dash wireframed and beta                 | 06/03/23        |
| MVP Reached                                     | 06/06/23        |
| Presentation Drafted                            | 06/08/23        |
| Present Finished Project                        | 06/10/23        |

# Data Sources

- 5 years of Annual school TNReady results datasets for each Tennessee public school, provided by the Tennessee Department of Education (TDOE).
- Tennessee School Directory, also provided by TDOE, which includes mailing addresses, regions, and school districts for all active public schools in Tennessee.
- Other publicly available Tennessee school data as needed.

# Known Issues and Challenges

1. Aligning disparate datasets
   - Thoroughly explore datasets' structure and content.
   - Use consistent data cleaning and transformation techniques.
   - Automate repetitive tasks with functions or reusable code blocks.
2. Converting school addresses to latitude and longitude
   - Study Google Maps API geocoding functionality.
   - Create a function to handle API requests and manage rate limits.
   - Test the function on a smaller subset before processing the entire dataset.
   - Store converted coordinates separately to avoid re-processing.
3. Determining usable demographic data
   - Conduct exploratory data analysis (EDA) on demographic variables.
   - Assess the relevance of each variable to the research question.
   - Obtain or derive additional demographic data if needed.
   - Consult with domain experts or stakeholders as necessary.
