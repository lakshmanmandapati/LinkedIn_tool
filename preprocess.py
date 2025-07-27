import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def process_posts(raw_file_path, processed_file_path=None):
    """
    Processes a JSON file of raw posts, extracts metadata,
    unifies tags, and saves the enriched posts to a new JSON file.
    """
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            print(f"Processing post: {post['text'][:50]}...") # Added for visibility
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    print("Extracting unified tags...") # Added for visibility
    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post.get('tags', []) # Use .get to handle cases where 'tags' might be missing
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags} # Use .get for robustness
        post['tags'] = list(new_tags)

    if processed_file_path:
        with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
            json.dump(enriched_posts, outfile, indent=4)
        print(f"Processed posts saved to {processed_file_path}") # Added for visibility
    else:
        print("Processed file path not provided. Returning enriched posts.")
        return enriched_posts


def extract_metadata(post_content): # Renamed 'post' to 'post_content' for clarity with the parameter
    """
    Uses an LLM to extract line count, language, and tags from a single post.
    """
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:
    {post_content}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm # Assuming 'llm' is a properly configured LangChain LLM model
    response = chain.invoke(input={"post_content": post_content})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        print(f"OutputParserException in extract_metadata for post: {post_content[:50]}... Error: {e}")
        # Optionally, return a default/empty metadata or re-raise more specific exception
        return {"line_count": 0, "language": "unknown", "tags": []} # Fallback for parsing errors
    except Exception as e:
        print(f"An unexpected error occurred in extract_metadata for post: {post_content[:50]}... Error: {e}")
        return {"line_count": 0, "language": "unknown", "tags": []}
    return res


def get_unified_tags(posts_with_metadata):
    """
    Identifies unique tags across all posts and uses an LLM to unify them.
    """
    unique_tags = set()
    for post in posts_with_metadata:
        # Ensure 'tags' key exists and is iterable
        if 'tags' in post and isinstance(post['tags'], list):
            unique_tags.update(post['tags'])

    if not unique_tags:
        print("No unique tags found for unification.")
        return {} # Return empty mapping if no tags

    unique_tags_list = ','.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with the following requirements,
    1. Tags are unified and merged to create a shorter list.
       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search".
       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
       Example 5: "AI", "Artificial Intelligence" can be mapped to "Artificial Intelligence"
       Example 6: "Hackathon", "Coding Challenge" can be mapped to "Hackathon"
       Example 7: "Internship", "Intern" can be mapped to "Internship"
       Example 8: "Industrial Visit", "Factory Tour" can be mapped to "Industrial Visit"
       Example 9: "Tech News", "Technology Updates" can be mapped to "Tech News"
    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
    3. Output should be a JSON object, No preamble
    4. Output should have mapping of original tag and the unified tag.
       For example: {{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}

    Here is the list of tags:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm # Assuming 'llm' is a properly configured LangChain LLM model
    response = chain.invoke(input={"tags": str(unique_tags_list)})
    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException as e:
        print(f"OutputParserException in get_unified_tags for tags: {unique_tags_list[:100]}... Error: {e}")
        return {tag: tag for tag in unique_tags} # Fallback: return original tags if parsing fails
    except Exception as e:
        print(f"An unexpected error occurred in get_unified_tags for tags: {unique_tags_list[:100]}... Error: {e}")
        return {tag: tag for tag in unique_tags}
    return res


if __name__ == "__main__":
    # --- CHANGE THESE FILENAMES ---
    raw_input_file = "data/student_posts.json"
    processed_output_file = "data/processed_student_posts.json"
    # -----------------------------

    print(f"Starting processing for {raw_input_file}...")
    process_posts(raw_input_file, processed_output_file)
    print("Processing complete.")