from pycparser.ply.ctokens import t_PLUS
from sqlalchemy.sql.operators import from_

from api.utils.graph import Graph
from api.utils.node import Node


first_btn = ''
second_btn = ''

graph = Graph()

# 1 Level

graph.add_node(Node(id=1, attachment={'text':  'Вы можете заключить доп соглашение воспользовавшись нашим функционалом:',
                                       'buttons': [
                                           {'to': 'to2node', 'text': 'Создать доп соглашение', 'color': first_btn},
                                           {'to': 'to3node', 'text': 'Отследить статус доп соглашения', 'color': second_btn}
                                       ], 'type': 'form',
                                       'field': None
                                       }))

graph.add_node(Node(id=2), attachment={'text':  'Напишите номер договора, к которому хотите создать доп. соглашение',
                                       'buttons': [], 'type': 'input',
                                       'field': 'number',
                                       })
graph.add_node(Node(id=3))

# 2 Level

graph.add_node(Node(id=4, attachment={'text':  'Укажите причину изменений',
                                       'buttons': [
                                           {'to': 5, 'text': 'Необходимо изменить объём работ', 'color': first_btn,
                                            'to': 9, 'text': 'Необходимо внести изменения в договор', 'color': second_btn,
                                            'to': 14, 'text': 'Изменились реквизиты сторон', 'color': first_btn,
                                            'to': 39, 'text': 'Изменились реквизиты сторон', 'color': second_btn}
                                       ], 'type': 'form',
                                       'field': 'reason_changes',
                                       }))

graph.add_node(Node(id=5, attachment={'text': 'Перед вами отобразятся все товары спецификации, пожалуйста отредактируйте необходимый товар',
                                      'buttons': [], 'type': 'inout', 'field': 'specification'}))

graph.add_node(Node(id=6, attachment={'text': 'Вам необходимо еще внести изменения?',
                                      'buttons': [
                                          {'to': 7, 'text': 'Подтверждаю', 'color': first_btn},
                                          {'to': 4, 'text': 'Отмена', 'color': second_btn}
                                      ], 'type': 'form'}))

graph.add_node(Node(id=7, attachment={'text': 'Вам необходимо еще внести изменения?',
                                      'buttons': [
                                          {'to': 4, 'text': 'Да', 'color': first_btn},
                                          {'to': 8, 'text': 'Нет', 'color': second_btn}
                                      ], 'type': 'form'}))

graph.add_node(Node(id=8, attachment={'text': 'Ваши изменения отправлены, ожидайте  решения. Уведомление также продублируется вам на почту.',
                                      'buttons': [
                                          {'to': 'download', 'text': 'Скачать сформированное доп.соглашение', 'color': first_btn},
                                          {'to': 'download', 'text': 'Скачать сформированную спецификацию', 'color': second_btn}
                                      ], 'type': 'form'}))

# 3 Level

graph.add_node(Node(id=9, attachment={'text': 'Введите номер пункта договора',
                                      'buttons': [], 'type': 'input'}))

graph.add_node(Node(id=10, attachment={'text': 'Введите вашу редакцию пункта договора',
                                       'buttons': [], 'type': 'input'}))

graph.add_node(Node(id=11, attachment={'text': 'Подтвердите корректность ранее введенных данных',
                                       'buttons': [
                                           {'to': 13, 'text': 'Подтверждаю', 'color': first_btn},
                                           {'to': 4, 'text': 'Отмена', 'color': second_btn}
                                       ]}))

graph.add_node(Node(id=12, attachment={'text': 'Вам необходимо еще внести изменения?',
                                       'buttons': [
                                           {'to': 4, 'text': 'Да', 'color': first_btn},
                                           {'to': 13, 'text': 'Нет', 'color': second_btn}
                                       ], 'type': 'form'}))


graph.add_node(Node(id=13, attachment={'text': 'Ваши изменения отправлены, ожидайте  решения. Уведомление также продублируется вам на почту.',
                                       'buttons': [
                                           {'to': 'download', 'text': 'Скачать сформированное доп.соглашение', 'color': first_btn}
                                       ], 'type': 'form'}))

