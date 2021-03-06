import pandas as pd
import numpy as np
#filters mapc dataset by land use code, poly-type, and lots with buildings


def convertZip(zipStr):
    """
        convert '2138.0' to '02138'
        """
    zipCode = ''
    if zipStr is not None:
        if '.' in zipStr:
            zipCode = '0' + zipStr[:4]
    return zipCode

def filter_luc(df):
  """filters by land use codes affiliated with MA state agencies
  """
  accepted_codes = ['910','911','912','913','914','915','916','917','918','919','920','921','922',
         '923','924','925','926','927','928','929','970','971','972','973','974','975']
  
  return df[df['luc_1'].isin(accepted_codes) | df['luc_2'].isin(accepted_codes) | \
          df['luc_adj_1'].isin(accepted_codes)| \
          df['luc_adj_2'].isin(accepted_codes)]


def filter_poly_typ(dataframe):
  # filter out data only with poly_typ equal to FEE or TAX
  accepted_codes = ['FEE', 'TAX']

  return dataframe[dataframe['poly_typ'].isin(accepted_codes)]



def filter_bldg(dataframe):
  '''
  Filter on related columns that indicate whether building(s) are present on the land parcel.
  Removes rows that correspond to land parcels that do not contain buildings.
  Ziba specified:
      bldg_value - for condos, generally includes land value
      bldg_area - may include garages, stairwells, basements, and other uninhabitable areas.
      bldgv_psf - building value $ per sq foot
  Additional:
      sqm_bldg - parcel area estimated to be covered by a building (sq meters)
      pct_bldg - % parcel area estimated to be covered by a building
  '''
  return dataframe.query('bldg_value >0 | \
                         bldg_area > 0  | \
                         bldgv_psf > 0  | \
                         sqm_bldg  > 0  | \
                         pct_bldg  >0')

                   
def apply_all(dataframe):
    dataframe = filter_luc(dataframe)
    dataframe = filter_poly_typ(dataframe)
    dataframe = dataframe[dataframe['owner_name'].str.endswith('HOUSING AUTHORITY',na=False)==False]
    
    #clean zipcode
    addressZip = dataframe['addr_zip']
    addressZip = addressZip.astype(str)
    addressZip = addressZip.apply(convertZip)
    dataframe['addr_zip'] = addressZip
    
    dataframe.to_csv('usable_state_land.csv')
    return dataframe



