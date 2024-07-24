import os
# import time
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


prompt = f"""
回答は日本語でおねがいします。
あなたのタスクは、提供された食材リストに基づいてレシピを提案することです。私が食材を提供するので、その食材を使ったレシピを考えてください。

以下が使用できる食材です:

<ingredients>
{{INGREDIENTS}}
</ingredients>
まず、これらの食材を使用したレシピのアイデアをいくつか考えてください。アイデアを<brainstorming>タグ内に書き出してください。少なくとも3つ、多くても5つのアイデアを出してください。提供された食材をできるだけ多く使うレシピに焦点を当ててください。
<brainstorming>
...
</brainstorming>
次に、ブレインストーミングに出力した各レシピアイデアについて、それぞれの詳細を以下の形式で書き出してください。
<recipe>
<recipe_name>...</recipe_name>
<recipe_description>
...
</recipe_description>
<ingredients>
<ingredient>
<ingredient_name>食材1</ingredient_name>
<ingredient_amount>...</ingredient_amount>
</ingredient>
<ingredient>
<ingredient_name>食材2</ingredient_name>
<ingredient_amount>...</ingredient_amount>
</ingredient>
...
</ingredients>
<instructions>
1. ステップ1の指示... (調理時間、温度、技術の詳細)
2. ステップ2の指示...
...
</instructions>
</recipe>
注意点:
回答は日本語で提供してください。
recipe_descriptionは、ユーザーが興味を持つような、レシピの魅力を伝える文章にしてください。
レシピの指示は非常に詳細にしてください。
各材料の切り方、調理時間、温度、技術、各食材を加えるタイミングなどを明確に記載してください。
レシピで使用する食材の量は、そのレシピが作る分量に対して適切であることを確認してください。
ブレインストーミング、スクラッチパッド、最終レシピを含む完全な回答を<result>タグ内に提供してください。
<result>
...
</result>
"""

def generate_recipi(ingredients: list[str]):
    # print("Welcome to the Groq Chatbot! Type 'exit' to end the conversation.")

    # Initialize chat history with the initial prompt
    chat_history = [
        {"role": "system", "content": prompt}
    ]

    # Add the user's message to the chat history
    chat_history.append({"role": "user", "content": "、".join(ingredients)})

    # Record the start time
    # last_time = time.time()

    # Create the completion request with the chat history
    stream = client.chat.completions.create(
        messages=chat_history,
        model="llama3-70b-8192",
        temperature=0.8,
        max_tokens=10000,
        top_p=1,
        stop=None,
        stream=True,
    )

    # Print the incremental deltas returned by the LLM.
    ai_response = ""
    print(f"responce: ", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            ai_response += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
        # last_time = time.time()

    # Add the AI's response to the chat history
    chat_history.append({"role": "assistant", "content": ai_response})
    return ai_response

if __name__ == "__main__":
    generate_recipi(["にんじん", "ジャガイモ", "玉ねぎ"])