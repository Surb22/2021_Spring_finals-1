"""
IS 597: Final Project
Team members:
Shubhda Sharma - shubhda2
Surbhi Bhargava - surbhib2

"""

import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_name: str, hypothesis_flag) -> pd.DataFrame:
    """
    Load file containing details of LCA and retain only useful columns.
    Replace the column names with meaningful heads.
    :param file_name: The path to the LCA data file.
    :param hypothesis_flag: Flag to differentiate between hypothesis one and three.
    :return: Dataframe with useful columns from the LCA data.
    """

    col_required = ['STATUS', 'CASE_STATUS', 'LCA_CASE_EMPLOYER_NAME', 'EMPLOYER_NAME', 'TOTAL_WORKERS',
                    'TOTAL_WORKER_POSITIONS',
                    'LCA_CASE_WORKLOC1_STATE', 'VISA_CLASS', 'LCA_CASE_NUMBER', 'LCA_CASE_NAICS_CODE', 'NAICS_CODE',
                    'TOTAL WORKERS', 'WORKSITE_STATE', 'WORKSITE_STATE_1', 'CASE_NUMBER', 'NAIC_CODE']

    df = pd.read_csv(filepath_or_buffer=file_name, usecols=lambda x: x in col_required,
                     dtype={'LCA_CASE_NAICS_CODE': 'str',
                            'NAICS_CODE': 'str',
                            'NAIC_CODE': 'str',
                            },
                     low_memory=False, encoding='ISO-8859-1')

    df = df.rename(
        columns={'LCA_CASE_NUMBER': 'CASE_NUMBER', 'CASE_STATUS': 'STATUS', 'LCA_CASE_EMPLOYER_NAME': 'EMPLOYER_NAME',
                 'TOTAL_WORKER_POSITIONS': 'TOTAL_WORKERS', 'LCA_CASE_WORKLOC1_STATE': 'WORKSITE_STATE',
                 'LCA_CASE_NAICS_CODE': 'NAICS_CODE', 'WORKSITE_STATE_1': 'WORKSITE_STATE', 'NAIC_CODE': 'NAICS_CODE',
                 'TOTAL WORKERS': 'TOTAL_WORKERS'})
    if hypothesis_flag == False:
        df['STATUS'] = df["STATUS"].str.upper()
        df = df[(df['STATUS'] == 'CERTIFIED') & (df['VISA_CLASS'] == 'H-1B')]
        df['NAICS_CODE'] = df['NAICS_CODE'].str[:2]
        return df
    elif hypothesis_flag == True:
        df['STATUS'] = df["STATUS"].str.upper()
        df['NAICS_CODE'] = df['NAICS_CODE'].str[:2]
        df = df[df['VISA_CLASS'] == 'H-1B']
        return df


def sector_range(row):
    """
    Used to split the NAICS sector codes containing "-"
    :param row: Each row of the dataframe
    :return: Returns the numbers after being split and all the values lying between those numbers
    >>> sector_range([13,15])
    [13, 14, 15]
    """

    if isinstance(row, list) and len(row) > 1:
        return list(range(int(row[0]), int(row[1]) + 1))
    elif isinstance(row, list):
        return row[0]


