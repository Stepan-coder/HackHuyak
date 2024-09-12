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



context = {
    'protocol_number': '1',
    'contract_date': '29 февраля 3034 года',
    'protocol_date': '«20» октября 2023 года',
    'protocol_city': 'г. Екатеринбург',
    'customer_FIO': 'Заказчиков Заказчик Заказчикович',
    'customer_company_fullname': 'Компания заказчика ООО "Какой большой"',
    'executor_FIO': 'Исполнителев Исполнитель Испольнительнович',
    'executor_company_fullname': 'Компания исполнителя ИП "За деньги ДА"',

    'customer_company_name': 'ООО "Какой большой"',
    'customer_company_index': '66666',
    'customer_company_adress': 'Россия, г. Усть-залупинск, ул. Хуйнахуй, д 66, к. 6',
    'customer_company_INN': '5655566556',
    'customer_company_KPP': '5655566556',
    'customer_company_OGRN': '1205900031501',
    'customer_director_name': 'Иванов И.И.',

    'executor_company_name': 'ИП "За деньги ДА"',
    'executor_company_index': '77777',
    'executor_company_adress': 'Россия, г. 3пизды, ул. Чернь, д 77, к. 7',
    'executor_company_INN': '5655566556',
    'executor_company_KPP': '5655566556',
    'executor_company_OGRN': '23452345234523452',
    'executor_director_name': 'Петров Н.Н.'}

doc_gen = DocumentGenerator("Протокол_разногласий (Шаблон).docx")
doc_gen.generate_document(context, "Протокол_разногласий new.docx")
