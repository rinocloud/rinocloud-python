
class Batch():
    @staticmethod
    def download(obj_list):
        for obj in obj_list:
            obj.download()

    @staticmethod
    def upload(obj_list):
        for obj in obj_list:
            obj.upload()

    @staticmethod
    def upload_meta(obj_list):
        for obj in obj_list:
            obj.upload_meta()

    @staticmethod
    def get(obj_list):
        for obj in obj_list:
            obj.get()

    @staticmethod
    def update(obj_list):
        for obj in obj_list:
            obj.update()
