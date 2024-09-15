import time

from models import YaGPT
from tqdm import tqdm

yagpt = YaGPT(catalog_id='b1gaa0i749eqe9ogone8', api_key='AQVN2yvuhm5p2BeZDjf-wj-k0qC1sHRVoZUYM_r3')
yagpt.set_context(context='Ты юрист и эксперт по тендерам, в особенности по тендерам и 44-ФЗ')
# yagpt.set_context(context='Ты бизнесмен изанимаешься, а возможно только хочешь заниматься тендерами, по 44-ФЗ')
#
# lines = []
# with open('44fz.txt') as file:
#     for line in file.readlines():
#         new_line = line
#         while '\n' in new_line or '  ' in new_line:
#             new_line = new_line.replace('\n', ' ').replace('  ', ' ').strip()
#         if len(line) != 0:
#             lines.append(new_line)
#
#
# questions = []
# for line in tqdm(lines):
#     question = yagpt.get_GPT_answer(query=f"Придумай 3 вопроса, разделенные симолом '#' к "
#                                           f"этому пункту/подпункту 44-ФЗ: {line}. В ответе напиши только эти 3 вопроса.")
#
#     while '\n' in question or  '*' in question or '  ' in question:
#         question = question.replace('\n', ' ').replace('*', ' ').replace('  ', ' ').strip()
#
#     for q in question.split('#'):
#         if len(q) > 0:
#             questions.append(q.strip() + '\n')
#     time.sleep(1)
#
# with open('questions.txt', 'w', encoding='utf-8') as file:
#     file.writelines(questions)




# answers = []
# with open('questions.txt') as file:
#     for question in tqdm(file.readlines()):
#         answer = yagpt.get_GPT_answer(query=f"Максимально четко и лаконично ответь на этот вопрос: {question}."
#                                             f"Ответ представь в виде одного абзаца текста. Дополительную разметку использовать нельзя.")
#
#         while '\n' in answer or '*' in answer or '  ' in answer:
#             answer = answer.replace('\n', ' ').replace('*', ' ').replace('  ', ' ').strip()
#         # print(question)
#         # print(">>>>", answer)
#         answers.append(answer + '\n')
#         time.sleep(1)
#
#
#
# with open('answers.txt', 'w', encoding='utf-8') as file:
#     file.writelines(answers)