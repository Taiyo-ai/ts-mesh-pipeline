# Data Ingestion Pipeline Template

This repository consists of boilerplate folder structure to write and organize your scripts for a data ingestion pipeline

## Folder Structure
The tree diagram below represents a general file structure

```
|--- data_source_name                      
     |--- deploy                            # pipeline orchestration and configuration of DAGs
     |    |---dev              
     |    |---prod
     |--- src
          |--- dependencies
          |    |--- cleaning
          |    |    |--- __init__.py
          |    |    |--- cleaner.py         ## Cleaning script here
          |    |--- geocoding
          |    |    |--- __init__.py
          |    |    |--- geocoder.py        ## Geocoding script here
          |    |--- scraping                # This folder contains all data harvesting scipts
          |    |    |--- __init__.py
          |    |    |--- scraper.py         ## Harvesting script here
          |    |--- standardization
          |    |    |--- __init__.py
          |    |    |--- standardizer.py    ## Standardization script here
          |    |--- utils                   # Utility and helper scipts to be placed here
          |         |--- __init__.py
          |--- .dockerignore
          |--- Dockerfile
          |--- client.py                    # Master script that connects all the above blocks
          |--- requirements.txt
```

## Different Blocks of ETL pipeline
1. Scraping/Data Harvesting
    - Contains all the scripts that extracts metadata and raw data to be processed further from database, websites, webservices, APIs, etc.
2. Cleaning
    - Treatment missing fields and values
    - Treatment of duplicate entries
    - Convert country codes to `ISO 3166-1 alpha3` i.e. 3 letter format
    - Identify region name and region code using the country code
3. Geocoding
    - Based upon location information available in the data
        - Location label
        - Geo-spatial coordinates
    - Missing field can be found either by using geocoding or reverse geocoding with max precision available
