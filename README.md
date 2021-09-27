# Cascadia Hiking Club

### This is a simple application for viewing & editing club members & their memberships, a board of directors & its committee members, and a simple ticketing system for managing data corrections & updates.

Built with Django 3.2.5, Python 3, Javascript ES6, JQuery 3.2.1, Bootstrap 4/5, HTML5, CSS3

Hosted on AWS Lightsail with Bitnami Django 3.2.5-8

### Try: [Simple Search (William Brown)](https://www.cascadiahiking.org/search/?q=William%20Brown)

---

### Structure
* A person has first and last name, a byline, a nickname, a phone number, email and physical address (FK), and partner (optional FK)
* Two individuals are manually associated with each other (Person.partner)
* A membership consists of at least one person, an address, type, expiration date, status, notes
* The Board of Directors consists of a person, a title, committees
* The Needs Review "ticket" consists of a summary, description, reason, Person (to be fixed), Membership (to be fixed), status, assigned (one of the board members)

### Highlights
* This is the first time I've used AWS for hosting & DNS + the Bitnami Django env
* Experiementing with new template tags and user permissions
* Learning about search functionality & logic is the Q library

### Known Issues
* CSS is a very unorganized and cluttered with obsolete classes & ids
* The Mobile design is an afterthought.
* The way 2 people are associated with each other (partner) is vulnerable data corruption leading to errors on the views or front-end. 
