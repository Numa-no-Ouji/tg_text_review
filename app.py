import streamlit as st
from advertools import extract_emoji
from nltk import tokenize
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def count_characters(str):
    return f'Осталось еще {160 - len(str)} символов' if len(str) <= 160 else f'Текст слишком длинный. Удалите {len(str) - 160} символов'

def symbol_search(text):
    sym_list = ['/', '|', '_', '\\']
    n_list = ['']
    for sym in sym_list:
        if text.count(sym):
            n_list[0] = n_list[0] + sym + ' , '
            continue
        else:
            continue
    if n_list != ['']:
        return (f'В тексте есть запрещенные символы: {n_list[0].rstrip(" ,")} .')
    else:
        return ('Запрещенных символов в тексте нет.')

def emoji_quantity(text):
    emoji_summary = extract_emoji(text).get('emoji')
    e_count = 0
    for emoji in emoji_summary:
        if emoji != []:
            e_count += 1
        else:
            pass
    if e_count > 1:
        return 'Количество эмодзи в тексте превышает рекомендованное: 1 .'
    elif e_count == 1:
        return 'Количество эмодзи в тексте не ревышает рекомендованного: 1 , но больше эмодзи не добавить.'
    else:
        return f'В текст можно добавить еще {1 - e_count} эмодзи.'
    
def emoji_search(text):
    emoji_list = ['\U0001F449', '\U0001F448', '\U0001F446', '\U0001F447', 
                '\U0000261D', '\U00002B06', '\U00002197', '\U000027A1', 
                '\U00002198', '\U00002B07', '\U00002199', '\U00002B05',
                '\U00002196']
    n_list = ['']
    for emoji in emoji_list:
        if text.count(emoji):
            n_list[0] = n_list[0] + emoji + ', '
            continue
        else:
            continue
    if n_list != ['']:
        return (f'В тексте есть запрещенные эмодзи: {n_list[0].rstrip(" ,")} .')
    else:
        return ('Запрещенных эмодзи в тексте нет.')
    
def split_text(str):
    fn = tokenize.WordPunctTokenizer()
    return fn.tokenize(str)

def second_person_check(text):
    list_of_2_person_words = '' 
    for word in split_text(text):
        try:
            str(morph.parse(word)[0].tag).split(',').index('2per sing')
            list_of_2_person_words = list_of_2_person_words + word.lower() + ','
        except ValueError:
            continue
    result_str = []
    for word in list_of_2_person_words.split(','):
        try:
            result_str.index(word)
            continue
        except ValueError:
            result_str.append(word)
    result_str = ', '.join(result_str).rstrip(', ')
    if result_str != '':
        return (f'В тексте есть обращение на «ты»: {result_str}.')
    else:
        return ('Обращения на «ты» в тексте нет.')

def imperative_check(text):
    all_words_list = []
    dict_impr = []
    list_of_impr_words = '' 
    for word in split_text(text):
        all_words_list.append(word)
        try:
            # отбираем из всех слов только глаголы 
            str(morph.parse(word)[0].tag).split(',').index('VERB') 
            # отбираем глаголы, для которых более одного варианта разбора
            if len(morph.parse(word)) > 1:
                dict_impr.append({'word': word, 'tag': '', 'count': 0})
                i = 0
                while i < len(morph.parse(word)):
                    tag = str(morph.parse(word)[i].tag)
                    # варианты разбора будут записаны поочередно в 'tag'
                    dict_impr[-1]['tag'] = dict_impr[-1]['tag'] + tag + ','
                    i += 1
                # количество возможных разборов сохраняется в 'count'
                dict_impr[-1]['count'] = i
            else: # заносим глаголы с одним вариантом разбора в список
                dict_impr.append({'word': word, 'tag': '', 'count': 1})
                tag = str(morph.parse(word)[0].tag)   
                dict_impr[-1]['tag'] = dict_impr[-1]['tag'] + tag + ','
        except ValueError:
            continue
    for position in dict_impr:
        # отбираем глаголы, определенные как императив
        if position['tag'].find('impr') != -1:
            # определяем, являются ли глаголы с более чем 1 вариантом разбора императивом
            if position['tag'].split(',').count('impr') != position['count']:
                try:
                    # проверяем, является ли предшествующее глаголу слово 
                    # местоимением 2-го лица множественного числа
                    str(morph.parse(all_words_list[all_words_list.index(position['word']) - 1])[0].tag).split(',').index('2per plur')
                    continue
                except ValueError:
                    list_of_impr_words = list_of_impr_words + position['word'].lower() + ','
                    continue      
            else:
                list_of_impr_words = list_of_impr_words + position['word'].lower() + ','
                continue
        else:
            continue
    result_str = []
    for word in list_of_impr_words.split(','):
        try:
            result_str.index(word)
            continue
        except ValueError:
            result_str.append(word)
    result_str = ', '.join(result_str).rstrip(', ')
    if result_str != '':
        return (f'В тексте есть повелительное наклонение: {result_str}.')
    else:
        return ('Повелительного наклонения в тексте нет.')

def superlative_check(text):
    all_words_list = []
    dict_supr = []
    list_of_superlative_words = '' 
    for word in split_text(text):
        all_words_list.append(word.lower())
        try:
            str(morph.parse(word)[0].tag).split(',').index('Supr') 
            tag = str(morph.parse(word)[0].tag)
            dict_supr.append({'word': word, 'tag': tag})
        except ValueError:
            continue
    for position in dict_supr:
        try:
            str(morph.parse(all_words_list[all_words_list.index(position['word']) - 1])[0].tag).split(',').index('Prnt')
            continue
        except ValueError:
            try:
                str(morph.parse(all_words_list[all_words_list.index(position['word']) - 2])[0].tag).split(',').index('Prnt')
                continue
            except ValueError:
                list_of_superlative_words = list_of_superlative_words + position['word'].lower() + ','
                continue      
    result_str = []
    for word in list_of_superlative_words.split(','):
        try:
            result_str.index(word)
            continue
        except ValueError:
            result_str.append(word)
    result_str = ', '.join(result_str).rstrip(', ')
    if result_str != '':
        return (f'В тексте есть абсолютные превосходные формы: {result_str}.')
    else:
        return ('Абсолютных превосходных форм в тексте нет.')
    
def comparative_check(text):
    all_words_list = []
    dict_comp = []
    list_of_comparative_words = '' 
    for word in split_text(text):
        all_words_list.append(word.lower())
        try:
            str(morph.parse(word)[0].tag).split(',').index('COMP') 
            tag = str(morph.parse(word)[0].tag)
            dict_comp.append({'word': word, 'tag': tag})
        except ValueError:
            continue
    for position in dict_comp:
        try:
            str(morph.parse(all_words_list[all_words_list.index(position['word']) - 1])[0].tag).split(',').index('Prnt')
            continue
        except ValueError:
            try:
                str(morph.parse(all_words_list[all_words_list.index(position['word']) - 2])[0].tag).split(',').index('Prnt')
                continue
            except ValueError:
                list_of_comparative_words = list_of_comparative_words + position['word'].lower() + ','
                continue      
    result_str = []
    for word in list_of_comparative_words.split(','):
        try:
            result_str.index(word)
            continue
        except ValueError:
            result_str.append(word)
    result_str = ', '.join(result_str).rstrip(', ')
    if result_str != '':
        return (f'В тексте есть абсолютные сравнительные формы: {result_str}.')
    else:
        return ('Абсолютных сравнительных форм в тексте нет.')

def main():    
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

if __name__ == '__main__':
    main()