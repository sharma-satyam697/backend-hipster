# import asyncio
# import os
# from datetime import datetime
# from typing import List, Union
#
# from bson import ObjectId
# from motor.motor_asyncio import AsyncIOMotorClient
#
# from utils.logger import Logger
#
#
#
# class MongoMotor:
#     client = None
#     db = None
#
#     @classmethod
#     async def connect_to_mongo(cls) -> None:
#         """
#         Connects to MongoDB using the provided URI and initializes the database.
#
#         Raises:
#             RuntimeError: If unable to connect to MongoDB.
#         """
#         try:
#             cls.client = AsyncIOMotorClient(os.getenv('MONGO_DB_URI'))
#             cls.db = cls.client[os.getenv('MONGO_DB_NAME')]
#         except Exception as e:
#             raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")
#
#     @classmethod
#     async def close_mongo_connection(cls) -> None:
#         """Closes the MongoDB connection."""
#         if cls.client:
#             cls.client.close()
#
#     @staticmethod
#     async def _add_timestamps(data: dict) -> dict:
#         """Adds 'created_at' and 'updated_at' timestamps to the given data."""
#         now = datetime.utcnow()
#         data['created_at'] = now
#         data['updated_at'] = now
#         return data
#
#     @staticmethod
#     async def insert_one(collection_name: str, data: dict) -> ObjectId:
#         """
#         inserts a single document into the specified collection.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             data (dict): The data to be inserted.
#
#         Returns:
#             ObjectId: The ID of the inserted document.
#         """
#         data = await MongoMotor._add_timestamps(data)
#         result = await MongoMotor.db[collection_name].insert_one(data)
#         return result.inserted_id
#
#     @staticmethod
#     async def insert_many(collection_name: str, data: List[dict]) -> bool:
#         """
#         inserts multiple documents into the specified collection.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             data (List[dict]): The list of data to be inserted.
#
#         Returns:
#             bool: True if the insertion is successful, False otherwise.
#         """
#         data = [await MongoMotor._add_timestamps(item) for item in data]
#         result = await MongoMotor.db[collection_name].insert_many(data, ordered=False)
#         return bool(result.inserted_ids)
#
#     @staticmethod
#     async def find_one(collection_name: str, find_filter: dict = None,
#                        value_filter: dict = None) -> Union[dict, None]:
#         """
#         finds a single document in the specified collection based on the provided filters.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             find_filter (dict): The filter for finding documents.
#             value_filter (dict): The filter for the returned values.
#
#         Returns:
#             Union[dict, None]: The document if found, None otherwise.
#         """
#         find_filter = {} if find_filter is None else find_filter
#         value_filter = {} if value_filter is None else value_filter
#
#         return await MongoMotor.db[collection_name].find_one(find_filter, value_filter)
#
#     @staticmethod
#     async def find_many(collection_name: str, find_filter: dict = None,
#                         value_filter: dict = None, sorting_value: list = None, limit: int = None) -> List[dict]:
#         """
#         finds multiple documents in the specified collection based on the provided filters.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             find_filter (dict): The filter for finding documents.
#             value_filter (dict): The filter for the returned values.
#             sorting_value (list): The sorting value for the results.
#
#         Returns:
#             List[dict]: List of documents matching the criteria.
#         """
#         find_filter = {} if find_filter is None else find_filter
#         value_filter = {} if value_filter is None else value_filter
#
#         results = MongoMotor.db[collection_name].find(find_filter, value_filter)
#
#         if sorting_value is not None:
#             results = results.sort(sorting_value)
#
#         if limit is not None:
#             results = results.limit(limit)
#
#         return [result async for result in results]
#
#     @staticmethod
#     async def update_one(collection_name: str, update_filter: dict, update_value: dict | list = None,
#                          remove_value: dict = None, pull_value: dict = None, upsert: bool = False,
#                          array_filters: list = None) -> None:
#         """
#         Updates a single document in the specified collection based on the provided filter.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             update_filter (dict): The filter for identifying the document to update.
#             update_value (dict | list): The values to be updated.
#             remove_value (dict): The values to be removed.
#             pull_value (dict): The values to be removed from arrays using $pull.
#             array_filters (list): Optional array filters for updating specific array elements.
#
#         Returns:
#             None
#         """
#         if update_value is None:
#             update_value = {}
#
#         if remove_value is None:
#             remove_value = {}
#
#         if pull_value is None:
#             pull_value = {}
#
#         # Create update kwargs dict for optional array_filters
#         update_kwargs = {}
#         if array_filters:
#             update_kwargs['array_filters'] = array_filters
#
#         # Add timestamp to update_value if provided
#         if isinstance(update_value, dict):
#             update_value['updated_at'] = datetime.utcnow()
#
#         # Build the update query
#         update_query = {}
#         if update_value:
#             update_query['$set'] = update_value
#         if remove_value:
#             update_query['$unset'] = remove_value
#         if pull_value:
#             update_query['$pull'] = pull_value
#
#         # Execute the update
#         await MongoMotor.db[collection_name].update_one(
#             update_filter,
#             update_query,
#             upsert=upsert,
#             **update_kwargs
#         )
#
#     @staticmethod
#     async def find_one_and_update_one(collection_name: str, find_filter: dict, update_operation: dict,
#                                       return_doc: bool = False, upsert=True, array_filters: list = None) -> dict:
#
#         """
#         finds and updates a single document in the specified collection based on the provided filter.
#
#         Args:
#             upsert:
#             return_doc (bool): True if the updated document should be returned, False otherwise.
#             collection_name (str): The name of the MongoDB collection.
#             find_filter (dict): The filter for identifying the document to update.
#             update_operation (dict): The values to be updated.
#
#         Returns:
#             dict: The updated document.
#         """
#         update_kwargs = {}
#         if array_filters:
#             update_kwargs['array_filters'] = array_filters
#
#         update_operation.setdefault("$set", {})["updated_at"] = datetime.utcnow()
#         return await MongoMotor.db[collection_name].find_one_and_update(find_filter, update_operation,
#                                                                         upsert=upsert, return_document=return_doc,
#                                                                         **update_kwargs)
#
#     @staticmethod
#     async def update_many(collection_name: str, update_filter: dict, update_value: dict | list) -> None:
#         """
#         updates multiple documents in the specified collection based on the provided filter.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             update_filter (dict): The filter for identifying the documents to update.
#             update_value (dict): The values to be updated.
#
#         Returns:
#             None
#         """
#         if isinstance(update_value, list):
#             update_value.append({"$set": {"updated_at": datetime.utcnow()}})
#
#         elif isinstance(update_value, dict):
#             update_value.update({"$set": {"updated_at": datetime.utcnow()}})
#         await MongoMotor.db[collection_name].update_many(update_filter, update_value)
#
#     @staticmethod
#     async def bulk_update(collection_name: str, update_list: List[dict]) -> None:
#         """
#         updates multiple documents in the specified collection using a list of update operations.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             update_list (List[dict]): List of dictionaries with "update_filter" and "update_value".
#
#         Returns:
#             None
#         """
#
#         tasks = [MongoMotor.update_one(collection_name, data["update_filter"], data["update_value"]) for data in
#                  update_list]
#         await asyncio.gather(*tasks)
#
#     @staticmethod
#     async def bulk_write(collection_name: str, operations: list):
#         """
#         Perform a bulk write operation on the specified collection.
#
#         :param collection_name: Name of the MongoDB collection.
#         :param operations: List of bulk operations (UpdateOne, InsertOne, etc.).
#         :return: BulkWriteResult or None if operations list is empty.
#         """
#         if not operations:
#             return None
#
#         try:
#             result = await MongoMotor.db[collection_name].bulk_write(operations, ordered=False)
#             return result
#         except Exception as e:
#             print(f"Bulk write error in {collection_name}: {e}")
#             return None
#
#     @staticmethod
#     async def delete_one(collection_name: str, find_filter: dict) -> None:
#         """
#         deletes a single document from the specified collection based on the provided filter.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             find_filter (dict): The filter for identifying the document to delete.
#
#         Returns:
#             None
#         """
#         await MongoMotor.db[collection_name].delete_one(find_filter)
#
#     @staticmethod
#     async def delete_many(collection_name: str, find_filter: dict) -> None:
#         """
#         deletes multiple documents from the specified collection based on the provided filter.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             find_filter (dict): The filter for identifying the documents to delete.
#
#         Returns:
#             None
#         """
#         await MongoMotor.db[collection_name].delete_many(find_filter)
#
#     @staticmethod
#     async def aggregate(collection_name: str, pipeline: List[dict]) -> List[dict]:
#         """
#         performs an aggregation on the specified collection using the provided pipeline.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             pipeline (List[dict]): The aggregation pipeline.
#
#         Returns:
#             List[dict]: List of documents resulting from the aggregation.
#         """
#         aggregate_data = MongoMotor.db[collection_name].aggregate(pipeline)
#         return [result async for result in aggregate_data]
#
#     @staticmethod
#     async def find_one_set_push(collection_name: str, update_filter: dict, update_value: dict,
#                                 push_data: dict, upsert: bool = True) -> dict:
#         """
#         Finds a single document and updates it in the specified collection.
#
#         If no document matches, a new one is created.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             update_filter (dict): The filter for identifying the document.
#             update_value (dict): The values to be updated or set (like created_at, user_id, etc.).
#             push_data (dict): The field and data to push into an array (e.g., {"messages": {...}}).
#             upsert (bool): Whether to create the document if it doesn't exist.
#
#         Returns:
#             dict: The updated or created document.
#         """
#         update_data = await MongoMotor.db[collection_name].find_one_and_update(
#             update_filter,
#             {'$set': update_value, '$push': push_data},
#             upsert=upsert,
#             return_document=True  # Returns the updated document
#         )
#         return update_data
#
#     @staticmethod
#     async def find_one_and_update_remove(collection_name: str, update_filter: dict, update_value: dict,
#                                          image: dict) -> dict:
#         """
#         finds a single document and updates it by removing specific data in the specified collection.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             update_filter (dict): The filter for identifying the document.
#             update_value (dict): The values to be updated.
#             image (dict): The image data to be pulled.
#
#         Returns:
#             dict: The updated document.
#         """
#         update_data = await MongoMotor.db[collection_name].find_one_and_update(update_filter,
#                                                                                {'$set': update_value, "$pull": image})
#         return update_data
#
#     @staticmethod
#     async def count_documents(collection_name: str, query_filter: dict) -> int:
#         """
#         count of documents that match the query in the specified collection.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             query_filter (dict): The filter for identifying the document.
#
#         Returns:
#             int: The count of documents.
#         """
#         count = await MongoMotor.db[collection_name].count_documents(query_filter)
#         return count
#
#     @classmethod
#     async def create_index(
#             cls,
#             collection_name: str,
#             keys: list,
#             expire_after_seconds: int = None,
#             **kwargs
#     ):
#         """
#         Creates an index on a collection with customizable parameters, including TTL.
#
#         Args:
#             collection_name (str): The name of the collection.
#             keys (list): A list of tuples specifying the fields and sort order (e.g., [("field1", 1), ("field2", -1)]).
#             expire_after_seconds (int, optional): The amount of time in seconds after which the document will expire.
#             **kwargs: Additional index options (e.g., unique=True).
#
#         Returns:
#             str: The name of the created index.
#         """
#         try:
#             collection = cls.db[collection_name]
#
#             # Check if the index already exists
#             existing_indexes = await collection.index_information()
#             index_name = f"{','.join(key[0] for key in keys)}_1"
#             if index_name in existing_indexes:
#                 await Logger.info_log(
#                     msg=f"Index '{index_name}' already exists on collection '{collection_name}'. Skipping index creation.")
#                 return index_name
#
#             # Create the index with TTL if specified
#             index_options = {}
#             if expire_after_seconds is not None:
#                 index_options['expireAfterSeconds'] = expire_after_seconds
#             index_name = await collection.create_index(keys, **index_options)
#             await Logger.info_log(msg=f"Index '{index_name}' created successfully on collection '{collection_name}'.")
#             return index_name
#         except Exception as e:
#             await Logger.error_log(file_name=__name__, func_name='create_index', error=e)
#             raise e
#
#     @staticmethod
#     async def delete_index(collection_name: str, index_name: str):
#         """
#         Deletes an index from the specified collection.
#
#         Args:
#             collection_name (str): The name of the MongoDB collection.
#             index_name (str): The name of the index to be deleted.
#
#         Returns:
#             None
#         """
#         try:
#             collection = MongoMotor.db[collection_name]
#             await collection.drop_index(index_name)
#             await Logger.info_log(msg=f"Index '{index_name}' deleted successfully from collection '{collection_name}'.")
#         except Exception as e:
#             await Logger.error_log(file_name=__name__, func_name='delete_index', error=e)
