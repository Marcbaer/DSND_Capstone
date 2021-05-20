''' This Script contains functions to process the raw provided datasets for further analysis.'''

import pandas as pd
import numpy as np

def process_portfolio(portfolio):
    """ Processes portfolio data into clean dataframe.
    INPUT:
        portfolio (dataframe): Pandas dataframe containing customer information
    OUTPUT:
        portfolio_clean (dataframe): Pandas dataframe containing cleaned portfolio data""" 
    
    #get dummy columns for channel values
    portfolio_clean=portfolio.copy()
    dummy = pd.get_dummies(portfolio_clean.channels.apply(pd.Series).stack()).sum(level=0)
    portfolio_clean = pd.concat([portfolio_clean, dummy], axis=1)
    portfolio_clean = portfolio_clean.drop(columns='channels')
    portfolio_clean = portfolio_clean.rename(columns={'id':'offer_id'})

    #get dummy columns for offer_type
    dummy = pd.get_dummies(portfolio_clean.offer_type.apply(pd.Series).stack()).sum(level=0)
    portfolio_clean = pd.concat([portfolio_clean, dummy], axis=1)
    portfolio_clean = portfolio_clean.drop(columns='offer_type')    
    
    return portfolio_clean

def process_profile(profile):
    """ Processes profile data into clean dataframe.
    INPUT:
        profile (dataframe): Pandas dataframe containing customer information
    OUTPUT:
        profile_clean (dataframe): Pandas dataframe containing cleaned customer information data"""    
    
    #drop rows with missing income/gender value (age value is 118 and not reasonable)
    profile_clean=profile.copy().dropna(subset = ['income','gender'])    
    
    profile_clean['became_member_on'] = pd.to_datetime(profile_clean['became_member_on'], format='%Y%m%d')

    profile_clean = profile_clean.rename(columns={'id':'customer_id'})

    #get dummy columns for offer_type
    dummy = pd.get_dummies(profile_clean.gender.apply(pd.Series).stack()).sum(level=0)
    profile_clean = pd.concat([profile_clean, dummy], axis=1)
    profile_clean = profile_clean.drop(columns='gender')
    
    #store only the year when customer became member
    profile_clean['became_member_on']=profile_clean['became_member_on'].dt.year
    
    #get dummy columns for each year
    dummy = pd.get_dummies(profile_clean.became_member_on.apply(pd.Series).stack()).sum(level=0)
    profile_clean = pd.concat([profile_clean, dummy], axis=1)
    
    profile_clean = profile_clean.drop(columns='became_member_on')

    return profile_clean


def process_transcript(transcript,profile_clean):
    """ Processes transcript data into two dataframes related to offer transcripts and transactions.
    INPUT:
        transcript (dataframe): Pandas dataframe containing transcripts
        profile_clean (dataframe): Pandas dataframe containing cleaned profile data
    OUTPUT:
        offer_data (dataframe): Pandas dataframe containing offer transcripts
        transaction (dataframe): Pandas dataframe containing transactions"""
    import numpy as np
    
    transcript_clean = transcript.rename(columns={'person':'customer_id'})
    
    #get dummy columns for 'event' column and extract offer id from 'value'
    dummy = pd.get_dummies(transcript_clean['event'])
    transcript_clean = pd.concat([transcript_clean, dummy], axis=1 )


    transcript_clean['offer_id'] = [[*i.values()][0]if [*i.keys()][0] in ['offer id','offer_id'] else None for i in transcript_clean.value]
    transcript_clean['amount'] = [np.round([*i.values()][0], decimals=2)if [*i.keys()][0] == 'amount' else None for i in transcript_clean.value]
    
    # Remove customer id's that are not in the customer profile DataFrame
    select_data = transcript_clean['customer_id'].isin(profile_clean['customer_id'])
    transcript_clean = transcript_clean[select_data]
    
    # Convert from hours to days
    transcript_clean['time'] /= 24.0

    # Change the name of the 'time' column to 'timedays'
    transcript_clean = transcript_clean.rename(columns={'time':'timedays'})

    # Select customer offers
    offer_data = transcript_clean[transcript_clean['transaction']==0].copy()
    offer_data = offer_data.reset_index(drop=True)
    offer_data = offer_data.drop(columns=['value','amount','transaction'])

    # Select customer transaction events
    transaction = transcript_clean[transcript_clean['transaction']==1].copy()
    transaction = transaction.reset_index(drop=True)

    # Create a DataFrame that describes customer transactions
    column_order = ['customer_id', 'timedays', 'amount']
    transaction = transaction[column_order]
    
    return offer_data, transaction

