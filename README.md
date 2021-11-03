# catanstat-underhood

### WHY?

Me and my friends are big fans of the boardgame "The settlers of Catan". The best game of all time.
Due to random we wonder how often this or that dice combination befell, who was the slowpoke and the fastest player ever and other geeky stuff 🤓

So we need an app that will gather game statistics.

[@owanturist](https://github.com/owanturist) implemented [awesome fast decision](https://github.com/owanturist/catanstat), but since the data are stored in localstorage I suggested writing back-end to keep data properly.
For me it is very cool practice of my software development skills.
And now here we are!

That is not final version, it's still in progress, so you can watch and like it (or not lol 😅)

## Tech stack
- python3.9
- PostgresSQL as DB
- Flask
- SQLAlchemy
- Flasgger for documentation

## TODO
- [ ] keep on working on README
- [ ] GET methods for showing statistics
- [ ] tests
- [ ] docker containers for localhost deployment
- [ ] staging deploymant to DigitalOcean
- [ ] production deployment
- [ ] logging to file
- [ ] authorization
- [ ] deployment to AWS (just to try and figure out)
- [ ] move to non-relational DB, if needed (just to try and figure out)

