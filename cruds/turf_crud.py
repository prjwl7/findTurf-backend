# cruds/turf_crud.py

from models import db, Turf, TurfImage

def create_turf(data):
    new_turf = Turf(
        name=data['name'],
        location=data['location'],
        city=data['city'],
        charges=data['charges'],
        availableTimeSlots=data['availableTimeSlots']
    )
    db.session.add(new_turf)
    db.session.flush()  # Flush to get TurfID for the new turf before committing

    # Handle image URLs
    image_urls_str = data.get('image_urls', '')
    if image_urls_str:
        image_urls = [url.strip() for url in image_urls_str.split(',')]
        for url in image_urls:
            new_turf_image = TurfImage(TurfID=new_turf.TurfID, ImageURL=url)
            db.session.add(new_turf_image)

    db.session.commit()
    return new_turf

def update_turf(turf_id, data):
    turf = Turf.query.get(turf_id)
    if not turf:
        raise ValueError("Turf not found")

    turf.name = data.get('name', turf.name)
    turf.location = data.get('location', turf.location)
    turf.city = data.get('city', turf.city)
    turf.charges = data.get('charges', turf.charges)
    turf.availableTimeSlots = data.get('availableTimeSlots', turf.availableTimeSlots)

    # Update image URLs
    if 'image_urls' in data:
        # Delete existing images
        TurfImage.query.filter_by(TurfID=turf_id).delete()
        # Add new images
        image_urls_str = data['image_urls']
        if image_urls_str:
            image_urls = [url.strip() for url in image_urls_str.split(',')]
            for url in image_urls:
                new_turf_image = TurfImage(TurfID=turf_id, ImageURL=url)
                db.session.add(new_turf_image)

    db.session.commit()
    return turf

def delete_turf(turf_id):
    turf = Turf.query.get(turf_id)
    if not turf:
        raise ValueError("Turf not found")

    # Delete associated images
    TurfImage.query.filter_by(TurfID=turf_id).delete()

    db.session.delete(turf)
    db.session.commit()
    return turf

def get_turfs():
    return Turf.query.all()

def get_turf_by_id(turf_id):
    return Turf.query.get(turf_id)
