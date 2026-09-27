from app.models.employee import Employee
from app.config.database import db

class EmployeeRepository:
    @staticmethod
    def create(employee):
        db.session.add(employee)
        db.session.commit()
        return employee 
    
    @staticmethod
    def get_by_id(employee_id):
        return db.session.get(Employee,employee_id)
    
    @staticmethod
    def get_by_user_id(user_id):
        return Employee.query.filter_by(
            user_id=user_id,
        ).first()
    
    @staticmethod
    def get_by_employee_code(employee_code):

        return Employee.query.filter_by(
            employee_code=employee_code
        ).first()

    @staticmethod
    def get_by_email(email):

        return Employee.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_all(
        page=1,
        per_page=10,
        search=None,
        department=None,
        is_active=None
    ):
        query= Employee.query
        if search:
            search_term= f"%{search}%"
            query=query.filter(
                db.or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.employee_code.ilike(search_term),
                    Employee.email.ilike(search_term)
                )
            )

        if department:
            query = query.filter_by(
                department=department
            )

        if is_active is not None:
            query = query.filter_by(
                is_active=is_active
            )

        return query.order_by(
            Employee.id.asc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def update(employee):

        db.session.commit()

        return employee

    @staticmethod
    def delete(employee):
        db.session.delete(employee)
        db.session.commit()

    @staticmethod
    def exists_by_employee_code(employee_code):

        return Employee.query.filter_by(
            employee_code=employee_code
        ).first() is not None

    @staticmethod
    def exists_by_email(email):

        return Employee.query.filter_by(
            email=email
        ).first() is not None