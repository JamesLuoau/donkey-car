from model import nvidia
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam


class Trainer(object):
    def __init__(
            self, model, learning_rate, epoch,
            custom_name="", multi_process=False, number_of_worker=4):
        self.model = model
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.multi_process = multi_process
        self.number_of_worker = number_of_worker
        self.model_name = "model_{}_lr{}_epoch{}".format(custom_name, learning_rate, epoch)

    def fit_generator(self, generator, generator_val):
        final_model_name = self.model_name
        model = self.model
        model.summary()

        checkpointer = ModelCheckpoint(
            filepath=final_model_name + "_current_{epoch:02d}_loss{loss:.3f}.h5",
            save_weights_only=True,
            verbose=1
        )

        # early_stop = EarlyStopping(monitor='val_mean_squared_error', min_delta=0.0001, patience=4, verbose=1, mode='min')

        adam = Adam(lr=self.learning_rate)
        model.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])

        print('Starting training')

        model_json = model.to_json()
        with open(final_model_name + ".json", "w") as json_file:
            json_file.write(model_json)

        model.fit_generator(generator,
                            epochs=self.epoch,
                            verbose=1,
                            steps_per_epoch=300,
                            # max_queue_size=20,
                            # workers=8,
                            # use_multiprocessing=self.multi_process,
                            validation_data=generator_val,
                            validation_steps=60,
                            callbacks=[checkpointer]
                            )
