from datetime import datetime, timedelta
import logging
import urllib.request
from io import StringIO, BytesIO
import pandas as pd
import pyarrow
import boto3
import os
import hashlib

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.INFO)


def fetch_exchange_rates(date_from, date_to):
    """ fetch_exchange_rates

    Parameters
    ----------
    Returns
    -------
    pandas parquet file
    """
    date_from_str = datetime.strftime(
        date_from,
        '%d/%b/%Y'
    )
    date_to_str = datetime.strftime(
        date_to,
        '%d/%b/%Y'
    )
    series_code = (
        'XUDLADS,'
        'XUDLCDS,'
        'XUDLBK89,'
        'XUDLBK25,'
        'XUDLDKS,'
        'XUDLERS,'
        'XUDLHDS,'
        'XUDLBK33,'
        'XUDLBK97,'
        'XUDLBK78,'
        'XUDLJYS,'
        'XUDLBK83,'
        'XUDLNDS,'
        'XUDLNKS,'
        'XUDLBK47,'
        'XUDLBK85,'
        'XUDLSRS,'
        'XUDLSGS,'
        'XUDLZRS,'
        'XUDLBK93,'
        'XUDLSKS,'
        'XUDLSFS,'
        'XUDLTWS,'
        'XUDLBK87,'
        'XUDLBK95,'
        'XUDLUSS'
    )
    url = (
        'http://www.bankofengland.co.uk/'
        'boeapps/'
        'iadb/'
        'fromshowcolumns.asp?'
        'csv.x=yes&'
        f'Datefrom={date_from_str}&'
        f'Dateto={date_to_str}&'
        f'SeriesCodes={series_code}&'
        f'UsingCodes=Y&'
        f'CSVF=CN&'
        f'VPD=Y'
    )

    try:
        parquet_file = BytesIO()
        response = urllib.request.urlopen(url)
        csv_string = StringIO(response.read().decode('utf-8'))
        dataframe = pd.read_csv(
            csv_string,
            delimiter=','
        )
        dataframe.DATE = pd.to_datetime(dataframe.DATE, format='%d %b %Y')
        dataframe.SERIES = dataframe.SERIES.astype('string')
        dataframe.VALUE = dataframe.VALUE.astype('float')
        dataframe.to_parquet(parquet_file, compression='snappy')
        parquet_file.seek(0)
        logger.info(dataframe.info())
        return parquet_file
    except Exception as error:
        logger.error(error)


def upload_parquet_to_s3(body, key, bucket):
    """ upload_parquet_to_s3
        Function to upload a
        bytes object to s3

    Parameters
    ----------
    body: bytes object

    key: @string,

    bucket: @string

    Returns
    -------
    @json response
    """
    logger.info('Uploading Parquet file to S3')

    response = boto3.client('s3').put_object(
        Body=body,
        Bucket=bucket,
        Key=key
    )

    return response


def lambda_handler(event, context):
    """ lambda_handler

    Parameters
    ----------
    event: JSON blob, required
        An Lambda event

    context: JSON blob, optional
        Automatically passed by lambda
        Not used by the function.
    Returns
    -------
    void
    """
    try:
        date_from = datetime.now() - timedelta(4)
        date_to = datetime.now() - timedelta(3)
        parquet_file = fetch_exchange_rates(date_from, date_to)

        year = date_from.strftime('%Y')
        month = date_from.strftime('%m')
        day = date_from.strftime('%d')

        hasher = hashlib.md5()
        hasher.update(parquet_file.read())

        key = (
            'BankOfEngland/exchange_rates/'
            f'year={year}/'
            f'month={month}/'
            f'day={day}/'
            'boe_exchange_rates_'
            f'{hasher.hexdigest()}'
            f'.snappy.parquet'
        )

        bucket = os.environ['BUCKET']
        parquet_file.seek(0)
        response = upload_parquet_to_s3(parquet_file, key, bucket)

        logger.info(response)
    except Exception as error:
        logger.error(error)


if __name__ == '__main__':
    lambda_handler('Lambda function started', '')
