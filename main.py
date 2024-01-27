"""
Fayzan Malik
251379967
November 17th, 2023
gets user input for tweet file, keyword file, and output file and writes a sentiment analysis report to the output file
"""

# Import the sentiment_analysis module
from sentiment_analysis import *
def main(): #main function, takes input of keword file, tweet file, and output file form user and creates sentiment analysis using functions from sentiment_analysis.py
    keyFile = input("Input keyword filename (.tsv file): ")
    if keyFile[-4:] != ".tsv":
        raise Exception("Must have tsv file extension!") #raises exception if suffix for file input in incorrect

    tweetFile = input("Input tweet filename (.csv file): ")
    if tweetFile[-4:] != ".csv":
        raise Exception("Must have csv file extension!") #raises exception if suffix for file input in incorrect


    outputFile = input("Input filename to output report in (.txt file): ")
    if outputFile[-4:] != ".txt":
        raise Exception("Must have txt file extension!") #raises exception if suffix for file input in incorrect

    keywordDict = read_keywords(keyFile)
    tweetList = read_tweets(tweetFile)
    if len(keywordDict) == 0 or len(tweetList) == 0:
        raise Exception("Tweet list or keyword dictionary is empty!") #raises exception if keyword or tweet file are non existent, returning empty list or dict
    report = make_report(tweetList, keywordDict)
    write_report(report, outputFile) #writes final report
    #Gets input from user and calls required functions from sentiment_analysis.py

main()
