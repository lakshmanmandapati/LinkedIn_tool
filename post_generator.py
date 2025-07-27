from llm_helper import llm
from few_shot import FewShotPosts
from langchain_core.prompts import PromptTemplate

# Initialize the FewShotPosts class with the path to your processed student data
few_shot = FewShotPosts(file_path="data/processed_student_posts.json")


def get_length_str(length_category):
    """
    Converts a length category (Short, Medium, Long) into a descriptive line count string.
    This aligns with the categorization logic in FewShotPosts.
    """
    if length_category == "Short":
        return "1 line"
    if length_category == "Medium":
        return "2 to 4 lines"
    if length_category == "Long":
        return "5 or more lines"
    return "" # Default for unexpected categories


def generate_post(topic, length, language):
    """
    Generates a LinkedIn post using few-shot learning based on the provided topic,
    desired length, and language.

    Args:
        topic (str): The desired topic for the post (should be one of the unified tags).
        length (str): The desired length category ("Short", "Medium", "Long").
        language (str): The desired language ("English", "Hinglish").

    Returns:
        str: The generated LinkedIn post content.
    """
    prompt_template = get_prompt(topic, length, language)
    # Using LangChain's invoke method with a dictionary input for prompt variables
    response = llm.invoke(prompt_template.format(user_topic=topic, user_length_str=get_length_str(length), user_language=language))
    return response.content


def get_prompt(topic, length_category, language):
    """
    Constructs the few-shot prompt for the LLM, including instructions,
    examples, and the user's current request.

    Args:
        topic (str): The desired topic for the post.
        length_category (str): The desired length category ("Short", "Medium", "Long").
        language (str): The desired language ("English", "Hinglish").

    Returns:
        PromptTemplate: A LangChain PromptTemplate object.
    """
    length_str = get_length_str(length_category)

    # Base instruction for the LLM, setting the persona and general rules
    base_instruction = f'''
You are an AI assistant that generates LinkedIn posts in the style of a passionate tech student.
Your posts should reflect enthusiasm for new technologies, AI tools, hackathons, projects, internships, and industrial visits.
Generate the post in the specified Language. If Language is Hinglish, blend Hindi and English naturally.
Ensure the post matches the requested topic and length.
Do not include any preamble or conversational text, just the generated post.
'''

    # Fetch relevant examples from your processed student posts
    # We'll try to get up to 2 examples that match the requested criteria
    examples = few_shot.get_filtered_posts(length_category, language, topic)

    # Construct the few-shot examples part of the prompt
    example_section = ""
    if len(examples) > 0:
        example_section += "\nHere are some examples of posts in the desired style, topic, length, and language:"
        for i, post in enumerate(examples):
            example_section += f'\n\nExample {i+1} - Input:\nTopic: {topic}\nLength: {length_category}\nLanguage: {language}\nExample {i+1} - Output:\n"{post["text"]}"'
            if i == 1: # Limit to max two samples to keep prompt concise
                break
    else:
        example_section += "\nNo specific examples found for this combination of topic, length, and language. I will generate a post based on the general student tech enthusiast style."


    # Construct the final prompt template
    full_template = base_instruction + example_section + f'''

Your Task - Input:
Topic: {{user_topic}}
Length: {{user_length_str}}
Language: {{user_language}}
Your Task - Output:
'''

    return PromptTemplate.from_template(full_template)


if __name__ == "__main__":
    # --- Example Usage for the Student Tech Persona ---

    print("--- Generating a Short, English post about AI ---")
    # Use a tag that exists in your processed_student_posts.json
    # Example tags from your output: 'Artificial Intelligence', 'Tech Event', 'Internship', 'Hackathon'
    post_ai_short = generate_post("Artificial Intelligence", "Short", "English")
    print(post_ai_short)
    print("\n" + "="*50 + "\n")

    print("--- Generating a Medium, Hinglish post about a Tech Event ---")
    post_tech_event_hinglish = generate_post("Tech Event", "Medium", "Hinglish")
    print(post_tech_event_hinglish)
    print("\n" + "="*50 + "\n")

    print("--- Generating a Long, English post about Internship ---")
    post_internship_long = generate_post("Internship", "Long", "English")
    print(post_internship_long)
    print("\n" + "="*50 + "\n")

    print("--- Generating a Short, English post about Quantum Computing ---")
    post_quantum_short = generate_post("Quantum Computing", "Short", "English")
    print(post_quantum_short)
    print("\n" + "="*50 + "\n")
