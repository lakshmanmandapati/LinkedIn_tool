import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Initialize FewShotPosts with the correct processed data file
# The default path in FewShotPosts is "data/processed_student_posts.json",
# so explicit path might not be strictly necessary if few_shot.py is unchanged,
# but it's good for clarity and robustness.
fs = FewShotPosts(file_path="data/processed_student_posts.json")

# Options for length and language
# These should align with the categories defined in few_shot.py's categorize_length
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# Get the unique tags from your processed student data
# This ensures the dropdown only shows relevant topics for the student persona
tags = fs.get_tags()

# Main app layout
def main():
    """
    Sets up the Streamlit interface for the LinkedIn Post Generator.
    Allows users to select topic, length, and language, then generates a post.
    """
    st.header("LinkedIn Post Generator:LM's Edition")
    st.markdown("Generate engaging LinkedIn posts in the style of a tech-savvy student!")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    with col1:
        # Dropdown for Topic (Tags)
        # Ensure 'tags' list is not empty before creating selectbox
        if tags:
            selected_tag = st.selectbox("Topic", options=tags, help="Select a tech-related topic for your post.")
        else:
            st.warning("No tags found. Please check your processed_student_posts.json file.")
            selected_tag = None # Set to None if no tags available

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options, help="Choose the desired length of the post.")

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options, help="Select the language for the post (English or Hinglish).")

    st.markdown("---") # Separator for better UI

    # Generate Button
    if st.button("Generate Post", type="primary"): # Added primary button style
        if selected_tag: # Only generate if a tag was successfully selected
            with st.spinner("Generating your LinkedIn post..."): # Add a loading spinner
                # IMPORTANT: Corrected the order of arguments for generate_post
                # It expects (topic, length, language)
                post = generate_post(selected_tag, selected_length, selected_language)
                st.write("### Generated Post:")
                st.success(post) # Display generated post in a success box
        else:
            st.error("Cannot generate post: No topic selected. Please ensure tags are loaded correctly.")


# Run the app
if __name__ == "__main__":
    main()

