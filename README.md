# draft-wisely
A classification model for determining a fantasy football team's success given their draft strategy

## Background


## Creating the Dataset

Sleeper's API is among the best in fantasy sports (one of the reasons we chose them), but they don't make it particularly easy to access the data of public leagues for which you do not already know the league ID. This ID is an 18 digit number, apparently randomly generated, so simply looping through all possible IDs and sending a request for each will quickly get you IP blocked. I needed a better approach to grab the data from as many leagues as possible.

I had the idea of starting with just 1 league - my own - and getting all of its users. Then, take each of those users and find all of their leagues (there is a request for this), since many fantasy players, myself included, play in multiple leagues. With this new, larger set of leagues, find all of the users in them, and keep repeating this until either a desired number of leagues is reached, or until the lists stop growing. 

```
Iteration 0:

Finding new users...
Found 12

Finding new leagues...
Found 2
Found 1
Found 2
...
```
The success of this method depends on some level of interconnectivity between players, so I wasn't sure I would get anywhere before stalling. Surprisingly enough, starting with 1 league, I had a list of over 2,000 league IDs after only 6 iterations.
```
...
Found 46
Found 3
Found 7
Found 21
Found 4
Found 10
Found 1
Found 2
Found 7
Found 18

Number of leagues after iteration 5: 2003
```

With a sizable list of real league IDs, I could build the dataset I needed for analysis. For each of those leagues, I needed to know, for each team, which position they drafted in each round of the league's draft, in addition to some league parameters for filtering and segmentation. It was important to start with a larger-than-needed leagues of leagues because many will be filtered out. Namely, those that do not meet the following conditions:

  1. 1 QB roster slot 
  2. The draft is at least 12 rounds
  3. Each player has a pick in the first 12 rounds



| user_id   | league_id |
| --------- | --------- |
|  string   | Content Cell  |
