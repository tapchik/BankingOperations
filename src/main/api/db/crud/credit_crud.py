from sqlalchemy.orm import Session

from src.main.api.db.models.credit_table import Credit


class CreditCrudDb:

    @staticmethod
    def get_credit_by_id(db: Session, credit_id: int) -> Credit | None:
        return db.query(Credit).filter_by(id=credit_id).first()

    @staticmethod
    def get_credit_by_account_id(db: Session, account_id: int) -> Credit | None:
        return db.query(Credit).filter_by(account_id=account_id).first()

    @staticmethod
    def delete_credit_by_id(db: Session, credit_id: int) -> None:
        credit = db.query(Credit).filter_by(id=credit_id).first()
        if credit:
            db.delete(credit)
            db.commit()
