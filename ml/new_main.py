from typing import List
from docworker.docreader import read_docx_in_paragraphs, read_table_in_paragraphs
from models import AnswerModel, RerankerModel
from NER import *
from docworker.templater import DocumentGenerator


# Загружаем модель для получения ответов
answer_model = AnswerModel()
# Загружаем модель для ранжировки вариантов ответов (наиболее подходящий - ближе к началу)
reranker_model = RerankerModel()

# Путь до договора ОБЯЗАТЕЛЬНО в формате .docx
file_path = 'docworker/Проект договора.docx'

# Читаем текст из документа
paragraphs = read_docx_in_paragraphs(file_path)

# Читаем ячейки таблицы из документа
cells = read_table_in_paragraphs(file_path)

# Запускаем распознавалку таких сущьностей как имена, деньги
text_mark_up = TextMarkUp(is_bert=False, download=False, is_pro_bert=False)

# Хитрая штука для получения 10 ответов на вопрос пользователя
def get_answer(question: str, documents: List[str]):
    text_ranks = reranker_model.predict(query=question, documents=documents)
    variants = list(set([answer_model.predict(question=question, context=tr) for tr in list(text_ranks.keys())[:10]]))
    text_ranks = reranker_model.predict(query=question, documents=variants)
    return list(text_ranks.keys())[0]





#
# # Поабзацно читаем текст
# list_of_paragraphs = []
# for i, paragraph in enumerate(paragraphs):
#     print(f"Абзац {i + 1}: {paragraph}")
#     list_of_paragraphs.append(paragraph)
#
#
# for i, cell in enumerate(cells):
#     print("cell=", cell)





context = {
    'additional_agreement_number': 'dcs',
    'contract_number': ' ',
    'contract_date': '35 февраля 2024',
    'contract_city': ' ',
    'customer_company_fullname': ' ',

    'customer_FIO': '',
    'by_statment':  ' ',

    'executor_company_fullname': get_answer(question="Полное название компании исполнителя", documents=paragraphs),
    'executor_FIO': '',

    'customer_company_index': '66666',
    'customer_company_adress': 'Усть залупинск',
    'customer_copany_INN': '3485734958732',
    'customer_company_KPP': '109823457039480934',
    'customer_company_OGRN': '2424234234234515',
    'customer_bank': 'Конча-банк',
    'customer_payment_account': '98759378246509384570319487503',
    'customer_correspondent_account': '99829342412313123',
    'customer_BIC': '1023472134',

    'executor_company_index': '29834239472',
    'executor_company_adress': 'Усть залупинск',
    'executor_company_INN': '10039480934',
    'executor_company_KPP': '89586596598',
    'executor_company_OGRN': '0871234987552135',
    'executor_payment_account': '0193485603948573091458734',
    'executor_correspondent_account': '098324576094756324',
    'executor_BIC': '2903587214',
}

context['additional_agreement_number'] = get_answer(question="Номер соглашения", documents=paragraphs)
context['contract_number'] = get_answer(question="Номер договора", documents=paragraphs)
context['contract_city'] = get_answer(question="В каком городе", documents=paragraphs)
context['customer_company_fullname'] = get_answer(question="Полное название компании заказчика", documents=paragraphs)
context['by_statment'] = get_answer(question="На основании", documents=paragraphs)
context['by_statment']= get_answer(question="На основании", documents=paragraphs)
context['executor_company_fullname'] = get_answer(question="Полное название компании исполнителя", documents=paragraphs)


names = []
for mrkp in text_mark_up.get_markup(text=" ".join(paragraphs)):
    if mrkp.block_type == MarkUpType.PERSON and mrkp.attachments["First"] is not None \
            and mrkp.attachments["Last"] is not None and mrkp.attachments["Middle"] is not None:
            names.append(f"{mrkp.attachments['Last']} {mrkp.attachments['First']} {mrkp.attachments['Middle']}")
        # print(mrkp.block_type, mrkp.text, mrkp.attachments)

context['customer_FIO'] = names[0]
context['executor_FIO'] = names[1]


for cell in cells:
    new_cell = cell
    while '\n' in new_cell or '  ' in new_cell :
        new_cell = str(new_cell).replace('\n', '  ').replace('  ', ' ').strip()
    if 'заказчик' in new_cell.lower():
        for mrkp in text_mark_up.get_markup(text=new_cell):
            if mrkp.block_type == MarkUpType.INN:
                context['customer_copany_INN'] = mrkp.text
            if mrkp.block_type == MarkUpType.KPP:
                context['customer_company_KPP'] = mrkp.text
            if mrkp.block_type == MarkUpType.OGRN:
                context['customer_company_OGRN'] = mrkp.text
            if mrkp.block_type == MarkUpType.BIC:
                context['customer_BIC'] = mrkp.text
            if mrkp.block_type == MarkUpType.RS:
                context['customer_payment_account'] = mrkp.text
            if mrkp.block_type == MarkUpType.LS:
                context['customer_correspondent_account'] = mrkp.text

    if 'поставщик' in new_cell.lower():
        for mrkp in text_mark_up.get_markup(text=new_cell):
            if mrkp.block_type == MarkUpType.INN:
                context['executor_copany_INN'] = mrkp.text
            if mrkp.block_type == MarkUpType.KPP:
                context['executor_company_KPP'] = mrkp.text
            if mrkp.block_type == MarkUpType.OGRN:
                context['executor_company_OGRN'] = mrkp.text
            if mrkp.block_type == MarkUpType.BIC:
                context['executor_BIC'] = mrkp.text
            if mrkp.block_type == MarkUpType.RS:
                context['executor_payment_account'] = mrkp.text
            if mrkp.block_type == MarkUpType.LS:
                context['executor_correspondent_account'] = mrkp.text

            print(mrkp.block_type, mrkp.text, new_cell)
    # print('cell=', new_cell)

print(context)


doc_gen = DocumentGenerator("docworker/templates/Дополнительное_соглашение_к_договору_поставки (Шаблон).docx")
doc_gen.generate_document(context, "Допсоглашение.docx")