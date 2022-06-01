from queues import app
from queues.email_server import send_email
from queues.queue import register_page, User


if __name__=='__main__':
    app.run(debug=True)



