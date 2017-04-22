import os
import re
from flask import jsonify, request
from PIL import Image
from io import BytesIO
import base64
from .upload_s3 import upload_to_s3_bucket


class ImageResize(object):
    def __init__(self):
        super(ImageResize, self).__init__()
        self.bucket_name = os.environ.get('BUCKET_NAME')
        self.folder_name = os.environ.get('FOLDER_NAME')
        self.upload_folder = os.path.abspath('./uploads')
        self.allowed_extension =  set(['.png', '.jpg', '.jpeg', '.gif', '.svg'])
        self.form = False

    def image_resize(self):

        images = request.json

        if len(request.files) != 0:
            self.form = True
            
            if "width" and "height" not in request.form:
                return jsonify({"success": False, "message": "Please mention width and height"})
            elif not all(isinstance(el , int) for el in [request.form.get("width"), request.form.get("height")]):
                 return jsonify({"success": False, "message": "width and height should be integer"})

            s3_images_url = list()
            resized_images = list()
            failed_images = list()
            files = request.files.getlist('image')
            for image in files:
                file, ext = os.path.splitext(image.filename)
                if ext in self.allowed_extension:
                    width = request.form.get("width")
                    height = request.form.get("height")
                    img = Image.open(image)
                    size = (int(width), int(height))
                    img.thumbnail(size, Image.ANTIALIAS)
                    new_file =  file.split('/')[-1] + "_resized_" + str(width) + "_" + str(height) + ext
                    saved_file = self.upload_folder + '/' + new_file
                    resized_images.append(saved_file)
                    s3_detination = self.folder_name + new_file
                    img.save(saved_file)
                    s3_images_url.append(upload_to_s3_bucket(self.bucket_name, saved_file, s3_detination))


        else:
            s3_images_url = list()
            resized_images = list()
            failed_images = list()
            for image in images:
                file, ext = os.path.splitext(image["name"])
                if ext in self.allowed_extension:
                    img = Image.open(BytesIO(base64.b64decode(image["data"])))
                    size = (image["width"], image["height"])
                    img.thumbnail(size, Image.ANTIALIAS)
                    new_file =  file.split('/')[-1] + "_resized_" + str(image["width"]) + "_" + str(image["height"]) + ext
                    saved_file = self.upload_folder + '/' + new_file
                    resized_images.append(saved_file)
                    s3_detination = self.folder_name + new_file
                    img.save(saved_file)
                    s3_images_url.append(upload_to_s3_bucket(self.bucket_name, saved_file, s3_detination))
                else:
                    failed_images.append(image["name"])


        self.delete_resized_images(resized_images)
        if len(failed_images) == 0:
            return jsonify({"success": True, "urls": s3_images_url})
        else:
            return jsonify({"success": s3_images_url , "failed" : ",".join(failed_images) + " , Image should be of type ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')"})



    def delete_resized_images(self, resized_images):
        for image in resized_images:
            if self.form:
                # uploaded_path, image_name = image.rsplit('/', 1)
                # image_name, ext = image_name.rsplit('.', 1)
                # original_image_name = re.sub(r"_resized_(.*)", '', image_name)
                # original_image = uploaded_path + '/' + original_image_name + '.' + ext
                # os.unlink(original_image)
                pass
            os.unlink(image)
