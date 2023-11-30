import openai

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

def prompting(tweets, topic="improving LGBTQIA+ rights", candidate=True):
    tweets_text = "\n".join([f"Your tweet: ### {i} ###" for i in tweets])
    # Question about candidates
    if candidate:
        question = f"""
Who do you think is doing better on {topic}, Trump or Biden?
State the candidate name without any other words in the same line.
In a new line, explain the reasons behind your answer.
"""
    # Question with topics
    else:
        question = f"""Please share your level of agreement with {topic}, with a score from 1 to 5, where 1 indicating strongly disagree and 5 indicating strongly agree.
The score should be an integer without any other words in the same line.
In a new line, explain the reasons behind your level of agreement.
"""
    # Prompt
    prompt = f'''Here are your tweets, you should try to find patterns in them and be ready to answer other questions with same attitude.
{tweets_text}

Your question is:
{question}
'''
    return prompt
