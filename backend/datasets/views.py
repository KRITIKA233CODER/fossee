import os
import pandas as pd
from django.conf import settings
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import DatasetSerializer, UploadSerializer, UserSerializer
import logging
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)
from .models import Dataset
from .utils import process_csv_and_create_dataset

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate JWT tokens and return in the same shape as the login endpoint
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'user': serializer.data,
            'access': access_token,
            'refresh': refresh_token,
        }, status=status.HTTP_201_CREATED)

class DatasetUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        serializer = UploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        f = serializer.validated_data['file']
        try:
            dataset, coercion_errors, summary, analytics = process_csv_and_create_dataset(f, uploader=request.user)
        except ValueError as e:
            logger.warning('Validation error during CSV processing: %s', e)
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # log full traceback for server-side diagnosis
            import traceback
            traceback.print_exc()
            logger.exception('Processing error while handling uploaded CSV')
            return Response({'error': f'Processing error: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            'id': str(dataset.id),
            'summary': summary,
            'analytics': analytics,
            'coercion_errors': coercion_errors,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class DatasetListView(generics.ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Dataset.objects.all().order_by('-uploaded_at')[:5]


class DatasetSummaryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            d = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # If analytics was persisted, return it directly
        if getattr(d, 'analytics', None):
            return Response(d.analytics)

        # Fallback: return the simple legacy summary
        summary = {
            'total_rows': d.total_rows,
            'averages': {'flowrate': d.avg_flowrate, 'pressure': d.avg_pressure, 'temperature': d.avg_temperature},
            'type_distribution': d.type_distribution,
        }
        return Response(summary)


class DatasetTableView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 50))
        sort = request.query_params.get('sort')
        order = request.query_params.get('order', 'asc')

        try:
            d = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        csv_path = os.path.join(settings.MEDIA_ROOT, d.csv_file.name)
        if not os.path.exists(csv_path):
            return Response({'error': 'CSV file missing on server.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        df = pd.read_csv(csv_path)
        # Normalize column names to lowercase for consistent keys
        df.columns = [c.strip().lower() for c in df.columns]

        if sort:
            ascending = (order == 'asc')
            try:
                df = df.sort_values(by=sort, ascending=ascending)
            except Exception:
                pass

        total = len(df)
        start = (page - 1) * page_size
        end = start + page_size
        rows = df.iloc[start:end].fillna('').to_dict(orient='records')

        return Response({'total': total, 'page': page, 'page_size': page_size, 'rows': rows})


class DatasetReportView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            d = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file_path = None
        if d.summary_pdf and os.path.exists(os.path.join(settings.MEDIA_ROOT, d.summary_pdf.name)):
            file_path = os.path.join(settings.MEDIA_ROOT, d.summary_pdf.name)
        
        # If missing or force refresh (optional), regenerate
        if not file_path or request.query_params.get('refresh') == 'true':
            try:
                print(f"[REGEN] Re-generating PDF for dataset {d.id}...")
                if d.csv_file and os.path.exists(d.csv_file.path):
                    import pandas as pd
                    from .utils import create_pdf_report
                    df = pd.read_csv(d.csv_file.path)
                    new_pdf_path = create_pdf_report(d, df)
                    d.summary_pdf.name = os.path.relpath(new_pdf_path, settings.MEDIA_ROOT).replace('\\', '/')
                    d.save()
                    file_path = new_pdf_path
                else:
                    return Response({'error': 'Source CSV missing, cannot regenerate.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': f'Regeneration failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        # Cleaner filename: strip existing .csv if present
        clean_name = d.filename.replace('.csv', '') if d.filename else str(d.id)
        response['Content-Disposition'] = f'attachment; filename="{clean_name}.pdf"'
        return response


class DatasetCleanDownloadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        try:
            d = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not d.cleaned_csv or not os.path.exists(os.path.join(settings.MEDIA_ROOT, d.cleaned_csv.name)):
            return Response({'error': 'Cleaned file not found.'}, status=status.HTTP_404_NOT_FOUND)

        file_path = os.path.join(settings.MEDIA_ROOT, d.cleaned_csv.name)
        response = FileResponse(open(file_path, 'rb'), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="cleaned_{d.filename or d.id}.csv"'
        return response
