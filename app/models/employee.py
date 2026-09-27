from datetime import datetime, timezone
from app.config.database import db

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(
        db.Integer,
        primary_key = True
        )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique = True,
        nullable = False
    )

    employee_code = db.Column(
        db.String(20),
        unique = True,
        nullable = False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(20),
        nullable=False
    )

    designation = db.Column(
        db.String(100),
        nullable=False
    )

    salary = db.Column(
        db.Numeric(12,2),
        nullable = True
    )

    joining_date = db.Column(
        db.Date,
        nullable=True
    )

    department = db.Column(
        db.String(100),
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    employment_status = db.Column(
    db.String(20),
    nullable=False,
    default="Active"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime,
        nullable = False,
        default=lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc)
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "employee",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<Employee {self.employee_code}>"
