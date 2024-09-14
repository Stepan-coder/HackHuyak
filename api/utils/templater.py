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
