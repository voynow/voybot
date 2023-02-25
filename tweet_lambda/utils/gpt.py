
import openai
import utils.secrets_manager as secrets_manager

openai.api_key = secrets_manager.get_secrets()['openai_secret_key']


def gpt_completion(
    model_engine,
    prompt,
    max_tokens=85,
    temperature=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    n=1,
    stop=None,
):

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        frequency_penalty=frequency_penalty, 
        presence_penalty=presence_penalty,
        n=n,
        stop=stop,
    )
    return completions.choices


def clean_gtp_response(body):
    """ Convert GPT response into realistic tweet text
    """
    msg = None
    tweet = body[0].text

    # Clean up space generated by text completion
    if "\n\n" in tweet:
      tweet = tweet.split("\n\n")[1]

    # remove double hashtag
    tweet = tweet.replace("##", "#")
    
    # Sometime GPT puts its response in a quote
    tweet = tweet.replace("\"", "")

    # do not tweet with these strngs
    invalid_strings = ["2020", "COVID", "pandemic"]
    for string in invalid_strings:
        if string in tweet:
            msg = f"InvalidStringError: {string}"

    # max tweet length == 280
    tweet_len = len(tweet)
    if tweet_len > 280:
        msg = f"InvalidLengthError: {tweet_len}"

    # invalid tweets will contain msg attribute
    if msg:
        return {"msg": msg, "tweet": tweet}
    else:
        return {"tweet": tweet}


def gen_tweet(model_engine: str, prompt: str):
    """ Generate tweet given engine and prompt
    """
    body = gpt_completion(
        model_engine,
        prompt,
        frequency_penalty=2,
        presence_penalty=2)
    return clean_gtp_response(body)