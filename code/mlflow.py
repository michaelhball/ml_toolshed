import git

from mlflow.tracking import MlflowClient

from .utils import scp_files


class MyMLFlowClient:
    """ Class to handle all MLFlow interactions. Only need one such client (i.e. can be used for many
        training runs).
    """

    def __init__(self, tracking_uri):
        """ Initialise

        :param tracking_uri (str) MLFlow tracking URI for tracking API
        """

        self.client = MlflowClient(tracking_uri=tracking_uri)
        self.run = None

    def create_new_run(self, experiment_name, user_name, set_tags=True, run_name=None):
        """ Creates a new Run in MLFlow tracking server (e.g. at start of training pipeline)

        :param experiment_name: (str) name of experiment to create run within
        :param user_name: (str) user name of person creating run
        :param set_tags: (bool) indicating whether to assign my default tagset to the given run
        :param run_name: (str) optional name of run (auto-generated ID will be used if not provided)
        :return run ID
        """

        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment is None:
                experiment_id = self.client.create_experiment(experiment_name)
                self.client.set_experiment_tag(experiment_id, "created_by", user_name)
            else:
                experiment_id = experiment.experiment_id
            run = self.client.create_run(experiment_id)
            run_id = run.info.run_id

            if set_tags:
                if not self._set_run_tags(user_name, run_id, run_name):
                    return False

            return run_id
        except Exception as e:
            print('Exception initialising MLFlow run', e)
            return False

    def _set_run_tags(self, user_name, run_id, run_name):
        """"""

        try:
            repo = git.Repo(search_parent_directories=True)
            self.client.set_tag(run_id, "run_id", run_id)
            self.client.set_tag(run_id, "mlflow.runName", run_name if run_name is not None else run_id)
            self.client.set_tag(run_id, "mlflow.user", user_name)
            self.client.set_tag(run_id, "mlflow.source.git.repoURL", repo.remotes.origin.url)
            self.client.set_tag(run_id, "mlflow.source.git.branch", repo.active_branch.name)
            self.client.set_tag(run_id, "mlflow.source.git.commit", repo.head.object.hexsha)
            return True
        except Exception as e:
            print('Exception setting MLFlow run system tags: \n', e)
            return False

    def log_param(self, run_id, param_dict):
        """ Log a dictionary of params to MLFlow tracking server

        :param run_id: (str) run ID
        :param param_dict: (dict) dictionary of param_name: param_value
        :return success indicator
        """

        try:
            for param_name, param_value in param_dict.items():
                self.client.log_param(run_id, param_name, param_value)
            return True
        except Exception as e:
            print(f'Exception logging params run {run_id}', e)
            return False

    def log_metrics(self, run_id, metric_dict, step=None, timestamp=None):
        """ Log a dictionary of metrics to MLFlow tracking server (at particular step or timestamp)

        :param run_id: (str) run ID
        :param metric_dict: (dict) dictionary of metric_name: metric_value
        :param step: (int) integer step to associate metrics with (e.g. epoch | iteration)
        :param timestamp: (time) timestamp to associate metrics with
        :return success indicator
        """

        try:
            for metric_name, metric_val in metric_dict.items():
                self.client.log_metric(run_id, metric_name, metric_val, step=step, timestamp=timestamp)
            return True
        except Exception as e:
            print(f'Exception logging metrics to run {run_id}', e)
            return False

    def download_artifact(self, run_id, remote_dir, local_dir, ssh_params=None):
        """ Downloads artifact from MLFlow server (either local or over SSH)

        :param run_id: (str) run ID
        :param remote_dir: (path) relative path to artifact (inside run artifact storage)
        :param local_dir: (path) local directory in which to save artifact
        :param ssh_params: (dict) must contain host, username, and password, if included
        :return: True if successful, False otherwise.
        """

        try:
            if ssh_params is not None:
                run = self.client.get_run(run_id)
                artifact_uri = f"{run.info.artifact_uri}/{remote_dir}"
                success = scp_files(**ssh_params, remote_dir=artifact_uri, local_dir=local_dir, direction='from')
                if isinstance(success, bool) and not success:
                    return False
            else:
                self.client.download_artifacts(run_id, remote_dir, local_dir)
            return True
        except Exception as e:
            print(f'Exception downloading artifact from run {run_id}', e)
            return False
