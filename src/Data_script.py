import pandas as pd
import gender_guesser.detector as gender

def clean_and_merge(transactions='src/data/transactions_clean - transactions.csv', customers='src/data/customer_summary_clean.csv'):
    df_customers=pd.read_csv(customers)
    df_transactions=pd.read_csv(transactions)
    gd=gender.Detector()
    df_customers['First Name']=df_customers['First Name'].apply(str.capitalize)
    df_customers['Gender']=df_customers['First Name'].apply(lambda x: gd.get_gender(x))
    df_customers['Gender'] = df_customers['Gender'].apply(
    lambda x: 'M' if x in ['male', 'mostly_male']
    else 'F' if x in ['female', 'mostly_female']
    else 'unknown')
    df=pd.merge(df_customers,df_transactions, on='Hashed Email Address')
    df.to_csv('src/data/merged.csv', index=False)

def main():
    clean_and_merge()

if __name__=='__main__':
    main()