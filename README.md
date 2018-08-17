# Scrape Optimizely Classic Results
By running this Python script in your own Python 3 environment you will be able to get all of your Optimizely Classic Experiment Results organized in one CSV file.

## Steps
If you have Python 3 downloaded and installed on your computer then begin with step 1, if not, download and install Python 3 on your computer [here](https://www.python.org/downloads/)

In your CLI
1. Clone this github repository
2. cd into the scrape_optimizely_classic_results directory
* Optional: Activate your virtual environment
3. Run
```
pip3 install requests
```
4. Generate your own [Optimizely v1 REST API Token](https://help.optimizely.com/Integrate_Other_Platforms/Generate_an_API_token_in_Optimizely_Classic)
5. Run
```
python3 app.py <your API Token>
```

The script can take up to 8 hours to run if there are 200+ experiments in the account. Once it is finished, all of your Optimizely Classic experiment results should be in a csv file called Optimizely_Classic_Experiment_Results.csv in the scrape_optimizely_classic_results directory.
