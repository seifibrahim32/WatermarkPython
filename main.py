import PyPDF2
import tkinter
from tkinter import filedialog
import cv2
from fpdf import FPDF
from imwatermark import WatermarkEncoder, WatermarkDecoder
from pdf2image import convert_from_path


def watermarkingImage():
    root = tkinter.Tk()  # pointing root to Tk() to use it as Tk() in program. >>>
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)  # Opened windows will be active.above all windows despite of selection.
    print("\nSelect your needed file to be watermarked\n")
    open_file = filedialog.askopenfilename()
    print(open_file)

    print("\nSelect the suitable watermark\n")
    img = cv2.imread(open_file)
    open_file = filedialog.askopenfilename()
    print(open_file)
    watermark = cv2.imread(open_file)

    percent_of_scaling = 50
    new_width = int(img.shape[1] * percent_of_scaling / 100)
    new_height = int(img.shape[0] * percent_of_scaling / 100)
    new_dim = (new_width, new_height)
    resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)

    wm_scale = 40
    wm_width = int(watermark.shape[1] * wm_scale / 100)
    wm_height = int(watermark.shape[0] * wm_scale / 100)
    wm_dim = (wm_width, wm_height)

    resized_wm = cv2.resize(watermark, wm_dim, interpolation=cv2.INTER_AREA)

    h_img, w_img, _ = resized_img.shape
    center_y = int(h_img / 2)
    center_x = int(w_img / 2)
    h_wm, w_wm, _ = resized_wm.shape
    top_y = center_y - int(h_wm / 2)
    left_x = center_x - int(w_wm / 2)
    bottom_y = top_y + h_wm
    right_x = left_x + w_wm

    roi = resized_img[top_y:bottom_y, left_x:right_x]
    result = cv2.addWeighted(roi, 1, resized_wm, 0.3, 0)
    resized_img[top_y:bottom_y, left_x:right_x] = result

    filename = 'watermarked_image.jpg'
    cv2.imwrite(filename, resized_img)
    cv2.imshow("Resized Input Image", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    root.destroy()


def watermarkingPDF():

    root = tkinter.Tk()  # pointing root to Tk() to use it as Tk() in program. >>>
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)  # Opened windows will be active.above all windows despite of selection.

    print("\nSelect your needed file to be watermarked\n")

    input_file = filedialog.askopenfilename()

    output_file = "watermarked_file.pdf"

    print("\nSelect your watermark\n")

    watermark_file = filedialog.askopenfilename()

    with open(input_file, "rb") as filehandle_input:
        # read content of the original file
        input_read_pdf = PyPDF2.PdfFileReader(filehandle_input)

        with open(watermark_file, "rb") as filehandle_watermark:
            # read content of the watermark
            watermark = PyPDF2.PdfFileReader(filehandle_watermark)

            merge_file = PyPDF2.PdfFileWriter()

            for i in range(input_read_pdf.getNumPages()):

                pdf_page = input_read_pdf.getPage(i)

                pdf_page.mergePage(watermark.getPage(0))

                merge_file.addPage(pdf_page)

            with open(output_file, "wb") as filehandle_output:
                # write the watermarked file to the new file
                merge_file.write(filehandle_output)

    root.destroy()

def invisiblewatermarkingPDF():
    print("\nSelect your pdf to be watermarked\n")

    root = tkinter.Tk()  # pointing root to Tk() to use it as Tk() in program. >>>
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)
    open_file = convert_from_path(filedialog.askopenfilename(),
                                  poppler_path=r'F:\Watermark Python\poppler-0.68.0\bin')

    pdf = FPDF()
    pdf.set_auto_page_break(0)
    img_list = []
    for i in range(len(open_file)):
        # Save pages as images in the pdf
        open_file[i].save('page' + str(i) + '.jpg', 'JPEG')

        bgr = cv2.imread('page'+str(i)+'.jpg')
        wm = 'Watermark'

        encoder = WatermarkEncoder()
        encoder.set_watermark('bytes', wm.encode('utf-8'))
        bgr_encoded = encoder.encode(bgr, 'dwtDct')

        cv2.imwrite('wmpage'+str(i)+'.jpg', bgr_encoded)
        img_list.append('wmpage'+str(i)+'.jpg')

    for img in img_list:
        pdf.add_page()
        pdf.image(img,w=130,h=200)

    pdf.output("invwatermarked.pdf")

def decodeinvisiblewatermarkingPDF():
    print("\nSelect your pdf to be watermarked\n")

    root = tkinter.Tk()  # pointing root to Tk() to use it as Tk() in program. >>>
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)
    open_file = convert_from_path(filedialog.askopenfilename(),
                                  poppler_path=r'F:\Watermark Python\poppler-0.68.0\bin')

    for i in range(len(open_file)):
        # Save pages as images in the pdf

        bgr = cv2.imread('wmpage'+str(i)+'.jpg')
        decoder = WatermarkDecoder('bytes', 32)
        watermark = decoder.decode(bgr, 'dwtDct')
        print(watermark.decode('utf-8'))




if __name__ == '__main__':

    while True:
        print('\nYou need to watermark:\n1)Image\n2)PDF\n3)Invisible Watermark\n4)Decoding inv.watermarked file\n')

        choice = int(input())
        if choice == 1:
            watermarkingImage()
        elif choice == 2:
            watermarkingPDF()
        elif choice == 3:
            invisiblewatermarkingPDF()
        else :
            decodeinvisiblewatermarkingPDF()


