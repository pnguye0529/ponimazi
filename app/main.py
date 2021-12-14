from app import app
from app import db
import views
from posts.blueprint import posts

app.register_blueprint(posts, url_prefix='/list')   # localhost:5000/post

if __name__ == '__main__':
    app.run()
