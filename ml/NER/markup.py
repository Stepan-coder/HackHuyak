# from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsNER
# from natasha import Doc
#
#
# class YourClass:
#     def __init__(self):
#         self.segmenter = Segmenter()
#         self.morph_vocab = MorphVocab()
#         self.embeddings = NewsEmbedding()
#         self.ner = NewsNER(self.embeddings)
#
#     def get_bert_markup(self, text: str, start_index: int = 0) -> List[MarkUpBlock]:
#         """
#         :param start_index:
#         :param text: The text which we need to markup
#         :return: List[MarkUpBlock]
#         """
#         last_block_type = None
#         text_markup = []
#
#         # Создание документа и выполнение NER
#         doc = Doc(text)
#         doc.segment(self.segmenter)
#         doc.tag_ner(self.ner)
#
#         for span in doc.spans:
#             tok = text[span.start:span.stop]
#             block_type = MarkUpType(str(span.type))
#
#             gap = text[:span.start]
#             text = text[span.stop:]
#
#             if span.type == 'O' or (block_type != last_block_type and
#                                     (not span.type.startswith("I-") or (
#                                             len(text_markup) == 0 and span.type.startswith("I-")))):
#                 text_markup.append(MarkUpBlock(text=(gap + tok).strip(),
#                                                block_type=block_type,
#                                                start=start_index,
#                                                end=start_index + len(gap) + len(tok)))
#             else:
#                 text_markup[-1].text += gap + tok
#                 text_markup[-1].text = text_markup[-1].text.strip()
#                 text_markup[-1].end += len(gap) + len(tok)
#
#             start_index += len(gap) + len(tok)
#             last_block_type = block_type
#
#         return text_markup
