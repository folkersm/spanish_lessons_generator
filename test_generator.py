#test
import google.generativeai as genai
import json

API_KEY = "AIzaSyDG9w2RXn7ndX8dFUdS_0R0jaJVerohJvg"
genai.configure(api_key =  API_KEY)
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")
themes = [
    "Life Story",
    "Communication & The Mail",
    "Daily Schedule",
    "Family",
    "Jobs",
    "Education",
    "Language Exchange Topics about… Languages!",
    "Home Life",
    "Events & Parties",
    "Politeness",
    "History",
    "Friends and Dating",
    "Food",
    "Religion and Politics",
    "Holidays",
    "Myths and Paranormal",
    "Pastimes and Hobbies",
    "Sports and the Outdoors",
    "Health and Healthcare",
    "Climate, Geography, and Urban Life",
    "Travel and Tourism",
    "Fashion and Style",
    "Art and Music",
    "Books and Literature",
    "Movies and Shows",
    "Plants and Animals",
    "The Internet",
    "Technology",
    "Spaces and Physics",
    "Self-care and Growth"
]

def prompt_gen(level, theme):
    first_part = "For a spanish learning exercise, write 30 sentences in spanish that an "
    middle_part = " spanish speaker could understand on the theme of "
    third_part = ". Choose a random verb, preposition, noun, or adjective in the sentence which will be the correct word surrounding it with two asterisks on both sides of the word. Then generate three incorrect words which would not make grammatical sense in place of the correct word. "
    last_part = " Return a json object with the sentence string, correctWord string, incorrectWords array. "    
    output_prompt = first_part + level + middle_part + theme + third_part + last_part
    return output_prompt

from pydantic import BaseModel, TypeAdapter
class Sentence(BaseModel):
    sentence: str
    wrong_words: list[str]
    correct_word: str

    # for i in range(30):
        # theme = themes[i]
        # response = model.generate_content("Write 30 sentences in spanish that an A1 speaker could understand on the theme of " + themes[0] + ". Then remove one word, replacing it with underscores. Then put the sentence in a json format with sentence, correct_word, incorrect_words, with the removed word as correct word, and create 3 spanish words that are incorrect and put them in a list for incorrect_words.")
        # file.write(theme)
# with open("a1_raw.txt", "w") as file:
    # file.write("test")
# import json
import re

def extract_json_array(response_text):
    # Find the first '['
    start = response_text.find("[")
    if start == -1:
        raise ValueError("No opening bracket '[' found.")

    # Find the matching closing ']', accounting for nested structures
    bracket_count = 0
    end = -1
    for i in range(start, len(response_text)):
        if response_text[i] == "[":
            bracket_count += 1
        elif response_text[i] == "]":
            bracket_count -= 1
            if bracket_count == 0:  # Found the matching closing bracket
                end = i
                break

    if end == -1:
        raise ValueError("No matching closing bracket ']' found.")

    # Extract the JSON array substring
    json_text = response_text[start:end + 1]

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing extracted JSON: {e}")


data = {}
level = "A1"

# response = model.generate_content(prompt_gen(level, themes[0]))
# print(f"Response for {themes[0]}: {response}")
for i in range(30):
    theme = themes[i]
    print("here")
    response = model.generate_content(prompt_gen(level, themes[i]))  # Get the response from the model
    print(response.text)
    print()
    print("printed response")
    response_text_array = extract_json_array(response.text)
    data[theme] = response_text_array

with open("a1_sentences.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# Print the response
# print(response.text)
