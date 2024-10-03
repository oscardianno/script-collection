import csv
import json
import os
import re
from collections import defaultdict


def clean_album_name(album_name):
    # List of words and patterns to remove
    patterns_to_remove = [
        r"\(Remastered.*?\)",
        r"\(Deluxe.*?\)",
        r"\(Expanded.*?\)",
        r"\(Bonus.*?\)",
        r"\(Anniversary.*?\)",
        r"\(Live.*?\)",
        r"\[.*?\]",  # Remove anything in square brackets
        r"\d{4}",  # Remove years
        "Edition",
        "Remaster",
        "Version",
    ]

    # Apply all patterns
    cleaned_name = album_name
    for pattern in patterns_to_remove:
        cleaned_name = re.sub(pattern, "", cleaned_name, flags=re.IGNORECASE)

    # Remove extra whitespace and trim
    cleaned_name = " ".join(cleaned_name.split()).strip()

    return cleaned_name, cleaned_name != album_name


def process_file(file_path, album_data, cleaned_albums):
    print(f"Processing file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for track in data:
            if (
                track["master_metadata_album_album_name"]
                and track["master_metadata_track_name"]
            ):
                original_album_name = track["master_metadata_album_album_name"]
                album_name, was_cleaned = clean_album_name(original_album_name)
                if was_cleaned:
                    cleaned_albums[original_album_name] = album_name

                track_name = track["master_metadata_track_name"]
                ms_played = track["ms_played"]
                skipped = track["skipped"]

                if (
                    not skipped and ms_played >= 30000
                ):  # Consider it a complete stream if played for at least 30 seconds
                    album_data[album_name]["tracks"][track_name] += 1
                    album_data[album_name]["total_streams"] += 1
                    album_data[album_name]["total_ms"] += ms_played
    print(f"Finished processing file: {file_path}")


def analyze_spotify_history(folder_path):
    album_data = defaultdict(
        lambda: {"tracks": defaultdict(int), "total_streams": 0, "total_ms": 0}
    )
    cleaned_albums = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            process_file(file_path, album_data, cleaned_albums)

    # Calculate scores and prepare results
    results = []
    for album, data in album_data.items():
        unique_tracks = len(data["tracks"])
        total_streams = data["total_streams"]
        total_hours = data["total_ms"] / (1000 * 60 * 60)  # Convert ms to hours

        # Score calculation: balance between unique tracks and total streams
        score = (unique_tracks * 0.6) + (total_streams * 0.4)

        results.append(
            {
                "album": album,
                "unique_tracks": unique_tracks,
                "total_streams": total_streams,
                "total_hours": round(total_hours, 2),
                "score": score,
            }
        )

    # Sort results by score in descending order
    results.sort(key=lambda x: x["score"], reverse=True)
    return results, cleaned_albums


def save_results(results, filename="spotify_analysis/results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "album",
                "unique_tracks",
                "total_streams",
                "total_hours",
                "score",
            ],
        )
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"Results saved to {filename}")


def save_cleaned_albums(
    cleaned_albums, filename="spotify_analysis/cleaned_album_names.csv"
):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Original Album Name", "Cleaned Album Name"])
        for original, cleaned in cleaned_albums.items():
            writer.writerow([original, cleaned])
    print(f"Cleaned album names saved to {filename}")


def print_results(results, top_n=20):
    print(f"Top {top_n} Albums:")
    for i, album in enumerate(results[:top_n], 1):
        print(f"{i}. {album['album']}")
        print(f"   Unique Tracks: {album['unique_tracks']}")
        print(f"   Total Streams: {album['total_streams']}")
        print(f"   Total Hours: {album['total_hours']}")
        print(f"   Score: {album['score']:.2f}")
        print()


if __name__ == "__main__":
    folder_path = input("Enter the path to your Spotify data folder: ")

    results, cleaned_albums = analyze_spotify_history(folder_path)
    print_results(results)

    os.makedirs("spotify_analysis", exist_ok=True)
    save_results(results)
    save_cleaned_albums(cleaned_albums)