def read_sector_data(filename: str) -> pd.DataFrame:
    """
    Load the NAICS data file, retaining only the most useful columns & rows.
    Change the layout for a few rows to make the data inclusive of all codes.
    :param filename: The path to the NAICS code data file.
    :return: Dataframe containing NAICS codes and their corresponding sectors.

    >>> read_sector_data('2017_NAICS_Structure_Summary_Table.csv')
        Sector                                               Name
    1       11         Agriculture, Forestry, Fishing and Hunting
    2       21      Mining, Quarrying, and Oil and Gas Extraction
    3       22                                          Utilities
    4       23                                       Construction
    5       31                                      Manufacturing
    5       32                                      Manufacturing
    5       33                                      Manufacturing
    6       42                                    Wholesale Trade
    7       44                                       Retail Trade
    7       45                                       Retail Trade
    8       48                     Transportation and Warehousing
    8       49                     Transportation and Warehousing
    9       51                                        Information
    10      52                              Finance and Insurance
    11      53                 Real Estate and Rental and Leasing
    12      54   Professional, Scientific, and Technical Services
    13      55            Management of Companies and Enterprises
    14      56  Administrative and Support and Waste Managemen...
    15      61                               Educational Services
    16      62                  Health Care and Social Assistance
    17      71                Arts, Entertainment, and Recreation
    18      72                    Accommodation and Food Services
    19      81      Other Services (except Public Administration)
    20      92                              Public Administration
    """
    sector_df = pd.read_csv(filepath_or_buffer=filename, encoding='ISO-8859-1')
    sector_df["Sector"] = sector_df["Sector"].str.split("-")
    sector_df['sector_range'] = sector_df["Sector"].apply(sector_range)
    sector_codes = sector_df['sector_range'].apply(pd.Series).reset_index().melt(id_vars='index').dropna()[
        ['index', 'value']].set_index('index')
    sector_codes_final = sector_codes.merge(sector_df['Name'], left_index=True, right_index=True, how='inner')
    sector_codes_final = sector_codes_final.rename(columns={"value": "Sector"})
    sector_codes_final['Sector'] = sector_codes_final['Sector'].astype('int8')
    return sector_codes_final


def hypothesis_one_cal(year_df, sector_data_df, yy) -> pd.DataFrame:
    """
    Merge yearly LCA data with NCAIS code data to be able to categorize LCA data according to industry sectors.
    Calculate total number of LCA approvals in a sector in an year.
    :param year_df: Yearly LCA data.
    :param sector_data_df: NCAIS code data.
    :param yy: The year of LCA data under consideration.
    :return: Dataframe containing total of LCA approvals for each sector ina year.
    """
    year_df = year_df.merge(sector_data_df, how='left', left_on='NAICS_CODE', right_on='Sector')
    stats_df = year_df.groupby(['Name'])['TOTAL_WORKERS'].sum().astype('int32').reset_index(name=yy)
    return stats_df


def hypothesis_one(file_list) -> pd.DataFrame:
    """
    Create a dataframe containing list of unique sector codes using NAICS data.
    Merge the above dataframe with yearly data of LCA approvals in each sector.

    >>> hypothesis_one(['H-1B_FY11.csv'])
                                                  Sectors    2011
    0          Agriculture, Forestry, Fishing and Hunting     452
    1       Mining, Quarrying, and Oil and Gas Extraction    1464
    2                                           Utilities     971
    3                                        Construction    1944
    4                                       Manufacturing   37772
    5                                     Wholesale Trade    4829
    6                                        Retail Trade    7660
    7                      Transportation and Warehousing    1586
    8                                         Information   25867
    9                               Finance and Insurance   17025
    10                 Real Estate and Rental and Leasing    1115
    11   Professional, Scientific, and Technical Services  488520
    12            Management of Companies and Enterprises    1204
    13  Administrative and Support and Waste Managemen...    5912
    14                               Educational Services   36065
    15                  Health Care and Social Assistance   27036
    16                Arts, Entertainment, and Recreation    1832
    17                    Accommodation and Food Services    2126
    18      Other Services (except Public Administration)    1911
    19                              Public Administration     875

    :param file_list: List of names of LCA yearly files.
    :return: Dataframe containing year wise estimates of LCA approvals in each sector.
    """
    sector_df = read_sector_data('2017_NAICS_Structure_Summary_Table.csv')
    sector_df['Sector'] = sector_df['Sector'].astype('str')
    sector_name = sector_df.Name.unique().tolist()
    plot_data_df = pd.DataFrame()
    plot_data_df['Sectors'] = sector_name
    for file in file_list:
        file_name = "data_H1B/" + file
        hypothesis_flag = False
        year_data = read_data(file_name, hypothesis_flag)
        year = '20' + file[7:9]
        stats = hypothesis_one_cal(year_data, sector_df, year)
        plot_data_df = plot_data_df.merge(stats, how='left', left_on='Sectors', right_on='Name')
        del plot_data_df['Name']
    return plot_data_df


