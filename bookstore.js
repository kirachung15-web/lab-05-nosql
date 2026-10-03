// Step 2: switch to bookstore database
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: display all books
db.books.find()

// Step 6: add two books
db.books.insertMany([
  {
    title: "The Great Gatsby",
    published_year: 1925,
    author_ids: ["author_004"]
  },
  {
    title: "1984",
    published_year: 1949,
    author_ids: ["author_005"]
  }
])

// Step 7: add the missing authors
db.authors.insertMany([
  {
    _id: "author_004",
    name: "F. Scott Fitzgerald",
    nationality: "American",
    bio: {
      short: "American novelist and short-story writer.",
      long: "F. Scott Fitzgerald was an American writer best known for novels about the Jazz Age, including The Great Gatsby."
    }
  },
  {
    _id: "author_005",
    name: "George Orwell",
    nationality: "British",
    bio: {
      short: "British novelist, essayist, and journalist.",
      long: "George Orwell was a British writer known for works examining politics and society, including 1984 and Animal Farm."
    }
  }
])

// Step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })