from flask import Flask, render_template, request, redirect, url_for
import json
import os 


app = Flask(__name__)


def read_json(file_path):
    """generates absolute path for blog_posts.json and returns the data in it"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, file_path)
        
        with open(full_path, "r") as file:
            data = json.load(file)
            print(f"Loaded data successfully from: {file_path}")
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error while parsing JSON: {e}")
        return []
    
def add_post_to_json(blog_posts, new_post):
    """Adds a new post to the blog posts dictionary"""
    if not blog_posts:
        new_id = 1
    else:
        new_id = max(int(key) for key in blog_posts.keys()) + 1
    blog_posts[str(new_id)] = new_post
    return blog_posts
    
def delete_post_from_json(blog_posts, post_id):
    """Deletes a post from the blog posts dictionary"""
    if str(post_id) in blog_posts:
        del blog_posts[str(post_id)]
    return blog_posts

def write_json(file_path, data):
    """Writes data to JSON file"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, file_path)
        with open(full_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved successfully to: {file_path}")
    except Exception as e:
        print(f"Error writing to JSON: {e}")

@app.route('/')
def index():
    """returns the blog entries from json"""
    blog_posts = read_json("blog_entries.json")
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        #grab all inputs from form
        title = request.form['title']
        author = request.form['author']
        date = request.form['date']
        content = request.form['content']
        
        # build new post
        new_post = {
            "title": title,
            "author": author,
            "date": date,
            "content": content
        }
        
        blog_posts = read_json("blog_entries.json")
        updated_posts = add_post_to_json(blog_posts, new_post)
        write_json("blog_entries.json", updated_posts)
        return redirect(url_for('index'))
    
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = read_json("blog_entries.json")
    if str(post_id) in blog_posts:
        del blog_posts[str(post_id)]
    
    write_json("blog_entries.json", blog_posts)
    return redirect(url_for('index'))
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
