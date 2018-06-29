import requests, csv

def scrapeResultsData():
    optimizely_token = 'CLASSIC TOKEN'

    all_project_info = {}
    all_experiment_data = {}

    # Get all projects
    all_projects = requests.get('https://www.optimizelyapis.com/experiment/v1/projects/',
                                headers={'Token': optimizely_token})
    for project in all_projects.json():
        all_project_info[str(project['id'])] = {
            "project_name": project['project_name'],
            "project_id": project['id']
        }

    # get all the experiments
    for project in all_project_info:
        all_experiment_info = requests.get(
            'https://www.optimizelyapis.com/experiment/v1/projects/' + project + '/experiments/',
            headers={'Token': optimizely_token})

        for experiment in all_experiment_info.json():
            if experiment['status'] != 'Not started':
                all_experiment_data[str(experiment['id'])] = {
                    "project_id": experiment['project_id'],
                    "project_name": all_project_info[project]['project_name'],
                    "experiment_name": experiment['description'],
                    "results_link": experiment['shareable_results_link'],
                    "status": experiment['status']
                }

    # get all the experiment results
    with open('Optimizely_Classic_Experiments.csv', 'w') as csvfile:
     filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
     for experiment in all_experiment_data:
        filewriter.writerow([all_experiment_data[experiment]['status']])
        each_experiment_info = requests.get(
            'https://www.optimizelyapis.com/experiment/v1/experiments/' + experiment + '/stats/',
            headers={'Token': optimizely_token})
        if each_experiment_info.status_code == 200:
            filewriter.writerow(['Project Name: ' + str(all_experiment_data[experiment]['project_name'])])
            filewriter.writerow(['Project ID: ' + str(all_experiment_data[experiment]['project_id'])])
            filewriter.writerow(['Experiment Name: ' + str(all_experiment_data[experiment]['experiment_name'])])
            filewriter.writerow(['Experiment ID: ' + str(experiment)])
            filewriter.writerow(['Experiment Sharable Results Link: ' + str(all_experiment_data[experiment]['results_link'])])
            resultsJson = each_experiment_info.json()
            for variation in resultsJson:
                filewriter.writerow(['------'])
                filewriter.writerow(['Goal Name: ' + variation['goal_name']])
                filewriter.writerow(['Variation Name: ' + variation['variation_name']])
                if variation['is_revenue'] == False:
                    filewriter.writerow(['Conversion Rate: ' + str(variation['conversion_rate'])])
                else:
                    filewriter.writerow(['Revenue Per Visitor: ' + str(variation['revenue_per_visitor'])])
                filewriter.writerow(['Statistical Significance: ' + str(variation['statistical_significance'])])
                filewriter.writerow(['Status: ' + variation['status']])
                filewriter.writerow(['------'])
            filewriter.writerow(['------------------------------------'])

scrapeResultsData()
