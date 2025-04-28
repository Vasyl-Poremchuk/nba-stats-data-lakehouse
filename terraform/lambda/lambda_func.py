import logging
from enum import StrEnum
from typing import Literal

import boto3
from botocore.paginate import PageIterator
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


class Client(StrEnum):
    S3 = "s3"


class BucketName(StrEnum):
    SOURCE = "nba-data-stats"
    DESTINATION = "nba-data-lakehouse"


class Prefix(StrEnum):
    SOURCE = "processed/"
    DESTINATION = "bronze/"


class LoadStatus(StrEnum):
    LOADED = "loaded"
    NOT_LOADED = "not_loaded"


class ResponseStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


# Initialize the S3 service client.
s3_client = boto3.client(Client.S3)


def get_pages(bucket: str, prefix: str) -> PageIterator:
    """Get pages of all available objects from the source bucket.

    :param bucket: Bucket name.
    :param prefix: Prefix of objects to retrieve.
    :return: Pages.
    """
    paginator = s3_client.get_paginator(operation_name="list_objects_v2")

    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

    return pages


def get_objects() -> list[dict]:
    """Get a list of objects as a dictionary of the bucket name and
    object prefix.

    :return: List of objects.
    """
    pages = get_pages(bucket=BucketName.SOURCE, prefix=Prefix.SOURCE)

    objects = []

    for page in pages:
        contents = page.get("Contents", [])

        for obj in contents:
            key = obj.get("Key")

            copy_source = {"Bucket": BucketName.SOURCE, "Key": key}

            objects.append(copy_source)

    return objects


def is_loaded(
    bucket: str, key: str
) -> Literal[LoadStatus.LOADED, LoadStatus.NOT_LOADED] | None:
    """Check if the object exists in the specified bucket.

    :param bucket: Bucket name.
    :param key: Key of the object to check.
    :return: True if object exists, False otherwise.
    """
    try:
        s3_client.head_object(Bucket=bucket, Key=key)

        return LoadStatus.LOADED
    except ClientError as e:
        status_code = e.response.get("Error", {}).get("Code")

        if status_code == "404":
            return LoadStatus.NOT_LOADED

        logger.error(msg=f"An unexpected error occurred: {e}")
        raise


def load_into_bronze_layer_handler(event, context) -> dict:
    """Lambda function handler that loads data from a raw source
    into the bronze layer without any transformations.

    :param event: Lambda event data.
    :param context: Lambda context object.
    :return:
    """
    logger.info(msg="Loading Data into the Bronze Layer")

    objects = get_objects()

    for copy_source in objects:
        source_key = copy_source.get("Key")
        destination_key = source_key.replace(Prefix.SOURCE, Prefix.DESTINATION)

        load_status = is_loaded(
            bucket=BucketName.DESTINATION, key=destination_key
        )

        # Skip previously added objects.
        if load_status == LoadStatus.LOADED:
            continue

        try:
            s3_client.copy_object(
                Bucket=BucketName.DESTINATION,
                CopySource=copy_source,
                Key=destination_key,
            )

            logger.info(
                msg=f"`{source_key}` copied from `{BucketName.SOURCE}` "
                f"to `{BucketName.DESTINATION}` as `{destination_key}`"
            )
        except Exception as e:
            logger.error(
                msg=f"Failed to copy `{source_key}` to `{destination_key}`: "
                f"{e}"
            )
            response = {"status": ResponseStatus.FAILURE, "message": str(e)}

            return response

    response = {
        "status": ResponseStatus.SUCCESS,
        "message": "Data is Loaded into the Bronze Layer",
    }

    return response
