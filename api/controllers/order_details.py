from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, detail):
    # Create a new instance of the OrderDetail model with the provided data
    db_details = models.OrderDetail(
        amount=detail.amount,
    )
    # Add the newly created OrderDetail object to the database session
    db.add(db_details)
    # Commit the changes to the database
    db.commit()
    # Refresh the OrderDetail object to ensure it reflects the current state in the database
    db.refresh(db_details)
    # Return the newly created OrderDetail object
    return db_details


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, detail_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()


def update(db: Session, detail_id, detail):
    # Query the database for the specific detail to update
    db_details = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id)
    # Extract the update data from the provided 'detail' object
    update_data = detail.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_details.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated detail record
    return db_details.first()


def delete(db: Session, detail_id):
    # Query the database for the specific order to delete
    db_details = db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id)
    # Delete the database record without synchronizing the session
    db_details.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
