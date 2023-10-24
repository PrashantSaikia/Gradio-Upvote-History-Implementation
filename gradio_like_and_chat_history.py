import gradio as gr
import json, pandas, datetime, random

def append_row(df, row):
    return pandas.concat([
                df, 
                pandas.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)

def vote(data: gr.LikeData, history):
    df = pandas.DataFrame(columns=['Query', 'Response', 'Upvote', 'Time'])

    if data.liked:
        query = history[data.index[0]][data.index[1]-1]
        response = data.value
        upvote = 1
        time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        new_row = pandas.Series({'Query': query, 'Response': response, 'Upvote': upvote, 'Time': time})
        df = append_row(df, new_row)

    else:
        query = history[data.index[0]][data.index[1]-1]
        response = data.value
        upvote = -1
        time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        new_row = pandas.Series({'Query': query, 'Response': response, 'Upvote': upvote, 'Time': time})
        df = append_row(df, new_row)

    # append data frame to CSV file
    df.to_csv('vote_history.csv', mode='a', index=False, header=False)

with gr.Blocks() as ui:
    with gr.Row():
        with gr.Column():
            msg = gr.Textbox(label="", placeholder="Enter a question")

            chatbot = gr.Chatbot(label=" ")
            chatbot.like(vote, chatbot, None)  # Need to the pass the chatbot as a parameter to the chatbot to get the chat history
            clear = gr.ClearButton([msg, chatbot])

        def respond(message, chat_history):
            bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
            chat_history.append((message, bot_message))            

            with open('chat_history.json', 'w') as file:
                    json.dump(chat_history, file)

            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])

ui.launch()