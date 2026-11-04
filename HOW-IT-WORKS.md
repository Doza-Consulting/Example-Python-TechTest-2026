# Escape Queue technical assessment: how it works

Thanks for taking the time to do this with us. This page explains what to
expect, so there are no surprises on the day.

## What this is

A paired-programming exercise. You'll work on a small, real application with
one or two of our engineers alongside you. We aren't trying to catch you out.
We want to see how you think, how you approach a problem, and how you explain
your decisions.

**You are not expected to finish everything.** A clear explanation of what you
did, and why, matters more than a long list of finished work you can't explain.

The technical exercise will take 1 hour and after that we will have a discussion
about how you think the exercise went and just review the changes that you made. 
Again, this is not to catch you out. The aim is to review the work as you would
any PR.

## The application

Escape Queue is a booking app for a chain of escape room venues. It has:

- `api/`: a FastAPI (Python) API
- `ui/`: a React + Vite + TypeScript front end
- `terraform/`: AWS infrastructure (S3 + CloudFront, Lambda, DynamoDB)

The root `README.md` explains how to run it. You don't need to read all of
the code before we start.

## How the tasks work

At the start of the session we'll give you a list of tasks to choose from. We'll
talk through your choice together, and tell you which branch to start from.

You may work on more than one task if time allows, but one done well is better
than several half-done.

## Before the session

Please have these ready, and tell us now if anything is a problem:

- Python 3.12 or newer (with `venv` and `pip`)
- Node.js 22.13 or newer, and npm
- Git, and a code editor you're comfortable in
- Access to the repository we send you for the session

Check it works:

```bash
git clone <repo-url>
cd <repo-folder>
make install               # API virtualenv + UI dependencies
make test                  # run all tests
make dev                   # API on :3000, UI on :5173
```

`make help` lists every command.


## Working in git

- Start from the branch we tell you to, then create your own working branch:

  ```bash
  git checkout -b your-name/your-task
  ```
- Commit as you go, with messages that explain what and why.
- Please don't push to `main` or to any shared branch. Push your own working
  branch if we ask you to.

## Tips for during the session

- **Talk us through it.** Say what you're thinking before you start typing.
  Saying "I'm not sure, here are the options" is a good thing to do.
- **Ask questions.** Requirements are deliberately a little open, as they are
  in real work. Ask us what you'd ask a teammate.
- **Make trade-offs visible.** If you cut a corner, say so and say what you'd do
  with more time.
- **Tests matter.** Wherever it fits the task, show us how you'd check your work.
- **It's collaborative.** Your pair can help, push back or suggest, just as a
  colleague would.

## AI
We are happy for you to use AI in the technical exercises. We only ask that you
communicate and tell us what you are using AI for and how you plan on making use of the AI. 
The most important thing that we are looking for is how you work and how you understand 
the solution that you implement. There is no point using AI if you just pointlessly accept 
all of its suggestions without reviewing and understanding what has been produced.

## What we're looking for

- how you break a problem down and decide what to do first
- code that is clear and sensible for the size of the problem
- how you handle edge cases, errors and testing
- how you communicate, and how you respond to questions and feedback
- honest judgement about what is done, what isn't, and what you'd do next

We are not looking for perfect code, the most features, or clever tricks.

## After the session

We'll ask you to demo what you have done in the hour, we will then spend some time discussing and reviewing your solution. Following the technical exercise we will have a short comfort break and then move on to a chat about your previous experience.
