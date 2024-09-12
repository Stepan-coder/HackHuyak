from sqladmin import ModelView
from models.contract_models import Contract, Agreement, Specification


class AgreementAdmin(ModelView, model=Agreement):
    column_list = [Agreement.id, Agreement.created_date]


class ContractAdmin(ModelView, model=Contract):
    column_list = [Contract.id, Contract.number]


class SpecificationAdmin(ModelView, model=Specification):
    column_list = [Specification.id, Specification.created_date]

