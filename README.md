# Questioner-v1-redo
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintainability](https://api.codeclimate.com/v1/badges/180499f84459b335085e/maintainability)](https://codeclimate.com/github/Dave-mash/Questioner-v1-redo/maintainability)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a511c4420c0b4e6f9538e6b93814f275)](https://www.codacy.com/app/macharia3041/Questioner-v1-redo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Dave-mash/Questioner-v1-redo&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/Dave-mash/Questioner-v1-redo/badge.svg?branch=develop)](https://coveralls.io/github/Dave-mash/Questioner-v1-redo?branch=develop)
## The following are API endpoints enabling one to:
* Create an account and log in.
* Create a meetup record.
* Fetch a meetup record.
* Get all meetup records.
* Get meetup questions.
* Post a question on a meetup.
* Comment to a meetup question.
* Edit a question
* Delete a question
* Edit a meetup
* Delete a meetup
* View comments
* RSVP for a meeting
* Upvote or Downvote a question
### Prerequisites
* Python3
* Git
* Postman
### Questioner application endpoints
| Endpoint        | Functionality           | HTTP method  |
| ------------- |:-------------:| -----:|
| `/auth/signup`      | Register a user | POST |
| `/auth/login`      | Login a user       |   POST |
| `/meetup` | Post a meetup       |    POST |
| `/meetup/<meetup-id>` | Fetch a meetup       |    GET |
| `/meetups/upcoming` | Fetch all meetups       |    GET |
| `/questions` | Post a question       |    POST |
| `/questions/<questionId>` | Delete a question        |    DELETE |
| `/questions/<questionId>/comment` | Post a comment to a  question        |    POST |
| `/questions/<questionId>/upvote` | Increase votes by 1        |    PATCH |
| `/questions/<questionId>/downvote` | Decrease votes by 1        |    PATCH |
| `/meetups/<meetup-id>/rsvps` | Respond to meetup RSVP        |    POST |

### Authors
David Macharia @[Dave-mash](https://github.com/Dave-mash)
