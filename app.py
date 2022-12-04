from flask import Flask, request, jsonify
from Models import Admin, Company, Location, Sensor, SensorData, db
from init import create_app


app= create_app()

@app.route('/admin', methods=['POST'])
def validate_admin():
    if request.method == 'POST':
        data= request.get_json()
        username= data['username']
        password= data['password']
        admin = Admin.query.filter_by(Username=username, Password=password).first()
        if admin is None:
            return jsonify({'message': 'Username not found'})
        if admin:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid password'})

@app.route('/api/addcompany', methods=['POST'])
def addcompany():
    data = request.get_json()
    company_name = data['company_name']
    company_api_key = data['company_api_key']
    user= data['username']
    password= data['password']

    admin= Admin.query.filter_by(Username=user, Password=password).first()
    
    if admin:
        company = Company.query.filter_by(company_name=company_name).first()
        if company:
            return jsonify({
                'status': 'fail',
                'message': 'Company already exists.'
            })
        else:   
            # console log
            print(company_name, company_api_key)
            company = Company(company_name=company_name, company_api_key=company_api_key)

            db.session.add(company)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Registered successfully.',
                'token': company.generate_token()
            })

@app.route('/api/addlocation', methods=['POST'])
def addlocation():
    data = request.get_json()
    company_id = data['company_id']
    location_name = data['location_name']
    location_country= data['location_country']
    location_city = data['location_city']
    location_meta = data['location_meta']
    user= data['user']
    password= data['password']
    
    admin= Admin.query.filter_by(Username=user, Password=password).first()
    
    if admin:
        location = Location.query.filter_by(location_name=location_name).first()
        if location:
            return jsonify({
                'status': 'fail',
                'message': 'Location already exists.'
            })
        else:   
            # console log
            print(company_id, location_name, location_country, location_city, location_meta)
            location = Location(company_id=company_id, location_name=location_name, location_country=location_country, location_city=location_city, location_meta=location_meta)
            location.save()
            return jsonify({
                'status': 'success',
                'message': 'Registered successfully.',
                'token': location.generate_token()
            })

@app.route('/api/addsensor', methods=['POST'])
def addsensor():
    data = request.get_json()
    location_id = data['location_id']
    sensor_name= data['sensor_name']
    sensor_category = data['sensor_category']
    sensor_meta = data['sensor_meta']
    sensor_api_key= data['sensor_api_key']
    user= data['user']
    password= data['password']
    
    admin= Admin.query.filter_by(Username=user, Password=password).first()    
    
    if admin: 
        # console log
        print(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
        sensor = Sensor(location_id=location_id, sensor_name=sensor_name, sensor_category=sensor_category, sensor_meta=sensor_meta, sensor_api_key=sensor_api_key)
        sensor.save()
        return jsonify({
            'status': 'success',
            'message': 'Registered successfully.',
            'token': sensor.generate_token()
        })

#create app.route with method get to get all locations from a company by company_api_key
@app.route('/api/getlocations', methods=['GET'])
def getlocations():
    data = request.get_json()
    company_api_key = data['company_api_key']

    locations = Location.query.filter_by(company_api_key=company_api_key).all()
    return jsonify({
        'status': 'success',
        'locations': [location.to_json() for location in locations]
    })

#create app.route with method get to get one location from a company by company_api_key and location_name
@app.route('/api/getlocation', methods=['GET'])
def getlocation():
    data = request.get_json()
    company_api_key = data['company_api_key']
    location_name = data['location_name']

    location = Location.query.filter_by(company_api_key=company_api_key, location_name=location_name).first()
    return jsonify({
        'status': 'success',
        'location': location.to_json()
    })

#create app.route with method get to get all sensors from a location by location_id and company_api_key
@app.route('/api/getsensors', methods=['GET'])
def getsensors():
    data = request.get_json()
    location_id = data['location_id']
    company_api_key = data['company_api_key']

    sensors = Sensor.query.filter_by(location_id=location_id, company_api_key=company_api_key).all()
    return jsonify({
        'status': 'success',
        'sensors': [sensor.to_json() for sensor in sensors]
    })

#create app.route with method get to get one sensor from a location by location_id and company_api_key and sensor_name
@app.route('/api/getsensor', methods=['GET'])
def getsensor():
    data = request.get_json()
    location_id = data['location_id']
    company_api_key = data['company_api_key']
    sensor_name = data['sensor_name']

    sensor = Sensor.query.filter_by(location_id=location_id, company_api_key=company_api_key, sensor_name=sensor_name).first()
    return jsonify({
        'status': 'success',
        'sensor': sensor.to_json()
    })

#create app.route with method put to update or insert a location by location_id and company_api_key
@app.route('/api/updatelocation', methods=['PUT'])
def updatelocation():
    data = request.get_json()
    location_id = data['location_id']
    company_api_key = data['company_api_key']
    location_name = data['location_name']
    location_country = data['location_country']
    location_city = data['location_city']
    location_meta = data['location_meta']

    location = Location.query.filter_by(location_id=location_id, company_api_key=company_api_key).first()
    if location:
        location.location_name = location_name
        location.location_country = location_country
        location.location_city = location_city
        location.location_meta = location_meta
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Location updated successfully.'
        })
    else:
        location = Location(location_id=location_id, company_api_key=company_api_key, location_name=location_name, location_country=location_country, location_city=location_city, location_meta=location_meta)
        location.save()
        return jsonify({
            'status': 'success',
            'message': 'Location inserted successfully.'
        })

