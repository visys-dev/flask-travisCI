from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from app.db import Expense, db
from app.schemas import expense_schema, expenses_schema

bp = Blueprint("expense", __name__, url_prefix="/expenses")


@bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    """
    Повертає список усіх витрат
    ---
    tags:
        - витрати
    produces:
        - application/json
    responses:
          200:
            description: Список витрат
            schema:
                type: array
                items:
                    $ref: '#/definitions/ExpenseOut'
    """
    return jsonify(expenses_schema.dump(current_user.expenses)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def add_expense():
    """
    Створює нову витрату
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
    - name: expense
      in: body
      description: Дані витрати
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        201:
            description: Створена витрата
            schema:
                $ref: '#/definitions/ExpenseOut'
    """
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    new_expense = Expense(
        title=data["title"], amount=data["amount"], user_id=current_user.id
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201


@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_expense(id):
    """
    Повертає одну витрату за ідентифікатором
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Ідентифікатор витрати
      required: true
      type: number
    responses:
        200:
            description: Знайдена витрата
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_expense(id):
    """
    Оновлює дані витрати за ідентифікатором
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Ідентифікатор витрати
      required: true
      type: number
    - name: expense
      in: body
      description: Дані для оновлення витрати
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        200:
            description: Оновлена витрата
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401
    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_expense(id):
    """
    Видаляє витрату за ідентифікатором
    ---
    tags:
        - витрати
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: Ідентифікатор витрати
      required: true
      type: number
    responses:
        204:
            description: Успішне видалення витрати
        404:
            description: Не знайдено витрату за ідентифікатором
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    if expense.user_id != current_user.id:
        return jsonify(error="У вас немає доступу до цієї витрати"), 401

    db.session.delete(expense)
    db.session.commit()
    return "", 204
