# Q - You'll never have to stand in line again!

Q is an online queue management system. Organizers can create queues for their events. Instead of waiting in line, people can register themselves in a virtual queue. This delocalizes the waiting process and allows people to be productive in the time that they would otherwise spend waiting. This gives organizers great flexibility in using Q. One can set up queues for anything from doctor's appointments to food distribution.

One particular use cases that inspired us: food distribution at hackathons. Standing in line for food at hackathons is painfully annoying, and takes away from time that would be better spent hacking. Q would allow people to queue up for food, all from the comfort of their chairs.

The backend for the project is a Flask server which processes incoming HTTP requests from Twilio (to respond to incoming user messages), and sends messages out to users. The Flask server also does the job of maintaining the queue as a simple Python data structure. The organizer interface is written with simple HTML/CSS/JavaScript, and has access to the "next person" option, which pops the first user, notifies them by SMS, and updates the queue. Skeleton.css is used to give the UI a sleek, polished feel.

Users interact with the queue through text messages on their mobile phones. They can interact with the queue with three commands: "<NAME>", "DEL", and "POS". Sending their name will add them to the queue. Sending "DEL" will delete the person from the queue, and "POS" will return the person's position in the queue.

Whenever "next person" is clicked by an organizer, AJAX is used to send a "GET" request to a Python script on the Flask server, which then performs the task of messaging. The server is exposed to Twilio using ngrok.

Future plans:
1. Give users the capacity to change their position in the queue by reporting delays.
2. Use a dedicated database to store the queue, rather than using the RAM of the Python script. This will help support scale-up
3. More freedom for organizers to control the queue: adding events, manually interacting with the queue, etc.

All of the code for this project was written during the HackTech 2016. The web app is currently fully functional.

- A project by Aditya Baradwaj and Jordan Hart
