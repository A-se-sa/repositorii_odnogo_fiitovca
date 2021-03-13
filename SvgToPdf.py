from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfFileReader, PdfFileWriter
from tkinter.filedialog import asksaveasfilename
import os, shutil
import requests

"""
Программа вытаскивает презентацию по ссылке с ббб
Скачивает страницы в директорий PARSER_DIR в svg-формате
в папку SVG_DIR.Затем файлы конвертируются в pdf страницы 
в папку PDF_DIR с помощью функции convert_to_pdf,а затем 
с помощью merge_pdf страницы склеиваются в 1 pdf файл по 
адресу LECTION_PATH.
Промежуточные папки со страницами удаляются в конце

"""
PARSER_DIR = 'D:/'
SVG_DIR = PARSER_DIR + 'SVG/'
PDF_DIR = PARSER_DIR + 'PDF/'
DESKTOP_PATH = 'C:/Users/роппг/Desktop'
LECTION_PATH = DESKTOP_PATH + 'Lection' + '.pdf'

def get_svg(link):
    svg_pos = link.rfind('/')
    link_path = link[:svg_pos + 1]
    i = 1
    while True:
        try:
            ufr = requests.get(link_path + str(i))
            if ufr.status_code == 404:
                break
            with open(SVG_DIR + str(i) +'.svg', 'wb') as f:
                f.write(ufr.content)
            print(i, '.svg')
            i += 1
        except Exception as e:
            print('Скачивание завершено', str(e))
            break


# Получает файлы из указанного директория
def get_files(path):
    try:
        return os.listdir(path)
    except IOError:
        print('Не удалось открыть директорий по адресу ', path)


# Сортирует файлы по имени по возрастанию в директории по указанному адресу
def get_sorted_files_name_asc(path):
    return sorted(get_files(path), key=lambda x: int(x.split('.')[0]))


# Если директорий не создан - создаёт директорий по указанному адресу
def create_dir(dir_):
    if not os.path.exists(dir_):
        os.mkdir(dir_)
        print(' Создан директорий ', dir_)


# Удаляет директории по указанному адресу
def del_med_dirs(pdf_dir, svg_dir):
    shutil.rmtree(svg_dir)
    shutil.rmtree(pdf_dir)


# 1 файл svg в файл 1 pdf
def svg_to_pdf_page(svg_path, pdf_page_path):
    drawing = svg2rlg(svg_path)
    renderPDF.drawToFile(drawing, pdf_page_path)


# Конверитрование всех svg из папки svg_dir в pdf в папку pdf_dir
def convert_to_pdf(svg_dir, pdf_dir):
    svg_pathes = get_files(svg_dir)
    print('SVG файлы', svg_pathes)
    for svg_path in svg_pathes:
        pdf_name = os.path.splitext(svg_path)[0] + '.pdf'
        print(pdf_name, ' создан.')
        svg_to_pdf_page(svg_dir + svg_path, pdf_dir + pdf_name)


# Склеивание всех pdf страниц в папке pdf_pages_path в 1 файл
def merge_pdf(pdf_pages_path, res_pdf):
    pdf_writer = PdfFileWriter()
    pdf_pathes = get_sorted_files_name_asc(pdf_pages_path)
    print('PDF листы ', pdf_pathes)
    for page_path in pdf_pathes:
        pdf_reader = PdfFileReader(pdf_pages_path + page_path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(res_pdf, 'wb') as res:
        pdf_writer.write(res)


def converting():

    # Конвертируем в pdf
    convert_to_pdf(SVG_DIR, PDF_DIR)
    print('Конвертирование завершено')

    # файловое диалоговое окно,получения пути к файлу сохранения
    lection_path = asksaveasfilename(
        initialfile='Lection.pdf',
        filetypes=(("PDF files", "*.pdf"),)
    )
    # если путь не передан
    if not lection_path:
        print(' Файл будет сохранён на рабочем столе')
        lection_path = LECTION_PATH

    print(' Путь: ', lection_path)

    # Склеиваем в 1 файл
    merge_pdf(PDF_DIR, lection_path)
    print(' PDF файл создан')

    # Удаляем промежуточные результаты
    del_med_dirs(PDF_DIR, SVG_DIR)

    # Открытие результата
    os.startfile(lection_path)


print(TEST_LINK)
link = input('введите ссылку на лист презентации из ббб: ')
# Создаём директории
create_dir(SVG_DIR)
create_dir(PDF_DIR)

get_svg(link)
converting()