# 4 Level

graph.add_node(Node(id=14, attachment={'text': 'Какие данные вы хотите изменить?',
                                       'buttons': [
                                           {'to': 36, 'text': 'КПП', 'color': first_btn},
                                           {'to': 35, 'text': 'ОГРН', 'color': second_btn},
                                           {'to': 37, 'text': 'Сокращенное наименование', 'color': first_btn},
                                           {'to': 38, 'text': 'Полное наименование', 'color': second_btn},
                                           {'to': 15, 'text': 'Банковские реквизиты', 'color': first_btn},
                                           {'to': 19, 'text': 'Данные руководителя', 'color': second_btn},
                                           {'to': 24, 'text': 'Юридический адрес', 'color': first_btn}
                                       ], 'type': 'form'}))

# Реквизиты

graph.add_node(Node(id=15, attachment={'text': 'Какие банковские реквизиты вы хотите изменить?',
                                       'buttons': [
                                           {'to': 16, 'text': 'Название банка', 'color': first_btn},
                                           {'to': 17, 'text': 'К/С', 'color': first_btn},
                                           {'to': 18, 'text': 'Р/С', 'color': first_btn}], 'type': 'form'}))

graph.add_node(Node(id=16, attachment={'text': 'Название банка',
                                       'buttons': [], 'type': 'input',
                                       'field': 'bank_name'}))

graph.add_node(Node(id=17, attachment={'text': 'К/С',
                                       'buttons': [], 'type': 'input',
                                       'field': 'k_s'}))

graph.add_node(Node(id=18, attachment={'text': 'Р/C',
                                       'buttons': [], 'type': 'input',
                                       'field': 'r_s'}))

# Владелец

graph.add_node(Node(id=19, attachment={'text': 'Какие данные по руководителю  вы хотите изменить?',
                                       'buttons': [
                                           {'to': 20, 'text': 'Имя', 'color': first_btn},
                                           {'to': 21, 'text': 'Фамилия', 'color': first_btn},
                                           {'to': 22, 'text': 'Отчество', 'color': first_btn},
                                           {'to': 23, 'text': 'Должность', 'color': first_btn}
                                       ], 'type': 'form'}))

graph.add_node(Node(id=20, attachment={'text': 'Имя',
                                       'buttons': [], 'type': 'input', 'field': 'name'}))

graph.add_node(Node(id=21, attachment={'text': 'Фамилия',
                                       'buttons': [], 'type': 'input', 'field': 'surname'}))

graph.add_node(Node(id=22, attachment={'text': 'Отчество',
                                       'buttons': [], 'type': 'input', 'field': 'patronymic'}))

graph.add_node(Node(id=23, attachment={'text': 'Должность',
                                       'buttons': [], 'type': 'input', 'field': 'position'}))

# Юридический адрес

graph.add_node(Node(id=24, attachment={'text': 'Какие данные в юридическом адресе вы хотите изменить?',
                                       'buttons': [
                                           {'to': 25, 'text': 'Индекс', 'color': first_btn},
                                           {'to': 26, 'text': 'Улица', 'color': first_btn},
                                           {'to': 27, 'text': 'Квартира', 'color': first_btn},
                                       ], 'type': 'input'}))

graph.add_node(Node(id=25, attachment={'text': 'Индекс',
                                       'buttons': [], 'type': 'input', 'field': 'index'}))

graph.add_node(Node(id=26, attachment={'text': 'Улица',
                                       'buttons': [], 'type': 'input', 'field': 'street'}))

graph.add_node(Node(id=27, attachment={'text': 'Квартира',
                                       'buttons': [], 'type': 'input', 'field': 'apartment'}))

# Почтовый адрес

graph.add_node(Node(id=28, attachment={'text': 'Какие данные в почтовом адресе вы хотите изменить?',
                                       'buttons': [
                                           {'to': 29, 'text': 'Индекс', 'color': first_btn},
                                           {'to': 30, 'text': 'Улица', 'color': first_btn},
                                           {'to': 31, 'text': 'Квартира', 'color': first_btn},
                                           {'to': 32, 'text': 'Регион', 'color': first_btn},
                                           {'to': 33, 'text': 'Населенный пункт', 'color': first_btn},
                                           {'to': 34, 'text': 'Дом', 'color': first_btn},
                                       ], 'type': 'input'}))

