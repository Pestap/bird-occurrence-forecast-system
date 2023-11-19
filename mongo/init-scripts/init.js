db.createUser({
    user: 'bird_app',
    pwd: 'Czapla#123',
    roles: [{ role: 'readWrite', db: 'bird_occurrence_forecast_system' }]
  });