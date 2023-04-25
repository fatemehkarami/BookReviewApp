from flask import Flask, render_template, request, redirect, url_for
import csv
import os


app = Flask(__name__)

# Define the path to the CSV file
csv_file = 'books.csv'

# Define the function to read the data from the CSV file
def read_csv():
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(data):
    fieldnames = ['id', 'title', 'author', 'rating', 'review']
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Get the last id from the CSV file and increment it by 1 to generate a new id
        if os.path.exists(csv_file):
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                last_id = max([int(row['id']) for row in reader])
        else:
            last_id = 0
        new_id = last_id + 1
        # Add the new id to the data dictionary
        data['id'] = new_id
        writer.writerow(data)


# Define the index route
@app.route('/')
def index():
    books = read_csv()
    return render_template('index.html', books=books)

# Define the show route
@app.route('/books/<int:id>')
def show(id):
    books = read_csv()
    book = [book for book in books if book['id'] == str(id)][0]
    return render_template('show.html', book=book)

# Define the create route
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get the next available ID
        books = read_csv()
        last_book_id = int(books[-1]['id'])
        next_id = last_book_id + 1

        # Create a new book object with the next available ID
        data = {
            'id': next_id,
            'title': request.form['title'],
            'author': request.form['author'],
            'rating': request.form['rating'],
            'review': request.form['review']
        }
        write_csv(data)
        return redirect(url_for('index'))
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
