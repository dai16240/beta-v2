![logo](static/icon.png)
# betA

#### Soccer predictions API

betA is an API that provides predictions for soccer games.
It scrapes regularly previous outcomes from [agones.gr](https://agones.gr) using [Scrapy](https://scrapy.org/).
Constructs a [Naive Bayes Classifier](https://scikit-learn.org/stable/modules/naive_bayes.html) and predicts the outcomes of "today's" soccer games.

Built with Flask/Python.

Check it out live [here](https://beta-v2.herokuapp.com)!