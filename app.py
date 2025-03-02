import bottle
import routes

app = routes.app

if __name__ == '__main__':
  app.run(host='localhost', port=8080)