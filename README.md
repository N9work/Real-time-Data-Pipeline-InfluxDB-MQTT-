# Real-time Data Pipeline with InfluxDB & MQTT

This project provides a real-time data pipeline that collects sensor data via MQTT and stores it in InfluxDB.

## Current Usage
- Run the application inside a container using the provided `Dockerfile`.
- InfluxDB and MQTT broker must be set up and run separately.

## Simulate Sensor
To test the system without a physical device, you can simulate sensor data.

There are **two files** inside the `simulate_sensor` folder:
- `publisher.py` – sends fake sensor data to the MQTT broker  
- `subscriber.py` – subscribes to the topic and receives data  

Run them manually in two terminals:

bash
# Terminal 1: start publisher
`python publisher.py`

# Terminal 2: start subscriber
`python subscriber.py`

# Frontend (3D web by three.js)
bash
npm install
npm install three
npm run dev

## Future Updates
- [ ] Add a `docker-compose.yaml` file to simplify deployment and run **MQTT + InfluxDB + App** together.