graph.add_node(Node(id=29, attachment={'text': 'Индекс',
                                       'buttons': [], 'type': 'input', 'field': 'index'}))

graph.add_node(Node(id=30, attachment={'text': 'Улица',
                                       'buttons': [], 'type': 'input', 'field': 'street'}))

graph.add_node(Node(id=31, attachment={'text': 'Квартира',
                                       'buttons': [], 'type': 'input', 'field': 'apartment'}))

graph.add_node(Node(id=32, attachment={'text': 'Регион',
                                       'buttons': [], 'type': 'input', 'field': 'region'}))

graph.add_node(Node(id=33, attachment={'text': 'Населенный пункт',
                                       'buttons': [], 'type': 'input', 'field': 'city'}))

graph.add_node(Node(id=34, attachment={'text': 'Дом',
                                       'buttons': [], 'type': 'input', 'field': 'house'}))

# ОГРН

graph.add_node(Node(id=35, attachment={'text': 'ОГРН',
                                       'buttons': [], 'type': 'input', 'field': 'ogrn'}))

# КПП

graph.add_node(Node(id=36, attachment={'text': 'КПП',
                                       'buttons': [], 'type': 'input', 'field': 'kpp'}))

# Сокращенное наименование

graph.add_node(Node(id=37, attachment={'text': 'Сокращенное наименование',
                                       'buttons': [], 'type': 'input', 'field': 'short_name'}))

# Полное наименование

graph.add_node(Node(id=38, attachment={'text': 'Полное наименование',
                                       'buttons': [], 'type': 'input', 'field': 'full_name'}))

# 5 Level

graph.add_node(Node(id=39))


# 1 Level
graph.add_edge(from_id=1, to_id=2, key='to2node')
graph.add_edge(from_id=1, to_id=3, key='to3node')

# 2 Level
graph.add_edge(from_id=2, to_id=4, key='to4node')

graph.add_edge(from_id=4, to_id=5, key='to5node')
graph.add_edge(from_id=4, to_id=9, key='to9node')
graph.add_edge(from_id=4, to_id=14, key='to14node')
graph.add_edge(from_id=4, to_id=39, key='to39node')

graph.add_edge(from_id=5, to_id=6, key='to6node')
graph.add_edge(from_id=9, to_id=10, key='to10node')
graph.add_edge(from_id=10, to_id=11, key='to11node')


graph.add_edge(from_id=15, to_id=16, key='to16node')
graph.add_edge(from_id=15, to_id=17, key='to17node')
graph.add_edge(from_id=15, to_id=18, key='to18node')

graph.add_edge(from_id=19, to_id=20, key='to20node')
graph.add_edge(from_id=19, to_id=21, key='to21node')
graph.add_edge(from_id=19, to_id=22, key='to22node')
graph.add_edge(from_id=19, to_id=23, key='to23node')

graph.add_edge(from_id=24, to_id=25, key='to25node')
graph.add_edge(from_id=24, to_id=26, key='to26node')
graph.add_edge(from_id=24, to_id=27, key='to27node')

graph.add_edge(from_id=28, to_id=29, key='to29node')
graph.add_edge(from_id=28, to_id=30, key='to30node')
graph.add_edge(from_id=28, to_id=31, key='to31node')
graph.add_edge(from_id=28, to_id=32, key='to32node')
graph.add_edge(from_id=28, to_id=33, key='to33node')
graph.add_edge(from_id=28, to_id=34, key='to34node')


graph.add_edge(from_id=14, to_id=35, key='to35node')
graph.add_edge(from_id=14, to_id=36, key='to36node')
graph.add_edge(from_id=14, to_id=37, key='to37node')
graph.add_edge(from_id=14, to_id=38, key='to38node')
graph.add_edge(from_id=14, to_id=15, key='to15node')
graph.add_edge(from_id=14, to_id=19, key='to19node')
graph.add_edge(from_id=14, to_id=24, key='to24node')





