from app import app, db, Service  


with app.app_context():
    db.create_all()

    new_service = Service(name='Ремонт фасадов', description='Ремонт фасадов зданий.')
    db.session.add(new_service)
    db.session.commit()

    print("Данные успешно добавлены в базу данных!")