#create app.route with method put to update or insert a sensor by sensor_id and company_api_key
@app.route('/api/updatesensor', methods=['PUT'])
def updatesensor():
    data = request.get_json()
    sensor_id = data['sensor_id']
    company_api_key = data['company_api_key']
    sensor_name = data['sensor_name']
    sensor_category = data['sensor_category']
    sensor_meta = data['sensor_meta']
    sensor_api_key = data['sensor_api_key']

    sensor = Sensor.query.filter_by(sensor_id=sensor_id, company_api_key=company_api_key).first()
    if sensor:
        sensor.sensor_name = sensor_name
        sensor.sensor_category = sensor_category
        sensor.sensor_meta = sensor_meta
        sensor.sensor_api_key = sensor_api_key
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Sensor updated successfully.'
        })
    else:
        sensor = Sensor(sensor_id=sensor_id, company_api_key=company_api_key, sensor_name=sensor_name, sensor_category=sensor_category, sensor_meta=sensor_meta, sensor_api_key=sensor_api_key)
        sensor.save()
        return jsonify({
            'status': 'success',
            'message': 'Sensor inserted successfully.'
        })

#create app.route with method delete to delete a location by location_id and company_api_key
@app.route('/api/deletelocation', methods=['DELETE'])
def deletelocation():
    data = request.get_json()
    location_id = data['location_id']
    company_api_key = data['company_api_key']

    location = Location.query.filter_by(location_id=location_id, company_api_key=company_api_key).first()
    if location:
        db.session.delete(location)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Location deleted successfully.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Location not found.'
        })

#create app.route with method delete to delete a sensor by sensor_id and company_api_key
@app.route('/api/deletesensor', methods=['DELETE'])
def deletesensor():
    data = request.get_json()
    sensor_id = data['sensor_id']
    company_api_key = data['company_api_key']

    sensor = Sensor.query.filter_by(sensor_id=sensor_id, company_api_key=company_api_key).first()
    if sensor:
        db.session.delete(sensor)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': 'Sensor deleted successfully.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Sensor not found.'
        })

#create app.route with method post to insert a sensor data by sensor_api_key
@app.route('/api/sensordata', methods=['POST'])
def sensordata():
    data = request.get_json()
    sensor_api_key = data['sensor_api_key']
    sensor_data = data['sensor_data']

    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if sensor:
        sensor_data = SensorData(sensor_id=sensor.sensor_id, sensor_data=sensor_data)
        sensor_data.save()
        return jsonify({
            'status': 'success',
            'message': 'Sensor data inserted successfully.'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Sensor not found.'
        })



app.run()