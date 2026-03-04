# name: Levi Sneller
# date: 3/4/25
# description: CS178 Lab 10 - Custom databse
# proposed score: 5 (out of 5)

# ----- Book Interface Code -----
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Books')

# This function creates a new book
# This function also creates an empty rating list for reviews to be added with update
def create_book():
    title = input("What is the book title? ")
    table.put_item(
        Item={
            "Title": title,
            "Ratings": []
        }
    )
    print(f"Book '{title}' added successfully.")

# Helper function to print books
def print_book(book):
    title = book.get("Title", "Unknown Title")
    author = book.get("Author", "Unknown Author")
    year = book.get("Year", "Unknown Year")
    ratings = book.get("Ratings", [])
    print(f"  Title  : {title}")
    print(f"  Author : {author}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print()

# Function to print all books
def print_all_books():
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No books found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)

# This is used to add a review to a book
def update_rating():
    try:
        title = input("What is the book title? ")
        rating = int(input("What is the rating (0-10): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]}
        )
        print(f"Rating {rating} added to '{title}' successfully.")
    except:
        print("error in updating book rating")

# Function to delete a book
def delete_book():
    title = input("What is the book title? ")
    table.delete_item(
        Key={"Title": title}
    )
    print(f"Book '{title}' deleted successfully.")

# Function to query a book and get its publication year and author
def query_book():
    title = input("What is the book title? ")
    response = table.get_item(Key={"Title": title})
    book = response.get("Item")
    
    if book is None:
        print("book not found")
        return
    
    year = book.get("Year")
    author = book.get("Author")
    
    print(f"Published Year: ", year)
    print(f"Author: ", author)

# Menu function
def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new book")
    print("Press R: to READ all books")
    print("Press U: to UPDATE a book (add a review)")
    print("Press D: to DELETE a book")
    print("Press Q: to QUERY a book's year and author")
    print("Press X: to EXIT application")
    print("----------------------------")

# Main function
def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_book()
        elif input_char.upper() == "R":
            print_all_books()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_book()
        elif input_char.upper() == "Q":
            query_book()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()