from tensorflow.keras.callbacks import Callback


class RestoreBestModel(Callback):
    """ Simple callback to restore model's weights from its best epoch before exiting training.
        Inspired by & modified from: https://stackoverflow.com/questions/61630990/tensorflow-callback-how-to-save-best-model-on-the-memory-not-on-the-disk
    """

    def __init__(self, monitor='val_loss', best='low'):

        super(RestoreBestModel, self).__init__()
        self.monitor = monitor  # metric to be monitored
        self.best = best        # whether low | high metric value is good
        self.best_score = float('inf') if best == 'low' else -float('inf')
        self.best_weights = None

    def on_epoch_end(self, epoch, logs=None):
        cond_1 = self.best_weights is None
        cond_2 = self.best == 'low' and logs[self.monitor] < self.best_score
        cond_3 = self.best == 'high' and logs[self.monitor] > self.best_score
        if cond_1 or cond_2 or cond_3:
            self.best_score = logs[self.monitor]
            self.best_weights = self.model.get_weights()

    def on_train_end(self, logs=None):
        self.model.set_weights(self.best_weights)
