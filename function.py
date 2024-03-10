import re
import pandas as pd
from io import BytesIO
import sqlite3






def clean_phone_number(nomor):
    nomor = re.sub(r'\D', '', nomor)

    nomor = re.sub(r'^0', '', nomor)

    if nomor.startswith('62') or nomor.startswith("+62") :
        nomor = '0' + nomor[2:]

    return nomor





################################################
    
import pandas as pd
import re


def clean_data(df):
    
    
    df = pd.read_csv(df, encoding='ISO-8859-1')
        
    df = df.drop(columns=['HS', 'Abusive', 'HS_Individual', 'HS_Group', 'HS_Religion', 'HS_Race', 'HS_Physical', 'HS_Gender', 'HS_Other', 'HS_Weak', 'HS_Moderate', 'HS_Strong'])
    
    df = df.drop_duplicates()
            


    pola_regex_link = re.compile(r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?')
    pola_regex_emoji = re.compile(r'\\x[0-9a-fA-F]+')
    pola_regex_rt = re.compile(r'\bRT\b')
    pola_regex_tanda_baca = re.compile(r'[^a-zA-Z0-9\s]')
    pola_regex_beruntun = re.compile(r'\b(\w+)(\s+\1)+\b')
    pola_regex_user = re.compile(r'\bUSER\b')
    #pola_regex_spasi  = re.compile(r'(?<=[a-zA-Z0-9])\s*?(?=[a-zA-Z0-9])')
    pola_regex_hatstag = re.compile(r'#\w+')

    def data_cleaning(text):
        text = re.sub(pola_regex_link, r'', text)
        text = re.sub(pola_regex_emoji, r'', text)
        text = re.sub(pola_regex_rt, r'', text)
        text = re.sub(pola_regex_tanda_baca, r'', text)
        text = re.sub(pola_regex_beruntun, r'', text)
        text = re.sub(pola_regex_user, r'', text)
        #text = re.sub(pola_regex_spasi, r'', text)
        text = re.sub(pola_regex_hatstag, r'', text)
        return text


    df['Tweet_Unclean'] = df['Tweet']
    df['Clean'] = df['Tweet'].apply(lambda x: data_cleaning(x))

    df2 = pd.read_csv(r"abusive.csv", encoding='ISO-8859-1')
    df['Clean'] = df['Clean'].str.lower()
    kata_kasar = df2['ABUSIVE'].tolist()

    def clean_kata_kasar(text):
        for kata in kata_kasar:
            text = text.replace(kata, "")
        return text

    df['Clean'] = df['Clean'].apply(lambda x: clean_kata_kasar(x))


    df_kamusalay = pd.read_csv(r'new_kamusalay.csv', encoding='ISO-8859-1', names=['before', 'after'])
    kamusalay_dict_map = dict(zip(df_kamusalay['before'], df_kamusalay['after']))

    def clean_alay(text):
        word_list = []
        for kata in text.split():
            if kata in kamusalay_dict_map:
                kata = kamusalay_dict_map[kata]
                word_list.append(kata)
            else:
                word_list.append(kata)
        return ' '.join(word_list)
    

    df['Clean'] = df['Clean'].apply(lambda x: clean_alay(x))

    # Rename column 'Clean' to 'Tweet_Clean'
    df = df.rename(columns={'Clean': 'Tweet_Clean'})
    
    # Drop rows with missing data in column: 'Tweet_Clean'
    
    df = df.dropna(subset=['Tweet_Clean'])
    

    
    cleaned_data_list = list(zip(df['Tweet_Clean'].tolist(), df['Tweet_Unclean'].tolist()))
    
    

    return cleaned_data_list


def clean_kata(kata):
    kata = pd.DataFrame({'test': [kata]})

    pola_regex_komaangka = re.compile(r',(\d+,)+\d+')
    pola_regex_link = re.compile(r'(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?\/[a-zA-Z0-9]{2,}|((https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z]{2,}(\.[a-zA-Z]{2,})(\.[a-zA-Z]{2,})?)|(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})?')
    pola_regex_emoji = re.compile(r'\\x[0-9a-fA-F]+')
    pola_regex_rt = re.compile(r'\bRT\b')
    pola_regex_tanda_baca = re.compile(r'[^a-zA-Z0-9\s]')
    pola_regex_beruntun = re.compile(r'\b(\w+)(\s+\1)+\b')
    pola_regex_user = re.compile(r'\bUSER\b')
    #pola_regex_spasi  = re.compile(r'(?<=[a-zA-Z0-9])\s*?(?=[a-zA-Z0-9])')
    pola_regex_hatstag = re.compile(r'#\w+')

    def data_cleaning(text):
        text = re.sub(pola_regex_komaangka,r'',text)
        text = re.sub(pola_regex_link, r'', text)
        text = re.sub(pola_regex_emoji, r'', text)
        text = re.sub(pola_regex_rt, r'', text)
        text = re.sub(pola_regex_tanda_baca, r'', text)
        text = re.sub(pola_regex_beruntun, r'', text)
        text = re.sub(pola_regex_user, r'', text)
        #text = re.sub(pola_regex_spasi, r'', text)
        text = re.sub(pola_regex_hatstag, r'', text)
        return text
    
    kata['test'] = kata['test'].apply(lambda x: data_cleaning(x))

    

    df2 = pd.read_csv(r"abusive.csv", encoding='ISO-8859-1')
    kata['test']=kata['test'].str.lower()
    kata_kasar = df2['ABUSIVE'].tolist()

    def clean_kata_kasar(text):
        for kata in kata_kasar:
            text = text.replace(kata, "")
        return text


    kata['test'] = kata['test'].apply(lambda x : clean_kata_kasar(x))

    df_kamusalay = pd.read_csv(r'new_kamusalay.csv', encoding='ISO-8859-1', names=['before', 'after'])
    kamusalay_dict_map = dict(zip(df_kamusalay['before'], df_kamusalay['after']))

    def clean_alay(text):
        word_list = []
        for kata in text.split():
            if kata in kamusalay_dict_map:
                kata = kamusalay_dict_map[kata]
                word_list.append(kata)
            else:
                word_list.append(kata)
        return ' '.join(word_list)
    


    kata['test'] = kata['test'].apply(lambda x :clean_alay(x))
    variable_kata = list(zip(kata['test'].tolist()))

    

    return variable_kata




