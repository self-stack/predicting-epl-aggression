## 1. Predicting if a song is popular or not
*Description:* I would like to predict if a song is popular based on featurized aspects of a song (track duration, start of song fade out, tempo, etc.). I will be using Billboard chart info for the metric if a song is popular or not. I have some options here, an API I found provided Hot 100 (The US music industry standard song popularity chart), Billboard 200 (), Artists 100 ().
My Approach: Start with Logistic Regression to predict if a song is popular or not, and then model a Linear Regression to determine features of song that make a song popular.
Devilerables (How will people react): Present findngs in markdown and slides
Data: [__Million Song Database__](http://millionsongdataset.com/)
- hosted on S3
- 300GB size db
- Also availble through academic sites
- Aqcuiring small sample for simple EDA
[__Billboards API__](https://rapidapi.com/LDVIN/api/billboard-api/endpoints)
- Historical data up to 1983. Data older is inconsistent.
Nice to have: Incorporate album art for albums [__MusicBrainz Cover Art Archive API__](https://musicbrainz.org/doc/Cover_Art_Archive/API)

## 2. Predicting smoking
Description:
My Approach: Random Forest
Deliverables: markdown
Data:

## 3. Predict which two English Premier League
Description: I am trying to predict which two teams from the EPL will make it to the championship game
My Approach:
Deliverables: 
Data: [__datahub.io__](https://datahub.io/sports-data/english-premier-league#data)




## Project Scaffolding 

High Level Description
	You should answer the question of "What are you trying to do". Note, you will use ML, stats ect. You're trying to solve a problem, and as such, this bullet should focus on something that has general appeal.

Your Approach
	Here, you can get into the specifics of what type of modeling you'd like to employ. It's reasonable to say that your approach may be informed by the EDA process, but you want to have a default plan of attack.

How will people interact with your work
	Does your project give insight into a particular domain? Maybe you should try to build a flask dashboard. If you're able to generate new predictions based on some limited data, a rest endpoint that people can pull up on their phones is really great here. If you want more of a narrative format, slides or excellently marked down notebooks can work here. Give some justification for how you'd like to present your work. n.b. - don't just put slides because you are concerned about time. You can always use this as a fall back if things slide, but be adventurous at the project outset.

What are your data sources
	You'll want to have specific sources of data identified. You can either use web scrapping or APIs to collect data. If it's the latter, you should probably use the API during the proposal process to ensure the dataset has the right fields to address your problems. Also note, that one week is short timeline for going through an entire project. As such, you should have every bite of data on day one of capstones. As your thinking about choosing between projects, collecting as much data on each topic is really useful in helping to inform what is possible.