4. Standardization
    - Fields to be strictly in **lower snake casing**
    - Taking care of data types and consistency of fields
    - Standardize fields like `sector`, `subsector`, `domain`, `subdomain`
    - Renaming of field names as per required standards
    - Manipulation of certain fields and values to meet up the global standards for presentation, analytics and business use of data
    - Refer to the [Global Field Standards](https://docs.google.com/spreadsheets/d/1Zyn0qLI1JdZD-3EQdvpi7twzUUy3vExg80SL3CK6sWI/edit#gid=0) spreadsheet for the standards to be followed

### Note
> Depending upon what fields are already available in the data `GEOCODING` step may or may not be required.

> It is recommended that the resultant data after each and every step is stored and backed up for recovery purpose.

> Apart from the primary fields listed down in [Global Field Standards](https://docs.google.com/spreadsheets/d/1Zyn0qLI1JdZD-3EQdvpi7twzUUy3vExg80SL3CK6sWI/edit#gid=0) spreadsheet, there are several other secondary fields that are to be scraped; given by the data provider for every document that holds significant business importance.

## Submission and Evaluation
- For assignment submission guidelines and evaluation criteria refer to the [WIKI](https://github.com/Taiyo-ai/ts-mesh-pipeline/wiki) documentation

---
Copyright © 2021 Taiyō.ai Inc.



### This is a web scrapper to fetch data from https://www.datacommons.org/tools/timeline
with the help of this web scrapper user can fetch 27 kinds of time series data related to covid 19 of any country.
it ask feature {feture_mapping} and country_name in which user took intersting. 

### to run the web_scraper

```diff
    there are four argument
        -c    take country name in ISO format
        -ac   take any string, it will fetch information for every country provided at datacommons
        -f    take feature number which is shown below 
        -af   take any string, it will fetch information for all feature of selected country

    one can use -c / -ac at a time
    one can use -f / -af at a time

    sample query : when you inside the "src" folder

        1. python3 client.py -c USA -f 1
            will return a csv file contain USA data of 'Count_MedicalConditionIncident_COVID_19_PatientInICU' 
        2. python3 client.py -ac yes -f 16
            will return number of csv file contain 16th feature of all countries

```

### feature mapping:
```diff
1 = 'Count_MedicalConditionIncident_COVID_19_PatientInICU'  
2 = 'Count_MedicalConditionIncident_COVID_19_PatientHospitalized'
3 = 'Count_MedicalConditionIncident_COVID_19_PatientOnVentilator'
4 = 'CumulativeCount_MedicalConditionIncident_COVID_19_ConfirmedOrProbableCase'
5 = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientDeceased'
6 = 'CumulativeCount_MedicalConditionIncident_COVID_19_ConfirmedCase'
7 = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientHospitalized'
8 = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientRecovered'
9 = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientInICU'
10 = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientOnVentilator'
11 = 'DaysSinceLastReportedCase_MedicalConditionIncident_COVID_19_ConfirmedCase'
12 = 'IncrementalCount_MedicalConditionIncident_COVID_19_ConfirmedCase'
13 = 'IncrementalCount_MedicalConditionIncident_COVID_19_ConfirmedOrProbableCase'
14 = 'IncrementalCount_MedicalConditionIncident_COVID_19_PatientDeceased'
15 = 'Count_MedicalTest_ConditionCOVID_19_Pending'
16 = 'CumulativeCount_MedicalTest_ConditionCOVID_19'
17 = 'CumulativeCount_MedicalTest_ConditionCOVID_19_Negative'
18 = 'CumulativeCount_MedicalTest_ConditionCOVID_19_Positive'
19 = 'IncrementalCount_MedicalTest_ConditionCOVID_19'
20 = 'IncrementalCount_Vaccine_COVID_19_Administered'
21 = 'CumulativeCount_Vaccine_COVID_19_Administered'
22 = 'Covid19MobilityTrend_GroceryStoreAndPharmacy'
23 = 'Covid19MobilityTrend_LocalBusiness'
24 = 'Covid19MobilityTrend_Park'
25 = 'Covid19MobilityTrend_Residence'
26 = 'Covid19MobilityTrend_TransportHub'
27 = 'Covid19MobilityTrend_Workplace'
```



Country Code Reference:
```diff
Afghanistan										AFG
Albania										ALB
Algeria										DZA
American Samoa										ASM
Andorra										AND
Angola										AGO
Anguilla										AIA
Antarctica										ATA
Antigua and Barbuda										ATG
Argentina										ARG
Armenia										ARM
Aruba										ABW
Australia										AUS
Austria										AUT
Azerbaijan										AZE
Bahamas (the)										BHS
Bahrain										BHR
Bangladesh										BGD
Barbados										BRB
Belarus										BLR
Belgium										BEL
Belize										BLZ
Benin										BEN
Bermuda										BMU
Bhutan										BTN
Bolivia (Plurinational State of)										BOL
Bonaire, Sint Eustatius and Saba										BES
Bosnia and Herzegovina										BIH
Botswana										BWA
Bouvet Island										BVT
Brazil										BRA
British Indian Ocean Territory (the)										IOT
Brunei Darussalam										BRN
Bulgaria										BGR
Burkina Faso										BFA
Burundi										BDI
Cabo Verde										CPV
Cambodia										KHM
Cameroon										CMR
Canada										CAN
Cayman Islands (the)										CYM
Central African Republic (the)										CAF
Chad										TCD
Chile										CHL
China										CHN
Christmas Island										CXR
Cocos (Keeling) Islands (the)										CCK
Colombia										COL
Comoros (the)										COM
Congo (the Democratic Republic of the)										COD
Congo (the)										COG
Cook Islands (the)										COK
Costa Rica										CRI
Croatia										HRV
Cuba										CUB
Curaçao										CUW
Cyprus										CYP
Czechia										CZE
Côte d'Ivoire										CIV
Denmark										DNK
Djibouti										DJI
Dominica										DMA
Dominican Republic (the)										DOM
Ecuador										ECU
Egypt										EGY
El Salvador										SLV
Equatorial Guinea										GNQ
Eritrea										ERI
Estonia										EST
Eswatini										SWZ
Ethiopia										ETH
Falkland Islands (the) [Malvinas]										FLK
Faroe Islands (the)										FRO
Fiji										FJI
Finland										FIN
France										FRA
French Guiana										GUF
French Polynesia										PYF
French Southern Territories (the)										ATF
Gabon										GAB
Gambia (the)										GMB
Georgia										GEO
Germany										DEU
Ghana										GHA
Gibraltar										GIB
Greece										GRC
Greenland										GRL
Grenada										GRD
Guadeloupe										GLP
Guam										GUM
Guatemala										GTM
Guernsey										GGY
Guinea										GIN
Guinea-Bissau										GNB
Guyana										GUY
Haiti										HTI
Heard Island and McDonald Islands										HMD
Holy See (the)										VAT
Honduras										HND
Hong Kong										HKG
Hungary										HUN
Iceland										ISL
India										IND
Indonesia										IDN
Iran (Islamic Republic of)										IRN
Iraq										IRQ
Ireland										IRL
Isle of Man										IMN
Israel										ISR
Italy										ITA
Jamaica										JAM
Japan										JPN
Jersey										JEY
Jordan										JOR
Kazakhstan										KAZ
Kenya										KEN
Kiribati										KIR
Korea (the Democratic People's Republic of)										PRK
Korea (the Republic of)										KOR
Kuwait										KWT
Kyrgyzstan										KGZ
Lao People's Democratic Republic (the)										LAO
Latvia										LVA
Lebanon										LBN
Lesotho										LSO
Liberia										LBR
Libya										LBY
Liechtenstein										LIE
Lithuania										LTU
Luxembourg										LUX
Macao										MAC
Madagascar										MDG
Malawi										MWI
Malaysia										MYS
Maldives										MDV
Mali										MLI
Malta										MLT
Marshall Islands (the)										MHL
Martinique										MTQ
Mauritania										MRT
Mauritius										MUS
Mayotte										MYT
Mexico										MEX
Micronesia (Federated States of)										FSM
Moldova (the Republic of)										MDA
Monaco										MCO
Mongolia										MNG
Montenegro										MNE
Montserrat										MSR
Morocco										MAR
Mozambique										MOZ
Myanmar										MMR
Namibia										NAM
Nauru										NRU
Nepal										NPL
Netherlands (the)										NLD
New Caledonia										NCL
New Zealand										NZL
Nicaragua										NIC
Niger (the)										NER
Nigeria										NGA
Niue										NIU
Norfolk Island										NFK
Northern Mariana Islands (the)										MNP
Norway										NOR
Oman										OMN
Pakistan										PAK
Palau										PLW
Palestine, State of										PSE
Panama										PAN
Papua New Guinea										PNG
Paraguay										PRY
Peru										PER
Philippines (the)										PHL
Pitcairn										PCN
Poland										POL
Portugal										PRT
Puerto Rico										PRI
Qatar										QAT
Republic of North Macedonia										MKD
Romania										ROU
Russian Federation (the)										RUS
Rwanda										RWA
Réunion										REU
Saint Barthélemy										BLM
Saint Helena, Ascension and Tristan da Cunha										SHN
Saint Kitts and Nevis										KNA
Saint Lucia										LCA
Saint Martin (French part)										MAF
Saint Pierre and Miquelon										SPM
Saint Vincent and the Grenadines										VCT
Samoa										WSM
San Marino										SMR
Sao Tome and Principe										STP
Saudi Arabia										SAU
Senegal										SEN
Serbia										SRB
Seychelles										SYC
Sierra Leone										SLE
Singapore										SGP
Sint Maarten (Dutch part)										SXM
Slovakia										SVK
Slovenia										SVN
Solomon Islands										SLB
Somalia										SOM
South Africa										ZAF
South Georgia and the South Sandwich Islands										SGS
South Sudan										SSD
Spain										ESP
Sri Lanka										LKA
Sudan (the)										SDN
Suriname										SUR
Svalbard and Jan Mayen										SJM
Sweden										SWE
Switzerland										CHE
Syrian Arab Republic										SYR
Taiwan (Province of China)										TWN
Tajikistan										TJK
Tanzania, United Republic of										TZA
Thailand										THA
Timor-Leste										TLS
Togo										TGO
Tokelau										TKL
Tonga										TON
Trinidad and Tobago										TTO
Tunisia										TUN
Turkey										TUR
Turkmenistan										TKM
Turks and Caicos Islands (the)										TCA
Tuvalu										TUV
Uganda										UGA
Ukraine										UKR
United Arab Emirates (the)										ARE
United Kingdom of Great Britain and Northern Ireland (the)										GBR
United States Minor Outlying Islands (the)										UMI
United States of America (the)										USA
Uruguay										URY
Uzbekistan										UZB
Vanuatu										VUT
Venezuela (Bolivarian Republic of)										VEN
Viet Nam										VNM
Virgin Islands (British)										VGB
Virgin Islands (U.S.)										VIR
Wallis and Futuna										WLF
Western Sahara										ESH
Yemen										YEM
Zambia										ZMB
Zimbabwe										ZWE
Åland Islands										ALA
```


<!-- 
recruitment asignment by manish kumar

created a webscraper to fetch the covid 19 data of all the countries, from datacommons.org. -->