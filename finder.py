import json
from collections import defaultdict


def find_traits_sources(traits):
    # Load the data from the file
    with open("results.json", "r") as f:
        data = json.load(f)

    # Create a dictionary to store the results
    results = defaultdict(list)

    # Iterate over the traits
    for trait in traits:
        # Iterate over the data
        for main_title, sub_titles in data.items():
            for sub_title, traits_list in sub_titles.items():
                # If the trait is in the list of traits for the current subtitle
                if trait in traits_list:
                    # Add the main title and subtitle to the results
                    results[trait].append(f"{main_title}/{sub_title}")

    return results


# Test the function
traits = ["M0112942", "M0004714", "M0005017"]
print(find_traits_sources(traits))
