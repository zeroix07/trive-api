from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np

# Load the trained Keras model
model = tf.keras.models.load_model('model.h5')

# Define the Flask app
app = Flask(__name__)

# Define a route to handle prediction requests
@app.route('/predict', methods=['POST'])
def predict():
    # Parse the JSON request
    data = request.json
    
    try:
        # Extract features from the JSON request
        battery_temperature = float(data['battery_temperature'])
        battery_voltage = float(data['battery_voltage'])
        battery_current = float(data['battery_current'])
        weather_conditions = [
            float(data['weather_cloudy']),
            float(data['weather_dark']),
            float(data['weather_dark_little_rainy']),
            float(data['weather_rainy']),
            float(data['weather_slightly_cloudy']),
            float(data['weather_sunny']),
            float(data['weather_sunrise']),
            float(data['weather_sunset'])
        ]

        # Combine all features into a single input array
        input_features = [
            battery_temperature,
            battery_voltage,
            battery_current
        ] + weather_conditions

        # Reshape the input to match the model's expected input shape
        input_tensor = np.array(input_features).reshape(1, 1, 11)

        # Make the prediction
        prediction = model.predict(input_tensor)

        # Return the prediction as a JSON response
        response = {
            'predicted_soc': float(prediction[0][0])
        }

    except KeyError as e:
        return jsonify({'error': f'Missing input: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(response)

# Define a basic route to check if the server is running
@app.route('/')
def index():
    return "SOC Battery Forecasting API is running."

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
