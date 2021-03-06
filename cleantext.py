from dependency import * 
tokenizer = ToktokTokenizer()
nltk.download('averaged_perceptron_tagger')


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_special_characters(text, remove_digits=False):
    pattern = re.compile('[^a-zA-z0-9.\s]') if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    return text



nltk.download('stopwords')
stopword_list = nltk.corpus.stopwords.words('english')
def remove_stopwords(text, is_lower_case=False,return_str=True):
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    if return_str:
        filtered_text = ' '.join(filtered_tokens)
        return filtered_text
    else: 
        return filtered_tokens
    

def remove_html(text):
    parse = BeautifulSoup(text,'lxml')
    return parse.get_text(' ').lower()


nltk.download('wordnet')
def lemmatize_text(text,pos='n'): 
    w = WordNetLemmatizer()
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens] #remove space
    filtered_tokens = [w.lemmatize(token,pos) for token in tokens ]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text 
    
def quick_clean_text(text,html=1, specchar=1, stopword=1,lemmatize=1): 
    if html == 1:
        text = remove_html(text)
    if specchar == 1: 
        text = remove_special_characters(text,remove_digits=True)
    if stopword == 1:
        text = remove_stopwords(text)
    if lemmatize == 1:
        text = lemmatize_text(text)
    return text 

