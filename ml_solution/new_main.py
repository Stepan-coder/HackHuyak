import os
from typing import List
from docworker.docreader import read_docx_in_paragraphs, read_table_in_paragraphs
from models import AnswerModel, RerankerModel
from NER import *
from docworker.templater import DocumentGenerator



# Хитрая штука для получения 10 ответов на вопрос пользователя
def get_answer(question: str, documents: List[str]):
    text_ranks = this_reranker_model.predict(query=question, documents=documents)
    variants = list(set([this_answer_model.predict(question=question, context=tr) for tr in list(text_ranks.keys())[:10]]))
    text_ranks = this_reranker_model.predict(query=question, documents=variants)
    return list(text_ranks.keys())[0]


def fill_context(context, paragraphs, cells, answer_model: AnswerModel, reranker_model: RerankerModel,
                 text_mark_up: TextMarkUp):
    context['additional_agreement_number'] = get_answer(question="Номер соглашения", documents=paragraphs)
    context['contract_number'] = get_answer(question="Номер договора", documents=paragraphs)
    context['contract_city'] = get_answer(question="В каком городе", documents=paragraphs)
    context['by_statment'] = get_answer(question="На основании", documents=paragraphs)
    names = []
    money = []
    # Вызываем 'разметчик", проверяем, что имя, фамилия и отчества присутствуют одновременно. Добавляем в список имен
    for mrkp in text_mark_up.get_markup(text=" ".join(paragraphs)):
        if mrkp.block_type == MarkUpType.PERSON and mrkp.attachments["First"] is not None \
                and mrkp.attachments["Last"] is not None and mrkp.attachments["Middle"] is not None:
            names.append(f"{mrkp.attachments['Last']} {mrkp.attachments['First']} {mrkp.attachments['Middle']}")
        if mrkp.block_type == MarkUpType.MONEY:
            money.append(mrkp.attachments['Amount'])

    # Первым всегда идет заказчик
    context['customer_FIO'] = names[0]

    # Вторым всегда идет поставщик
    context['executor_FIO'] = names[1]

    # Тут у нас распаршены таблицы (поячеячно), с помощью нейронок достаем нужные данные (говнокод, время 6 утра)))))
    for cell in cells:
        new_cell = cell
        while '\n' in new_cell or '  ' in new_cell:
            new_cell = str(new_cell).replace('\n', '  ').replace('  ', ' ').strip()
        for mrkp in text_mark_up.get_markup(text=new_cell):
            if mrkp.block_type == MarkUpType.MONEY:
                money.append(mrkp.attachments['Amount'])
        if 'заказчик' in new_cell.lower():
            for mrkp in text_mark_up.get_markup(text=new_cell):
                if mrkp.block_type == MarkUpType.INN:
                    context['customer_copany_INN'] = mrkp.text.lower().replace('инн', '').strip()
                    context['customer_company_fullname'] = answer_model.predict(
                        question="Какое полное название у заказчика?",
                        context=new_cell).strip()
                    context['customer_company_adress'] = answer_model.predict(
                        question="Какой полный юридический адрес?",
                        context=new_cell).strip()
                    context['customer_bank'] = answer_model.predict(question="Какой банк у организации?",
                                                                    context=new_cell).strip()
                if mrkp.block_type == MarkUpType.KPP:
                    context['customer_company_KPP'] = mrkp.text.lower().replace('кпп', '').strip()
                if mrkp.block_type == MarkUpType.OGRN:
                    context['customer_company_OGRN'] = mrkp.text.lower().replace('огрн', '').strip()
                if mrkp.block_type == MarkUpType.BIC:
                    context['customer_BIC'] = mrkp.text.lower().replace('бик', '').strip()
                if mrkp.block_type == MarkUpType.RS:
                    context['customer_payment_account'] = mrkp.text.replace('р/с', '').strip()
                if mrkp.block_type == MarkUpType.LS:
                    context['customer_correspondent_account'] = mrkp.text.replace('к/с', '').strip()
                if mrkp.block_type == MarkUpType.INDEX:
                    context['customer_company_index'] = mrkp.text

        if 'поставщик' in new_cell.lower():
            for mrkp in text_mark_up.get_markup(text=new_cell):
                if mrkp.block_type == MarkUpType.INN:
                    context['executor_copany_INN'] = mrkp.text.lower().replace('инн', '').strip()
                    context['executor_company_fullname'] = answer_model.predict(
                        question="Какое полное название у поставщика?",
                        context=new_cell).strip()
                    context['executor_company_adress'] = answer_model.predict(
                        question="Какой полный юридический адрес?",
                        context=new_cell).strip()
                    context['executor_bank'] = answer_model.predict(question="Какой банк у организации?",
                                                                    context=new_cell).strip()
                if mrkp.block_type == MarkUpType.KPP:
                    context['executor_company_KPP'] = mrkp.text.lower().replace('кпп', '').strip()
                if mrkp.block_type == MarkUpType.OGRN:
                    context['executor_company_OGRN'] = mrkp.text.lower().replace('огрн', '').strip()
                if mrkp.block_type == MarkUpType.BIC:
                    context['executor_BIC'] = mrkp.text.lower().replace('бик', '').strip()
                if mrkp.block_type == MarkUpType.RS:
                    context['executor_payment_account'] = mrkp.text.replace('р/с', '').strip()
                if mrkp.block_type == MarkUpType.INDEX:
                    context['executor_company_index'] = mrkp.text.replace('к/с', '').strip()
    context['contract_summ'] = sorted(money, reverse=True)[0]
    return context


