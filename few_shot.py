import pandas as pd
import json


class FewShotPosts:
    """
    A class to load and filter processed LinkedIn posts for few-shot learning.
    It categorizes post length and provides methods to filter posts by tags,
    language, and length.
    """
    def __init__(self, file_path="data/processed_student_posts.json"):
        """
        Initializes the FewShotPosts instance by loading data from the specified JSON file.

        Args:
            file_path (str): The path to the processed JSON file containing LinkedIn posts.
        """
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        """
        Loads the posts from the given JSON file into a pandas DataFrame,
        categorizes their length, and collects all unique tags.

        Args:
            file_path (str): The path to the JSON file.
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
                self.df = pd.json_normalize(posts)
                # Apply length categorization based on line_count
                self.df['length'] = self.df['line_count'].apply(self.categorize_length)

                # Collect all unique tags from the 'tags' column
                # Ensure 'tags' column contains lists, and sum them up to get all tags
                all_tags = []
                for tags_list in self.df['tags']:
                    if isinstance(tags_list, list): # Ensure it's a list before extending
                        all_tags.extend(tags_list)
                self.unique_tags = sorted(list(set(all_tags))) # Sort for consistent order
                print(f"Loaded {len(self.df)} posts from {file_path}")
                print(f"Found {len(self.unique_tags)} unique unified tags.")

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}. Please check the path.")
            self.df = pd.DataFrame() # Initialize empty DataFrame on error
            self.unique_tags = []
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {file_path}. Check file format.")
            self.df = pd.DataFrame()
            self.unique_tags = []
        except Exception as e:
            print(f"An unexpected error occurred while loading posts: {e}")
            self.df = pd.DataFrame()
            self.unique_tags = []


    def get_filtered_posts(self, length, language, tag):
        """
        Filters posts based on specified length, language, and the presence of a tag.

        Args:
            length (str): The desired length category ("Short", "Medium", "Long").
            language (str): The desired language ("English", "Hinglish").
            tag (str): A specific tag that must be present in the post's tags.

        Returns:
            list: A list of dictionaries, where each dictionary represents a filtered post.
        """
        if self.df.empty:
            print("No data loaded. Cannot filter posts.")
            return []

        df_filtered = self.df[
            (self.df['tags'].apply(lambda tags_list: tag in tags_list if isinstance(tags_list, list) else False)) &
            (self.df['language'] == language) &
            (self.df['length'] == length)
        ]
        return df_filtered.to_dict(orient='records')

    def categorize_length(self, line_count):
        """
        Categorizes the post's length based on the number of lines.

        Args:
            line_count (int): The number of lines in the post.

        Returns:
            str: The length category ("Short", "Medium", "Long").
        """
        if line_count < 2: # Adjusted for shorter LinkedIn posts
            return "Short"
        elif 2 <= line_count <= 4: # Adjusted for typical LinkedIn post medium length
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        """
        Returns a list of all unique unified tags found in the dataset.

        Returns:
            list: A list of unique tags.
        """
        return self.unique_tags


if __name__ == "__main__":
    # Initialize with the new processed student posts file
    fs = FewShotPosts(file_path="data/processed_student_posts.json")

    # Print all unique tags found in the student posts to help with filtering
    print("\nAvailable Unique Tags:")
    print(fs.get_tags())

    # Example usage: Filter for a post relevant to the student tech persona
    # Let's try to get a 'Medium' 'English' post about 'Artificial Intelligence'
    print("\nFiltering for Medium, English, Artificial Intelligence posts:")
    posts_ai = fs.get_filtered_posts("Medium", "English", "Artificial Intelligence")
    print(posts_ai)

    # Another example: A 'Short' 'Hinglish' post about 'Tech Event'
    print("\nFiltering for Short, Hinglish, Tech Event posts:")
    posts_hinglish_event = fs.get_filtered_posts("Short", "Hinglish", "Tech Event")
    print(posts_hinglish_event)

    # Example of a tag that might not exist in the student data (like 'Job Search' from old data)
    print("\nFiltering for Medium, English, Job Search posts (should be empty):")
    posts_job_search = fs.get_filtered_posts("Medium", "English", "Job Search")
    print(posts_job_search)
