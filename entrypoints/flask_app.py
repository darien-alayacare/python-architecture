from datetime import datetime
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config
from domains.oder_line import OrderLine
from domains.model import OutOfStock
from adapters.sql_alchemy import SqlAlchemyRepository
from orm.orm import start_mappers
import service_layer



start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = SqlAlchemyRepository(session)
    line = OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )

    try:
        batchref = service_layer.allocate(ref=line.orderid, qty=line.qty, sku=line.sku, repo=repo, session=session)
    except (OutOfStock, service_layer.InvalidSku) as e:
        return {"message": str(e)}, 400

    return {"batchref": batchref}, 201

@app.route("/add_batch", methods=['POST'])
def add_batch():
    session = get_session()
    repo = SqlAlchemyRepository(session)
    eta = request.json['eta']
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    service_layer.add_batch(
        request.json['ref'], request.json['sku'], request.json['qty'], eta,
        repo, session
    )
    return 'OK', 201