# Наш json - который редактируем
context = {
    'additional_agreement_number': 'test',
    'contract_number': 'test',
    'contract_date': 'test',
    'contract_city': 'test',
    'customer_company_fullname': 'test',

    'contract_summ': 'test',

    'customer_FIO': 'test',
    'by_statment': 'test',

    'executor_company_fullname': 'test',
    'executor_FIO': 'test',

    'detail_paragraph': 'test',
    'detail_text': 'test',
    'except_paragraph': 'test',
    'additional_paragraph': 'test',
    'additional_text': 'test',
    'metadata': '',

    'customer_company_index': 'test',
    'customer_company_adress': 'test',
    'customer_copany_INN': 'test',
    'customer_company_KPP': 'test',
    'customer_company_OGRN': 'test',
    'customer_bank': 'test',
    'customer_payment_account': 'test',
    'customer_correspondent_account': 'test',
    'customer_BIC': 'ТЕСТ',

    'executor_company_index': 'test',
    'executor_company_adress': 'test',
    'executor_company_INN': 'test',
    'executor_company_KPP': 'test',
    'executor_company_OGRN': 'test',
    'executor_bank': 'test',
    'executor_payment_account': 'test',
    'executor_correspondent_account': 'test',
    'executor_BIC': 'test',
}


# Загружаем модель для получения ответов
this_answer_model = AnswerModel()

# Загружаем модель для ранжировки вариантов ответов (наиболее подходящий - ближе к началу)
this_reranker_model = RerankerModel()

# Запускаем распознавалку таких сущностей как имена, деньги
this_text_mark_up = TextMarkUp(is_bert=False, download=False, is_pro_bert=False)

for file in os.listdir(os.path.join(os.getcwd(), 'documents')):
    print(file)
    try:
        # Путь до договора ОБЯЗАТЕЛЬНО в формате .docx
        file_path = os.path.join(os.getcwd(), 'documents', file)

        # Читаем текст из документа
        paragraphs1 = read_docx_in_paragraphs(file_path)

        # Читаем ячейки таблицы из документа
        cells1 = read_table_in_paragraphs(file_path)

        if len(cells1) == 0 and len(paragraphs1) == 0:
            continue

        # Переменная для хранения списка име (у нас всего 2 стороны, причем сперва пишется заказчик, а потом исполнитель)
        new_context = fill_context(context=context,
                                   paragraphs=paragraphs1,
                                   cells=cells1,
                                   answer_model=this_answer_model,
                                   reranker_model=this_reranker_model,
                                   text_mark_up=this_text_mark_up)
        print(file, len(paragraphs1), len(cells1))
        # Читаем шаблон
        doc_gen = DocumentGenerator("docworker/templates/Дополнительное_соглашение_к_договору_поставки (Шаблон).docx")

        # Сохраняем файл
        doc_gen.generate_document(context, f"dopniki/Доп_соглашение для {file.split('.')[0]}.docx")
    except:
        pass