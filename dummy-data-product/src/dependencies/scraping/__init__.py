import pandas as pd
import datacommons as dc
from pathlib import Path

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
    
    def scraper(country_iso_code, feature_no):
        
        # create a directory
        DATA_DIR = Path('data') / country_iso_code
        DATA_DIR.mkdir(exist_ok=True)
        
        feature_name = feature_mapping[feature_no]
        c_country = 'country/'+country_iso_code
        
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

        # save dataframe  ... !
        df_sort.to_csv(str(DATA_DIR)+'/'+feature_name.lower()+'.csv', index=False)
        print("Done for country --",country_iso_code,'-- for feature --',feature_name,"--")
