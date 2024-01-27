"""
Fayzan Malik
251379967
November 17th, 2023
defines functions that create and write a sentiment analysis report ot tweets to a .txt output file, given a .tsv keyword file and a .csv tweet file
"""
def read_keywords(keyword_file_name): #gets name of keyword file, returns a dictionary of keywords and sentiment values, if file doenst exist, IOError is raised and empty dictionary returned
    totalList = []
    totalDict = {}
    try:
        file = open(keyword_file_name, "r")
    except IOError:
        print("Could not open file '%s'!" % keyword_file_name)
        return totalDict
    for line in file:
        line = line.rstrip()
        listVals = line.split("\t")
        totalList.append(listVals)
    for list in totalList:
        totalDict[list[0]] = int(list[1]) #makes keyword as keyword of dictionary, and sentiment value as value of dicitonary using indexing
    file.close()
    return totalDict



def clean_tweet_text(tweet_text): #takes text as arguemnt, and removes everything except for english characters and whitespace, and lowercases, returns as string
    newText = ''.join((char for char in tweet_text if not char.isdigit())) #joins characters in string that that are alphanumeircal and whitespace using comprehension, does not join any other value (digits, special characters)
    newText = ''.join((char for char in newText if char.isalnum() or char.isspace()))
    newText = newText.lower()
    return newText

def calc_sentiment(tweet_text, keyword_dict): #returns sentiment score (int value) of tweet based on sentiment value of words in keyword dictionary
    sentiment = 0
    tweetTextList = tweet_text.split(" ")
    for word in tweetTextList:
        if word in keyword_dict:
            val = keyword_dict.get(word)
            sentiment += val
    return sentiment

def classify(score): #classifies score based on sentiment value (string)
    if score > 0:
        return "positive"
    if score == 0:
        return "neutral"
    if score < 0:
        return "negative"

def read_tweets(tweet_file_name): #returns list containing dictionary of all info of tweet and user, uses cleantext function for text key value
    tweetDicList = []
    tweetsList = []
    try:
        file = open(tweet_file_name, "r")
    except IOError:
        print("Could not open file '%s'" % tweet_file_name)
        return tweetDicList
    for line in file:
        line = line.rstrip()
        line = line.split(",")
        tweetsList.append(line)
    for list in tweetsList: #uses list indexing to get appropriate value of tweet for each keyword
        valueDict = {}
        valueDict["city"] = list[-3]
        valueDict["country"] = list[6]
        valueDict["date"] = list[0]
        valueDict["favorite"] = int(list[4])
        valueDict["lang"] = list[5]
        valueDict["lat"] = list[-2]
        if valueDict["lat"] != "NULL":
            valueDict["lat"] = float(list[-2])
        valueDict["lon"] = list[-1]
        if valueDict["lon"] != "NULL":
            valueDict["lon"] = float(list[-1])
        valueDict["retweet"] = int(list[3])
        valueDict["state"] = list[7]
        valueDict["text"] = clean_tweet_text(list[1])
        valueDict["user"] = list[2]
        tweetDicList.append(valueDict)
    file.close()
    return tweetDicList