def plot_hypothesis_one(data_plot):
    """
    To plot number of LCA approval over the years in different sectors.
    :param data_plot: Dataframe containing the total LCA approvals per year for different sectors over 2011-20.
    :return: None
    """
    data_plot = data_plot.set_index('Sectors')
    data_plot = data_plot.iloc[:, :-1]
    colors = plt.rcParams["axes.prop_cycle"]()
    fig, axes = plt.subplots(5, 4, figsize=(10, 10))
    fig.suptitle("Trend for number of LCA approvals in various sectors")
    r = 0
    c = 0
    for i, (name, row) in enumerate(data_plot.iterrows()):
        plot_df = row.to_frame()
        col = next(colors)["color"]
        plot_df.plot(ax=axes[r, c], legend=False, sharex=True, yticks=[], color=col)
        if c/4 == 0.75:
            r = r+1
            c = 0
        else:
            c = c+1
    fig.legend(loc="lower left", bbox_to_anchor=(1.0, 0.2))
    plt.show


def hypothesis_two(directory) -> pd.DataFrame:
    """
    Create a dataframe containing country wise data on H1B approvals per year from 2011-20.

    >>> hypothesis_two(['FY11NIVDetailTable.csv'])
                               Nationality     2011
    0                     China - mainland  10849.0
    1                       China - Taiwan   1705.0
    2                                India  72438.0
    3                         Korea, South   3501.0
    4                               Mexico   2647.0
    5                               Brazil   1614.0
    6                            Australia    537.0
    7                               Russia    883.0
    8   Great Britain and Northern Ireland   3660.0
    9                              Germany   1627.0
    10                              France   2069.0
    11                         Philippines   2369.0

    :param directory: File names of all the yearly H1B data files.
    :return: Dataframe containing the total H1B approvals per year for selected countries over 2011-20.
    """
    country = ['China - mainland', 'China - Taiwan', 'India', 'Korea, South', 'Mexico', 'Brazil', 'Australia',
               'Russia', 'Great Britain and Northern Ireland',
               'Germany', 'France', 'Philippines']
    sd = pd.DataFrame({"Nationality": country})
    for file in directory:
        col_name = 'Fiscal Year 20' + file[2:4]
        file_name = "data_Country/" + file
        df = pd.read_csv(filepath_or_buffer=file_name, thousands=',', dtype={'H-1B': 'float'})
        df = df.rename(columns={'Unnamed: 0': 'Visa_Country', col_name: 'Visa_Country'})
        df = df[['Visa_Country', 'H-1B']]
        col = '20' + file[2:4]
        df = df.rename(columns={'H-1B': col})
        sd = sd.merge(df, how='left', left_on='Nationality', right_on='Visa_Country')
        del sd['Visa_Country']

    return sd


def plot_hypothesis_two(data_plot):
    """
    To plot change in number of H-1B visas for different nationalities over the years.
    :param data_plot: Dataframe containing the total H1B approvals per year for selected countries over 2011-19.
    :return: None

    """
    data_plot = data_plot.set_index('Nationality')
    data_plot = data_plot.iloc[:, :-1]
    colors = plt.rcParams["axes.prop_cycle"]()
    fig, axes = plt.subplots(4, 3, figsize=(11, 11))
    fig.suptitle("Trend for number of H1-B approvals for different nationalities over the years")
    r = 0
    c = 0
    for i, (name, row) in enumerate(data_plot.iterrows()):
        plot_df = row.to_frame()
        col = next(colors)["color"]
        plot_df.plot(ax=axes[r, c], yticks=[], color=col)
        if c / 2 == 1:
            r = r + 1
            c = 0
        else:
            c = c + 1

    plt.show


