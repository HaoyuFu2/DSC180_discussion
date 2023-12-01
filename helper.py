import pandas as pd
from langdetect import detect
import seaborn as sns
import matplotlib.pyplot as plt
plt.subplots_adjust(wspace=0.5)

def sample_user(df, n=1):
    """
    Sample n unique users from the column 'user_id'

    Parameters:
        df  - pandas DataFrame where users are sampled
        n   - number of users to be sampled
    Return:
        users - a pandas Series of sampled users

    """
    users = df['user_id'].drop_duplicates().sample(n=n, random_state=1)
    return users

def sample_tweet(df, user, n=20):
    """
    Sample n tweets from the given user_id

    Parameters:
        df  - pandas DataFrame where tweets are sampled
        user- the user_id whose tweets are sampled
        n   - number of tweets to be sampled
    Return:
        a pandas Series of sampled tweets
    
    """
    df = df[df['user_id']== user]['cleaned_tweets']
    if df.shape[0] > n:
        return df.sample(n=n, random_state=1)
    else:
        return df
    
def sample_tweet_group(df, users, n=20):
    """
    Sample n tweets from each user of the given users

    Parameters:
        df      - pandas DataFrame where tweets are sampled
        users   - the user ids whose tweets are sampled
        n       - number of tweets to be sampled from each user
    Return:
        a pandas DataFrame of users with their sampled tweets
    """
    result = pd.DataFrame({'user_id':[], 'cleaned_tweets':[]})
    for u in users:
        tweets = sample_tweet(df, u, n=20)
        tweets = pd.DataFrame(tweets).assign(user_id=u)
        result = pd.concat([result, tweets])
    return result

def visualize(df, question_No, topics):
    col = 'score_topic_' + str(question_No)
    fig, ax = plt.subplots(1, 2, sharex=False, sharey=True)
    fig.suptitle('Distribution of agreement on ' + topics[question_No])
    sns.histplot(ax=ax[0], data=df[df['candidate']=='trump'], x=col, stat='percent',
                 hue='candidate', palette=['red'], discrete=True, binrange=[1,5])
    sns.histplot(ax=ax[1], data=df[df['candidate']=='biden'], x=col, stat='percent',
                 hue='candidate', palette=['blue'], discrete=True, binrange=[1,5])