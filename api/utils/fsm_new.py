from pycparser.ply.ctokens import t_PLUS
from sqlalchemy.sql.operators import from_

from api.utils.graph import Graph
from api.utils.node import Node


first_btn = ''
second_btn = ''

graph = Graph()

# Старт

graph.add_node(Node(id=1, attachment="""{'text':  'Вы можете заключить доп соглашение воспользовавшись нашим функционалом:',
                                       'buttons': [
                                           {'to': 2, 'text': 'Создать доп соглашение', 'color': first_btn},
                                       ], 'type': 'form',
                                       'field': None
                                       }"""))

graph.add_node(Node(id=2, attachment="""{'text':  'Напишите номер договора, к которому хотите создать дополнительное соглашение:',
                                        'placeholder': 'Введите номер договора',
                                       'buttons': [], 'type': 'input',
                                       'field': 'contract_number' 
                                       }"""))

# Изложение договора


graph.add_node(Node(id=3, attachment="""{'text': 'Выберите действие с договором:',
                                      'buttons': [
                                          {'to': 4, 'text': 'Изменить пункты договора', 'color': first_btn},
                                          {'to': 14, 'text': 'Изменить реквизиты договора', 'color': first_btn},
                                          {'to': 38, 'text': 'Завершить редактирование договора', 'color': first_btn}
                                      ], 'type': 'form'}"""))

graph.add_node(Node(id=4, attachment="""{'text': 'Выберите действия с пунктами договора:',
                                      'buttons': [
                                          {'to': 8, 'text': 'Изложение пункта', 'color': first_btn},
                                          {'to': 10, 'text': 'Исключение пункта', 'color': second_btn},
                                          {'to': 11, 'text': 'Добавление пункта', 'color': first_btn},
                                          {'to': 3, 'text': 'Назад', 'color': second_btn}
                                      ], 'type': 'form'}"""))

# Изменение пунктов договора

graph.add_node(Node(id=8, attachment="""{'text': 'Напишите название пункта, который вы хотите изложить подробнее:',
                                      'type': 'input', 'buttons': [], 'field': 'detail_paragraph',
                                      'placeholder': 'Введите название пункта'}"""))

graph.add_node(Node(id=9, attachment="""{'text': 'Напишите редакцию, которую вы хотите изменить :',
                                      'type': 'input', 'buttons': [], 'field': 'detail_text',
                                      'placeholder': 'Введите текст редакции', 'main_to': 4}"""))


# Исключение пунктов договора

graph.add_node(Node(id=10, attachment="""{'text': 'Напишите название пункта, который вы хотите исключить:',
                                      'type': 'input', 'buttons': [], 'field': 'except_paragraph',
                                      'placeholder': 'Введите название пункта', 'main_to': 4}"""))

# Добавление пункта договора

graph.add_node(Node(id=11, attachment="""{'text': 'Напишите название пункта, который вы хотите добавить:',
                                      'type': 'input', 'buttons': [], 'field': 'additional_paragraph',
                                      'placeholder': 'Введите название пункта'}"""))

graph.add_node(Node(id=12, attachment="""{'text': 'Напишите редакцию, в которой вы хотите добавить пункт:',
                                      'type': 'input', 'buttons': [], 'field': 'additional_text',
                                      'placeholder': 'Введите текст редакции', 'main_to': 4}"""))

# Редактирование реквизитов сторон

graph.add_node(Node(id=14, attachment="""{'text': 'Выберите сторону договора, реквизиты которой нужно изменить:',
                                      'buttons': [
                                          {'to': 15, 'text': 'Заказчик', 'color': first_btn},
                                          {'to': 16, 'text': 'Поставщик', 'color': second_btn},
                                          {'to': 3, 'text': 'Назад', 'color': second_btn}
                                      ], 'type': 'form'}"""))

# Заказчик