def make_report(tweet_list, keyword_dict): #returns a dictionary that is a report of information regarding all tweets in csv file using list of tweets and list of keywords and values
    #initiealize varaibles (counters, lists, dictionaries)
    reportDict = {}
    countryList = []
    sentimentFavs = 0
    numFavTweets = 0
    sentimentRTs = 0
    numRtTweets = 0
    numNeg = 0
    numNeut = 0
    numPos = 0
    totalTweets = 0
    totalSentiment = 0
    totalList = []
    for tweet in tweet_list: #conditionals to check whether tweet is classified as positive, degative, or neutral, and counts total of each
        totalTweets += 1
        if tweet["favorite"] > 0:
            sentimentFavs += calc_sentiment(tweet["text"], keyword_dict)
            numFavTweets += 1
        if tweet["retweet"] > 0:
            sentimentRTs += calc_sentiment(tweet["text"], keyword_dict)
            numRtTweets += 1
        totalSentiment += calc_sentiment(tweet["text"], keyword_dict)
        sentiment = classify(calc_sentiment(tweet["text"], keyword_dict))
        if sentiment == "negative":
            numNeg += 1
        elif sentiment == "neutral":
            numNeut += 1
        elif sentiment == "positive":
            numPos += 1
        if tweet["country"] not in countryList: #creates list of all seperate countries in csv
            if tweet["country"] != "NULL":
                countryList.append(tweet["country"])
        for country in countryList:
            if tweet["country"] == country: #gets totalsentiment values for all tweets, creates dictionary of tweet and country and adds it to a total list
                sentiment = calc_sentiment(tweet["text"], keyword_dict)
                testDict = {country: sentiment}
                totalList.append(testDict)

    totalPerCountry = {}
    for dict in totalList: #adds up total sentiment value of each country, puts it into totalPerCountry dictionary
        for country in dict:
            if country in totalPerCountry:
                if isinstance(dict[country], int):
                    totalPerCountry[country] += dict[country]
            else:
                totalPerCountry[country] = dict[country]

    dictCheck = {}
    for country in countryList: #creates dictionary for number of instances of each country in list of all country sentiment key value pairs in total list
        check = [k[country] for k in totalList if k.get(country)]
        occurances = len(check)
        dictCheck[country] = occurances

    averageDict = {}
    for key in totalPerCountry: #calculates average sentiment of each country and adds it to a Dictionary
            for key2 in dictCheck:
                if key == key2:
                    if dictCheck[key] != 0:
                        averageDict[key] = totalPerCountry[key] / dictCheck[key]
                    else: averageDict[key] = dictCheck[key]
    sortedCountries = sorted(averageDict.items(), key=lambda item: item[1]) #sorts all ocuntries by average sentiment
    topFive = sortedCountries[-5:] #takes 5 highest sentiment values as tuples in ascending order
    topFiveList = [i[0] for i in topFive] #turns tuples into list of values
    topFiveList.reverse() #reverses list for descending order
    top_five_avg_sentiment_final = ', '.join(topFiveList) #creates string of top 5 countries ranked by highest average sentiment in descending order
    if numFavTweets > 0:
        avgFavs = sentimentFavs/numFavTweets
        reportDict["avg_favorite"] = float("%8.2f" % avgFavs)
    elif numFavTweets == 0:
        reportDict["avg_favorite"] = "NAN"
    if numRtTweets > 0:
        avgRts = sentimentRTs/numRtTweets
        reportDict["avg_retweet"] = float("%8.2f" % avgRts)
    elif numRtTweets == 0:
        reportDict["avg_retweet"] = "NAN"
    avgSentiment = totalSentiment / totalTweets
    reportDict["avg_sentiment"] = float(("%8.2f" % avgSentiment))
    reportDict["num_favorite"] = int(numFavTweets)
    reportDict["num_negative"] = int(numNeg)
    reportDict["num_neutral"] = int(numNeut)
    reportDict["num_positive"] = int(numPos)
    reportDict["num_retweet"] = int(numRtTweets)
    reportDict["num_tweets"] = int(totalTweets)
    reportDict["top_five"] = top_five_avg_sentiment_final
    return reportDict
    # Should return a dictionary containing the report values.


def write_report(report, output_file): #writes final report into output file containing the contents of make_report
    try:
        file = open(output_file, "w")
    except IOError:
        print("Could not open file [%s]" % output_file)
    sentAvg = report["avg_sentiment"]
    totalTweets = report["num_tweets"]
    posTweets = report["num_positive"]
    negTweets = report["num_negative"]
    neutTweets = report["num_neutral"]
    favTweets = report["num_favorite"]
    favTweetSent = report["avg_favorite"]
    rtTweets = report["num_retweet"]
    rtTweetsSent = report["avg_retweet"]
    topFive = report["top_five"]
    file.write("Average sentiment of all tweets: %s\n" % sentAvg)
    file.write("Total number of tweets: %s\n" % totalTweets)
    file.write("Number of positive tweets: %s\n" % posTweets)
    file.write("Number of negative tweets: %s\n" % negTweets)
    file.write("Number of neutral tweets: %s\n" % neutTweets)
    file.write("Number of favorited tweets: %s\n" % favTweets)
    file.write("Average sentiment of favorited tweets: %s\n" % favTweetSent)
    file.write("Number of retweeted tweets: %s\n" % rtTweets)
    file.write("Average sentiment of retweeted tweets: %s\n" % rtTweetsSent)
    file.write("Top five countries by average sentiment: %s\n" % topFive)
    print("Wrote report to", output_file)
    file.close()
    # Add your code here
	# Should write the report to the output_file.