# Doctor-Appointment Bot

This is an example chatbot demonstrating how to build AI assistants for scheduling doctor Appointment. This starter pack can be used as a base for your own development or as a reference guide for implementing common Appointment features with Rasa. It includes pre-built intents, actions, and stories for handling conversation flows like scheduling and cancelling appointments and storing information in database.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Doctor Appointment Example Bot](#Doctor-Appointment-example-bot)
  - [Install dependencies](#install-dependencies)
  - [Run the bot](#run-the-bot)
  - [Overview of the files](#overview-of-the-files)
  - [Things you can ask the bot](#things-you-can-ask-the-bot)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install dependencies

Run:
```bash
pip install -r requirements.txt
```

To install development dependencies:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

> With pre-commit installed, the `black` and `doctoc` hooks will run on every `git commit`.
> If any changes are made by the hooks, you will need to re-add changed files and re-commit your changes.

## Run the bot

Use `rasa train` to train a model.

Then, to run, first set up your action server in one terminal window:
```bash
rasa run actions
```

In another window, run the duckling server (for entity extraction):
```bash
docker run -p 8000:8000 rasa/duckling
```

Then to talk to the bot, run:
```
rasa shell --debug
```


Note that `--debug` mode will produce a lot of output meant to help you understand how the bot is working
under the hood. To simply talk to the bot, you can remove this flag.

## Setting the database


Install MySQL in your RASA Environment

Setup the database by creating localhost

```bash
mysql -u root -p
```
Create database containing columns PatientName, AppointmentDate, time



## Overview of the files

`data/core.md` - contains stories

`data/nlu.md` - contains NLU training data

`actions.py` - contains custom action/api code

`domain.yml` - the domain file, including bot response templates

`config.yml` - training configurations for the NLU pipeline and policy ensemble

`tests/e2e.md` - end-to-end test stories

`database.connectivity.py` - for database queries


## Things you can ask the bot

The bot currently has the following skills. You can ask it to:
1. You can ask it to book appointments.
2. You can ask it to cancel appointments.
3. You can ask it to book for testing.
4. The bot keeps updating the information in the database.


You can change any of these by modifying `actions.py` and the corresponding NLU data.

## RASA UI

For final UI experience type and run

```bash
rasa x
```
