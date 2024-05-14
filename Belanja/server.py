import grpc
from concurrent import futures
import shopping_pb2
import shopping_pb2_grpc
import mysql.connector
import logging

class ShoppingServicer(shopping_pb2_grpc.ShoppingServiceServicer):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Configure logging to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="monic",
                password="monic",
                database="insis"
            )
            self.cursor = self.db.cursor()
            self.logger.info("Database connection successful")
        except Exception as e:
            self.logger.error("Failed to connect to database: %s", e)

    def CreateItem(self, request, context):
        try:
            sql = "INSERT INTO items (item_name, price) VALUES (%s, %s)"
            val = (request.item_name, request.price)
            self.cursor.execute(sql, val)
            self.db.commit()
            return shopping_pb2.CreateItemResponse(success=True, message="Item added successfully")
        except Exception as e:
            self.logger.error("Failed to create item: %s", e)
            return shopping_pb2.CreateItemResponse(success=False, message="Failed to create item")

    def ReadItem(self, request, context):
        try:
            sql = "SELECT item_name, price FROM items WHERE id = %s"
            val = (request.id,)
            self.cursor.execute(sql, val)
            item = self.cursor.fetchone()
            if item:
                return shopping_pb2.ReadItemResponse(item=shopping_pb2.Item(id=request.id, item_name=item[0], price=item[1]))
            else:
                return shopping_pb2.ReadItemResponse(item=shopping_pb2.Item(id=0, item_name="", price=0))
        except Exception as e:
            self.logger.error("Failed to read item: %s", e)
            return shopping_pb2.ReadItemResponse(item=shopping_pb2.Item(id=0, item_name="", price=0))

    def UpdateItem(self, request, context):
        try:
            sql = "UPDATE items SET item_name = %s, price = %s WHERE id = %s"
            val = (request.item_name, request.price, request.id)
            self.cursor.execute(sql, val)
            self.db.commit()
            return shopping_pb2.UpdateItemResponse(success=True, message="Item updated successfully")
        except Exception as e:
            self.logger.error("Failed to update item: %s", e)
            return shopping_pb2.UpdateItemResponse(success=False, message="Failed to update item")

    def DeleteItem(self, request, context):
        try:
            # Menghapus item dari database
            sql_delete = "DELETE FROM items WHERE id = %s"
            val_delete = (request.id,)
            self.cursor.execute(sql_delete, val_delete)
            self.db.commit()

            # Mengatur ulang ID setelah penghapusan
            sql_reset_id = "ALTER TABLE items AUTO_INCREMENT = 1"
            self.cursor.execute(sql_reset_id)
            self.db.commit()

            return shopping_pb2.DeleteItemResponse(success=True, message="Item deleted successfully")
        except Exception as e:
            self.logger.error("Failed to delete item: %s", e)
            return shopping_pb2.DeleteItemResponse(success=False, message="Failed to delete item")


def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        shopping_pb2_grpc.add_ShoppingServiceServicer_to_server(ShoppingServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()
    except Exception as e:
        logging.error("Server error: %s", e)

if __name__ == '__main__':
    serve()
