import twint
import sys, os
import numpy as np


from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def usrexist(name):
    blockPrint()
    """
    It takes a username as an input and returns True if the profile exists and False if it doesn't
    
    :param name: The username to search for
    :return: A list of dictionaries, each dictionary is a tweet.
    """
    c = twint.Config()
    c.Username = name
    c.Store_object = True

    existstat = False #True if the profile exist

    try:
        twint.run.Lookup(c)
        existstat = True
    except:
        existstat = False

    enablePrint()

    return existstat



def interest(name):
    """
    It takes a username as input, and returns a list of words that are used in the tweets of the user
    
    :param name: The username of the Twitter account you want to scrape
    :return: a list of words that are not in the list of words that are not interesting.
    """
    cls()
    print("loading...")
    print("________________________________________")
    print("               ")


    #user input
    blockPrint()

    c = twint.Config()
    c.Username = name
    c.Limit = 2000
    c.Store_object = True

    twint.run.Search(c)
    tweets = twint.output.tweets_list
    enablePrint()

    msg = ['{}'.format(tweet.tweet) for tweet in tweets]


    wordset = set()

    #Decoupage en un dictionaire de mots
    wordlist = []

    for message in msg:
        message = message.replace("'", " ").replace(",", " ").replace(".", " ").replace("’", " ").replace("“", " ").replace("”", " ").replace("!", " ").replace("?", " ").replace("-", " ").replace("_", " ").replace(";", " ").replace(":", " ").replace("/", " ").replace("\\", " ").replace("(", " ").replace(")", " ").replace("[", " ").replace("]", " ").replace("{", " ").replace("}", " ").replace("*", " ").replace("$", " ").replace("^", " ").replace("&", " ").replace("=", " ").replace("+", " ").replace("|", " ").replace("<", " ").replace(">", " ").replace("~", " ").replace("`", " ").replace("_", " ").replace("-", " ").replace('"'," ")
        wordlistmsg = message.split(" ")
        for word in wordlistmsg:
            wordlist.append(word)

    wordset = set(e for e in wordlist)

    # comptage des mots

    wordcount = dict()

    for word in wordset:
        #compte un mot en particulier
        count = 0
        for ele in wordlist:
            if word == ele:
                count+=1

        wordcount[word]=count

    #move hashtags to a set
    hashtags = set()
    for tweet in tweets:
        hashtags.update(tweet.hashtags)

    #count the most common hashtags in the wordlist
    hashtagscount = dict()
    for hashtag in hashtags:
        count = 0
        for ele in wordlist:
            if hashtag == ele:
                count+=1
        hashtagscount[hashtag]=count

    #sort the hashtags by count
    hashtagscount = sorted(hashtagscount.items(), key=lambda x: x[1], reverse=True)

    #keep only the hashtags with a count of at least 1
    hashtagscount = [x for x in hashtagscount if x[1]>0]

    #tri des mots par ordre decroissant
    sorted_wordcount = sorted(wordcount.items(), key=lambda x: x[1], reverse=True)

    #get the first quartile of the list
    quartile = int(len(sorted_wordcount)/4)
    value_quartile = sorted_wordcount[quartile]

    #delete of the words that apprear less than n times from the list of tuples
    n = value_quartile[1]
    sorted_wordcount = [x for x in sorted_wordcount if x[1] > n]
    

    #common words in french that are not interesting
    MotCour = ["le","les","Les","de","un","être","et","à","il","avoir","ne","je","son","que","se","qui","ce","dans","en","du",
    "elle","au","de","ce","ces","le","la","c'est","n'est","a","des","est",'été', 'Avec', 'peu', 'La',
    "j'ai", 'très',"merci","afin", "quoi", "même", "cet","⬇️", "C'est","oui","non","ses","tweet","cet","trop","ont","sous","d'en","aussi", 'Il', 'Ce',"pour", '💚', 'vit.', 'Ça', 'aux', 'oui,' ,'cette', 'Pour', 'peut',
    ':', '🙂', 'fait', "ni", "vit", "sera", "ai", "mis", "cf"," depuis", "sa", "amp", "soit", "–", "surtout", "milliers", "milliards", "cause", "👇", "➡️","soit", "sous", "qu'il", "faut", ":)", "=)", 'Je', "1","2","3","4","5","6","7","8","9","10", 'ça', 'donner','😊', "ma","donc",'une', '🙏',
    'sont', 'Merci',"pas","que","vous","par","sur","faire","plus","dire","me","on","mon","lui","nous","comme","mais","pouvoir","avec","tout","y",
    "aller","avez","ds", "😏", "💚🙏", "dois", "bon", "vis", "bonjour", "encore", "rien","delà",  "faudrait","semble","leurs","serai","effectivement","voir","👆👆👆","haha","là","autre","autres","fois","petit","nouvelle","nouveau","avez","voilà","ah","ruy","RT","ferais","j","te","tous","mes","beaucoup",
    "alors","svp","dit","contre","ya","quand","cas","évidemment","personnes","en","qu","va","avait","fais","votre","suis","passe","entre","n°","ℹ️","jour","📚","chaque","forme","mises","vos","jour","propos","tanté",
    "après","bonne","mauvaise","notre","nos","ils","quelques","tellement","journée","fe","tienes","moment","el","ton","🙏🏻🤍","jours","som","foc","c","ici","chez","depuis","avant","année","es","bien","où","sans","✅","❌","🌱",")","(","n","C", "celui", "déjà", "vers", "indiqué", "Retrouvez", "nombreuses", "Concernant","majoritairement","tu","ou","%","chez","prise","etc","leur","homme","si","deux","l","mari","moi","?","!",".",",","d","t","","moins","plus"]

    #common words in english that are not interesting
    MotCourEn = ["to","when", "the", "the", "of","much", "a", "be", "and", "am", "at", "he", "have", "do", "I", " his "," that "," is "," who "," this "," in "," in "," of ",
    "she", "at", "of","as","m","co","are","from","which","why","about","don","oh","each", "this", "these", "the", "the", "it", "is","s", "a", "of", "is ", 'With', 'little', 'La',
    "i", 'very', "thank","you","thanks","for","your","there","their","It's", "so", "what", "been","even", "this", "it's", "yes", "no", "his", "tweet "," this "," too "," have "," under "," from "," also ", 'He', 'This'," for ",' 💚 ','live',' That ',' to ',' yes, ',' this', 'For', 'may',
    ':', '🙂', 'done', "under", "that", "must", 'I', "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 'that', 'give', '😊', "my", "therefore", 'a', '🙏', 'are ',' Thank you ', "not", "that", "you", "by", "on", "do", "more", "say", "me", "on", "my", "him", "we", "like", "but", "can", "with", "all", "y",
    "go", "see", "in","really", '"',"just","because","re","make","high","long","now","ve","let","owe","choose","they","then", "them", "good", "where", "without", "you", "or", "their", "man", "if", "two", "husband ","me","?","!",".",","]

    french_stop_words = stopwords.words("french")
    english_stop_words = stopwords.words("english")

    #add french stop words to mot cour
    MotCour.append(list(french_stop_words))
    MotCourEn.append(list(english_stop_words))


    #filter out the words that are in the common words list (both french and english)
    sorted_wordcount = dict(filter(lambda key: not(key[0].lower() in MotCour or key[0].lower() in MotCourEn) and not(key[0].startswith("http")) and not(key[0].startswith("@")),sorted_wordcount))

    print("The most common hashtags are:")
    print(hashtagscount)


    print("the most common words are:")
    for key in sorted_wordcount:
        print(key, sorted_wordcount[key])

    

    #empty the list of tweets and variables that might interfere with the next run
    twint.output.tweets_list = []
    msg = []
    wordlist = []
    wordset = set()




def main():
    usrinput =""

    while(usrinput!="exit"):
        usrinput = input("Twitter username (or exit):")
        if(not(usrinput=="exit") and usrexist(usrinput)):
            interest(usrinput)
        else:
            print("This user could not be found (or you exited)")

if __name__ == "__main__":
    # execute only if run as a script
    main()
