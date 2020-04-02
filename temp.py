# Importing necessary libraries and packages

#import os
import nltk
import random
import string
import warnings
from gtts import gTTS
import winsound
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')



# Importing packages from nltk
# No need to run it always normally  
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


# Read corpus text file 
f=open('corpus.txt','r',errors = 'ignore')
raw = f.read()
# print(raw)


text = raw

# converts to list of sentences 
sent_tokens = nltk.sent_tokenize(text)
# print(sent_tokens)


# WordNet is a NLTK based dictionary of English
lemmer = nltk.stem.WordNetLemmatizer()


# Function to return a list of lemmatized lower case words and punctuations are removed
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greetings based on keywords
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREETING_RESPONSES = ["Hi", "Hey", "*nods*", "Hi, there", "Hello", "I am glad! You are talking to me"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        
        
# Generate response using TfidVectorizer and cosine similarity
def response(user_response):
    bot_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        bot_response = bot_response+"I am sorry! I don't understand you"
        return bot_response
    else:
        bot_response = bot_response + sent_tokens[idx]
        return bot_response

def seperation():
    print()
    print("////////////////////////////////")
    print()

def audio_output(texto):
    
    tts = gTTS(texto)
    #tts.save('audio.wav')
    tts.save('audio.mp3')
    
    winsound.PlaySound('audio.wav', winsound.SND_FILENAME)
    #os.system("mpg321 audio.mp3")  works for linux
    

# Main conditons and loop for bot   
flag=True
print("Doctorbot: My name is Doctorbot. I'm an informative Chatbot for Coronavirus. If you want to exit, type 'exit'")

tts = gTTS('Bye! take care stay home stay safe')
tts.save('audio.mp3')
winsound.PlaySound('audio.mp3', winsound.SND_FILENAME)

while(flag==True):
    print("User:")
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='exit'):
        if(user_response=='thanks' or user_response=='thank you' or user_response=='thankyou' ):
            flag=False
            print("Doctorbot: You are welcome...")

            tts = gTTS('Doctorbot: You are welcome...')
            tts.save('audio.mp3')
            seperation()

        else:
            if(greeting(user_response)!=None):
                print("Doctorbot: "+ greeting(user_response))
                
                bot_response1 = greeting(user_response)
                audio_output(bot_response1)
                seperation()

            else:
                
                print("Doctorbot: ", end="")

                bot_response = response(user_response)
                print(bot_response)

                
                audio_output(bot_response)
                seperation()

                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Doctorbot: Bye! take care stay home stay safe")


        tts = gTTS('Bye! take care stay home, stay safe')
        tts.save('audio.mp3')
        winsound.PlaySound('audio.mp3', winsound.SND_FILENAME)
        seperation()
