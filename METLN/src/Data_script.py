import pandas as pd
import gender_guesser.detector as gender #found on internet

def clean_and_merge(transactions='METLN/src/data/transactions_clean - transactions.csv', customers='METLN/src/data/customer_summary_clean.csv'):
    '''Input: 2 CSVS from MLET (one of customers and one transactions)
       Output - Add Gender Column using gender guesser and merge
    '''
    df_customers=pd.read_csv(customers)
    df_transactions=pd.read_csv(transactions)
    gd=gender.Detector()
    df_customers['First Name']=df_customers['First Name'].apply(str.capitalize) #standardize otherwise get more unknowns
    df_customers['Gender']=df_customers['First Name'].apply(lambda x: gd.get_gender(x))
    df_customers['Gender'] = df_customers['Gender'].apply(
    lambda x: 'M' if x in ['male', 'mostly_male'] 
    else 'F' if x in ['female', 'mostly_female'] #makes it easier to filter m/f
    else 'unknown') #we can make a dictionary of common unknown names but this isn't scalable
    df=pd.merge(df_customers,df_transactions, on='Hashed Email Address')
    df.to_csv('METLN/src/data/merged.csv', index=False)

def main():
    clean_and_merge()

if __name__=='__main__':
    main()