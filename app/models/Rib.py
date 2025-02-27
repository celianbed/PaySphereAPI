from app import db
import random
import string


class Rib(db.Model):

    __tablename__ = 'rib'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    compte_id = db.Column(db.Integer, db.ForeignKey('compte.id'))
    iban = db.Column(db.String(34), unique=True, nullable=False)
    bic = db.Column(db.String(11), nullable=False)
    titulaire_compte = db.Column(db.String(100), nullable=False)
    banque = db.Column(db.String(100), nullable=False)
    agence = db.Column(db.String(100), nullable=True)
    adresse_banque = db.Column(db.Text, nullable=True)

    compte = db.relationship("Compte", back_populates="rib")


    def __init__(self,compte_id, iban, bic, titulaire_compte, banque, agence=None, adresse_banque=None):
        self.compte_id = compte_id
        self.iban = iban
        self.bic = bic
        self.titulaire_compte = titulaire_compte
        self.banque = banque
        self.agence = agence
        self.adresse_banque = adresse_banque

    def __repr__(self):
        return f'<Rib {self.id} {self.compte_id} {self.iban} {self.bic} {self.titulaire_compte} {self.banque} {self.agence} {self.adresse_banque}>'


    def to_dict(self):
        return {
            "id": self.id if self.id else None,
            "compte_id": self.compte_id,
            "iban": self.iban,
            "bic": self.bic,
            "titulaire_compte": self.titulaire_compte,
            "banque": self.banque,
            "agence": self.agence,
            "adresse_banque": self.adresse_banque,
        }


    @staticmethod
    def generate_iban(country_code="FR"):

        country_code = country_code.upper()
        control_digits = random.randint(10, 99)

        bank_code = ''.join(random.choices(string.digits, k=4))
        account_number = ''.join(random.choices(string.digits, k=11))

        iban = f"{country_code}{control_digits:02d}{bank_code}{account_number}"
        return iban, country_code

