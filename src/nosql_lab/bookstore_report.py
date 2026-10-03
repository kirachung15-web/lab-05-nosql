#!/usr/bin/env python3

import logging
import os

import pymongo


# Read MongoDB Atlas credentials from environment variables.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")


def main():
    """Connect to MongoDB Atlas and print a bookstore inventory report."""

    # Authors to include in the report.
    # This includes authors from the starter data and one author we added.
    author_ids = ["author_001", "author_002", "author_004"]

    client = None

    try:
        # Connect to MongoDB Atlas using environment variables.
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )

        # Confirm that the connection works.
        client.admin.command("ping")
        logging.info("Connected to MongoDB Atlas successfully.")

        # Select the bookstore database and its collections.
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count the authors in our selected list.
        author_count = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"Authors: {author_count}")

        # Find each author and print all books linked to that author.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author %s was not found.", author_id)
                continue

            print(f"\n{author['name']}")

            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

    except Exception as error:
        logging.error("MongoDB error: %s", error)

    finally:
        # Always close the MongoDB client when finished.
        if client is not None:
            client.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()