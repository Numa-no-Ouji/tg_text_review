import streamlit as st
from common_library import *

st.title('Проверка текста для Telegram Ads', anchor='top')
tab_ads, tab_channel_posts = st.tabs(['Проверка текста объявления Telegram Ads','Проверка постов из канала Telegram Ads'])
    
with tab_ads:
    text = st.text_input('Укажите текст вашего объявления ниже:', value='', max_chars=5000, key='ad_text', type='default', placeholder=None, help='Введите текст объявления. Допустимая длина текста - не более 160 символов с пробелами.')
    if st.button('Проверить', key='running_text_check') and text != '':
        st.write(count_characters(text))
        st.write(symbol_search(text))
        st.write(emoji_quantity(text))
        st.write(emoji_search(text))
        st.write(imperative_check(text))
        st.write(superlative_check(text))
        st.write(comparative_check(text))
        st.write(second_person_check(text))

with tab_channel_posts:
    st.write('Для начала убедитесь, что ваш канал - публичный.')
    text = st.text_input('Укажите ссылку на ваш Telegram-канал ниже:', value='', key='channel_link', type='default', placeholder=None, help='Введите ссылку на Telegram-канал в формате https://t.me/eLama_russia')
    if st.button('Проверить', key='running_channel_check') and text != '':
        st.write('Пук-среньк')