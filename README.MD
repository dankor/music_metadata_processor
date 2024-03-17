# Introduction

This is my own implementation of [Take-Home Task: Music Metadata Processing System with MusicBrainz](https://cotton-radar-ab3.notion.site/Take-Home-Task-Music-Metadata-Processing-System-with-MusicBrainz-0d0dcdd4e2af4073900ea589e0f4242b).

# Plan

## Business requirement

In a nutshell, we have to provide two basic options:

- Fetch metadata from musicbrainz web service by artist and store it in database
- Search for the most relevant song based on the keyword

*Disclaimer: I'm not 100% positive this is the valid assumption. However, it's not a big deal as we aren't delivering any business value. What we really care is a technical solution.*

## Musicbrainz API research

In order to get all relevant metadata from the site we have to investigate how this data is stored in musicbrainz. Let's use its python library to investigate as suggested. 

### Entities

Basically, there are few entities which will be useful.

#### Artist

That's very self-descriptive entity. It's an band or artist. Let's pick **Imagine Dragons** as suggested in the task. We can easily find an artist metadata using *search_artists* method. It has to return a list of artists containing the keyword, let's suggest we need one and its name should match. It has a lof of the metadata, but eventually we will need only its id and name:

```json
{
    "id": "012151a8-0f9a-44c9-997f-ebd68b5389f9",
    "name": "Imagine Dragons"
}
```

#### Release group

This is kind of album, singles, soundtracks, etc entity. For the sake of simplicity let's keep it vanilla and stick to albums only. There is a *browse_release_groups* method and it has to return a list of album metadata items. What we really care are id and title: 
```json
{
    "id": "caef5f01-8568-4573-8458-c9e99ff7c734",
    "title": "Night Visions"
}
```

#### Release

This is kind of CD products. They may be distributed over either hundred of countries or dedicated to one specific containing some remixes, editions, etc based on their strategy or other regulations. Honestly, no clue. For our purposes we need the one, let's rank them by countries count and pick only the most widely spread. *browse_releases* method returns its metadata, but according to our task this entity per se is useless, we will keep only its id to get the tracks.


#### Recording

In order to get tracks and their length we will need to work with recording entity. *browse_recordings* will provide list of items in the following format:

```json
{
  "id": "eb5913a4-c8d6-4e1c-81e5-03fed0b6a8ee",
  "title": "Amsterdam",
  "length": "241426"
}
```

### Limitation

One of the biggest limitation is you can't get more than 100 entity items per request. So you have to loop using an offset until you hit the empty array.

## Database design

We will need to perform two type of operations:

- ingest new records
- perform recording search

Due to the transactional nature of data let's keep this data normalized. Let's create three tables:

- artist
- album
- recording

Every children entity should contain foreign key of its parent and useful metadata.

As we will query recording name a lot, it's better to create an trigram index against this column to avoid full table scan every request and execute efficient text search.

Plus, I'll be using a **similarity** function to rank rows to define the most relevant name. There are more options like *Full Text Searching*, *External integration*, even you can build your own neural network. But in our case we have too short text and similarity should be efficient option since:

- it's build-in function
- It can benefit from index
- it produces more or less relevant ranking to real needs

The initialization script you can find [here](init.sql).

## Web service

I'll be using flask as it's very lightweight and popular framework.

### Endpoints

#### GET /fetch/<artist_name>

It will download and ingest all data for defined artist. It means all tables will be populated with metadata related to the specific artist. Also, It will return a table of all imported recordings.

#### GET /search/<song_keyword>

Based on the keyword value it performs the song lookup and returns a table with one row containing the most relevant recording. 

# Playground 

To play locally all you need is to clone this repo, install docker and run:

```bash
docker-compose up --build
```

[Download all Imagine Dragons metadata](http://127.0.0.1:5000/fetch/Imagine%20Dragons);

[Search the best recording match with the keyword](http://127.0.0.1:5000/search/demon);

# Unit tests

In order to run unit tests please instal pytest and execute the following command from the root directory:

```bash
pytest tests/
```

# DEMO

[Recordig file](demo.webm)

Recording is stored in this repo.

# Status

- [x] Database design
- [x] Beckend implementation
- [x] Docker deployment
- [x] Basic unit test support
- [ ] Advanced unit test support
- [x] Detailed README 
- [x] Demo Recording
- [ ] GKE deployment
- [ ] Monitoring
