import os
from docxtpl import DocxTemplate


class DocumentGenerator:
    """Class to generate documents from a Word template."""

    def __init__(self, template_path):
        """
        Initialize DocumentGenerator with a template path.

        Args:
            template_path (str): Path to the Word template file.

        Raises:
            FileNotFoundError: If the template does not exist.
        """
        if not os.path.isfile(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        self.template = DocxTemplate(template_path)

    def generate_document(self, context, output_path):
        """
        Generate a document by rendering the template with the given context.

        Args:
            context (dict): Context data to render in the document.
            output_path (str): Path where the generated document will be saved.

        Raises:
            ValueError: If context is not a dictionary.
            FileNotFoundError: If the output directory does not exist.
        """
        if not isinstance(context, dict):
            raise ValueError("Context must be a dictionary.")

        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            raise FileNotFoundError(f"Directory not found: {output_dir}")

        self.template.render(context)
        self.template.save(output_path)



# # # Протокол разногласий (ОСНОВНОЕ)
# context = {
#     'additional_agreement_number': '1',
#     'contract_number': 'номердоговора',
#     'contract_date': '35 февраля 2024',
#     'contract_city': 'Усть-залупинск',
#     'customer_company_fullname': 'ООО "Залупки"',
#
#     'customer_FIO': 'Заказчиков Заказчик Заказчикович',
#     'by_statment': 'Устава',
#
#     'executor_company_fullname': 'ИП "Усть"',
#     'executor_FIO': 'Полнителевич Исполнитель Исполнительевич',
#
#     'customer_company_index': '66666',
#     'customer_company_adress': 'Усть залупинск',
#     'customer_copany_INN': '3485734958732',
#     'customer_company_KPP': '109823457039480934',
#     'customer_company_OGRN': '2424234234234515',
#     'customer_bank': 'Конча-банк',
#     'customer_payment_account': '98759378246509384570319487503',
#     'customer_correspondent_account': '99829342412313123',
#     'customer_BIC': '1023472134',
#
#     'executor_company_index': '29834239472',
#     'executor_company_adress': 'Усть залупинск',
#     'executor_company_INN': '10039480934',
#     'executor_company_KPP': '89586596598',
#     'executor_company_OGRN': '0871234987552135',
#     'executor_payment_account': '0193485603948573091458734',
#     'executor_correspondent_account': '098324576094756324',
#     'executor_BIC': '2903587214',
# }
# doc_gen = DocumentGenerator("templates/Дополнительное_соглашение_к_договору_поставки (Шаблон).docx")
# doc_gen.generate_document(context, "Допсоглашение.docx")

# # Протокол разногласий
# context = {
#     'protocol_number': '1',
#     'contract_date': '29 февраля 3034 года',
#     'protocol_date': '«20» октября 2023 года',
#     'protocol_city': 'г. Екатеринбург',
#     'customer_FIO': 'Заказчиков Заказчик Заказчикович',
#     'customer_company_fullname': 'Компания заказчика ООО "Какой большой"',
#     'executor_FIO': 'Исполнителев Исполнитель Испольнительнович',
#     'executor_company_fullname': 'Компания исполнителя ИП "За деньги ДА"',
#
#     'customer_company_name': 'ООО "Какой большой"',
#     'customer_company_index': '66666',
#     'customer_company_adress': 'Россия, г. Усть-залупинск, ул. Хуйнахуй, д 66, к. 6',
#     'customer_company_INN': '5655566556',
#     'customer_company_KPP': '5655566556',
#     'customer_company_OGRN': '1205900031501',
#     'customer_director_name': 'Иванов И.И.',
#
#     'executor_company_name': 'ИП "За деньги ДА"',
#     'executor_company_index': '77777',
#     'executor_company_adress': 'Россия, г. 3пизды, ул. Чернь, д 77, к. 7',
#     'executor_company_INN': '5655566556',
#     'executor_company_KPP': '5655566556',
#     'executor_company_OGRN': '23452345234523452',
#     'executor_director_name': 'Петров Н.Н.'}
# doc_gen = DocumentGenerator("Протокол_разногласий (Шаблон).docx")
# doc_gen.generate_document(context, "Протокол_разногласий new.docx")


# # # Протокол разногласий (ОСНОВНОЕ)
# context = {
#     'additional_agreement_number': '1',
#     'contract_number': 'номердоговора',
#     'contract_date': '35 февраля 2024',
#     'contract_city': 'Усть-залупинск',
#     'customer_company_fullname': 'ООО "Залупки"',
#
#     'customer_FIO': 'Заказчиков Заказчик Заказчикович',
#     'by_statment': 'Устава',
#
#     'executor_company_fullname': 'ИП "Усть"',
#     'executor_FIO': 'Полнителевич Исполнитель Исполнительевич',
#
#     'customer_company_index': '66666',
#     'customer_company_adress': 'Усть залупинск',
#     'customer_copany_INN': '3485734958732',
#     'customer_company_KPP': '109823457039480934',
#     'customer_company_OGRN': '2424234234234515',
#     'customer_bank': 'Конча-банк',
#     'customer_payment_account': '98759378246509384570319487503',
#     'customer_correspondent_account': '99829342412313123',
#     'customer_BIC': '1023472134',
#
#     'executor_company_index': '29834239472',
#     'executor_company_adress': 'Усть залупинск',
#     'executor_company_INN': '10039480934',
#     'executor_company_KPP': '89586596598',
#     'executor_company_OGRN': '0871234987552135',
#     'executor_payment_account': '0193485603948573091458734',
#     'executor_correspondent_account': '098324576094756324',
#     'executor_BIC': '2903587214',
# }
# doc_gen = DocumentGenerator("templates/Дополнительное_соглашение_к_договору_поставки (Шаблон).docx")
# doc_gen.generate_document(context, "Допсоглашение.docx")

# # Протокол разногласий
# context = {
#     'protocol_number': '1',
#     'contract_date': '29 февраля 3034 года',
#     'protocol_date': '«20» октября 2023 года',
#     'protocol_city': 'г. Екатеринбург',
#     'customer_FIO': 'Заказчиков Заказчик Заказчикович',
#     'customer_company_fullname': 'Компания заказчика ООО "Какой большой"',
#     'executor_FIO': 'Исполнителев Исполнитель Испольнительнович',
#     'executor_company_fullname': 'Компания исполнителя ИП "За деньги ДА"',
#
#     'customer_company_name': 'ООО "Какой большой"',
#     'customer_company_index': '66666',
#     'customer_company_adress': 'Россия, г. Усть-залупинск, ул. Хуйнахуй, д 66, к. 6',
#     'customer_company_INN': '5655566556',
#     'customer_company_KPP': '5655566556',
#     'customer_company_OGRN': '1205900031501',
#     'customer_director_name': 'Иванов И.И.',
#
#     'executor_company_name': 'ИП "За деньги ДА"',
#     'executor_company_index': '77777',
#     'executor_company_adress': 'Россия, г. 3пизды, ул. Чернь, д 77, к. 7',
#     'executor_company_INN': '5655566556',
#     'executor_company_KPP': '5655566556',
#     'executor_company_OGRN': '23452345234523452',
#     'executor_director_name': 'Петров Н.Н.'}
# doc_gen = DocumentGenerator("Протокол_разногласий (Шаблон).docx")
# doc_gen.generate_document(context, "Протокол_разногласий new.docx")


# # Соглашение о расторжении контракта
# context = {'agreement_number': '123',
#            'contract_number': '345',
#            'contract_date': '23 июля 2019 года',
#            'agreement_city': 'г. Москва',
#            'agreement_date': '17 апреля 2024',
#            'customer_company_fullname': 'Компания заказчика ООО "Какой большой"',
#            'customer_position': 'Заместистель директора',
#            'customer_FIO': 'Заказчиков Заказчик Заказчикович',
#            'customer_basis_of': 'Приказ о том, что мужык главный',
#            'executor_company_fullname': 'Компания заказчика ООО "Какой большой"',
#            'executor_position': 'Заместистель директора',
#            'executor_FIO': 'Поставщик Поставщик Поставщик',
#            'executor_basis_of': 'Приказ о том, что мужык главный',
#            'order_sum': '1 000 000 000',
#            'customer_company_name': 'ООО "Какой большой"',
#            'customer_company_INN': '5655566556',
#            'customer_company_KPP': '5655566556',
#            'customer_company_adress': 'Россия, г. Усть-залупинск, ул. Хуйнахуй, д 66, к. 6',
#            'customer_company_phone': '8 (800) 555-35-35',
#            'customer_company_email': 'help@me.lps',
#            'executor_company_name': 'ООО "Какой большой"',
#            'executor_company_INN': '5655566556',
#            'executor_company_KPP': '5655566556',
#            'executor_company_adress': 'Россия, г. Солевой-Петербург, ул. Нюхачная, д 13, к. 6',
#            'executor_company_phone': '8 (800) 555-35-35',
#            'executor_company_email': 'help@me.lps'}
# doc_gen = DocumentGenerator("Образец соглашения расторжения контракта по 44-ФЗ по соглашению сторон (Шаблон).docx")
# doc_gen.generate_document(context, "расторжения контракта по 44-ФЗ по соглашению сторон.docx")
