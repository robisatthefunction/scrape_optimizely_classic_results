import requests, csv, argparse

def scrapeResultsData():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="paste your Optimizely v1 REST API token here")
    args = parser.parse_args()
    optimizely_token = args.token

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

    # get all the experiments in each project
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
    with open('Optimizely_Classic_Experiment_Results.csv', 'w') as csvfile:
     filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
     for experiment in all_experiment_data:
        each_experiment_info = requests.get(
            'https://www.optimizelyapis.com/experiment/v1/experiments/' + experiment + '/stats/',
            headers={'Token': optimizely_token})
        if each_experiment_info.status_code == 200:
            resultsJson = each_experiment_info.json()
            filewriter.writerow(['Project Name: %s' % (str(all_experiment_data[experiment]['project_name']))])
            filewriter.writerow(['Project ID: %s' % (str(all_experiment_data[experiment]['project_id']))])
            filewriter.writerow(['Experiment Name: %s' % (str(all_experiment_data[experiment]['experiment_name']))])
            filewriter.writerow(['Experiment ID: %s' % (str(experiment))])
            filewriter.writerow(['Experiment Sharable Results Link: %s' % (str(all_experiment_data[experiment]['results_link']))])
            filewriter.writerow(['Begin Time: %s' % (str(resultsJson[0]['begin_time']))])
            filewriter.writerow(['End Time: %s' % (str(resultsJson[0]['end_time']))])
            for variation in resultsJson:
                filewriter.writerow(['------'])
                filewriter.writerow(['Goal Name: %s' % (str(variation['goal_name']))])
                filewriter.writerow(['Variation Name: %s' % (str(variation['variation_name']))])
                if variation['is_revenue'] == False:
                    filewriter.writerow(['Conversion Rate: %s' % (str(variation['conversion_rate']))])
                else:
                    filewriter.writerow(['Revenue Per Visitor: %s' % (str(variation['revenue_per_visitor']))])
                    filewriter.writerow(['Revenue: %s' % (str(variation['revenue']))])
                filewriter.writerow(['Statistical Significance: %s' % (str(variation['statistical_significance']))])
                filewriter.writerow(['Status: %s' % (str(variation['status']))])
                filewriter.writerow(['------'])
            filewriter.writerow(['------------------------------------'])

scrapeResultsData()
