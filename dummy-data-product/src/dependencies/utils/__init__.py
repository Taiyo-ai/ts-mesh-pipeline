#defines libraries
import pandas as pd
import datacommons as dc
from pathlib import Path
import json

# defines mapping for feature
feature_mapping = {}
feature_mapping[1] = 'Count_MedicalConditionIncident_COVID_19_PatientInICU'
feature_mapping[2] = 'Count_MedicalConditionIncident_COVID_19_PatientHospitalized'
feature_mapping[3] = 'Count_MedicalConditionIncident_COVID_19_PatientOnVentilator'
feature_mapping[4] = 'CumulativeCount_MedicalConditionIncident_COVID_19_ConfirmedOrProbableCase'
feature_mapping[5] = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientDeceased'
feature_mapping[6] = 'CumulativeCount_MedicalConditionIncident_COVID_19_ConfirmedCase'
feature_mapping[7] = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientHospitalized'
feature_mapping[8] = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientRecovered'
feature_mapping[9] = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientInICU'
feature_mapping[10] = 'CumulativeCount_MedicalConditionIncident_COVID_19_PatientOnVentilator'
feature_mapping[11] = 'DaysSinceLastReportedCase_MedicalConditionIncident_COVID_19_ConfirmedCase'
feature_mapping[12] = 'IncrementalCount_MedicalConditionIncident_COVID_19_ConfirmedCase'
feature_mapping[13] = 'IncrementalCount_MedicalConditionIncident_COVID_19_ConfirmedOrProbableCase'
feature_mapping[14] = 'IncrementalCount_MedicalConditionIncident_COVID_19_PatientDeceased'
feature_mapping[15] = 'Count_MedicalTest_ConditionCOVID_19_Pending'
feature_mapping[16] = 'CumulativeCount_MedicalTest_ConditionCOVID_19'
feature_mapping[17] = 'CumulativeCount_MedicalTest_ConditionCOVID_19_Negative'
feature_mapping[18] = 'CumulativeCount_MedicalTest_ConditionCOVID_19_Positive'
feature_mapping[19] = 'IncrementalCount_MedicalTest_ConditionCOVID_19'
feature_mapping[20] = 'IncrementalCount_Vaccine_COVID_19_Administered'
feature_mapping[21] = 'CumulativeCount_Vaccine_COVID_19_Administered'
feature_mapping[22] = 'Covid19MobilityTrend_GroceryStoreAndPharmacy'
feature_mapping[23] = 'Covid19MobilityTrend_LocalBusiness'
feature_mapping[24] = 'Covid19MobilityTrend_Park'
feature_mapping[25] = 'Covid19MobilityTrend_Residence'
feature_mapping[26] = 'Covid19MobilityTrend_TransportHub'
feature_mapping[27] = 'Covid19MobilityTrend_Workplace'


class Scraper:
    # data, country

    def scraper(self, c_country, feature_name):
        #call datacommon API 
        series_data = dc.get_stat_series(c_country, feature_name)
        
        # create a dictionary
        keys = series_data.keys()
        values = series_data.values()
        data = {'dates':keys, feature_name.lower():values}
        
        # convert dictionary into data frame
        df = pd.DataFrame(data)
        df_sort = df.sort_values('dates')

        # reset the index to the current index order
        df_sort.reset_index(drop=True, inplace=True)

        return df_sort
    
    def generate_meta_data(self, start_date, end_date, feature_name, country_iso_code=None):
        country_df = pd.read_csv('country_code.csv')
        country_name = country_df.loc[country_df['code'] == country_iso_code, 'country'].values[0]
        
        json_dir = Path('meta_data')/country_iso_code
        json_dir.mkdir(exist_ok=True)
        iso_code = country_iso_code


        json_file = {
            'Identifier':{
            'aug_id':country_iso_code.lower()+ '_' +feature_name.lower(),
            'original_id':country_iso_code.lower()+ '_' +feature_name.lower(),
            'sample_frequency': 'Weekly',
            },
            'Basic Specs':{
                'name':country_iso_code.lower()+ '_' +feature_name.lower(),
                'description':'it is data of {0} country for the features of {1}'.format(country_name, feature_name),
                'units':'Real numbers',
                'source': 'datacommons.org'
            },
            'Links and URLs' : {'url':'https://www.datacommons.org/tools/timeline'},
            'Sector/Subsector or Industry Type':{
                'domain' : 'Health',
                'subdomain':'epidemic / covid 19',
                'tags' :'virus, pandemic, vaccination, variant, mask, lockdown, quarantine, social distancing, immunity, Delta, booster, PCR test, contact tracing, ventilator, hospitalization, outbreak, spread, asymptomatic, herd immunity, SARS-CoV-2'
            },
            'Critical Dates':{
                'timestamps' : {'start date' : start_date, 'end_date': end_date},
            },
            'Location Information':{
                'country':{
                    'country_name':country_name, 
                    'country_code':country_iso_code
                    }
            }
        }
        
        with open('meta_data/' + iso_code + '/' + feature_name  + '.json', 'w') as f:
            json.dump(json_file, f, indent=4)
        print("meta data generated successfully ... !")

    def scraper_a_s(self, country_iso_code):
        '''
            input: country_iso_code - take three letter code of a country
            output: will save a CSV file contain all the feature of specific country
        '''
        data_dir = Path('data')/country_iso_code
        data_dir.mkdir(exist_ok=True)


        for i in range(1,27):

            c_country = 'country/'+country_iso_code
            feature_name = feature_mapping[i]
            df_sort = self.scraper(c_country, feature_name)

            start_date = df_sort['dates'].min()
            end_date = df_sort['dates'].max()

            # save dataframe  ... !
            df_sort.to_csv(str(data_dir)+'/'+feature_name.lower()+'.csv', index=False)
            print("Done for country --",country_iso_code,'-- for feature --',feature_name,"--")

            self.generate_meta_data(start_date, end_date, feature_name, country_iso_code)
            
    def scraper_s_a(self, feature_no):
        '''
            input: feature_no - digit which represent particular features
            output: will save number of CSV file of specific feature with different countries folders
        '''
        feature_name = feature_mapping[feature_no]
        df = pd.read_csv('country_code.csv')
        for country_code in df['code']:
        
            data_dir = Path('data')/country_code
            data_dir.mkdir(exist_ok=True)
            c_country = 'country/'+country_code

            df_sort = self.scraper(c_country, feature_name)
            
            # save dataframe  ... !
            df_sort.to_csv(str(data_dir)+'/'+feature_name.lower()+'.csv', index=False)
            print("Done for country --",country_code,'-- for feature --',feature_name,"--")

            start_date = df_sort['dates'].min()
            end_date = df_sort['dates'].max()

            self.generate_meta_data(start_date, end_date, feature_name, country_code)

    
    def scraper_a_a(self):
        '''
            Input: no input required
            output: will save number of CSV of number of feature to each country
        '''
        
        df = pd.read_csv('country_code.csv')

        for country_code in df['code']:    
            data_dir = Path('data')/country_code
            data_dir.mkdir(exist_ok=True)
  
            for i in range(1,27):         

                c_country = 'country/'+country_code
                feature_name = feature_mapping[i] 

                df_sort = self.scraper(c_country, feature_name)

                # save dataframe  ... !
                df_sort.to_csv(str(data_dir)+'/'+feature_name.lower()+'.csv', index=False)
                print("Done for country --",country_code,'-- for feature --',feature_name,"--")


                start_date = df_sort['dates'].min()
                end_date = df_sort['dates'].max()
                self.generate_meta_data(start_date, end_date, feature_name, country_code)
