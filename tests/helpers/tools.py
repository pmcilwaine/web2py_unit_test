import cgi
import mimetypes
import os


def upload(field_name, file_path):
    """

    :param field_name: The name of the upload field
    :param file_path: The path to the file in the testing folder. Should be relative to the test_files folder
    """
    file_path = os.path.join(
        os.getcwd(), 'test_files', file_path
    )

    field = cgi.FieldStorage()

    field.name = field_name
    field.filename = os.path.basename(file_path)
    field.type = mimetypes.guess_type(file_path)[0]
    field.file = field.make_file()
    field.file.write(open(file_path, 'rb').read())
    field.file.seek(0)

    return field
