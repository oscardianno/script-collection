import json
from typing import Dict, List, Set


def extract_viewers(story_data: List[Dict]) -> Set[str]:
    """Extract usernames of viewers from a single story's data"""
    return {viewer["user"]["username"] for viewer in story_data}


def find_skippers(stories_data: Dict) -> Dict[int, List[str]]:
    """
    Find users who skipped watching stories by comparing consecutive stories.
    Returns a dictionary with story index and list of users who skipped that story.
    """
    story_groups = stories_data["stories"]

    if not story_groups or len(story_groups) <= 1:
        return {}

    skippers = {}

    # Process each story group
    for i in range(len(story_groups) - 1):
        current_viewers = extract_viewers(story_groups[i])
        next_viewers = extract_viewers(story_groups[i + 1])

        # Find users who viewed the current story but not the next one
        skipped_users = current_viewers - next_viewers

        if skipped_users:
            skippers[i + 1] = sorted(list(skipped_users))

    return skippers


def analyze_story_views(json_file_path: str) -> None:
    """
    Analyze story views and print out who skipped which stories.
    """
    try:
        # Try UTF-8 first
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except UnicodeDecodeError:
            # If UTF-8 fails, try with utf-8-sig (handles BOM)
            try:
                with open(json_file_path, "r", encoding="utf-8-sig") as file:
                    data = json.load(file)
            except UnicodeDecodeError:
                # Last resort: try with latin-1
                with open(json_file_path, "r", encoding="latin-1") as file:
                    data = json.load(file)

        skippers = find_skippers(data)

        if not skippers:
            print("No skips detected or insufficient data to analyze skips.")
            return

        print("\nStory Skip Analysis:")
        print("-------------------")
        for story_index, users in skippers.items():
            print(f"\nUsers who skipped story #{story_index + 1}:")
            for username in users:
                print(f"- {username}")

    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file.")
    except KeyError as e:
        print(f"Error: Missing required key in JSON structure: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example usage
if __name__ == "__main__":
    file_path = "stories_data.json"  # Replace with your JSON file path
    analyze_story_views(file_path)
