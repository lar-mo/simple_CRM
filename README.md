# Cascadia Hiking Club

### This is a simple application for viewing & editing club members & their memberships, a board of directors & its committee members, and a simple ticketing system for managing data corrections & updates.

Built with Django 3.2.5, Python 3, Javascript ES6, JQuery 3.2.1, Bootstrap 4/5, HTML5, CSS3

Hosted on AWS Lightsail with Bitnami Django 3.2.5-8

### Try: [Simple Search (William Brown)](https://www.cascadiahiking.org/search/?q=William%20Brown)

---

Structure:
A person has first and last name, a byline, a nickname, a phone number, an address.
Individuals can be associated together as a family (Person.partner)
A membership consists of at least one person, an address, type, expiration date, status, notes
The Board of Directors consists of a person, a title, committees
The Needs Review "ticket" consists of a summary, description, reason, Person (to be fixed), Membership (to be fixed), status, assigned (one of the board members)

Highlights:
TBD
