import openai
import pandas as pd
import re

openai.api_key='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'

def chat_with_model(prompt):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-1106',
        messages=[
            {"role": "system", "content": "Your task is to discuss political election questions and provide persuasive answers with supporting reasons. Please engage in a thoughtful and informed discussion, presenting well-reasoned arguments to convince others of your perspective on political issues. Your responses should be clear, concise, and persuasive, addressing the concerns and questions raised about political elections. Consider supporting your arguments with relevant examples, statistics, or expert opinions to strengthen your persuasive approach.  Please note that your responses should be flexible enough to allow for various relevant and creative answers. You should focus on providing well-supported and convincing arguments to persuade others about the importance and significance of political elections in different contexts and scenarios."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.1
    )
    return completion.choices[0].message["content"]

def prompting(tweets, topics):
    tweets_text = "\n".join([f"Your tweet: ### {i} ###" for i in tweets])

    # Questions list
    questions = ["""Question 1: 
Do you support Donald Trump or Joe Biden in the upcoming 2020 Presidential Election?
Your answer should be the last name of a candidate without any other words.
"""
                 ]
    
    # Other questions
    for i in range(len(topics)):
        q = f"""Question {i+2}: 
Please share your level of agreement with {topics[i]}, with a score from 1 to 5, where 1 indicating strongly disagree and 5 indicating strongly agree.
The score should be an integer without any other words in the same line.
In a new line, explain the reasons behind your level of agreement.
"""
        questions.append(q)
    questions = "\n\n".join(questions)
    
    # Prompt
    prompt = f'''Here are your tweets. You should try to find patterns in them and be ready to answer other questions with same attitude.
{tweets_text}

Please deliminate your answers to each question with a new line.
Please don't include extra deliminaters, question numbers, etc.

Your questions are:
{questions}
'''
    return prompt

def generate_results(df, topics):
    results = {}
    for u in df['user_id'].unique():
        tweets = df[df['user_id']==u]['cleaned_tweets']
        prompt = prompting(tweets, topics)
        result = chat_with_model(prompt)
        results[u]=result
    return results

def parse_results(df, results, num_topics):
    # df.groupby('user_id').agg({'cleaned_tweets':prompting}).reset_index().iloc[0]['cleaned_tweets']
    
    # Initializing returning dataframe
    cols = ['user_id', 'candidate', 'hashtag']
    for i in range(num_topics):
        cols.append(f'score_topic_{i}')
    df_result = pd.DataFrame({col:[] for col in cols})

    # Parse responses for each user
    for u, r in results.items():
        ans_lst = r.split('\n')
        while(ans_lst.count('')): 
            ans_lst.remove('') 

        # unify the format of candidate name
        candidate = ans_lst[0]
        if candidate.lower() in ['donald', 'donald trump', 'trump']:
            candidate = 'trump'
        elif candidate.lower() in ['joe', 'joe biden', 'biden']:
            candidate = 'biden'
        else:
            candidate = 'N/A'

        # parse scores
        scores = re.findall(r'\n([0-9])\n', r)
        ans_dict = {'user_id': u, 'candidate': candidate, 
                    'hashtag':df[df['user_id']==u]['hashtag'].iloc[0]}
        if len(scores) > 10: scores = scores[-10:]
        for i in range(len(scores)):
            ans_dict[cols[i+3]] = scores[i]
        df_result = df_result.append(ans_dict, ignore_index=True)

    return df_result