def combine_data(portfolio_clean,profile_clean,offer_data,transaction):
    """ Creates a dataset containing information related to offer successes and customer information.
    The final dataframe describes the effectiveness of a specific offer to a specific customer.
    INPUT:
        customer_id (string): String identifying a unique customer
        portfolio_clean (dataframe): input dataframe for offer portfolio
        profile_clean (dataframe): customer details data
        offer_data (dataframe): offer transcripts
        transaction: transaction transcripts
    OUTPUT:
        result (dataframe): Resulting Dataframe"""
    
    customerid_list = offer_data['customer_id'].unique()
    result=[]
    
    #iterate over available customers
    
    for i,j in enumerate(customerid_list):
    
        customer_id=j
        
        #Filter for customers available in the profile dataset
        cur_customer = profile_clean[profile_clean['customer_id'] == customer_id]

        # Select offer data for a specific customer
        customer_offer_data = offer_data[offer_data['customer_id'] == customer_id]
        customer_offer_data = customer_offer_data.drop(columns='customer_id')
        customer_offer_data = customer_offer_data.reset_index(drop=True)

        # Select transactions for a specific customer
        customer_transaction_data = transaction[transaction['customer_id'] == customer_id]
        customer_transaction_data =customer_transaction_data.drop(columns='customer_id')
        customer_transaction_data =customer_transaction_data.reset_index(drop=True)

        # event dataframes
        event_type = ['offer completed','offer received','offer viewed']

        offer_received =customer_offer_data[customer_offer_data['offer received'] == 1]
        offer_received = offer_received.drop(columns=event_type)
        offer_received = offer_received.reset_index(drop=True)

        offer_viewed =customer_offer_data[customer_offer_data['offer viewed'] == 1]
        offer_viewed = offer_viewed.drop(columns=event_type)
        offer_viewed = offer_viewed.reset_index(drop=True)

        offer_completed =customer_offer_data[customer_offer_data['offer completed'] == 1]
        offer_completed = offer_completed.drop(columns=event_type)
        offer_completed = offer_completed.reset_index(drop=True)

        # Iterate over each offer a customer receives and append data to list
        rows = []
        for idx in range(offer_received.shape[0]):
                # Initialize offer id
                cur_offer_id = offer_received.iloc[idx]['offer_id']

                # Look-up the description of the offer      
                cur_offer = portfolio_clean.loc[portfolio_clean['offer_id'] == cur_offer_id]
                durationdays = cur_offer['duration'].values[0]

                # Initialize the time frame when offer is valid
                cur_offer_startime = offer_received.iloc[idx]['timedays']

                cur_offer_endtime =offer_received.iloc[idx]['timedays'] + durationdays

                # Select transaction within valid time frame
                select_transaction =np.logical_and(customer_transaction_data['timedays'] >=
                                   cur_offer_startime,
                                   customer_transaction_data['timedays'] <=
                                   cur_offer_endtime)

                # Select description when customer completes the offer
                select_offer_completed =np.logical_and(offer_completed['timedays'] >= cur_offer_startime,
                                   offer_completed['timedays'] <= cur_offer_endtime)

                # Select description when customer views the offer
                select_offer_viewed =np.logical_and(offer_viewed['timedays'] >= cur_offer_startime,
                                   offer_viewed['timedays'] <= cur_offer_endtime)

                # Evaluate if offer is successfull
                cur_offer_successful =select_offer_completed.sum() > 0 and select_offer_viewed.sum() > 0

                # Select customer transcations that occurred within the valid time window
                cur_offer_transactions = customer_transaction_data[select_transaction]

                # Create dictionary that describes the current customer offer
                cur_row = {'offer_id': cur_offer_id,
                           'customer_id': customer_id,
                           'time': cur_offer_startime,
                           'offersuccessful': int(cur_offer_successful),
                           'totalamount': cur_offer_transactions['amount'].sum()}

                cur_row.update(cur_offer.iloc[0,:].to_dict())

                cur_row.update(cur_customer.iloc[0,:].to_dict())
                rows.append(cur_row)
                
        result.extend(rows)
    
    #order columns  
    result_df=pd.DataFrame(result)   
    
    order = ['offer_id', 'totalamount','age','income','duration','bogo','discount','informational']
    order.extend([elem for elem in result_df.columns if elem not in order])
    result_df = result_df[order]

    
    return result_df