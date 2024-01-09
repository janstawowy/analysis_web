from website import create_app

app = create_app()
#1:14:30
if __name__ == '__main__':
    app.run(debug=True)