from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from tkinter import Tk, Label, Entry, StringVar, OptionMenu, Button

# Function to generate receipt
def generate_receipt(data):
    try:
        # Create a PDF file
        pdf_file = SimpleDocTemplate("receipt.pdf", pagesize=A4)

        # Create a list to store the elements of the PDF
        elements = []

        # Create the title
        title_style = ParagraphStyle(name='Title', fontSize=24, alignment=TA_CENTER)
        title = Paragraph("Transaction Receipt", title_style)
        elements.append(title)
        elements.append(Spacer(1, 10 * mm))

        # Create the date
        date_style = ParagraphStyle(name='Date', fontSize=12)
        date = Paragraph("Date: " + datetime.now().strftime("%d-%m-%Y"), date_style)
        elements.append(date)
        elements.append(Spacer(1, 5 * mm))

        # Create the transaction details table
        details_style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 3 * mm)
        ])
        details = Table(data, style=details_style)
        elements.append(details)
        elements.append(Spacer(1, 10 * mm))

        # Create the footer
        footer_style = ParagraphStyle(name='Footer', fontSize=12, alignment=TA_CENTER)
        footer = Paragraph("Thank you for your transaction!", footer_style)
        elements.append(footer)

        # Build the PDF
        pdf_file.build(elements)

        return "receipt.pdf"

    except Exception as e:
        return str(e)

# Function to get form data
def get_form_data():
    def submit_fields():
        amount = amount_entry.get()
        quantity = quantity_entry.get()
        mode_of_payment = mode_of_payment_var.get()
        payment_details = payment_details_entry.get()

        data = [
            ["Description", "Amount"],
            ["Quantity", quantity],
            ["Mode of Payment", mode_of_payment],
            ["Payment Details", payment_details],
            ["Total Amount", amount]
        ]

        root.destroy()
        generate_receipt(data)

    root = Tk()
    root.title("Transaction Receipt Form")

    Label(root, text="Amount").grid(row=0, column=0)
    amount_entry = Entry(root)
    amount_entry.grid(row=0, column=1)

    Label(root, text="Quantity").grid(row=1, column=0)
    quantity_entry = Entry(root)
    quantity_entry.grid(row=1, column=1)

    mode_of_payment_var = StringVar(root)
    mode_of_payment_var.set("Cash")
    Label(root, text="Mode of Payment").grid(row=2, column=0)
    mode_of_payment_menu = OptionMenu(root, mode_of_payment_var, "Cash", "Card", "Online")
    mode_of_payment_menu.grid(row=2, column=1)

    Label(root, text="Payment Details").grid(row=3, column=0)
    payment_details_entry = Entry(root)
    payment_details_entry.grid(row=3, column=1)

    Button(root, text="Submit", command=submit_fields).grid(row=4, column=1)

    root.mainloop()

get_form_data()