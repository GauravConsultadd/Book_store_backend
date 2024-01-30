from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import OrderModel
from .serializer import *
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Create your views here.
# to implement
class createOrderView(APIView):
    permission_classes = [IsAuthenticated]
    model = OrderModel

    def post(self,request):

        try:
            data = request.data
            order = createOrderSerializer(data=data)

            if not order.is_valid():
                return Response({'message': order.error_messages},status=400)
            
            order.save()

            orders = self.model.objects.filter(user__id = request.user.id)
            serializer = getMyOrderSerializer(orders,many = True)

            return Response({
                'orders': serializer.data
            },status=200)

            
        except Exception as err:
            return Response({'message': err.args},status=500)
        

class getRespectiveOrders(APIView):
    permission_classes = [IsAuthenticated]
    model = OrderModel

    def get(self,request):
        try:
            orders = self.model.objects.filter(user__id = request.user.id)
            serializer = getMyOrderSerializer(orders,many = True)

            return Response({
                'orders': serializer.data
            },status=200)

        except Exception as err:
            return Response({'message': err.args},status=500)


class getAllOrders(APIView):
    permission_classes = [IsAuthenticated]
    model = OrderModel

    def get(self,request):
        try:
            orders = self.model.objects.all()

            serializer = getOrderSerializer(orders,many = True)

            return Response({
                'orders': serializer.data
            },status=200)
        except Exception as err:
            return Response({'message': err.args},status=500)


class GenerateInvoice(APIView):
    # permission_classes = [IsAuthenticated]
    model = OrderModel

    def get(self, request, order_id):
        try:
            order = OrderModel.objects.get(id=order_id)
            pdf_buffer = self.generate_pdf(order)

            # Create a response with FileResponse
            response = FileResponse(BytesIO(pdf_buffer.getvalue()), content_type='application/pdf')

            # Set Content-Disposition header for download
            response['Content-Disposition'] = f'inline; filename=invoice_{order_id}.pdf'

            return response
        except OrderModel.DoesNotExist:
            return Response({'message': 'Order not found'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=500)
        
    
    def generate_pdf(self, order):
        buffer = BytesIO()

        # Create PDF document using reportlab
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Add main heading
        main_heading = Paragraph('<b>Book Management</b>', getSampleStyleSheet()['Heading1'])
        elements.append(main_heading)

        # Add order information
        user_info = f'Username: {order.user.username}'
        order_date_info = f'Order Date: {order.order_date.strftime("%Y-%m-%d %H:%M:%S")}'

        user_info_paragraph = Paragraph(user_info, getSampleStyleSheet()['Normal'])
        order_date_paragraph = Paragraph(order_date_info, getSampleStyleSheet()['Normal'])

        elements.extend([user_info_paragraph, order_date_paragraph])

        # Add a line to separate heading and table
        elements.append(Spacer(1, 12))

        # Add content to the PDF
        elements.append(self.get_invoice_table(order))
        
        # Build the PDF
        doc.build(elements)

        buffer.seek(0)
        return buffer

    def get_invoice_table(self, order):
        # Define table data
        book_titles = ', '.join([book.title for book in order.books.all()])

        # Convert order_date to a readable format
        formatted_order_date = order.order_date.strftime('%Y-%m-%d %H:%M:%S')

        # Define table data
        data = [
            ['Order ID', 'Books', 'Total Price'],
            [order.id, book_titles, order.total_price],
        ]

        # Define custom column widths (adjust as needed)
        col_widths = [80, 300, 80]

        # Create the table with custom column widths
        table = Table(data, colWidths=col_widths, rowHeights=30)

        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'grey'),
        ])
        table.setStyle(style)

        return table