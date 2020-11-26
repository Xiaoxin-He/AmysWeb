from app import app, db
from app.models import User, Product,admin

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'admin': admin}

if __name__ == '__main__':
    app.run(debug=True)

# if __name__=="__main__":
#     app.run()