graph.add_node(Node(id=15, attachment="""{'text': 'Выберите реквизиты заказчика, которые вы хотели бы изменить:',
                                       'buttons': [
                                           {'to': 17, 'text': 'ИНН', 'color': first_btn},
                                           {'to': 18, 'text': 'ОГРН', 'color': second_btn},
                                           {'to': 19, 'text': 'КПП', 'color': first_btn},
                                           {'to': 20, 'text': 'Юридический адрес', 'color': second_btn},
                                           {'to': 21, 'text': 'Юридический индекс', 'color': first_btn},
                                           {'to': 22, 'text': 'Юридическое имя', 'color': second_btn},
                                           {'to': 23, 'text': 'Банк', 'color': first_btn},
                                           {'to': 24, 'text': 'БИК', 'color': second_btn},
                                           {'to': 25, 'text': 'Р/С', 'color': first_btn},
                                           {'to': 26, 'text': 'К/С', 'color': second_btn},
                                           {'to': 3, 'text': 'Назад', 'color': second_btn}
                                       ], 'type': 'form'}"""))

details = {'company_INN': 'ИНН', 'company_OGRN': 'ОГРН', 'company_KPP': 'КПП', 'company_adress': 'адрес',
           'company_index': 'индекс', 'company_fullname': 'Юридическое имя', 'bank': 'Банк', 'BIC': 'БИК', 'payment_account': 'Р/С',
           'correspondent_account': 'К/С'}


for i, field, name in zip(range(17, 27), list(details.keys()), list(details.values())):
    attachment = {'text': f'Напишите {name} заказчика',
                                           'buttons': [], 'type': 'input',
                                           'field': f'customer_{field}', 'placeholder': f'Введите {name} заказчика',
                                           'main_to': 15}
    graph.add_node(Node(id=i, attachment=f"""{attachment}"""))



# Поставщик

graph.add_node(Node(id=16, attachment="""{'text': 'Выберите реквизиты заказчика, которые вы хотели бы изменить:',
                                       'buttons': [
                                           {'to': 27, 'text': 'ИНН', 'color': first_btn},
                                           {'to': 28, 'text': 'ОГРН', 'color': second_btn},
                                           {'to': 29, 'text': 'КПП', 'color': first_btn},
                                           {'to': 30, 'text': 'Юридический адрес', 'color': second_btn},
                                           {'to': 31, 'text': 'Юридический индекс', 'color': first_btn},
                                           {'to': 32, 'text': 'Юридическое имя заказчика', 'color': second_btn},
                                           {'to': 33, 'text': 'Банк', 'color': first_btn},
                                           {'to': 34, 'text': 'БИК', 'color': second_btn},
                                           {'to': 35, 'text': 'Р/С', 'color': first_btn},
                                           {'to': 36, 'text': 'К/С', 'color': second_btn},
                                           {'to': 3, 'text': 'Назад', 'color': second_btn}
                                       ], 'type': 'form'}"""))


for i, field, name in zip(range(27, 37), list(details.keys()), list(details.values())):
    attachment = {'text': f'Напишите {name} поставщика',
                                           'buttons': [], 'type': 'input',
                                           'field': f'supplier_{field}', 'placeholder': f'Введите {name} поставщика',
                                           'main_to': 16}
    graph.add_node(Node(id=i, attachment=f"""{attachment}"""))


graph.add_node(Node(id=37, attachment="""{'text': 'Это всё что вы хотели отредактировать?',
                                       'buttons': [
                                           {'to': 38, 'text': 'Да', 'color': first_btn},
                                           {'to': 3, 'text': 'Нет', 'color': second_btn}
                                       ], 'type': 'form'}"""))

graph.add_node(Node(id=38, attachment="""{'type': 'save'}"""))

# Старт

graph.add_edge(from_id=1, to_id=2, key='to2node')
graph.add_edge(from_id=2, to_id=3, key='to3node')

graph.add_edge(from_id=3, to_id=4, key='to4node')

graph.add_edge(from_id=4, to_id=8, key='to5node')
graph.add_edge(from_id=4, to_id=10, key='to6node')
graph.add_edge(from_id=4, to_id=11, key='to7node')

graph.add_edge(from_id=8, to_id=9, key='to9node')

# Редактирование реквизитов сторон

graph.add_edge(from_id=11, to_id=12, key='to12node')

graph.add_edge(from_id=14, to_id=15, key='to15node')
graph.add_edge(from_id=14, to_id=16, key='to16node')

for i in range(17, 27):
    graph.add_edge(from_id=15, to_id=i, key=f'to{i}node')

for i in range(27, 37):
    graph.add_edge(from_id=16, to_id=i, key=f'to{i}node')

# Заказчик