def hypothesis_three(file_list) -> pd.DataFrame:
    """
     Used to return a dataframe containing Employer name along with its market capital and
     LCA approval rate from 2011-20
     :param file_list: File names of all the yearly LCA data files.
     :return: Returns a dataframe containing Employer name along with its market capital and
     LCA approval rate from 2011-20
     """
    company_df = pd.read_csv("companylist.csv", dtype={'MarketCap': 'float64'})
    final_df = pd.DataFrame()
    list_of_df = []
    for file in file_list:
        file_name = "data_H1B/" + file
        hypothesis_flag = True
        year_data = read_data(file_name, hypothesis_flag)
        year = '20' + file[7:9]
        company_df['name_lower'] = company_df['Name'].str.lower()
        year_data['EMPLOYER_NAME_lower'] = year_data['EMPLOYER_NAME'].str.lower()
        companylist_merged_df = year_data.merge(company_df, left_on='EMPLOYER_NAME_lower', right_on='name_lower')
        companylist_merged_df_certified = pd.DataFrame()
        companylist_merged_df_total = pd.DataFrame()
        companylist_merged_df_total = companylist_merged_df.groupby(['EMPLOYER_NAME', 'MarketCap'])[
            'TOTAL_WORKERS'].sum().reset_index(name="TOTAL_WORKERS_OVERALL")
        companylist_merged_df_certified = \
        companylist_merged_df[companylist_merged_df['STATUS'] == 'CERTIFIED'].groupby(['EMPLOYER_NAME', 'MarketCap'])[
            'TOTAL_WORKERS'].sum().reset_index(name="CERTIFIED_TOTAL_WORKERS")
        companylist_merged_df_certified['year'] = year
        companylist_merged_df_total['year'] = year
        new_data = companylist_merged_df_certified.merge(companylist_merged_df_total, on='EMPLOYER_NAME')
        new_data['MarketCap_x'].astype('float64')
        new_data['Rate'] = (new_data['CERTIFIED_TOTAL_WORKERS'] / new_data['TOTAL_WORKERS_OVERALL']) * 100
        new_data = new_data[['EMPLOYER_NAME', 'Rate', 'MarketCap_x', 'year_x']]
        list_of_df.append(new_data)
    final_df = pd.concat(list_of_df, ignore_index=True)
    return final_df


def analysis_state_cal(states_data_df, year_df, yy) -> pd.DataFrame:
    """
    Used to merge state list with yearly LCA data frame to return a dataframe
    containing detail of LCA filings for every state.
    :param states_data_df: Dataframe containing the list of states in America.
    :param year_df: Yearly LCA dataframe.
    :param yy: Year of LCA data file
    :return: Dataframe containing list of states and corresponding
    number of LCA filings in which the state was the primary worksite.
    """
    year_df = year_df.merge(states_data_df, how='left', left_on='WORKSITE_STATE', right_on='Abbreviation')
    stats_df = year_df.groupby(['State'])['TOTAL_WORKERS'].sum().reset_index(name=yy)
    return stats_df


def analysis_state(file_list) -> pd.DataFrame:
    """
    Create a dataframe containing 50 states of America along with the number of LCA containing that state as worksite.
    :param file_list: File names of all the yearly LCA data files.
    :return: Returns a dataframe containing States along with LCA approvals from 2011-20.
    """
    states_df = pd.read_csv('states.csv')
    state_name = states_df.State.unique().tolist()
    plot_data_df = pd.DataFrame()
    plot_data_df['Worksite State'] = state_name
    for file in file_list:
        file_name = "data_H1B/" + file
        hypothesis_flag = False
        year_data = read_data(file_name, hypothesis_flag)
        year = '20' + file[7:9]
        stats = analysis_state_cal(states_df, year_data, year)
        plot_data_df = plot_data_df.merge(stats, how='left', left_on='Worksite State', right_on='State')
        del plot_data_df['State']
    plot_data_df = plot_data_df.set_index('Worksite State')

    return plot_data_df
