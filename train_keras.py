# tutorial/src/train.py
import os
import argparse

from azureml.core import Run

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard
import gzip
import numpy as np


def load_image(path):
    f = gzip.open(path, "r")

    image_size = 28
    f.read(16)
    buf = f.read()
    data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)

    data = data.reshape(int(data.shape[0] / 28 / 28), image_size, image_size, 1)
    f.close()
    return data


def load_label(path):
    f_p = gzip.open(path, "r")
    f_p.read(8)
    buf = f_p.read()
    data = np.frombuffer(buf, dtype=np.uint8).astype(np.int8)
    f_p.close()
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_folder", type=str, help="Path to the training data")
    parser.add_argument(
        "--log_folder", type=str, help="Path to the log", default="./logs"
    )
    args = parser.parse_args()

    print("===== DATA =====")
    print("DATA PATH: " + args.data_path)
    print("LIST FILES IN DATA PATH...")
    print(os.listdir(args.data_path))
    print("================")
    run = Run.get_context()

    # Load mnist data
    train_image = load_image(
        os.path.join(args.data_folder, "train-images-idx3-ubyte.gz")
    )
    train_label = load_label(
        os.path.join(args.data_folder, "train-labels-idx1-ubyte.gz")
    )
    test_image = load_image(os.path.join(args.data_folder, "t10k-images-idx3-ubyte.gz"))
    test_label = load_label(os.path.join(args.data_folder, "t10k-labels-idx1-ubyte.gz"))

    train_image /= 255
    train_label = to_categorical(train_label)
    test_image /= 255
    test_label = to_categorical(test_label)

    # LeNet
    input_layer = Input(shape=(28, 28, 1))
    layers = Conv2D(filters=6, kernel_size=(5, 5), activation="tanh")(input_layer)
    layers = MaxPooling2D(pool_size=(2, 2))(layers)
    layers = Conv2D(filters=16, kernel_size=(5, 5), activation="tanh")(layers)
    layers = MaxPooling2D(pool_size=(2, 2))(layers)
    layers = Flatten()(layers)
    layers = Dense(120, activation="tanh")(layers)
    layers = Dense(84, activation="tanh")(layers)
    output = Dense(10, activation="softmax")(layers)
    model = Model(inputs=input_layer, outputs=output)
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    # Tensorboard

    tb_callback = TensorBoard(
        log_dir=args.log_folder,
        histogram_freq=0,
        write_graph=True,
        write_images=True,
        embeddings_freq=0,
        embeddings_layer_names=None,
        embeddings_metadata=None,
    )
    # train the network

    history_callback = model.fit(
        train_image,
        train_label,
        epochs=10,
        validation_split=0.2,
        batch_size=10,
        callbacks=[tb_callback],
    )

    run.log("train_loss", history_callback.history["loss"])
    run.log("train_accuracy", history_callback.history["accuracy"])
    run.log("val_loss", history_callback.history["val_loss"])
    run.log("val_accuracy", history_callback.history["val_accuracy"])

    print("Finished Training")
    model.save("outputs/keras_lenet.h5")
    print("Saved Model")


if __name__ == "__main__":
    main()
