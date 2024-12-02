import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import os

class ForexPredictor:
    def __init__(self, input_window=30, output_window=15):
        self.input_window = input_window
        self.output_window = output_window
        self.scaler = MinMaxScaler()
        self.checkpoint_path = 'Database/checkpoints'
        os.makedirs(self.checkpoint_path, exist_ok=True)
        self.model = self._build_model()
        
    def _build_model(self):
        model = Sequential([
            Input(shape=(self.input_window, 5)),
            LSTM(128, return_sequences=True),
            Dropout(0.2),
            LSTM(64, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation='relu'),
            Dense(self.output_window * 5)
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        return model
    
    def prepare_data(self, df):
        features = ['open', 'close', 'max', 'min', 'volume']
        data = df[features].values
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(len(scaled_data) - self.input_window - self.output_window):
            X.append(scaled_data[i:(i + self.input_window)])
            y.append(scaled_data[(i + self.input_window):(i + self.input_window + self.output_window)].flatten())
        
        return np.array(X), np.array(y)
    
    def train(self, trainer_path='Database/entrenador'):
        checkpoint_file = os.path.join(self.checkpoint_path, 'model_epoch_{epoch:02d}_val_loss_{val_loss:.4f}.keras')
        
        callbacks = [
            ModelCheckpoint(
                filepath=checkpoint_file,
                save_best_only=True,
                save_weights_only=False,
                monitor='val_loss',
                mode='min',
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=2,
                min_lr=0.00001
            )
        ]
        
        for file in os.listdir(trainer_path):
            if file.endswith('.csv'):
                print(f"\nEntrenando con {file}")
                df = pd.read_csv(os.path.join(trainer_path, file))
                X, y = self.prepare_data(df)
                
                split = int(len(X) * 0.8)
                X_train, X_val = X[:split], X[split:]
                y_train, y_val = y[:split], y[split:]
                
                self.model.fit(
                    X_train, y_train,
                    validation_data=(X_val, y_val),
                    epochs=5,
                    batch_size=32,
                    callbacks=callbacks,
                    verbose=1
                )
    
    def load_checkpoint(self, checkpoint_file):
        checkpoint_path = os.path.join(self.checkpoint_path, checkpoint_file)
        self.model = load_model(checkpoint_path)
        print(f"Modelo cargado desde: {checkpoint_path}")
    
    def predict_next(self, current_data):
        scaled_data = self.scaler.transform(current_data[-self.input_window:])
        prediction = self.model.predict(np.array([scaled_data]))
        prediction = prediction.reshape(-1, 5)
        return self.scaler.inverse_transform(prediction)

if __name__ == "__main__":
    predictor = ForexPredictor()
    predictor.train()
